"""
Rate limiting utilities for API requests.
"""

import time
import asyncio
import logging
from typing import Dict, Any

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# Model-specific rate limiting settings
RATE_LIMITS = {
    'gpt4': {
        'initial_delay': 2.0,
        'min_delay': 1.0,
        'max_delay': 10.0,
        'batch_size': 2,
        'min_retry_delay': 2.0,
        'retry_multiplier': 2.0
    },
    'gemini': {
        'initial_delay': 1.5,
        'min_delay': 0.8,
        'max_delay': 6.0,
        'batch_size': 3,
        'min_retry_delay': 1.5,
        'retry_multiplier': 1.5
    },
    'grok': {
        'initial_delay': 2.0,
        'min_delay': 1.0,
        'max_delay': 8.0,
        'batch_size': 2,
        'min_retry_delay': 2.0,
        'retry_multiplier': 2.0
    },
    'default': {
        'initial_delay': 2.0,
        'min_delay': 1.0,
        'max_delay': 8.0,
        'batch_size': 2,
        'min_retry_delay': 2.0,
        'retry_multiplier': 2.0
    }
}

class ModelRateLimiter:
    """Rate limiter for API models with adaptive delay."""
    
    def __init__(self, model_name: str):
        """
        Initialize rate limiter for a specific model.
        
        Args:
            model_name: Name of the model to apply rate limiting to
        """
        self.model_name = model_name
        self.settings = RATE_LIMITS.get(model_name, RATE_LIMITS['default'])
        self.current_delay = self.settings['initial_delay']
        self.lock = asyncio.Lock()
        self.last_request_time = 0
        self.consecutive_failures = 0
    
    async def wait(self):
        """Wait for the appropriate delay before making a request."""
        async with self.lock:
            now = time.time()
            time_since_last = now - self.last_request_time
            if time_since_last < self.current_delay:
                wait_time = self.current_delay - time_since_last
                await asyncio.sleep(wait_time)
            self.last_request_time = time.time()
    
    def increase_delay(self):
        """Increase delay due to rate limiting or failures."""
        # Increase delay more aggressively if we've had consecutive failures
        self.consecutive_failures += 1
        multiplier = self.settings['retry_multiplier'] * (1.5 ** (self.consecutive_failures - 1))
        new_delay = self.current_delay * multiplier
        self.current_delay = min(
            max(new_delay, self.settings['min_retry_delay']), 
            self.settings['max_delay']
        )
        logger.info(
            f"Increased {self.model_name} delay to {self.current_delay:.1f}s "
            f"after {self.consecutive_failures} consecutive failures"
        )
    
    def decrease_delay(self):
        """Decrease delay after successful requests."""
        # Reset consecutive failures on success
        self.consecutive_failures = 0
        self.current_delay = max(
            self.current_delay * 0.8, 
            self.settings['min_delay']
        )
        logger.info(
            f"Decreased {self.model_name} delay to {self.current_delay:.1f}s "
            f"due to successful request"
        )
    
    @property
    def batch_size(self) -> int:
        """Get current batch size, reduced if there have been failures."""
        # Reduce batch size if we've had failures
        return max(1, self.settings['batch_size'] - self.consecutive_failures)

# Global rate limiters for each model
rate_limiters = {
    'gpt4': ModelRateLimiter('gpt4'),
    'gemini': ModelRateLimiter('gemini'),
    'grok': ModelRateLimiter('grok'),
    'default': ModelRateLimiter('default')
}

def get_rate_limiter(model_name: str) -> ModelRateLimiter:
    """
    Get rate limiter for a specific model.
    
    Args:
        model_name: Name of the model
        
    Returns:
        ModelRateLimiter: Rate limiter instance for the model
    """
    return rate_limiters.get(model_name, rate_limiters['default'])