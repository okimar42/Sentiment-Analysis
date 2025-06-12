from typing import Any, Dict, Union, BinaryIO
from pathlib import Path

# Main functions
def load_file(filename: Union[str, Path], device: str = ...) -> Dict[str, Any]: ...

def save_file(tensors: Dict[str, Any], filename: Union[str, Path], metadata: Dict[str, str] = ...) -> None: ...

def load(data: bytes) -> Dict[str, Any]: ...

def save(tensors: Dict[str, Any], metadata: Dict[str, str] = ...) -> bytes: ...

# Torch integration
class torch:
    @staticmethod
    def load_file(filename: Union[str, Path], device: str = ...) -> Dict[str, Any]: ...
    
    @staticmethod
    def save_file(tensors: Dict[str, Any], filename: Union[str, Path], metadata: Dict[str, str] = ...) -> None: ...
    
    @staticmethod
    def load(data: bytes) -> Dict[str, Any]: ...
    
    @staticmethod 
    def save(tensors: Dict[str, Any], metadata: Dict[str, str] = ...) -> bytes: ...

__all__ = [
    "load_file",
    "save_file", 
    "load",
    "save",
    "torch"
]