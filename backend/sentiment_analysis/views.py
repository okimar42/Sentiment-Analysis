import asyncio
import logging
from typing import Any, Dict

import aiohttp
from drf_spectacular.openapi import AutoSchema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from django.db import models
from django.http import Http404, StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import SentimentAnalysis, SentimentResult
from .serializers import (
    SentimentAnalysisCreateSerializer,
    SentimentAnalysisSerializer,
    SentimentResultSerializer,
    UserRegistrationSerializer,
)
from .image_tasks import get_model  # type: ignore

logger = logging.getLogger(__name__)


def get_analysis_summary(results) -> Dict[str, Any]:
    """Compute summary statistics for a queryset of SentimentResult."""
    scores = [r.final_score for r in results]
    total_posts = len(scores)
    avg_score = sum(scores) / total_posts if total_posts else 0
    positive = sum(1 for s in scores if s > 0.05)
    negative = sum(1 for s in scores if s < -0.05)
    neutral = sum(1 for s in scores if -0.05 <= s <= 0.05)
    return {
        "total_posts": total_posts,
        "average_score": avg_score,
        "sentiment_distribution": {
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
        },
        "sentiment_percentages": {
            "positive": (positive / total_posts) * 100 if total_posts else 0,
            "negative": (negative / total_posts) * 100 if total_posts else 0,
            "neutral": (neutral / total_posts) * 100 if total_posts else 0,
        },
    }


class SentimentAnalysisViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing sentiment analysis tasks and their results.
    Provides endpoints for creating analyses, retrieving results, and getting summary statistics.
    """

    permission_classes = [AllowAny]
    serializer_class = SentimentAnalysisSerializer
    schema = AutoSchema()

    def update_result(self, request, pk=None, result_id=None):
        """Update a specific result's sentiment score."""
        try:
            analysis = self.get_object()
            result = SentimentResult.objects.get(
                id=result_id, sentiment_analysis=analysis
            )
            manual_sentiment = request.data.get("manual_sentiment")
            if manual_sentiment is None:
                manual_sentiment = request.data.get("score")
            if manual_sentiment is not None:
                result.manual_sentiment = manual_sentiment
                result.score = manual_sentiment
                result.manual_override = True
                result.override_reason = request.data.get("override_reason", "")
                result.override_date = timezone.now()
                result.override_by = (
                    request.user if request.user.is_authenticated else None
                )
                result.save()
            return Response(SentimentResultSerializer(result).data)
        except SentimentResult.DoesNotExist:
            return Response(
                {"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating result: {str(e)}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["get"])
    def health(self, request):
        """Health check endpoint."""
        try:
            SentimentAnalysis.objects.count()
            from celery import current_app

            current_app.control.inspect().active()
            return Response(
                {
                    "status": "healthy",
                    "database": "connected",
                    "redis": "connected",
                    "timestamp": timezone.now().isoformat(),
                }
            )
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return Response(
                {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": timezone.now().isoformat(),
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

    def get_queryset(self) -> models.QuerySet:
        """Return all sentiment analyses, sorted by newest first."""
        return SentimentAnalysis.objects.all().order_by("-created_at")

    def get_serializer_class(self) -> type:
        """Return appropriate serializer based on action."""
        if self.action == "create":
            return SentimentAnalysisCreateSerializer
        return SentimentAnalysisSerializer

    def perform_create(self, serializer: SentimentAnalysisSerializer) -> None:
        """Create a new sentiment analysis and start the analysis task."""
        analysis = serializer.save()
        for src in analysis.source:
            if src == "reddit":
                from .tasks import analyze_reddit_sentiment

                analyze_reddit_sentiment.delay(analysis.id)
            elif src == "twitter":
                from .tasks import analyze_twitter_sentiment

                analyze_twitter_sentiment.delay(analysis.id)

    @action(detail=True, methods=["get"])
    def results(self, request: Any, pk: int = None) -> Response:
        """Get all results for a specific sentiment analysis."""
        analysis = get_object_or_404(SentimentAnalysis, pk=pk)
        if analysis.status != "completed":
            return Response(
                {
                    "status": analysis.status,
                    "message": "Analysis is not completed yet.",
                },
                status=status.HTTP_202_ACCEPTED,
            )
        results = (
            analysis.results.filter(is_ad=False)
            .select_related("sentiment_analysis")
            .prefetch_related("image_results")
        )
        if not results.exists():
            return Response(
                {"message": "No results available yet"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = SentimentResultSerializer(results, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def summary(self, request: Any, pk: int = None) -> Response:
        """Get summary statistics for a sentiment analysis."""
        analysis = get_object_or_404(SentimentAnalysis, pk=pk)
        results = (
            SentimentResult.objects.filter(sentiment_analysis=analysis, is_ad=False)
            .select_related("sentiment_analysis")
            .prefetch_related("image_results")
        )
        if not results.exists():
            return Response(
                {"message": "No results available yet"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(get_analysis_summary(results))

    @action(detail=True, methods=["get"], url_path="sentiment-by-date")
    def sentiment_by_date(self, request, pk=None):
        """Get sentiment scores grouped by date using final_score."""
        analysis = get_object_or_404(SentimentAnalysis, pk=pk)
        results = (
            analysis.results.filter(is_ad=False)
            .select_related("sentiment_analysis")
            .prefetch_related("image_results")
        )
        if not results.exists():
            return Response(
                {"message": "No results available yet"},
                status=status.HTTP_404_NOT_FOUND,
            )
        date_map = {}
        for r in results:
            if not r.post_date:
                continue
            date_str = r.post_date.date().isoformat()
            if date_str not in date_map:
                date_map[date_str] = []
            date_map[date_str].append(r.final_score)
        sentiment_by_date = [
            {
                "post_date": date,
                "avg_score": sum(scores) / len(scores) if scores else 0,
                "count": len(scores),
            }
            for date, scores in sorted(date_map.items())
        ]
        return Response(sentiment_by_date)

    @action(detail=True, methods=["get"], url_path="iq-distribution")
    def iq_distribution(self, request, pk=None):
        """Get distribution of perceived IQ scores."""
        analysis = get_object_or_404(SentimentAnalysis, pk=pk)
        results = (
            analysis.results.filter(is_ad=False)
            .select_related("sentiment_analysis")
            .prefetch_related("image_results")
        )
        if not results.exists():
            return Response(
                {"message": "No results available yet"},
                status=status.HTTP_404_NOT_FOUND,
            )
        iq_distribution = list(
            results.values("perceived_iq")
            .annotate(count=models.Count("id"))
            .order_by("perceived_iq")
        )
        return Response(iq_distribution)

    @action(detail=True, methods=["get"], url_path="bot-analysis")
    def bot_analysis(self, request, pk=None):
        """Get bot detection analysis results."""
        analysis = get_object_or_404(SentimentAnalysis, pk=pk)
        results = (
            analysis.results.filter(is_ad=False)
            .select_related("sentiment_analysis")
            .prefetch_related("image_results")
        )
        if not results.exists():
            return Response(
                {"message": "No results available yet"},
                status=status.HTTP_404_NOT_FOUND,
            )
        total_posts = results.count()
        bot_analysis = {
            "total": total_posts,
            "bots": results.filter(is_bot=True).count(),
            "not_bots": results.filter(is_bot=False).count(),
            "avg_bot_probability": results.aggregate(avg=models.Avg("bot_probability"))[
                "avg"
            ]
            or 0,
        }
        return Response(bot_analysis)

    @action(detail=True, methods=["get"], url_path="full-details")
    def full_details(self, request, pk=None):
        """
        Return all relevant data for an analysis in a single response:
        - analysis metadata
        - results
        - summary
        - sentiment by date
        - IQ distribution
        - bot analysis
        - twitter_grok_summary (if twitter is a source)
        """
        try:
            analysis = self.get_object()
            results = (
                analysis.results.filter(is_ad=False)
                .select_related("sentiment_analysis")
                .prefetch_related("image_results")
            )
            results_data = SentimentResultSerializer(results, many=True).data
            summary = get_analysis_summary(results)
            # Sentiment by date
            date_map = {}
            for r in results:
                if not r.post_date:
                    continue
                date_str = r.post_date.date().isoformat()
                if date_str not in date_map:
                    date_map[date_str] = []
                date_map[date_str].append(r.final_score)
            sentiment_by_date = [
                {
                    "post_date": date,
                    "avg_score": sum(scores) / len(scores) if scores else 0,
                    "count": len(scores),
                }
                for date, scores in sorted(date_map.items())
            ]
            # IQ distribution
            iq_distribution = list(
                results.values("perceived_iq")
                .annotate(count=models.Count("id"))
                .order_by("perceived_iq")
            )
            # Bot analysis
            bot_analysis = {
                "total": summary["total_posts"],
                "bots": results.filter(is_bot=True).count(),
                "not_bots": results.filter(is_bot=False).count(),
                "avg_bot_probability": results.aggregate(
                    avg=models.Avg("bot_probability")
                )["avg"]
                or 0,
            }
            # --- Twitter Grok Summary ---
            twitter_grok_summary = None
            if "twitter" in analysis.source:
                twitter_results = results.filter(source_type="twitter")
                twitter_texts = [r.content for r in twitter_results]
                prompt = None
                if twitter_texts:
                    joined = "\n".join(twitter_texts[:50])
                    prompt = f"Summarize the overall sentiment and main opinions expressed in the following tweets. Be concise and focus on the general mood and key points:\n{joined}\nSummary:"
                else:
                    prompt = "Summarize the current overall sentiment and main opinions on Twitter about this topic."

                async def grok_summary_call():
                    url = "https://api.x.ai/v1/chat/completions"
                    headers = {
                        "Authorization": f"Bearer {settings.GROK_API_KEY}",
                        "Content-Type": "application/json",
                    }
                    data = {
                        "model": "grok-beta",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a social media sentiment analysis assistant. Summarize the overall sentiment and main opinions in a concise paragraph.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        "stream": False,
                        "temperature": 0,
                    }
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            url, headers=headers, json=data
                        ) as resp:
                            if resp.status != 200:
                                return (
                                    f"Grok API error: {resp.status} {await resp.text()}"
                                )
                            result = await resp.json()
                            try:
                                return result["choices"][0]["message"]["content"]
                            except Exception:
                                return str(result)

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    twitter_grok_summary = loop.run_until_complete(grok_summary_call())
                finally:
                    loop.close()
            return Response(
                {
                    "analysis": SentimentAnalysisSerializer(analysis).data,
                    "results": results_data,
                    "summary": summary,
                    "sentiment_by_date": sentiment_by_date,
                    "iq_distribution": iq_distribution,
                    "bot_analysis": bot_analysis,
                    "twitter_grok_summary": twitter_grok_summary,
                }
            )
        except Http404:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in full_details: {str(e)}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["get"], url_path="gemma-status")
    def gemma_status(self, request):
        """Check the status of the Gemma model."""
        try:
            tokenizer, model = get_model()
            if tokenizer is not None and model is not None:
                return Response({"status": "ready"})
            else:
                return Response({"status": "loading"})
        except Exception as e:
            logger.error(f"Error checking Gemma status: {str(e)}")
            return Response({"status": "error"})

    @action(detail=True, methods=["get"], url_path="search")
    def search_results(self, request, pk=None):
        """Search results with advanced filtering and sorting."""
        analysis = get_object_or_404(SentimentAnalysis, pk=pk)
        # Return all posts for the analysis, no is_ad filter
        results = (
            SentimentResult.objects.filter(sentiment_analysis=analysis)
            .select_related("sentiment_analysis")
            .prefetch_related("image_results")
        )
        # Apply search query
        search_query = request.query_params.get("q", "")
        if search_query:
            results = results.filter(content__icontains=search_query)
        # Apply sentiment filter ONLY if set to a restrictive value
        sentiment = request.query_params.get("sentiment")
        if sentiment in ("positive", "negative", "neutral"):
            if sentiment == "positive":
                results = results.filter(final_score__gt=0.05)
            elif sentiment == "negative":
                results = results.filter(final_score__lt=-0.05)
            elif sentiment == "neutral":
                results = results.filter(final_score__gte=-0.05, final_score__lte=0.05)
        # Apply sarcasm filter ONLY if set to 'true'
        sarcasm = request.query_params.get("sarcasm")
        if sarcasm is not None and sarcasm.lower() == "true":
            results = results.filter(is_sarcastic=True)
        # Apply bot filter ONLY if set to 'true'
        bot = request.query_params.get("bot")
        if bot is not None and bot.lower() == "true":
            results = results.filter(is_bot=True)
        # Apply IQ filter
        min_iq = request.query_params.get("min_iq")
        if min_iq is not None:
            try:
                min_iq = float(min_iq)
                results = results.filter(perceived_iq__gte=min_iq)
            except ValueError:
                pass
        # Apply sorting
        sort_by = request.query_params.get("sort_by", "date")
        sort_order = request.query_params.get("sort_order", "desc")
        sort_field = {
            "score": "score",
            "date": "post_date",
            "iq": "perceived_iq",
            "bot_probability": "bot_probability",
        }.get(sort_by, "post_date")
        if sort_order == "asc":
            results = results.order_by(sort_field)
        else:
            results = results.order_by(f"-{sort_field}")
        # Return all results for the analysis, no pagination (for debugging)
        raw_ids = list(results.values_list("id", flat=True))
        serializer = SentimentResultSerializer(results, many=True)
        return Response(
            {
                "results": serializer.data,
                "total_count": results.count(),
                "page": 1,
                "page_size": results.count(),
                "total_pages": 1,
                "raw_ids": raw_ids,
            }
        )

    @action(detail=True, methods=["get"], url_path="export-csv")
    def export_csv(self, request, pk=None):
        """Export analysis results as CSV."""
        analysis = get_object_or_404(SentimentAnalysis, pk=pk)
        if analysis.status != "completed":
            return Response(
                {
                    "status": analysis.status,
                    "message": "Analysis is not completed yet.",
                },
                status=status.HTTP_202_ACCEPTED,
            )
        results = (
            analysis.results.filter(is_ad=False)
            .select_related("sentiment_analysis")
            .prefetch_related("image_results")
        )
        if not results.exists():
            return Response(
                {"message": "No results available yet"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Define CSV header
        header = [
            "id",
            "post_id",
            "content",
            "score",
            "compound_score",
            "created_at",
            "has_images",
            "vader_score",
            "gpt4_score",
            "claude_score",
            "gemini_score",
            "grok_score",
            "sarcasm_score",
            "is_sarcastic",
            "perceived_iq",
            "bot_probability",
            "is_bot",
            "post_date",
            "source_type",
        ]

        def row_gen():
            yield header
            for r in results:
                yield [
                    r.id,
                    r.post_id,
                    r.content,
                    r.final_score,
                    r.compound_score,
                    r.created_at,
                    getattr(r, "has_images", False),
                    getattr(r, "vader_score", ""),
                    getattr(r, "gpt4_score", ""),
                    getattr(r, "claude_score", ""),
                    getattr(r, "gemini_score", ""),
                    getattr(r, "grok_score", ""),
                    getattr(r, "sarcasm_score", ""),
                    getattr(r, "is_sarcastic", ""),
                    getattr(r, "perceived_iq", ""),
                    getattr(r, "bot_probability", ""),
                    getattr(r, "is_bot", ""),
                    r.post_date,
                    r.source_type,
                ]

        pseudo_buffer = (",".join(map(str, row)) + "\n" for row in row_gen())
        response = StreamingHttpResponse(pseudo_buffer, content_type="text/csv")
        response[
            "Content-Disposition"
        ] = f'attachment; filename="analysis_{analysis.id}_results.csv"'
        return response

    @action(detail=True, methods=["get"], url_path="debug-results")
    def debug_results(self, request, pk=None):
        from .models import SentimentResult

        analysis = get_object_or_404(SentimentAnalysis, pk=pk)
        results = SentimentResult.objects.filter(sentiment_analysis=analysis)
        return Response(
            {
                "count": results.count(),
                "ids": list(results.values_list("id", flat=True)),
                "sample": list(
                    results.values("id", "content", "score", "final_score")[:5]
                ),
            }
        )


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "healthy"})
