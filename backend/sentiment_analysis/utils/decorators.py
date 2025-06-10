"""
Decorator utilities for performance monitoring and task management.
"""

import time
import functools
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

def timing_decorator(func):
    """
    Decorator to log execution time of functions.
    
    Args:
        func: Function to wrap with timing
        
    Returns:
        Wrapped function that logs execution time
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"[TIMING] {func.__name__} took {duration:.2f}s")
        return result
    return wrapper