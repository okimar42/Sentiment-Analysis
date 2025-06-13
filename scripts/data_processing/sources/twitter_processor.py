from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Dict, Any

import os

import tweepy  # type: ignore

from scripts.data_processing.sources.base_processor import BaseProcessor


class TwitterProcessor(BaseProcessor):
    """Fetch tweets for sentiment processing using the Twitter API v2.

    The implementation mirrors the original web-app logic in
    `backend/sentiment_analysis/tasks_original_backup.py::analyze_twitter_sentiment`
    but returns raw tweet dictionaries for downstream analysis instead of
    persisting to Django models.
    """

    def __init__(
        self,
        bearer_token: str | None = None,
        api_key: str | None = None,
        api_secret: str | None = None,
        access_token: str | None = None,
        access_token_secret: str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._client = tweepy.Client(
            bearer_token=bearer_token or os.getenv("TWITTER_BEARER_TOKEN"),
            consumer_key=api_key or os.getenv("TWITTER_API_KEY"),
            consumer_secret=api_secret or os.getenv("TWITTER_API_SECRET"),
            access_token=access_token or os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=access_token_secret or os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
            wait_on_rate_limit=True,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def fetch_posts(self, query: str) -> List[Dict[str, Any]]:  # noqa: D401
        """Search recent tweets matching *query* and return post dictionaries.

        The behaviour follows the web-app: recent tweets only, up to
        *max_posts*. Date range filtering is handled client-side when necessary.
        """
        all_results: List[Dict[str, Any]] = []

        # Build search params
        search_kwargs: Dict[str, Any] = {
            "query": query,
            "tweet_fields": ["created_at", "text", "attachments"],
            "max_results": min(self.max_posts, 100),  # per-request cap
        }

        # API allows start_time / end_time within last 7 days window for recent search
        if self.start_date:
            search_kwargs["start_time"] = self.start_date.astimezone(timezone.utc)
        if self.end_date:
            search_kwargs["end_time"] = self.end_date.astimezone(timezone.utc)

        paginator = tweepy.Paginator(
            self._client.search_recent_tweets,
            **search_kwargs,
        )

        for response in paginator:
            if response.data is None:
                break
            for tweet in response.data:
                created_at: datetime | None = getattr(tweet, "created_at", None)
                if created_at is None:
                    # Twitter may omit timestamp; skip such tweets
                    continue
                # Additional safety filtering for date range if API params not effective
                if self.start_date and created_at < self.start_date:
                    continue
                if self.end_date and created_at > self.end_date:
                    continue

                has_images = bool(getattr(tweet, "attachments", None))

                all_results.append(
                    {
                        "post_id": tweet.id,
                        "content": tweet.text,
                        "created_at": created_at,
                        "has_images": has_images,
                        "source_type": "twitter",
                        "source_metadata": {
                            "created_at": created_at.isoformat() if created_at else None,
                        },
                    }
                )

                if len(all_results) >= self.max_posts:
                    break
            if len(all_results) >= self.max_posts:
                break

        return all_results