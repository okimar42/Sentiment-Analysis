from django.contrib import admin

from .models import ImageSentimentResult, SentimentAnalysis, SentimentResult


@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):
    list_display = ("query", "source", "model", "user", "created_at", "status")
    list_filter = ("source", "model", "created_at", "status")
    search_fields = ("query", "user__username")
    readonly_fields = ("created_at", "updated_at")


@admin.register(SentimentResult)
class SentimentResultAdmin(admin.ModelAdmin):
    list_display = (
        "post_id",
        "sentiment_analysis",
        "score",
        "compound_score",
        "vader_score",
        "gpt4_score",
        "claude_score",
        "gemini_score",
        "grok_score",
        "created_at",
    )
    list_filter = ("sentiment_analysis", "created_at")
    search_fields = ("post_id", "content")
    readonly_fields = ("created_at",)


@admin.register(ImageSentimentResult)
class ImageSentimentResultAdmin(admin.ModelAdmin):
    list_display = (
        "sentiment_result",
        "image_url",
        "score",
        "gpt4_vision_score",
        "claude_vision_score",
        "gemini_vision_score",
        "created_at",
    )
    list_filter = ("sentiment_result__sentiment_analysis", "created_at")
    search_fields = ("image_url", "image_description")
    readonly_fields = ("created_at",)
