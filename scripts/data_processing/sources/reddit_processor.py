from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Dict, Any

import os

import praw  # type: ignore

from scripts.data_processing.sources.base_processor import BaseProcessor


class RedditProcessor(BaseProcessor):
    """Fetch Reddit submissions for sentiment processing.

    This is an extraction of the logic that previously lived in
    `backend/sentiment_analysis/tasks_original_backup.py::analyze_reddit_sentiment`.
    It remains faithful to the original behaviour while removing all Django
    dependencies. Only public PRAW APIs are used.
    """

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        user_agent: str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._reddit = praw.Reddit(
            client_id=client_id or os.getenv("REDDIT_CLIENT_ID"),
            client_secret=client_secret or os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=user_agent or os.getenv("REDDIT_USER_AGENT", "sentiment-processor/1.0"),
            # PRAW will fall back to read-only mode if credentials are missing
        )

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------

    def fetch_posts(self, query: str) -> List[Dict[str, Any]]:  # noqa: D401
        """Return posts for *subreddits* specified in *query*.

        The *query* parameter is interpreted exactly the same way as the webapp:
        a comma-separated list of subreddit names (case-insensitive, no leading
        'r/'). Each subreddit is fetched using the `.hot` listing. PRAW does
        not currently offer server-side time filtering on the `hot` endpoint,
        so we simply filter client-side after retrieval.
        """
        subreddits = [s.strip() for s in query.split(",") if s.strip()]
        all_results: List[Dict[str, Any]] = []

        for subreddit_name in subreddits:
            subreddit = self._reddit.subreddit(subreddit_name)
            try:
                # Fetch up to *max_posts* posts per subreddit (as per original code)
                submissions = subreddit.hot(limit=self.max_posts)
            except Exception as exc:  # pragma: no cover — network/credential issues
                # Log and continue instead of failing the entire pipeline.
                print(f"[RedditProcessor] Error fetching subreddit {subreddit_name}: {exc}")
                continue

            for submission in submissions:
                # Combine title and self-text similar to original implementation
                title = submission.title or ""
                body = submission.selftext or ""
                if not (title or body):
                    continue  # Skip empty content

                created_at = datetime.fromtimestamp(submission.created_utc, tz=timezone.utc)
                # Date range filtering (if provided)
                if self.start_date and created_at < self.start_date:
                    continue
                if self.end_date and created_at > self.end_date:
                    continue

                has_images = bool(
                    submission.url and submission.url.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))
                )

                all_results.append(
                    {
                        "post_id": submission.id,
                        "content": f"{title}\n{body}".strip(),
                        "created_at": created_at,
                        "has_images": has_images,
                        "source_type": "reddit",
                        "source_metadata": {
                            "author": submission.author.name if submission.author else None,
                            "subreddit": submission.subreddit.display_name,
                            "upvotes": submission.ups,
                            "downvotes": submission.downs,
                            "num_comments": submission.num_comments,
                            "permalink": submission.permalink,
                            "url": submission.url,
                        },
                    }
                )

            if len(all_results) >= self.max_posts:
                break  # Global limit reached.

        return all_results[: self.max_posts]