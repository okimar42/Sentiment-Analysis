from __future__ import annotations

from typing import List, Dict, Any

from ..utils.sentiment import compute_vader_score


class SentimentEngine:
    """Replicate webapp's multi-model sentiment analysis (skeleton).

    For the initial extraction we only implement VADER sentiment to validate
    the data-fetch + scoring pipeline. Support for GPT-4, Claude, Gemini etc.
    will be added in subsequent iterations.
    """

    def __init__(self, models: List[str]):
        self.models = models

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Analyze *texts* and return list of result dicts matching webapp schema."""
        results: List[Dict[str, Any]] = []
        for text in texts:
            r: Dict[str, Any] = {}
            if "vader" in self.models:
                r["vader_score"] = compute_vader_score(text)
            # Placeholder for future models.
            # We preserve the schema keys even if not calculated to maintain compatibility.
            for key in [
                "gpt4_score",
                "claude_score",
                "gemini_score",
                "gemma_score",
                "grok_score",
            ]:
                if key not in r:
                    r[key] = 0.0
            results.append(r)
        return results