from __future__ import annotations

from typing import List, Dict, Any

from ..utils.sentiment import compute_vader_score
from ..utils.metrics import get_metrics


class SentimentEngine:
    """Multi-model sentiment analysis replicating the logic in the webapp.

    Each model is queried with the *exact* same system/user message pattern as
    the original implementation so that the returned JSON can be parsed to a
    numeric `score` between -1 and 1.  If an LLM request fails (network error,
    bad credentials, invalid JSON, etc.) the engine falls back to a neutral
    score of 0.0 **without** raising – this mirrors the robustness of the
    original code.
    """

    SYSTEM_PROMPT = (
        "You are a sentiment analysis assistant. \n"
        "You must respond with a valid JSON object containing a 'score' field.\n"
        "The score should be a number between -1 and 1.\n"
        "Example response: {\"score\": 0.75}"
    )

    def __init__(self, models: List[str]):
        # Normalise to lowercase for comparison
        self.models = [m.lower() for m in models]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Analyze *texts* with all requested models.

        The return structure matches the Django model fields used by the
        original web-app so that downstream consumers do not need to branch.
        """

        results: List[Dict[str, Any]] = []

        for text in texts:
            entry: Dict[str, Any] = {}

            # VADER – always available offline
            if "vader" in self.models or not self.models:
                entry["vader_score"] = compute_vader_score(text)

            # GPT-4 (OpenAI)
            if "gpt4" in self.models:
                entry["gpt4_score"] = self._analyze_with_gpt4(text)

            # Claude (Anthropic)
            if "claude" in self.models:
                entry["claude_score"] = self._analyze_with_claude(text)

            # Gemini (Google)
            if "gemini" in self.models:
                entry["gemini_score"] = self._analyze_with_gemini(text)

            # Preserve keys even if not requested to stay schema-compatible
            for key in [
                "gpt4_score",
                "claude_score",
                "gemini_score",
                "gemma_score",
                "grok_score",
            ]:
                entry.setdefault(key, 0.0)

            # Sarcasm detection -------------------------------------------------
            sarcasm = self._detect_sarcasm(text)
            entry.update(
                {
                    "sarcasm_score": sarcasm["confidence"],
                    "is_sarcastic": sarcasm["sarcastic"],
                }
            )

            # IQ estimation ----------------------------------------------------
            iq = self._estimate_iq(text)
            entry.update(
                {
                    "perceived_iq": iq["iq_score"],
                }
            )

            # Bot detection ----------------------------------------------------
            bot = self._detect_bot(text)
            entry.update(
                {
                    "bot_probability": bot["probability"],
                    "is_bot": bot["is_bot"],
                }
            )

            results.append(entry)

        return results

    # ------------------------------------------------------------------
    # Private helpers – one per model
    # ------------------------------------------------------------------

    def _analyze_with_gpt4(self, text: str) -> float:
        try:
            metrics = get_metrics()
            
            import os
            import json

            import openai  # type: ignore # noqa: F401

            messages = [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ]

            # OpenAI python SDK v1 style – fall back to legacy if v0
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key is None:
                raise RuntimeError("OPENAI_API_KEY not set")

            try:
                client = openai.OpenAI(api_key=api_key)  # type: ignore[attr-defined]
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages,  # type: ignore[arg-type]
                    temperature=0.3,
                )
                content = response.choices[0].message.content  # type: ignore[index]
            except AttributeError:
                # Older openai<1.0 fallback
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,  # type: ignore[arg-type]
                    temperature=0.3,
                    api_key=api_key,
                )
                content = response["choices"][0]["message"]["content"]

            metrics.record_api_call(success=True)
            return float(json.loads(content).get("score", 0.0))
        except Exception:
            from ..utils.metrics import get_metrics
            get_metrics().record_api_call(success=False, error="GPT-4 API error")
            # Log omission quietly to keep runtime output clean
            return 0.0

    def _analyze_with_claude(self, text: str) -> float:
        try:
            metrics = get_metrics()
            
            import os
            import json

            import anthropic  # type: ignore # noqa: F401

            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            response = client.messages.create(
                model="claude-3-opus-20240229",
                system=self.SYSTEM_PROMPT,
                messages=[{"role": "user", "content": text}],  # type: ignore[arg-type]
                max_tokens=256,
            )
            content = response.content[0].text  # type: ignore[index]
            metrics.record_api_call(success=True)
            return float(json.loads(content).get("score", 0.0))
        except Exception:
            from ..utils.metrics import get_metrics
            get_metrics().record_api_call(success=False, error="Claude API error")
            return 0.0

    def _analyze_with_gemini(self, text: str) -> float:
        try:
            metrics = get_metrics()
            
            import json
            import google.generativeai as genai  # type: ignore # noqa: F401

            # API key is taken from environment (GOOGLE_API_KEY)
            genai.configure()
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(text=self.SYSTEM_PROMPT + "\n" + text)  # type: ignore[arg-type]
            content = response.text  # type: ignore[attr-defined]
            metrics.record_api_call(success=True)
            return float(json.loads(content).get("score", 0.0))
        except Exception:
            from ..utils.metrics import get_metrics
            get_metrics().record_api_call(success=False, error="Gemini API error")
            return 0.0

    # ------------------------------------------------------------------
    # Sarcasm / IQ / Bot Detection helpers
    # ------------------------------------------------------------------

    def _choose_llm(self) -> str | None:
        """Return preferred LLM model name present in self.models or None."""
        for candidate in ["gpt4", "gemini", "claude"]:
            if candidate in self.models:
                return candidate
        return None

    def _detect_sarcasm(self, text: str) -> Dict[str, Any]:
        model = self._choose_llm()
        if model is None:
            return {"confidence": 0.0, "sarcastic": False}

        prompt_system = (
            "You are a sarcasm detection assistant. Analyze the text and respond with a JSON object containing: "
            "- confidence: A number between 0 and 1 indicating confidence in the detection "
            "- sarcastic: A boolean indicating if the text is sarcastic "
            "- reasoning: A brief explanation of the analysis "
            "Example response: {\"confidence\": 0.9, \"sarcastic\": true, \"reasoning\": \"The text uses obvious sarcastic markers\"}"
        )

        messages = [{"role": "system", "content": prompt_system}, {"role": "user", "content": text}]

        try:
            import json

            if model == "gpt4":
                import os
                import openai  # type: ignore # noqa: F401

                api_key = os.getenv("OPENAI_API_KEY")
                if api_key is None:
                    raise RuntimeError("OPENAI_API_KEY not set")

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,  # type: ignore[arg-type]
                    temperature=0.3,
                    api_key=api_key,
                )
                content = response["choices"][0]["message"]["content"]
            elif model == "gemini":
                import google.generativeai as genai  # type: ignore # noqa: F401

                genai.configure()
                mdl = genai.GenerativeModel("gemini-pro")
                response = mdl.generate_content(text=messages[1]["content"])  # type: ignore[arg-type]
                content = response.text  # type: ignore[attr-defined]
            elif model == "claude":
                import os
                import anthropic  # type: ignore # noqa: F401

                client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                response = client.messages.create(
                    model="claude-3-opus-20240229",
                    system=messages[0]["content"],
                    messages=[{"role": "user", "content": text}],  # type: ignore[arg-type]
                    max_tokens=256,
                )
                content = response.content[0].text  # type: ignore[index]
            else:
                return {"confidence": 0.0, "sarcastic": False}

            parsed = json.loads(content)
            return {
                "confidence": float(parsed.get("confidence", 0.0)),
                "sarcastic": bool(parsed.get("sarcastic", False)),
            }
        except Exception:
            return {"confidence": 0.0, "sarcastic": False}

    def _estimate_iq(self, text: str) -> Dict[str, Any]:
        model = self._choose_llm()
        if model is None:
            return {"iq_score": 0.5}

        prompt_system = (
            "You are an IQ analysis assistant. Analyze the text and respond with a JSON object containing: "
            "- iq_score: A number between 0 and 1 indicating the perceived intelligence "
            "- raw_iq: A number between 55 and 145 representing the estimated IQ "
            "- confidence: A number between 0 and 1 indicating confidence in the analysis "
            "- reasoning: A brief explanation of the analysis "
            "Example response: {\"iq_score\": 0.8, \"raw_iq\": 120, \"confidence\": 0.9, \"reasoning\": \"The text shows high analytical ability\"}"
        )

        messages = [{"role": "system", "content": prompt_system}, {"role": "user", "content": text}]

        try:
            import json

            if model == "gpt4":
                import os
                import openai  # type: ignore # noqa: F401

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,  # type: ignore[arg-type]
                    temperature=0.3,
                    api_key=os.getenv("OPENAI_API_KEY"),
                )
                content = response["choices"][0]["message"]["content"]
            elif model == "gemini":
                import google.generativeai as genai  # type: ignore # noqa: F401

                genai.configure()
                mdl = genai.GenerativeModel("gemini-pro")
                response = mdl.generate_content(text=messages[1]["content"])  # type: ignore[arg-type]
                content = response.text  # type: ignore[attr-defined]
            elif model == "claude":
                import os
                import anthropic  # type: ignore # noqa: F401

                client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                response = client.messages.create(
                    model="claude-3-opus-20240229",
                    system=messages[0]["content"],
                    messages=[{"role": "user", "content": text}],  # type: ignore[arg-type]
                    max_tokens=256,
                )
                content = response.content[0].text  # type: ignore[index]
            else:
                return {"iq_score": 0.5}

            parsed = json.loads(content)
            return {"iq_score": float(parsed.get("iq_score", 0.5))}
        except Exception:
            return {"iq_score": 0.5}

    def _detect_bot(self, text: str) -> Dict[str, Any]:
        model = self._choose_llm()
        if model is None:
            return {"probability": 0.0, "is_bot": False}

        prompt_system = (
            "You are a bot detection assistant. Analyze the given text for bot-like behavior and respond with a JSON object containing: "
            "- probability: A number between 0 and 1 indicating the likelihood of the text being from a bot "
            "- is_bot: A boolean indicating if the text is likely from a bot (true if probability > 0.7) "
            "- reasoning: A brief explanation of your analysis "
            "Example response: {\"probability\": 0.85, \"is_bot\": true, \"reasoning\": \"Text shows repetitive patterns and lacks natural language variation\"}"
        )

        messages = [{"role": "system", "content": prompt_system}, {"role": "user", "content": text}]

        try:
            import json

            if model == "gpt4":
                import os
                import openai  # type: ignore # noqa: F401

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,  # type: ignore[arg-type]
                    temperature=0.3,
                    api_key=os.getenv("OPENAI_API_KEY"),
                )
                content = response["choices"][0]["message"]["content"]
            elif model == "gemini":
                import google.generativeai as genai  # type: ignore # noqa: F401

                genai.configure()
                mdl = genai.GenerativeModel("gemini-pro")
                response = mdl.generate_content(text=messages[1]["content"])  # type: ignore[arg-type]
                content = response.text  # type: ignore[attr-defined]
            elif model == "claude":
                import os
                import anthropic  # type: ignore # noqa: F401

                client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                response = client.messages.create(
                    model="claude-3-opus-20240229",
                    system=messages[0]["content"],
                    messages=[{"role": "user", "content": text}],  # type: ignore[arg-type]
                    max_tokens=256,
                )
                content = response.content[0].text  # type: ignore[index]
            else:
                return {"probability": 0.0, "is_bot": False}

            parsed = json.loads(content)
            return {
                "probability": float(parsed.get("probability", 0.0)),
                "is_bot": bool(parsed.get("is_bot", False)),
            }
        except Exception:
            return {"probability": 0.0, "is_bot": False}