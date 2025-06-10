"""
Gemma model analysis utilities.
"""

import os
import sys
import logging
from typing import Optional, Tuple, Any, Dict
from celery.utils.log import get_task_logger
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = get_task_logger(__name__)

# Initialize VADER as fallback
vader: SentimentIntensityAnalyzer = SentimentIntensityAnalyzer()

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
        if 'migrate' in sys.argv:
            return 0.0
            
        # Skip model loading if not in backend service
        if os.getenv('SERVICE_ROLE') != 'backend':
            logger.info("Not in backend service, skipping model loading")
            return 0.0
            
        from .huggingface import get_model
        
        # Lazy load the model
        tokenizer: Any
        model: Any
        tokenizer, model = get_model()
        
        if tokenizer is None or model is None:
            logger.info("[Gemma] Using VADER as fallback for sentiment analysis")
            fallback_scores: Dict[str, float] = vader.polarity_scores(text)
            return fallback_scores['compound']
            
        import torch
        
        # Tokenize input
        inputs: Dict[str, Any] = tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            max_length=512
        )
        
        # Run inference
        with torch.no_grad():
            outputs: Any = model(**inputs)
            scores: torch.Tensor = torch.softmax(outputs.logits, dim=1)
            
        # Calculate sentiment score
        sentiment_score: float = float(scores[0][1] - scores[0][0])
        return sentiment_score
        
    except Exception as e:
        logger.error(f"Error in analyze_with_gemma: {str(e)}")
        logger.info("[Gemma] Falling back to VADER due to error")
        error_fallback_scores: Dict[str, float] = vader.polarity_scores(text)
        return error_fallback_scores['compound']