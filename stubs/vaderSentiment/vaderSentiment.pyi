from typing import Dict

class SentimentIntensityAnalyzer:
    """
    VADER sentiment analysis class.
    """
    def __init__(self, lexicon_file: str = ..., emoji_lexicon: str = ...) -> None: ...
    
    def polarity_scores(self, text: str) -> Dict[str, float]:
        """
        Return a float for sentiment strength based on the input text.
        Positive values are positive valence, negative value are negative valence.
        
        Returns:
            Dict with keys 'compound', 'pos', 'neu', 'neg' and float values
        """
        ...

__all__ = ["SentimentIntensityAnalyzer"]