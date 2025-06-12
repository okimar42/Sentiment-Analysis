from typing import Dict, Any, Union, Set, Optional, Callable

# Emoji data - main constant used in the codebase
EMOJI_DATA: Dict[str, Any]

# Core functions
def emojize(string: str, language: str = ..., delimiters: tuple = ..., variant: Optional[str] = ...) -> str: ...

def demojize(string: str, language: str = ..., delimiters: tuple = ..., variant: Optional[str] = ...) -> str: ...

def replace_emoji(string: str, replace: Union[str, Callable] = ..., language: str = ...) -> str: ...

def emoji_count(string: str) -> int: ...

def distinct_emoji_list(string: str) -> list: ...

def is_emoji(string: str) -> bool: ...

# Language support
def get_emoji_unicode_dict(language: str = ...) -> Dict[str, str]: ...

__all__ = [
    "EMOJI_DATA",
    "emojize",
    "demojize", 
    "replace_emoji",
    "emoji_count",
    "distinct_emoji_list",
    "is_emoji",
    "get_emoji_unicode_dict"
]