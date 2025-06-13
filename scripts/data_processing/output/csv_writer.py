from __future__ import annotations

"""Utility to export analysis results to CSV matching webapp format."""

import csv
from pathlib import Path
from typing import List, Dict, Any

CSV_HEADER = [
    "ID",
    "Content",
    "Score",
    "Post Date",
    "Perceived IQ",
    "Bot Probability",
    "Source Type",
    "Post ID",
    "Manual Sentiment",
    "Override Reason",
]


def save_analysis_csv(results: List[Dict[str, Any]], filepath: str | Path) -> None:
    """Save *results* (list of dicts) to CSV at *filepath*.

    Each dict should follow the schema produced by SentimentEngine & Processor.
    Fields missing in the CSV header will be left blank.
    """
    path = Path(filepath)
    if path.parent.exists() is False:
        path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADER)

        for idx, item in enumerate(results, start=1):
            writer.writerow(
                [
                    idx,
                    item.get("content", ""),
                    item.get("score")
                    or item.get("compound_score")
                    or item.get("vader_score"),
                    item.get("post_date"),
                    item.get("perceived_iq", ""),
                    item.get("bot_probability", ""),
                    item.get("source_type", ""),
                    item.get("post_id", ""),
                    item.get("manual_sentiment", ""),
                    item.get("override_reason", ""),
                ]
            )