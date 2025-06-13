from __future__ import annotations

"""Image sentiment analysis using vision-enabled LLMs.

This module is an extraction of the logic present in
`backend/sentiment_analysis/tasks_original_backup.py::analyze_image` but
adapted to work in a standalone script context without Django.
"""

from base64 import b64encode
from typing import Dict, Any, List

import requests  # type: ignore


class ImageAnalyzer:
    """Analyze an image URL with one or more vision-capable models."""

    def __init__(self, models: List[str] | None = None):
        self.models = [m.lower() for m in (models or ["gpt4"])]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def analyze(self, image_url: str) -> Dict[str, Any]:
        """Return ImageSentimentResult-like dict for *image_url*."""
        try:
            response = requests.get(image_url, timeout=15)
            response.raise_for_status()
        except Exception as exc:  # pragma: no cover
            return {
                "image_url": image_url,
                "image_description": f"Failed to download image: {exc}",
                "score": 0.0,
                "gpt4_vision_score": 0.0,
                "claude_vision_score": 0.0,
                "gemini_vision_score": 0.0,
            }

        img_b64 = b64encode(response.content).decode("utf-8")

        result: Dict[str, Any] = {
            "image_url": image_url,
            "image_description": "",
            "score": 0.0,
            "gpt4_vision_score": 0.0,
            "claude_vision_score": 0.0,
            "gemini_vision_score": 0.0,
        }

        # GPT-4 Vision ---------------------------------------------------
        if "gpt4" in self.models or "gpt4-vision" in self.models:
            r = self._analyze_with_gpt4(img_b64)
            result.update(r)

        # Gemini Vision --------------------------------------------------
        if "gemini" in self.models:
            r = self._analyze_with_gemini(img_b64)
            result.update(r)

        # Claude Vision --------------------------------------------------
        if "claude" in self.models:
            r = self._analyze_with_claude(img_b64)
            result.update(r)

        # Compute overall score as average of available model scores (non-zero)
        scores = [result.get("gpt4_vision_score", 0), result.get("gemini_vision_score", 0), result.get("claude_vision_score", 0)]
        non_zero = [s for s in scores if s != 0]
        if non_zero:
            result["score"] = sum(non_zero) / len(non_zero)

        return result

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _analyze_with_gpt4(self, img_b64: str) -> Dict[str, Any]:
        try:
            import os
            import json
            import openai  # type: ignore

            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # type: ignore[attr-defined]
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # assumes vision support
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Analyze this image and respond with a JSON object containing: "
                            "sentiment_score (between -1 and 1), content_description, emotional_impact"
                        ),
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analyze this image"},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"},
                            },
                        ],
                    },
                ],
                max_tokens=300,
            )
            content = response.choices[0].message.content  # type: ignore[index]
            parsed = json.loads(content)
            score = float(parsed.get("sentiment_score", 0.0))
            desc = str(parsed.get("content_description", ""))
            return {
                "gpt4_vision_score": score,
                "image_description": desc,
            }
        except Exception:
            return {"gpt4_vision_score": 0.0}

    def _analyze_with_gemini(self, img_b64: str) -> Dict[str, Any]:
        try:
            import google.generativeai as genai  # type: ignore

            genai.configure()
            model = genai.GenerativeModel("gemini-pro-vision")
            response = model.generate_content(
                [
                    "Analyze this image and provide sentiment, content description, and emotional impact",
                    {"mime_type": "image/jpeg", "data": img_b64},
                ]
            )
            content = response.text  # type: ignore[attr-defined]
            # Heuristic sentiment extraction as in webapp
            sentiment_score = 0.0
            if "positive" in content.lower():
                sentiment_score = 0.5
            elif "negative" in content.lower():
                sentiment_score = -0.5
            return {
                "gemini_vision_score": sentiment_score,
            }
        except Exception:
            return {"gemini_vision_score": 0.0}

    def _analyze_with_claude(self, img_b64: str) -> Dict[str, Any]:
        """Placeholder: Claude vision; returns 0 if unavailable."""
        try:
            import os
            import json
            import anthropic  # type: ignore

            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            response = client.messages.create(
                model="claude-3-opus-20240229",  # vision-capable model
                system="You are an image sentiment analysis assistant.",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "image", "source": {"data": img_b64, "media_type": "image/jpeg"}},
                            {"type": "text", "text": "Please analyze this image and provide a JSON with a 'sentiment_score'."},
                        ],
                    }
                ],  # type: ignore[arg-type]
                max_tokens=300,
            )
            content = response.content[0].text  # type: ignore[index]
            parsed = json.loads(content)
            return {"claude_vision_score": float(parsed.get("sentiment_score", 0.0))}
        except Exception:
            return {"claude_vision_score": 0.0}