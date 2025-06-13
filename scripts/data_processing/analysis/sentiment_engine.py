from __future__ import annotations

from typing import List, Dict, Any

from ..utils.sentiment import compute_vader_score


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

            results.append(entry)

        return results

    # ------------------------------------------------------------------
    # Private helpers – one per model
    # ------------------------------------------------------------------

    def _analyze_with_gpt4(self, text: str) -> float:
        try:
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

            return float(json.loads(content).get("score", 0.0))
        except Exception:
            # Log omission quietly to keep runtime output clean
            return 0.0

    def _analyze_with_claude(self, text: str) -> float:
        try:
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
            return float(json.loads(content).get("score", 0.0))
        except Exception:
            return 0.0

    def _analyze_with_gemini(self, text: str) -> float:
        try:
            import json
            import google.generativeai as genai  # type: ignore # noqa: F401

            # API key is taken from environment (GOOGLE_API_KEY)
            genai.configure()
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(text=self.SYSTEM_PROMPT + "\n" + text)  # type: ignore[arg-type]
            content = response.text  # type: ignore[attr-defined]
            return float(json.loads(content).get("score", 0.0))
        except Exception:
            return 0.0