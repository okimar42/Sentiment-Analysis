from typing import Any

class CeleryError(Exception):
    """Base class for all Celery exceptions."""
    pass

class MaxRetriesExceededError(CeleryError):
    """Raised when a task exceeds its maximum retry count."""
    pass

class Retry(CeleryError):
    """Signal task retry."""
    pass

__all__ = ["CeleryError", "MaxRetriesExceededError", "Retry"]