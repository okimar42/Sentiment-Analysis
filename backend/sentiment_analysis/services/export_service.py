"""
Export service for sentiment analysis data.
"""

import csv
import io
from typing import Generator, List, Dict, Any
from django.http import HttpResponse


class ExportService:
    """Service for exporting analysis data in various formats."""
    
    @staticmethod
    def export_to_csv(analysis_id: int) -> HttpResponse:
        """
        Export analysis results to CSV format.
        
        Args:
            analysis_id: ID of the analysis to export
            
        Returns:
            HttpResponse with CSV data
        """
        from ..models import SentimentAnalysis, SentimentResult
        
        try:
            analysis = SentimentAnalysis.objects.get(id=analysis_id)
            results = SentimentResult.objects.filter(analysis=analysis)
            
            # Create CSV response
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="analysis_{analysis_id}_results.csv"'
            
            # Create CSV writer
            writer = csv.writer(response)
            
            # Write header
            writer.writerow([
                'ID',
                'Content',
                'Score',
                'Post Date',
                'Perceived IQ',
                'Bot Probability',
                'Source Type',
                'Post ID',
                'Manual Sentiment',
                'Override Reason'
            ])
            
            # Write data rows
            for result in ExportService._row_generator(results):
                writer.writerow(result)
            
            return response
            
        except SentimentAnalysis.DoesNotExist:
            response = HttpResponse('Analysis not found', status=404)
            return response
    
    @staticmethod
    def _row_generator(results) -> Generator[List[str], None, None]:
        """
        Generate CSV rows from results queryset.
        
        Args:
            results: QuerySet of SentimentResult objects
            
        Yields:
            List of strings representing a CSV row
        """
        for result in results:
            yield [
                result.id,
                result.content,
                result.final_score,
                result.post_date.isoformat(),
                result.perceived_iq or '',
                result.bot_probability or '',
                result.source_type or '',
                result.post_id or '',
                result.manual_sentiment or '',
                result.override_reason or ''
            ]
    
    @staticmethod
    def export_summary_to_dict(analysis_id: int) -> Dict[str, Any]:
        """
        Export analysis summary as a dictionary.
        
        Args:
            analysis_id: ID of the analysis to export
            
        Returns:
            Dictionary with summary data
        """
        from .statistics_service import StatisticsService
        from ..models import SentimentAnalysis, SentimentResult
        
        try:
            analysis = SentimentAnalysis.objects.get(id=analysis_id)
            results = SentimentResult.objects.filter(analysis=analysis)
            
            return {
                'analysis_info': {
                    'id': analysis.id,
                    'query': analysis.query,
                    'source': analysis.source,
                    'model': analysis.model,
                    'created_at': analysis.created_at.isoformat(),
                    'status': analysis.status
                },
                'summary': StatisticsService.get_analysis_summary(results),
                'sentiment_by_date': StatisticsService.get_sentiment_by_date(results),
                'iq_distribution': StatisticsService.get_iq_distribution(results),
                'bot_analysis': StatisticsService.get_bot_analysis(results)
            }
        except SentimentAnalysis.DoesNotExist:
            return {'error': 'Analysis not found'}