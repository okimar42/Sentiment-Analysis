from __future__ import annotations

"""Error alerting and notification utilities."""

import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional

import requests  # type: ignore

from .metrics import get_metrics
from .health_check import get_health_status


def send_slack_alert(webhook_url: str, message: str, channel: Optional[str] = None) -> bool:
    """Send alert to Slack webhook."""
    try:
        payload = {
            "text": message,
            "username": "sentiment-processor",
            "icon_emoji": ":warning:",
        }
        if channel:
            payload["channel"] = channel
            
        response = requests.post(webhook_url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception:
        return False


def send_email_alert(
    smtp_host: str,
    smtp_port: int,
    username: str,
    password: str,
    to_email: str,
    subject: str,
    message: str,
    use_tls: bool = True,
) -> bool:
    """Send email alert via SMTP."""
    try:
        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))
        
        server = smtplib.SMTP(smtp_host, smtp_port)
        if use_tls:
            server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception:
        return False


def check_alert_conditions() -> Dict[str, Any]:
    """Check if any alert conditions are met."""
    health = get_health_status()
    metrics = get_metrics()
    
    alerts = []
    
    # High error rate
    if metrics.api_calls_made > 0:
        error_rate = metrics.api_errors / metrics.api_calls_made
        if error_rate > 0.5:
            alerts.append({
                "severity": "critical",
                "message": f"High API error rate: {error_rate:.1%} ({metrics.api_errors}/{metrics.api_calls_made})",
                "metric": "error_rate",
                "value": error_rate,
            })
    
    # No data sources available
    if not health["checks"]["has_data_source"]:
        alerts.append({
            "severity": "critical", 
            "message": "No data sources available (missing Reddit/Twitter credentials)",
            "metric": "data_sources",
            "value": 0,
        })
    
    # No analysis models available
    if not health["checks"]["has_analysis_model"]:
        alerts.append({
            "severity": "warning",
            "message": "No LLM models available (missing API keys), falling back to VADER only",
            "metric": "analysis_models", 
            "value": 0,
        })
    
    # Zero posts fetched (potential issue)
    if metrics.posts_fetched == 0:
        alerts.append({
            "severity": "warning",
            "message": "No posts were fetched - check query parameters or API connectivity",
            "metric": "posts_fetched",
            "value": 0,
        })
    
    return {
        "alerts": alerts,
        "alert_count": len(alerts),
        "has_critical": any(a["severity"] == "critical" for a in alerts),
        "has_warnings": any(a["severity"] == "warning" for a in alerts),
    }


def send_alerts_if_needed() -> None:
    """Check conditions and send alerts via configured channels."""
    alert_status = check_alert_conditions()
    
    if alert_status["alert_count"] == 0:
        return
    
    # Format alert message
    alerts = alert_status["alerts"]
    critical_alerts = [a for a in alerts if a["severity"] == "critical"]
    warning_alerts = [a for a in alerts if a["severity"] == "warning"]
    
    message_parts = ["🚨 Sentiment Processor Alerts"]
    
    if critical_alerts:
        message_parts.append("\n**CRITICAL:**")
        for alert in critical_alerts:
            message_parts.append(f"• {alert['message']}")
    
    if warning_alerts:
        message_parts.append("\n**WARNINGS:**")
        for alert in warning_alerts:
            message_parts.append(f"• {alert['message']}")
    
    metrics = get_metrics()
    message_parts.extend([
        f"\n**Summary:**",
        f"• Posts fetched: {metrics.posts_fetched}",
        f"• Posts analyzed: {metrics.posts_analyzed}", 
        f"• API calls: {metrics.api_calls_made}",
        f"• API errors: {metrics.api_errors}",
        f"• Duration: {metrics.processing_duration:.1f}s",
    ])
    
    message = "\n".join(message_parts)
    
    # Send to Slack if configured
    slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
    if slack_webhook:
        send_slack_alert(slack_webhook, message)
    
    # Send email if configured
    if all(os.getenv(k) for k in ["SMTP_HOST", "SMTP_USER", "SMTP_PASS", "ALERT_EMAIL"]):
        send_email_alert(
            smtp_host=os.getenv("SMTP_HOST", ""),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            username=os.getenv("SMTP_USER", ""),
            password=os.getenv("SMTP_PASS", ""),
            to_email=os.getenv("ALERT_EMAIL", ""),
            subject="Sentiment Processor Alert",
            message=message,
        )