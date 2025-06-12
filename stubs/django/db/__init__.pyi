from typing import Any, Optional, Union, Dict, List, Callable, Type, TypeVar, Generic
from typing_extensions import ParamSpec

_T = TypeVar('_T')
_P = ParamSpec('_P')

# Transaction management
class transaction:
    def __init__(self, using: Optional[str] = ..., savepoint: bool = ..., durable: bool = ...) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None: ...
    
    @staticmethod
    def atomic(using: Optional[str] = ..., savepoint: bool = ..., durable: bool = ...) -> Any: ...
    
    @staticmethod
    def commit(using: Optional[str] = ...) -> None: ...
    
    @staticmethod
    def rollback(using: Optional[str] = ...) -> None: ...
    
    @staticmethod
    def savepoint(using: Optional[str] = ...) -> str: ...
    
    @staticmethod
    def savepoint_commit(sid: str, using: Optional[str] = ...) -> None: ...
    
    @staticmethod
    def savepoint_rollback(sid: str, using: Optional[str] = ...) -> None: ...

__all__ = ["transaction"]