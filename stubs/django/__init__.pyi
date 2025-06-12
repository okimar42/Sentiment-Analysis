from typing import Any

# Version info
VERSION: tuple
version: str

def setup(set_prefix: bool = ...) -> None: ...

__all__ = ["VERSION", "setup"]