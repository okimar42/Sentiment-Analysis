#!/usr/bin/env python3
"""Standalone Sentiment Analysis Processor
Replicates webapp functionality for automated execution (skeleton).
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Any

import click

# ---------------------------------------------------------------------------
# Data classes & configuration helpers
# ---------------------------------------------------------------------------


@dataclass
class ProcessingConfig:
    """Configuration matching webapp's SentimentAnalysis model"""

    query: str  # Search terms or subreddits
    sources: List[str]  # ["reddit", "twitter"]
    models: List[str]  # ["vader", "gpt4", "claude", "gemini", "gemma"]
    start_date: datetime
    end_date: datetime
    include_images: bool = False
    max_posts: int = 100
    output_format: str = "json"  # "json", "csv", "sqlite"
    output_path: str | Path = Path("results")

    def to_json(self) -> str:
        """Return a JSON string representation suitable for logging/debugging."""
        def _serialize(o):
            if isinstance(o, (datetime, Path)):
                return str(o)
            return o

        return json.dumps(asdict(self), default=_serialize, indent=2)

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """Construct ProcessingConfig from dict (parsed from JSON)."""
        # Parse datetimes if provided as strings
        def _parse_datetime(value: str | datetime) -> datetime:
            if isinstance(value, datetime):
                return value
            return datetime.fromisoformat(value)

        return cls(
            query=data["query"],
            sources=data["sources"],
            models=data["models"],
            start_date=_parse_datetime(data["start_date"]),
            end_date=_parse_datetime(data["end_date"]),
            include_images=data.get("include_images", False),
            max_posts=int(data.get("max_posts", 100)),
            output_format=data.get("output_format", "json"),
            output_path=data.get("output_path", "results"),
        )


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------


def _build_config_from_cli(
    query: str,
    sources: str,
    models: str,
    days_back: int,
    max_posts: int,
    output_format: str,
    output_path: str,
    include_images: bool,
) -> ProcessingConfig:
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days_back)

    return ProcessingConfig(
        query=query,
        sources=[s.strip() for s in sources.split(",") if s.strip()],
        models=[m.strip() for m in models.split(",") if m.strip()],
        start_date=start_date,
        end_date=end_date,
        include_images=include_images,
        max_posts=max_posts,
        output_format=output_format,
        output_path=output_path,
    )


