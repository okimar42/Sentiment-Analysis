"""
Text processing utility functions.
"""

import emoji

def is_mostly_emojis(text: str) -> bool:
    """
    Check if the text consists mostly of emojis.
    
    Args:
        text: Text to analyze
        
    Returns:
        bool: True if more than 50% of characters are emojis
    """
    if not text:
        return False
    
    # Count emoji characters
    emoji_count = sum(1 for char in text if char in emoji.EMOJI_DATA)
    
    # Calculate emoji ratio
    emoji_ratio = emoji_count / len(text)
    
    # Consider text mostly emojis if more than 50% are emojis
    return emoji_ratio > 0.5