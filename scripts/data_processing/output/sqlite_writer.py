from __future__ import annotations

"""Utility to persist analysis results into a local SQLite DB matching webapp schema."""

import sqlite3
from pathlib import Path
from typing import List, Dict, Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS sentiment_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id TEXT,
    content TEXT,
    score REAL,
    compound_score REAL,
    post_date TEXT,
    perceived_iq REAL,
    bot_probability REAL,
    source_type TEXT,
    manual_sentiment REAL,
    override_reason TEXT
);
"""

INSERT_SQL = """
INSERT INTO sentiment_results (
    post_id, content, score, compound_score, post_date, perceived_iq, bot_probability,
    source_type, manual_sentiment, override_reason
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""


def save_analysis_sqlite(results: List[Dict[str, Any]], db_path: str | Path) -> None:
    """Save *results* into SQLite database located at *db_path*.

    Only a subset of the full Django model fields is stored—the same subset
    exported in the CSV—to keep the schema light.
    """
    path = Path(db_path)
    if path.parent.exists() is False:
        path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(path.as_posix())
    cur = conn.cursor()
    cur.executescript(SCHEMA)

    for item in results:
        cur.execute(
            INSERT_SQL,
            (
                item.get("post_id"),
                item.get("content"),
                item.get("score")
                or item.get("compound_score")
                or item.get("vader_score"),
                item.get("compound_score", 0.0),
                str(item.get("post_date")),
                item.get("perceived_iq"),
                item.get("bot_probability"),
                item.get("source_type"),
                item.get("manual_sentiment"),
                item.get("override_reason"),
            ),
        )

    conn.commit()
    conn.close()