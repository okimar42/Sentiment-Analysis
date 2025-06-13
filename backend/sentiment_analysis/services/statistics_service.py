"""
Statistics calculation service for sentiment analysis.
"""

from collections import defaultdict
from typing import Any, Dict, List


class StatisticsService:
    """Service for calculating various statistics from sentiment analysis results."""

    @staticmethod
    def get_analysis_summary(results: Any) -> Dict[str, Any]:
        """
        Compute summary statistics for a queryset of SentimentResult.

        Args:
            results: QuerySet of SentimentResult objects

        Returns:
            Dict containing summary statistics
        """
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

    @staticmethod
    def get_sentiment_by_date(results: Any) -> List[Dict[str, Any]]:
        """
        Get sentiment scores grouped by date.

        Args:
            results: QuerySet of SentimentResult objects

        Returns:
            List of dictionaries with date and sentiment data
        """
        sentiment_by_date = {}
        for result in results:
            if not result.post_date:
                continue  # Skip results with no date
            date_key = result.post_date.date()
            if date_key not in sentiment_by_date:
                sentiment_by_date[date_key] = []
            sentiment_by_date[date_key].append(result.final_score)

        # Calculate average sentiment per date
        sentiment_by_date_list = []
        for date, scores in sentiment_by_date.items():
            avg_score = sum(scores) / len(scores) if scores else 0
            sentiment_by_date_list.append(
                {
                    "post_date": date.isoformat(),
                    "avg_score": avg_score,
                    "count": len(scores),
                }
            )

        # Sort by date
        sentiment_by_date_list.sort(key=lambda x: x["post_date"])
        return sentiment_by_date_list

    @staticmethod
    def get_iq_distribution(results: Any) -> List[Dict[str, Any]]:
        """
        Get IQ score distribution.

        Args:
            results: QuerySet of SentimentResult objects

        Returns:
            List of dictionaries with IQ distribution data
        """
        # Extract IQ scores and group into ranges
        iq_scores = [
            result.perceived_iq for result in results if result.perceived_iq is not None
        ]

        # Create IQ ranges (bins of 10)
        iq_distribution: defaultdict[int, int] = defaultdict(int)
        for iq in iq_scores:
            # Round to nearest 10 for grouping
            bin_value = int(iq // 10) * 10
            iq_distribution[bin_value] += 1

        # Convert to list format
        distribution_list = []
        for iq_range, count in sorted(iq_distribution.items()):
            distribution_list.append({"perceived_iq": iq_range, "count": count})

        return distribution_list

    @staticmethod
    def get_bot_analysis(results: Any) -> Dict[str, Any]:
        """
        Get bot analysis statistics.

        Args:
            results: QuerySet of SentimentResult objects

        Returns:
            Dictionary with bot analysis data
        """
        bot_probabilities = [
            result.bot_probability
            for result in results
            if result.bot_probability is not None
        ]

        total = len(bot_probabilities)
        if total == 0:
            return {"total": 0, "bots": 0, "not_bots": 0, "avg_bot_probability": 0.0}

        # Consider posts with >0.7 probability as bots
        bots = sum(1 for prob in bot_probabilities if prob > 0.7)
        not_bots = total - bots
        avg_bot_probability = sum(bot_probabilities) / total

        return {
            "total": total,
            "bots": bots,
            "not_bots": not_bots,
            "avg_bot_probability": avg_bot_probability,
        }

    @staticmethod
    def get_full_details(analysis_id: int) -> Dict[str, Any]:
        """
        Get complete analysis details including all statistics.

        Args:
            analysis_id: ID of the analysis

        Returns:
            Dictionary with complete analysis details
        """
        from ..models import SentimentAnalysis, SentimentResult

        try:
            analysis = SentimentAnalysis.objects.get(id=analysis_id)
            results = SentimentResult.objects.filter(sentiment_analysis=analysis)

            return {
                "analysis": {
                    "id": analysis.id,
                    "query": analysis.query,
                    "source": analysis.source,
                    "model": analysis.model,
                    "created_at": analysis.created_at.isoformat(),
                    "status": analysis.status,
                    "twitter_grok_summary": getattr(
                        analysis, "twitter_grok_summary", None
                    ),
                },
                "summary": StatisticsService.get_analysis_summary(results),
                "sentiment_by_date": StatisticsService.get_sentiment_by_date(results),
                "iq_distribution": StatisticsService.get_iq_distribution(results),
                "bot_analysis": StatisticsService.get_bot_analysis(results),
                "results": [
                    {
                        "id": result.id,
                        "content": result.content,
                        "score": result.final_score,
                        "post_date": result.post_date.isoformat() if result.post_date else None,
                        "perceived_iq": result.perceived_iq,
                        "bot_probability": result.bot_probability,
                        "source_type": result.source_type,
                        "post_id": result.post_id,
                        "grok_score": getattr(result, "grok_score", 0.0),
                    }
                    for result in results[:100]  # Limit to first 100 for performance
                ],
            }
        except SentimentAnalysis.DoesNotExist:
            return {"error": "Analysis not found"}
