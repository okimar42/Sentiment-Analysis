from __future__ import annotations

"""Prometheus metrics collection for sentiment processor monitoring."""

import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ProcessingMetrics:
    """Collect runtime metrics for monitoring and alerting."""
    
    start_time: float = field(default_factory=time.time)
    posts_fetched: int = 0
    posts_analyzed: int = 0
    api_calls_made: int = 0
    api_errors: int = 0
    processing_duration: float = 0.0
    source_counts: Dict[str, int] = field(default_factory=dict)
    model_counts: Dict[str, int] = field(default_factory=dict)
    error_details: list[str] = field(default_factory=list)
    
    def record_fetch(self, source: str, count: int) -> None:
        """Record posts fetched from a source."""
        self.posts_fetched += count
        self.source_counts[source] = self.source_counts.get(source, 0) + count
    
    def record_analysis(self, model: str, count: int = 1) -> None:
        """Record analysis completed with a model."""
        self.posts_analyzed += count
        self.model_counts[model] = self.model_counts.get(model, 0) + count
    
    def record_api_call(self, success: bool = True, error: Optional[str] = None) -> None:
        """Record API call result."""
        self.api_calls_made += 1
        if not success:
            self.api_errors += 1
            if error:
                self.error_details.append(error)
    
    def finalize(self) -> None:
        """Mark processing complete and calculate duration."""
        self.processing_duration = time.time() - self.start_time
    
    def to_prometheus_format(self) -> str:
        """Export metrics in Prometheus text format."""
        lines = [
            f"# HELP sentiment_processor_posts_fetched_total Total posts fetched",
            f"# TYPE sentiment_processor_posts_fetched_total counter",
            f"sentiment_processor_posts_fetched_total {self.posts_fetched}",
            "",
            f"# HELP sentiment_processor_posts_analyzed_total Total posts analyzed", 
            f"# TYPE sentiment_processor_posts_analyzed_total counter",
            f"sentiment_processor_posts_analyzed_total {self.posts_analyzed}",
            "",
            f"# HELP sentiment_processor_api_calls_total Total API calls made",
            f"# TYPE sentiment_processor_api_calls_total counter", 
            f"sentiment_processor_api_calls_total {self.api_calls_made}",
            "",
            f"# HELP sentiment_processor_api_errors_total Total API errors",
            f"# TYPE sentiment_processor_api_errors_total counter",
            f"sentiment_processor_api_errors_total {self.api_errors}",
            "",
            f"# HELP sentiment_processor_duration_seconds Processing duration",
            f"# TYPE sentiment_processor_duration_seconds gauge",
            f"sentiment_processor_duration_seconds {self.processing_duration:.2f}",
            "",
        ]
        
        # Source-specific metrics
        if self.source_counts:
            lines.extend([
                "# HELP sentiment_processor_posts_by_source Posts fetched by source",
                "# TYPE sentiment_processor_posts_by_source gauge",
            ])
        for source, count in self.source_counts.items():
            lines.extend([
                f"sentiment_processor_posts_by_source{{source=\"{source}\"}} {count}",
            ])
        
        # Model-specific metrics  
        if self.model_counts:
            lines.extend([
                "# HELP sentiment_processor_analyses_by_model Analyses by model",
                "# TYPE sentiment_processor_analyses_by_model gauge",
            ])
        for model, count in self.model_counts.items():
            lines.extend([
                f"sentiment_processor_analyses_by_model{{model=\"{model}\"}} {count}",
            ])
            
        return "\n".join(lines)
    
    def to_dict(self) -> Dict[str, Any]:
        """Export as dictionary for JSON health checks."""
        return {
            "posts_fetched": self.posts_fetched,
            "posts_analyzed": self.posts_analyzed,
            "api_calls_made": self.api_calls_made,
            "api_errors": self.api_errors,
            "processing_duration": self.processing_duration,
            "source_counts": self.source_counts,
            "model_counts": self.model_counts,
            "error_count": len(self.error_details),
            "success_rate": (self.api_calls_made - self.api_errors) / max(1, self.api_calls_made),
        }


# Global metrics instance for the processor
_metrics: Optional[ProcessingMetrics] = None


def get_metrics() -> ProcessingMetrics:
    """Get or create global metrics instance."""
    global _metrics
    if _metrics is None:
        _metrics = ProcessingMetrics()
    return _metrics


def reset_metrics() -> None:
    """Reset global metrics (for testing or new runs)."""
    global _metrics
    _metrics = ProcessingMetrics()