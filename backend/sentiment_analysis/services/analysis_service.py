"""
Core analysis service for sentiment analysis operations.
"""

from typing import Any, Dict, Optional

from celery import current_app

from django.db import transaction


class AnalysisService:
    """Service for core analysis operations and business logic."""

    @staticmethod
    def create_analysis(data: Dict[str, Any]) -> "SentimentAnalysis":
        """
        Create a new sentiment analysis with validation and task dispatch.

        Args:
            data: Analysis creation data

        Returns:
            Created SentimentAnalysis instance
        """
        from ..models import SentimentAnalysis

        # Validate required fields
        required_fields = ["query", "source", "model"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        # Create analysis instance
        analysis = SentimentAnalysis.objects.create(
            query=data["query"],
            source=data["source"],
            model=data["model"],
            status="pending",
        )

        # Dispatch appropriate task based on source
        AnalysisService.dispatch_analysis_task(analysis)

        return analysis

    @staticmethod
    def dispatch_analysis_task(analysis: "SentimentAnalysis") -> None:
        """
        Dispatch the appropriate Celery task(s) based on analysis sources.
        """
        sources = (
            analysis.source if isinstance(analysis.source, list) else [analysis.source]
        )
        for source in sources:
            if source.lower() == "reddit":
                from ..tasks.reddit import analyze_reddit_sentiment

                analyze_reddit_sentiment.delay(analysis.id)
            elif source.lower() == "twitter":
                from ..tasks.twitter import analyze_twitter_sentiment

                analyze_twitter_sentiment.delay(analysis.id)
            else:
                # Optionally log or handle unknown sources
                pass

    @staticmethod
    def update_result_sentiment(
        analysis_id: int,
        result_id: int,
        manual_sentiment: str,
        override_reason: str = "",
    ) -> Optional["SentimentResult"]:
        """
        Update sentiment of a specific result with manual override.

        Args:
            analysis_id: ID of the analysis
            result_id: ID of the result to update
            manual_sentiment: New sentiment value
            override_reason: Reason for the override

        Returns:
            Updated SentimentResult or None if not found
        """
        from ..models import SentimentResult

        try:
            with transaction.atomic():
                result = SentimentResult.objects.select_for_update().get(
                    id=result_id, sentiment_analysis_id=analysis_id
                )

                # Accept manual_sentiment as int or str, always save as int
                sentiment_map_str_to_num = {"positive": 1, "neutral": 0, "negative": -1}
                if isinstance(manual_sentiment, str):
                    manual_sentiment_num = sentiment_map_str_to_num.get(
                        manual_sentiment.lower(), 0
                    )
                elif isinstance(manual_sentiment, int):
                    manual_sentiment_num = manual_sentiment
                else:
                    manual_sentiment_num = 0
                result.manual_sentiment = manual_sentiment_num
                result.override_reason = override_reason
                result.save()
                return result

        except SentimentResult.DoesNotExist:
            return None

    @staticmethod
    def search_results(
        analysis_id: int,
        search: Optional[str] = None,
        ordering: Optional[str] = None,
        sentiment: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """
        Search and filter analysis results.

        Args:
            analysis_id: ID of the analysis
            search: Text search query
            ordering: Field to order by
            sentiment: Sentiment filter
            page: Page number
            page_size: Results per page

        Returns:
            Dictionary with paginated results
        """
        from ..models import SentimentResult

        # Base queryset
        queryset = SentimentResult.objects.filter(analysis_id=analysis_id)

        # Apply filters
        if search:
            queryset = queryset.filter(content__icontains=search)

        if sentiment and sentiment != "all":
            if sentiment == "positive":
                queryset = queryset.filter(final_score__gt=0.05)
            elif sentiment == "negative":
                queryset = queryset.filter(final_score__lt=-0.05)
            elif sentiment == "neutral":
                queryset = queryset.filter(
                    final_score__gte=-0.05, final_score__lte=0.05
                )

        # Apply ordering
        if ordering:
            if ordering.startswith("-"):
                queryset = queryset.order_by(ordering)
            else:
                queryset = queryset.order_by(f"-{ordering}")
        else:
            queryset = queryset.order_by("-post_date")

        # Pagination
        total_count = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        results = queryset[start:end]

        total_pages = (total_count + page_size - 1) // page_size

        return {
            "results": [
                {
                    "id": result.id,
                    "content": result.content,
                    "score": result.final_score,
                    "post_date": result.post_date.isoformat()
                    if result.post_date
                    else None,
                    "perceived_iq": result.perceived_iq,
                    "bot_probability": result.bot_probability,
                    "source_type": result.source_type or "",
                    "post_id": result.post_id,
                    "manual_sentiment": result.manual_sentiment,
                    "override_reason": result.override_reason,
                }
                for result in results
            ],
            "total_count": total_count,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    @staticmethod
    def check_gemma_status() -> Dict[str, Any]:
        """
        Check if Gemma model is available and working.

        Returns:
            Dictionary with status information
        """
        try:
            from ..models.gemma import analyze_with_gemma

            # Test with a simple text
            test_score = analyze_with_gemma("This is a test")

            return {
                "available": True,
                "status": "operational",
                "test_score": test_score,
            }
        except Exception as e:
            return {"available": False, "status": "error", "error": str(e)}

    @staticmethod
    def get_health_status() -> Dict[str, Any]:
        """
        Get overall system health status.

        Returns:
            Dictionary with health information
        """
        try:
            # Check database connectivity
            from ..models import SentimentAnalysis

            SentimentAnalysis.objects.count()

            # Check Celery connectivity
            celery_status = "unknown"
            try:
                inspect = current_app.control.inspect()
                active_tasks = inspect.active()
                celery_status = "healthy" if active_tasks is not None else "degraded"
            except Exception:
                celery_status = "error"

            return {
                "status": "healthy",
                "database": "healthy",
                "celery": celery_status,
                "gemma": AnalysisService.check_gemma_status(),
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
