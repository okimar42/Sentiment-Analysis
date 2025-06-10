from typing import Any, Optional, Tuple

float16: Any

class _CudaModule:
    @staticmethod
    def is_available() -> bool: ...
    @staticmethod
    def empty_cache() -> None: ...
    @staticmethod
    def mem_get_info() -> Tuple[int, int]: ...

cuda: _CudaModule

def __getattr__(name: str) -> Any: ...