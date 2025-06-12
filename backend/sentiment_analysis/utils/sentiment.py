"""
Sentiment analysis utility functions.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER once at module level
vader = SentimentIntensityAnalyzer()

def compute_vader_score(text):
    """
    Compute VADER sentiment score for a given text.
    
    Args:
        text: Text to analyze
        
    Returns:
        float: VADER compound score between -1 and 1
    """
    if not isinstance(text, str):
        raise TypeError('Input to compute_vader_score must be a string')
    return vader.polarity_scores(text)['compound']