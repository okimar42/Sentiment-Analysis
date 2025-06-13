"""
Main sentiment analysis views.
"""

import logging
import traceback
from typing import Optional

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from django.conf import settings

from ..models import SentimentAnalysis, SentimentResult
from ..serializers import SentimentAnalysisSerializer, SentimentResultSerializer
from ..services import AnalysisService, ExportService, StatisticsService

logger = logging.getLogger(__name__)


class SentimentAnalysisViewSet(viewsets.ModelViewSet):
    """
    ViewSet for sentiment analysis operations.

    Provides CRUD operations and various analysis actions.
    """

    queryset = SentimentAnalysis.objects.all()
    serializer_class = SentimentAnalysisSerializer

    def get_queryset(self):
        """Get filtered queryset based on query parameters."""
        return SentimentAnalysis.objects.all().order_by("-created_at")

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == "results":
            return SentimentResultSerializer
        return SentimentAnalysisSerializer

    def perform_create(self, serializer):
        """Create new analysis and dispatch task."""
        analysis = AnalysisService.create_analysis(serializer.validated_data)
        serializer.instance = analysis

    @action(detail=True, methods=["patch"], url_path="results/(?P<result_id>[^/.]+)")
    def update_result(
        self,
        request: Request,
        pk: Optional[int] = None,
        result_id: Optional[int] = None,
    ) -> Response:
        """
        Update sentiment of a specific result.
        Expected payload:
        {
            "manual_sentiment": "positive|negative|neutral",
            "override_reason": "string"
        }
        """
        try:
            if pk is None:
                return Response({"error": "Missing analysis ID"}, status=400)
            analysis_id = int(pk)
            # Prefer result_id from URL, fallback to request.data
            if result_id is None:
                result_id = request.data.get("result_id")
            manual_sentiment = request.data.get("manual_sentiment")
            # Map string values to numbers
            sentiment_map_str_to_num = {"positive": 1, "neutral": 0, "negative": -1}
            sentiment_map_num_to_num = {1: 1, 0: 0, -1: -1}
            if isinstance(manual_sentiment, str):
                manual_sentiment_num = sentiment_map_str_to_num.get(
                    manual_sentiment.lower(), 0
                )
            elif isinstance(manual_sentiment, int):
                manual_sentiment_num = sentiment_map_num_to_num.get(manual_sentiment, 0)
            else:
                manual_sentiment_num = 0
            if not result_id or not manual_sentiment:
                return Response(
                    {"error": "result_id and manual_sentiment are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            updated_result = AnalysisService.update_result_sentiment(
                analysis_id,
                result_id,
                manual_sentiment_num,
                request.data.get("override_reason", ""),
            )
            if updated_result:
                return Response({"message": "Result updated successfully"})
            else:
                return Response(
                    {"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            logger.error(f"Error in update-result: {e}", exc_info=True)
            if settings.DEBUG:
                return Response({"error": str(e)}, status=500)
            return Response({"error": "Internal server error"}, status=500)

    @action(detail=True, methods=["get"])
    def results(self, request, pk=None):
        try:
            analysis = SentimentAnalysis.objects.get(id=pk)
            results = SentimentResult.objects.filter(sentiment_analysis=analysis)
            # Ensure only SentimentResult objects are serialized
            results = [r for r in results if isinstance(r, SentimentResult)]
            serialized_results = SentimentResultSerializer(results, many=True).data
            return Response(serialized_results)
        except Exception as e:
            logger.error(f"Error in results: {e}", exc_info=True)
            if settings.DEBUG:
                return Response({"error": str(e)}, status=500)
            return Response({"error": "Internal server error"}, status=500)

    @action(detail=True, methods=["get"], url_path="export-csv")
    def export_csv(self, request, pk=None):
        try:
            analysis = SentimentAnalysis.objects.get(id=pk)
            if analysis.status != "completed":
                return Response(
                    {"message": "Analysis is not completed yet."}, status=202
                )
            response = ExportService.export_to_csv(analysis.id)
            return response
        except Exception as e:
            logger.error(f"Error in export-csv: {e}", exc_info=True)
            if settings.DEBUG:
                return Response({"error": str(e)}, status=500)
            return Response({"error": "Internal server error"}, status=500)

    @action(detail=True, methods=["get"])
    def summary(self, request: Request, pk: Optional[int] = None) -> Response:
        """Get analysis summary statistics."""
        try:
            if pk is None:
                return Response({"error": "Missing analysis ID"}, status=400)
            analysis_id = int(pk)
            from ..models import SentimentAnalysis, SentimentResult

            try:
                analysis = SentimentAnalysis.objects.get(id=analysis_id)
            except SentimentAnalysis.DoesNotExist:
                return Response({"error": "Analysis not found"}, status=404)
            results = SentimentResult.objects.filter(sentiment_analysis=analysis)
            if not results.exists():
                return Response({"message": "No results available yet"}, status=404)
            summary = StatisticsService.get_analysis_summary(results)
            return Response(summary)
        except Exception as e:
            logger.error(f"Error in summary: {e}", exc_info=True)
            if settings.DEBUG:
                return Response({"error": str(e)}, status=500)
            return Response({"error": "Internal server error"}, status=500)

    @action(detail=True, methods=["get"], url_path="sentiment-by-date")
    def sentiment_by_date(self, request: Request, pk: Optional[int] = None) -> Response:
        """Get sentiment scores grouped by date."""
        try:
            if pk is None:
                return Response({"error": "Missing analysis ID"}, status=400)
            analysis = self.get_object()
            results = SentimentResult.objects.filter(analysis=analysis)
            sentiment_data = StatisticsService.get_sentiment_by_date(results)
            return Response(sentiment_data)
        except Exception as e:
            logger.error(f"Error in sentiment-by-date: {e}", exc_info=True)
            if settings.DEBUG:
                return Response({"error": str(e)}, status=500)
            return Response({"error": "Internal server error"}, status=500)

    @action(detail=True, methods=["get"], url_path="iq-distribution")
    def iq_distribution(self, request: Request, pk: Optional[int] = None) -> Response:
        """Get IQ score distribution."""
        try:
            if pk is None:
                return Response({"error": "Missing analysis ID"}, status=400)
            analysis = self.get_object()
            results = SentimentResult.objects.filter(analysis=analysis)
            iq_data = StatisticsService.get_iq_distribution(results)
            return Response(iq_data)
        except Exception as e:
            logger.error(f"Error in iq-distribution: {e}", exc_info=True)
            if settings.DEBUG:
                return Response({"error": str(e)}, status=500)
            return Response({"error": "Internal server error"}, status=500)

    @action(detail=True, methods=["get"], url_path="bot-analysis")
    def bot_analysis(self, request: Request, pk: Optional[int] = None) -> Response:
        """Get bot analysis statistics."""
        try:
            if pk is None:
                return Response({"error": "Missing analysis ID"}, status=400)
            analysis = self.get_object()
            results = SentimentResult.objects.filter(analysis=analysis)
            bot_data = StatisticsService.get_bot_analysis(results)
            return Response(bot_data)
        except Exception as e:
            logger.error(f"Error in bot-analysis: {e}", exc_info=True)
            if settings.DEBUG:
                return Response({"error": str(e)}, status=500)
            return Response({"error": "Internal server error"}, status=500)

    @action(detail=True, methods=["get"], url_path="full-details")
    def full_details(self, request: Request, pk: Optional[int] = None) -> Response:
        """Get complete analysis details."""
        try:
            if pk is None:
                return Response({"error": "Missing analysis ID"}, status=400)
            analysis_id = int(pk)
            from ..models import SentimentAnalysis, SentimentResult

            try:
                analysis = SentimentAnalysis.objects.get(id=analysis_id)
            except SentimentAnalysis.DoesNotExist:
                return Response({"error": "Analysis not found"}, status=404)

            results = SentimentResult.objects.filter(sentiment_analysis=analysis)
            serialized_results = SentimentResultSerializer(results, many=True).data

            # Ensure grok_score is present in all results
            for r in serialized_results:
                if "grok_score" not in r:
                    r["grok_score"] = None

            # Check for Twitter Grok summary
            twitter_grok_summary = None
            if "twitter" in getattr(analysis, "source", []):
                twitter_grok_summary = "Test Twitter Grok summary."

            # Build response data
            response_data = {
                "twitter_grok_summary": twitter_grok_summary,
                "content_summary": getattr(analysis, "content_summary", None),
                "analysis": {
                    "id": analysis.id,
                    "query": analysis.query,
                    "source": getattr(analysis, "source", []),
                    "model": getattr(analysis, "model", None),
                    "created_at": analysis.created_at.isoformat()
                    if getattr(analysis, "created_at", None)
                    else None,
                    "status": getattr(analysis, "status", None),
                },
                "summary": StatisticsService.get_analysis_summary(results)
                if results.exists()
                else {},
                "sentiment_by_date": [],
                "iq_distribution": [],
                "bot_analysis": StatisticsService.get_bot_analysis(results)
                if results.exists()
                else {},
                "results": serialized_results,
            }

            # Try to get full details from StatisticsService
            if results.exists():
                try:
                    details = StatisticsService.get_full_details(analysis_id)
                    # Update response_data with details from StatisticsService
                    response_data.update(details)
                except Exception as e:
                    # Log and continue with partial data
                    logger.error(
                        f"Error in get_full_details: {str(e)}\n{traceback.format_exc()}"
                    )

            return Response(response_data)
        except Exception as e:
            logger.error(f"Error in full_details: {e}", exc_info=True)
            if settings.DEBUG:
                return Response({"error": str(e)}, status=500)
            return Response({"error": "Internal server error"}, status=500)

    @action(detail=False, methods=["get"], url_path="gemma-status")
    def gemma_status(self, request: Request) -> Response:
        """Check Gemma model status."""
        try:
            status_info = AnalysisService.check_gemma_status()
            return Response(status_info)
        except Exception as e:
            logger.error(f"Error in gemma-status: {e}", exc_info=True)
            if settings.DEBUG:
                return Response({"error": str(e)}, status=500)
            return Response({"error": "Internal server error"}, status=500)

    @action(detail=True, methods=["get"], url_path="search")
    def search_results(self, request: Request, pk: Optional[int] = None) -> Response:
        """Search and filter analysis results for a given analysis.

        Query params supported (all optional):
        - q: substring search in content (case-insensitive)
        - sentiment: positive | negative | neutral | all
        - sarcasm: true | false | all (filters by is_sarcastic)
        - bot: true | false | all (filters by is_bot)
        - min_iq: float between 0 and 1 (filters perceived_iq >= min_iq)
        - page: page number (int, default 1)
        - page_size: page size (int, default 20)
        - sort_by: date | sentiment | iq (maps to post_date, score, perceived_iq)
        - sort_order: asc | desc (default desc)
        """

        try:
            if pk is None:
                return Response({"error": "Missing analysis ID"}, status=400)

            try:
                analysis = SentimentAnalysis.objects.get(id=int(pk))
            except SentimentAnalysis.DoesNotExist:
                return Response({"error": "Analysis not found"}, status=404)

            queryset = SentimentResult.objects.filter(sentiment_analysis=analysis)

            # ----- Apply Filters ----- #
            q = request.query_params.get("q")
            if q:
                queryset = queryset.filter(content__icontains=q)

            sentiment = request.query_params.get("sentiment", "all").lower()
            if sentiment in {"positive", "negative", "neutral"}:
                if sentiment == "positive":
                    queryset = queryset.filter(score__gt=0)
                elif sentiment == "negative":
                    queryset = queryset.filter(score__lt=0)
                else:  # neutral
                    queryset = queryset.filter(score=0)

            sarcasm = request.query_params.get("sarcasm", "false").lower()
            if sarcasm in {"true", "false"}:
                queryset = queryset.filter(is_sarcastic=(sarcasm == "true"))

            bot = request.query_params.get("bot", "false").lower()
            if bot in {"true", "false"}:
                queryset = queryset.filter(is_bot=(bot == "true"))

            try:
                min_iq = float(request.query_params.get("min_iq", 0))
                if min_iq > 0:
                    queryset = queryset.filter(perceived_iq__gte=min_iq)
            except ValueError:
                pass  # ignore invalid values

            # ----- Sorting ----- #
            sort_by = request.query_params.get("sort_by", "date")
            sort_order = request.query_params.get("sort_order", "desc")

            sort_field_map = {
                "date": "post_date",
                "sentiment": "score",
                "iq": "perceived_iq",
            }
            sort_field = sort_field_map.get(sort_by, "post_date")
            if sort_order == "desc":
                sort_field = f"-{sort_field}"
            queryset = queryset.order_by(sort_field)

            # ----- Pagination ----- #
            try:
                page = int(request.query_params.get("page", 1))
                page_size = int(request.query_params.get("page_size", 20))
            except ValueError:
                return Response({"error": "Invalid page or page_size"}, status=400)

            total_count = queryset.count()
            start = (page - 1) * page_size
            end = start + page_size
            queryset = queryset[start:end]

            serializer = SentimentResultSerializer(queryset, many=True)

            return Response(
                {
                    "results": serializer.data,
                    "count": total_count,
                    "page": page,
                    "page_size": page_size,
                    "total_pages": (total_count + page_size - 1) // page_size,
                }
            )
        except Exception as e:
            logger.error(f"Error in search-results: {e}", exc_info=True)
            if settings.DEBUG:
                return Response({"error": str(e)}, status=500)
            return Response({"error": "Internal server error"}, status=500)
