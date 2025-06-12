from typing import Any, Dict

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class SentimentAnalysis(models.Model):
    """
    Represents a sentiment analysis job, including query, sources, selected models, and status.
    """

    SOURCE_CHOICES = [
        ("reddit", "Reddit"),
        ("twitter", "Twitter"),
    ]

    MODEL_CHOICES = [
        ("vader", "VADER"),
        ("gpt4", "GPT-4"),
        ("claude", "Claude"),
        ("gemini", "Gemini"),
        ("gemma", "Gemma"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    query = models.CharField(max_length=255)
    source = models.JSONField(default=list, blank=True)
    model = models.CharField(max_length=10, choices=MODEL_CHOICES, default="vader")
    selected_llms = models.JSONField(default=list, blank=True)
    subreddits = models.JSONField(null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    include_images = models.BooleanField(default=False)
    content_summary = models.TextField(blank=True, null=True)

    def clean(self) -> None:
        """Validate that all sources are allowed."""
        allowed = {c[0] for c in self.SOURCE_CHOICES}
        if not isinstance(self.source, list):
            raise ValueError("source must be a list")
        for s in self.source:
            if s not in allowed:
                raise ValueError(f"Invalid source: {s}")

    class Meta:
        verbose_name_plural = "Sentiment Analyses"
        """Meta options for SentimentAnalysis model."""

    def __str__(self) -> str:
        """String representation of the analysis."""
        sources = (
            ",".join(self.source) if isinstance(self.source, list) else self.source
        )
        return f"{self.query} [{sources}] ({self.status})"


class SentimentResult(models.Model):
    """
    Stores the result of a sentiment analysis for a single post/tweet.
    """

    sentiment_analysis = models.ForeignKey(
        SentimentAnalysis, on_delete=models.CASCADE, related_name="results"
    )
    post_id = models.CharField(max_length=255)
    content = models.TextField()
    score = models.FloatField()
    compound_score = models.FloatField()
    has_images = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    post_date = models.DateTimeField(null=True, blank=True)

    # VADER score
    vader_score = models.FloatField(default=0)

    # LLM scores
    gpt4_score = models.FloatField(default=0)
    claude_score = models.FloatField(default=0)
    gemini_score = models.FloatField(default=0)

    # Sarcasm detection
    sarcasm_score = models.FloatField(default=0)
    is_sarcastic = models.BooleanField(default=False)

    # New fields for IQ and bot detection
    perceived_iq = models.FloatField(default=0)
    bot_probability = models.FloatField(default=0)
    is_bot = models.BooleanField(default=False)

    # Manual override fields
    manual_sentiment = models.FloatField(null=True, blank=True)
    manual_override = models.BooleanField(default=False)
    override_reason = models.TextField(blank=True)
    override_date = models.DateTimeField(null=True, blank=True)
    override_by = models.ForeignKey(
        "auth.User", null=True, blank=True, on_delete=models.SET_NULL
    )

    # Source-specific fields
    source_type = models.CharField(
        max_length=50, default="reddit"
    )  # 'reddit' or 'twitter'
    source_metadata = models.JSONField(default=dict)  # Store source-specific data

    # Ad flag
    is_ad = models.BooleanField(default=False)

    # Grok score
    grok_score = models.FloatField(default=0)

    class Meta:
        unique_together = ("sentiment_analysis", "post_id")
        indexes = [
            models.Index(fields=["post_date"]),
            models.Index(fields=["perceived_iq"]),
            models.Index(fields=["bot_probability"]),
            models.Index(fields=["source_type"]),
        ]
        """Meta options for SentimentResult model."""

    def __str__(self) -> str:
        """String representation of the result."""
        return f"Result for {self.sentiment_analysis.query} ({self.score})"

    @property
    def final_score(self) -> float:
        """Get the final sentiment score, considering manual overrides and model-specific scores."""
        if self.manual_override and self.manual_sentiment is not None:
            return self.manual_sentiment

        # If the main score is 0.0 but we have model-specific scores, use those instead
        if self.score == 0.0:
            # Check the analysis model to determine which score to prioritize
            analysis_model = self.sentiment_analysis.model
            if analysis_model == "vader" and self.vader_score != 0.0:
                return self.vader_score
            elif analysis_model == "gpt4" and self.gpt4_score != 0.0:
                return self.gpt4_score
            elif analysis_model == "gemini" and self.gemini_score != 0.0:
                return self.gemini_score
            elif analysis_model == "grok" and self.grok_score != 0.0:
                return self.grok_score
            # Fallback to VADER if no model-specific score is available
            elif self.vader_score != 0.0:
                return self.vader_score

        return self.score

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with all relevant fields."""
        return {
            "id": self.id,
            "post_id": self.post_id,
            "content": self.content,
            "score": self.final_score,
            "compound_score": self.compound_score,
            "has_images": self.has_images,
            "created_at": self.created_at,
            "post_date": self.post_date,
            "vader_score": self.vader_score,
            "gpt4_score": self.gpt4_score,
            "claude_score": self.claude_score,
            "gemini_score": self.gemini_score,
            "sarcasm_score": self.sarcasm_score,
            "is_sarcastic": self.is_sarcastic,
            "perceived_iq": self.perceived_iq,
            "bot_probability": self.bot_probability,
            "is_bot": self.is_bot,
            "manual_override": self.manual_override,
            "manual_sentiment": self.manual_sentiment,
            "source_type": self.source_type,
            "source_metadata": self.source_metadata,
            "grok_score": self.grok_score,
        }


class ImageSentimentResult(models.Model):
    sentiment_result = models.ForeignKey(
        SentimentResult, on_delete=models.CASCADE, related_name="image_results"
    )
    image_url = models.URLField()
    image_description = models.TextField()
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Vision model scores
    gpt4_vision_score = models.FloatField(default=0)
    claude_vision_score = models.FloatField(default=0)
    gemini_vision_score = models.FloatField(default=0)

    class Meta:
        unique_together = ("sentiment_result", "image_url")

    def __str__(self):
        return f"Image result for {self.sentiment_result.sentiment_analysis.query} ({self.score})"
