from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any


class BaseProcessor(ABC):
    """Abstract base class for data source processors (e.g., Reddit, Twitter)."""

    def __init__(self, max_posts: int = 100, start_date: datetime | None = None, end_date: datetime | None = None):
        self.max_posts = max_posts
        self.start_date = start_date
        self.end_date = end_date

    @abstractmethod
    def fetch_posts(self, query: str) -> List[Dict[str, Any]]:
        """Fetch and return a list of post dictionaries matching *query*.

        Each dictionary MUST contain at minimum the following keys so that the
        downstream sentiment engine can operate without branching logic:
            - post_id (str | int)
            - content (str)             Full text content (title + body for Reddit)
            - created_at (datetime)
            - has_images (bool)
            - source_metadata (dict[str, Any])

        Implementations may return additional keys which will be preserved.
        """
        raise NotImplementedError