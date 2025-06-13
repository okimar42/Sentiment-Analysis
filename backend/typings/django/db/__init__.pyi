from typing import Any, ContextManager

class _Transaction:
    def atomic(self, *args: Any, **kwargs: Any) -> ContextManager[Any]: ...

transaction: _Transaction