@click.command()
@click.option("--config", "config_path", help="JSON config file path")
@click.option("--query", "-q", help="Search query or subreddits (comma-separated)")
@click.option("--sources", default="reddit,twitter", help="Data sources: reddit,twitter")
@click.option("--models", default="vader", help="Models: vader,gpt4,claude,gemini,gemma")
@click.option("--days-back", type=int, default=7, help="Days of data to analyze")
@click.option("--max-posts", type=int, default=100, help="Max posts per source")
@click.option(
    "--output-format",
    type=click.Choice(["json", "csv", "sqlite"]),
    default="json",
    help="Output format",
)
@click.option("--output-path", default="./results", help="Output directory/file path")
@click.option("--include-images", is_flag=True, help="Include image analysis")
@click.option("--dry-run", is_flag=True, help="Show what would be processed without executing")
@click.option("--incremental", is_flag=True, help="Skip posts that were previously processed (uses .state directory)")
@click.option("--metrics-file", help="Write Prometheus metrics to file after processing")
@click.option("--health-check", is_flag=True, help="Print health status and exit")
@click.option("--enable-alerts", is_flag=True, help="Send alerts on errors (requires SLACK_WEBHOOK_URL or SMTP config)")
def main(
    config_path: Optional[str],
    query: Optional[str],
    sources: str,
    models: str,
    days_back: int,
    max_posts: int,
    output_format: str,
    output_path: str,
    include_images: bool,
    dry_run: bool,
    incremental: bool,
    metrics_file: Optional[str],
    health_check: bool,
    enable_alerts: bool,
):
    """Main entry point - replicate webapp's analyze_reddit_sentiment/analyze_twitter_sentiment (skeleton)."""

    if health_check:
        from scripts.data_processing.utils.health_check import health_check_json
        click.echo(health_check_json())
        return

    # Initialize metrics
    from scripts.data_processing.utils.metrics import get_metrics, reset_metrics
    reset_metrics()
    metrics = get_metrics()

    if config_path:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg_raw = json.load(f)
        config = ProcessingConfig.from_dict(cfg_raw)
    else:
        if not query:
            click.echo("Error: --query must be provided when not using --config", err=True)
            sys.exit(1)
        config = _build_config_from_cli(
            query=query,
            sources=sources,
            models=models,
            days_back=days_back,
            max_posts=max_posts,
            output_format=output_format,
            output_path=output_path,
            include_images=include_images,
        )

    click.echo("[SentimentProcessor] Configuration:\n" + config.to_json())

    if dry_run:
        click.echo("[SentimentProcessor] Dry-run enabled. Exiting without processing.")
        return

    # ---------------------------------------------------------------
    # Minimal end-to-end pipeline (Reddit + VADER only for now)
    # ---------------------------------------------------------------

    from scripts.data_processing.sources.reddit_processor import (
        RedditProcessor,
    )
    from scripts.data_processing.analysis.sentiment_engine import (
        SentimentEngine,
    )

    all_posts = []

    if "reddit" in [s.lower() for s in config.sources]:
        rp = RedditProcessor(
            max_posts=config.max_posts,
            start_date=config.start_date,
            end_date=config.end_date,
        )
        reddit_posts = rp.fetch_posts(config.query)
        if incremental:
            from scripts.data_processing.utils.state_tracker import StateTracker

            tracker = StateTracker()
            reddit_posts = tracker.filter_new(f"reddit_{config.query}", reddit_posts)
        metrics.record_fetch("reddit", len(reddit_posts))
        click.echo(
            f"[SentimentProcessor] Retrieved {len(reddit_posts)} posts from Reddit"
        )
        all_posts.extend(reddit_posts)

    if "twitter" in [s.lower() for s in config.sources]:
        try:
            from scripts.data_processing.sources.twitter_processor import (
                TwitterProcessor,
            )

            tp = TwitterProcessor(
                max_posts=config.max_posts,
                start_date=config.start_date,
                end_date=config.end_date,
            )
            twitter_posts = tp.fetch_posts(config.query)
            if incremental:
                from scripts.data_processing.utils.state_tracker import StateTracker

                tracker = StateTracker()
                twitter_posts = tracker.filter_new(f"twitter_{config.query}", twitter_posts)
            metrics.record_fetch("twitter", len(twitter_posts))
            click.echo(
                f"[SentimentProcessor] Retrieved {len(twitter_posts)} tweets from Twitter"
            )
            all_posts.extend(twitter_posts)
        except Exception as exc:
            click.echo(
                f"[SentimentProcessor] Error fetching tweets: {exc}",
                err=True,
            )

    if not all_posts:
        click.echo("[SentimentProcessor] No posts retrieved. Exiting.")
        return

    engine = SentimentEngine(models=config.models)
    texts = [p["content"] for p in all_posts]
    analysis_results = engine.analyze_batch(texts)

    # Record analysis metrics
    for model in config.models:
        metrics.record_analysis(model, len(texts))

    # Merge results back into post dictionaries
    for post, sentiment in zip(all_posts, analysis_results):
        post.update(sentiment)

    # Write output (JSON only for initial version)
    output_dir = Path(config.output_path)
    if output_dir.is_dir() is False:
        output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    if config.output_format == "json":
        output_file = output_dir / f"sentiment_{config.query.replace(',', '_')}_{timestamp}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "analysis_summary": {
                        "processed_at": datetime.utcnow().isoformat(),
                        "total_posts": len(all_posts),
                        "models_used": config.models,
                        "sources": config.sources,
                    },
                    "results": all_posts,
                },
                f,
                default=str,
                indent=2,
            )
        click.echo(f"[SentimentProcessor] JSON saved to {output_file}")

    elif config.output_format == "csv":
        from scripts.data_processing.output.csv_writer import save_analysis_csv

        output_file = output_dir / f"sentiment_{config.query.replace(',', '_')}_{timestamp}.csv"
        save_analysis_csv(all_posts, output_file)
        click.echo(f"[SentimentProcessor] CSV saved to {output_file}")

    elif config.output_format == "sqlite":
        from scripts.data_processing.output.sqlite_writer import save_analysis_sqlite

        output_file = output_dir / f"sentiment_{config.query.replace(',', '_')}_{timestamp}.db"
        save_analysis_sqlite(all_posts, output_file)
        click.echo(f"[SentimentProcessor] SQLite DB saved to {output_file}")

    else:
        click.echo(f"[SentimentProcessor] Unknown output format: {config.output_format}", err=True)

    # Finalize metrics and optionally write to file
    metrics.finalize()
    
    # Send alerts if enabled and conditions are met
    if enable_alerts:
        from scripts.data_processing.utils.alerting import send_alerts_if_needed
        send_alerts_if_needed()
    
    if metrics_file:
        with open(metrics_file, "w", encoding="utf-8") as f:
            f.write(metrics.to_prometheus_format())
        click.echo(f"[SentimentProcessor] Metrics written to {metrics_file}")


if __name__ == "__main__":
    main()