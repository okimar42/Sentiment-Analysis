from typing import Any

class _Control:
    def inspect(self) -> Any: ...

class _CeleryApp:
    control: _Control

current_app: _CeleryApp