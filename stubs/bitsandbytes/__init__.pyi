from typing import Any, Optional

# Quantization classes
class Linear8bitLt:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class Linear4bit:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

# Optimizer classes
class AdamW8bit:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class SGD8bit:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

# Utility functions
def quantize(tensor: Any, **kwargs: Any) -> Any: ...
def dequantize(tensor: Any, **kwargs: Any) -> Any: ...

__all__ = [
    "Linear8bitLt",
    "Linear4bit", 
    "AdamW8bit",
    "SGD8bit",
    "quantize",
    "dequantize"
]