"""
Gemma model analysis utilities.
"""

import os
import sys

from celery.utils.log import get_task_logger
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = get_task_logger(__name__)

# Initialize VADER as fallback
vader = SentimentIntensityAnalyzer()


def analyze_with_gemma(text: str) -> float:
    """
    Analyze text using Gemma model with fallback to VADER.

    Args:
        text: Text to analyze

    Returns:
        float: Sentiment score between -1 and 1
    """
    try:
        # Skip model loading during migrations
        if "migrate" in sys.argv:
            return 0.0

        # Skip model loading if not in backend service
        if os.getenv("SERVICE_ROLE") != "backend":
            logger.info("Not in backend service, skipping model loading")
            return 0.0

        from .huggingface import get_model

        # Lazy load the model
        tokenizer, model = get_model()

        if tokenizer is None or model is None:
            logger.info("[Gemma] Using VADER as fallback for sentiment analysis")
            return vader.polarity_scores(text)["compound"]

        import torch

        # Tokenize input
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

        # Run inference
        with torch.no_grad():
            outputs = model(**inputs)
            scores = torch.softmax(outputs.logits, dim=1)

        # Calculate sentiment score
        sentiment_score = float(scores[0][1] - scores[0][0])
        return sentiment_score

    except Exception as e:
        logger.error(f"Error in analyze_with_gemma: {str(e)}")
        logger.info("[Gemma] Falling back to VADER due to error")
        return vader.polarity_scores(text)["compound"]
