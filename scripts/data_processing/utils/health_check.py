from __future__ import annotations

"""Health check endpoint for monitoring sentiment processor status."""

import json
import os
from datetime import datetime
from typing import Dict, Any

from .metrics import get_metrics


def check_api_keys() -> Dict[str, bool]:
    """Check if required API keys are available."""
    return {
        "reddit": all([
            os.getenv("REDDIT_CLIENT_ID"),
            os.getenv("REDDIT_CLIENT_SECRET"),
            os.getenv("REDDIT_USER_AGENT")
        ]),
        "twitter": bool(os.getenv("TWITTER_BEARER_TOKEN")),
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
        "google": bool(os.getenv("GOOGLE_API_KEY")),
    }


def get_health_status() -> Dict[str, Any]:
    """Generate comprehensive health check response."""
    metrics = get_metrics()
    api_keys = check_api_keys()
    
    # Determine overall health
    has_any_source = api_keys["reddit"] or api_keys["twitter"]
    has_any_model = api_keys["openai"] or api_keys["anthropic"] or api_keys["google"]
    
    status = "healthy"
    if not has_any_source:
        status = "degraded"  # Can't fetch data
    elif metrics.api_errors > 0 and metrics.api_errors / max(1, metrics.api_calls_made) > 0.5:
        status = "unhealthy"  # High error rate
    
    return {
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "api_keys_available": api_keys,
        "capabilities": {
            "sources": [k for k, v in api_keys.items() if v and k in ["reddit", "twitter"]],
            "models": [k for k, v in api_keys.items() if v and k in ["openai", "anthropic", "google"]],
        },
        "metrics": metrics.to_dict(),
        "checks": {
            "has_data_source": has_any_source,
            "has_analysis_model": has_any_model,
            "error_rate_acceptable": metrics.api_errors / max(1, metrics.api_calls_made) < 0.5,
        }
    }


def health_check_json() -> str:
    """Return health status as JSON string."""
    return json.dumps(get_health_status(), indent=2)


def health_check_simple() -> str:
    """Return simple OK/ERROR status."""
    status = get_health_status()
    return "OK" if status["status"] == "healthy" else "ERROR"