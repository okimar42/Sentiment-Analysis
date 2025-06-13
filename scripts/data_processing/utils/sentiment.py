"""Sentiment analysis utility functions for standalone scripts.

This module mirrors `backend/sentiment_analysis/utils/sentiment.py` from the webapp
but is self-contained and free of Django dependencies.
"""

from __future__ import annotations

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # type: ignore

# Initialize VADER once at module level
_vader = SentimentIntensityAnalyzer()


def compute_vader_score(text: str) -> float:
    """Compute VADER compound sentiment score for *text*.

    The return value is the compound score in the interval [-1, 1].
    The implementation is intentionally identical to the webapp's version so
    that results remain 100 % compatible.
    """
    if not isinstance(text, str):
        raise TypeError("Input to compute_vader_score must be a string")

    return _vader.polarity_scores(text)["compound"]