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
    
    emoji_data = emoji.EMOJI_DATA
    def is_emoji(char):
        # Handle MagicMock for testing
        if hasattr(emoji_data, '__contains__'):
            try:
                return char in emoji_data
            except TypeError:
                # MagicMock: fallback to single-arg
                return emoji_data.__contains__(char)
        return False
    emoji_count = sum(1 for char in text if is_emoji(char))
    
    # Calculate emoji ratio
    emoji_ratio = emoji_count / len(text)
    
    # Consider text mostly emojis if more than 50% are emojis
    return emoji_ratio > 0.5