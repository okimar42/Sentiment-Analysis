from typing import Any, Callable, Optional

# Main Celery application class
class Celery:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def config_from_object(self, obj: Any, **kwargs: Any) -> None: ...
    def autodiscover_tasks(self, *args: Any, **kwargs: Any) -> None: ...
    
    class Control:
        class Inspect:
            def active(self) -> Any: ...
        
        inspect: Inspect
    
    control: Control

# Task decorator
def shared_task(func: Optional[Callable] = ..., **kwargs: Any) -> Callable: ...

# Current app instance
current_app: Celery

__all__ = ["Celery", "shared_task", "current_app"]