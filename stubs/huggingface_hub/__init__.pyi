from typing import Optional

# Public API we rely on

def login(token: Optional[str] = ...) -> None: ...

class HfFolder:
    @staticmethod
    def get_token() -> Optional[str]: ...