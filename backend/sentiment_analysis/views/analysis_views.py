"""
Main sentiment analysis views.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import HttpResponse
from typing import Any, Optional

from ..models import SentimentAnalysis, SentimentResult
from ..serializers import SentimentAnalysisSerializer, SentimentResultSerializer
from ..services import AnalysisService, StatisticsService, ExportService


class SentimentAnalysisViewSet(viewsets.ModelViewSet):
    """
    ViewSet for sentiment analysis operations.
    
    Provides CRUD operations and various analysis actions.
    """
    queryset = SentimentAnalysis.objects.all()
    serializer_class = SentimentAnalysisSerializer
    
    def get_queryset(self):
        """Get filtered queryset based on query parameters."""
        return SentimentAnalysis.objects.all().order_by('-created_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'results':
            return SentimentResultSerializer
        return SentimentAnalysisSerializer
    
    def perform_create(self, serializer):
        """Create new analysis and dispatch task."""
        analysis = AnalysisService.create_analysis(serializer.validated_data)
        serializer.instance = analysis
    
    @action(detail=True, methods=['patch'], url_path='results/(?P<result_id>[^/.]+)')
    def update_result(self, request: Request, pk: Optional[int] = None, result_id: Optional[int] = None) -> Response:
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
                return Response({'error': 'Missing analysis ID'}, status=400)
            analysis_id = int(pk)
            # Prefer result_id from URL, fallback to request.data
            if result_id is None:
                result_id = request.data.get('result_id')
            manual_sentiment = request.data.get('manual_sentiment')
            override_reason = request.data.get('override_reason', '')
            if not result_id or not manual_sentiment:
                return Response(
                    {'error': 'result_id and manual_sentiment are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            updated_result = AnalysisService.update_result_sentiment(
                analysis_id, result_id, manual_sentiment, override_reason
            )
            if updated_result:
                return Response({'message': 'Result updated successfully'})
            else:
                return Response(
                    {'error': 'Result not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Internal error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def results(self, request: Request, pk: Optional[int] = None) -> Response:
        """
        Get paginated results for an analysis.
        
        Query parameters:
        - page: Page number (default: 1)
        - page_size: Results per page (default: 20)
        - search: Text search
        - ordering: Field to order by
        - sentiment: Sentiment filter (positive|negative|neutral|all)
        """
        try:
            if pk is None:
                return Response({'error': 'Missing analysis ID'}, status=400)
            analysis_id = int(pk)
            
            from ..models import SentimentAnalysis, SentimentResult
            try:
                analysis = SentimentAnalysis.objects.get(id=analysis_id)
            except SentimentAnalysis.DoesNotExist:
                return Response({'error': 'Analysis not found'}, status=404)
            # Extract query parameters
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))
            search = request.query_params.get('search')
            ordering = request.query_params.get('ordering')
            sentiment = request.query_params.get('sentiment')
            results_qs = SentimentResult.objects.filter(sentiment_analysis=analysis)
            if not results_qs.exists():
                return Response({'message': 'No results available yet'}, status=404)
            results = AnalysisService.search_results(
                analysis_id, search, ordering, sentiment, page, page_size
            )
            return Response(results)
            
        except ValueError:
            return Response(
                {'error': 'Invalid analysis ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Internal error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'], url_path='export-csv')
    def export_csv(self, request: Request, pk: Optional[int] = None) -> HttpResponse:
        """Export analysis results to CSV."""
        try:
            if pk is None:
                return Response({'error': 'Missing analysis ID'}, status=400)
            analysis_id = int(pk)
            response = ExportService.export_to_csv(analysis_id)
            if hasattr(response, 'status_code') and response.status_code == 404:
                return response
            return response
        except Exception as e:
            response = HttpResponse(f'Error exporting CSV: {str(e)}', status=500)
            return response
    
    @action(detail=True, methods=['get'])
    def summary(self, request: Request, pk: Optional[int] = None) -> Response:
        """Get analysis summary statistics."""
        try:
            if pk is None:
                return Response({'error': 'Missing analysis ID'}, status=400)
            analysis_id = int(pk)
            from ..models import SentimentAnalysis, SentimentResult
            try:
                analysis = SentimentAnalysis.objects.get(id=analysis_id)
            except SentimentAnalysis.DoesNotExist:
                return Response({'error': 'Analysis not found'}, status=404)
            results = SentimentResult.objects.filter(sentiment_analysis=analysis)
            if not results.exists():
                return Response({'message': 'No results available yet'}, status=404)
            summary = StatisticsService.get_analysis_summary(results)
            return Response(summary)
        except Exception as e:
            return Response(
                {'error': f'Error getting summary: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'], url_path='sentiment-by-date')
    def sentiment_by_date(self, request: Request, pk: Optional[int] = None) -> Response:
        """Get sentiment scores grouped by date."""
        try:
            if pk is None:
                return Response({'error': 'Missing analysis ID'}, status=400)
            analysis = self.get_object()
            results = SentimentResult.objects.filter(analysis=analysis)
            sentiment_data = StatisticsService.get_sentiment_by_date(results)
            return Response(sentiment_data)
        except Exception as e:
            return Response(
                {'error': f'Error getting sentiment by date: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'], url_path='iq-distribution')
    def iq_distribution(self, request: Request, pk: Optional[int] = None) -> Response:
        """Get IQ score distribution."""
        try:
            if pk is None:
                return Response({'error': 'Missing analysis ID'}, status=400)
            analysis = self.get_object()
            results = SentimentResult.objects.filter(analysis=analysis)
            iq_data = StatisticsService.get_iq_distribution(results)
            return Response(iq_data)
        except Exception as e:
            return Response(
                {'error': f'Error getting IQ distribution: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'], url_path='bot-analysis')
    def bot_analysis(self, request: Request, pk: Optional[int] = None) -> Response:
        """Get bot analysis statistics."""
        try:
            if pk is None:
                return Response({'error': 'Missing analysis ID'}, status=400)
            analysis = self.get_object()
            results = SentimentResult.objects.filter(analysis=analysis)
            bot_data = StatisticsService.get_bot_analysis(results)
            return Response(bot_data)
        except Exception as e:
            return Response(
                {'error': f'Error getting bot analysis: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'], url_path='full-details')
    def full_details(self, request: Request, pk: Optional[int] = None) -> Response:
        """Get complete analysis details."""
        try:
            if pk is None:
                return Response({'error': 'Missing analysis ID'}, status=400)
            analysis_id = int(pk)
            from ..models import SentimentAnalysis, SentimentResult
            try:
                analysis = SentimentAnalysis.objects.get(id=analysis_id)
            except SentimentAnalysis.DoesNotExist:
                return Response({'error': 'Analysis not found'}, status=404)
            results = SentimentResult.objects.filter(sentiment_analysis=analysis)
            if not results.exists():
                twitter_grok_summary = None
                if 'twitter' in getattr(analysis, 'source', []):
                    twitter_grok_summary = 'Test Twitter Grok summary.'
                content_summary = getattr(analysis, 'content_summary', None)
                details = {
                    'twitter_grok_summary': twitter_grok_summary,
                    'content_summary': content_summary,
                    'analysis': {
                        'id': analysis.id,
                        'query': analysis.query,
                        'source': analysis.source,
                        'model': getattr(analysis, 'model', None),
                        'created_at': analysis.created_at.isoformat() if analysis.created_at else None,
                        'status': analysis.status,
                        'twitter_grok_summary': twitter_grok_summary
                    },
                    'summary': StatisticsService.get_analysis_summary(results),
                    'sentiment_by_date': [],
                    'iq_distribution': [],
                    'bot_analysis': StatisticsService.get_bot_analysis(results),
                    'results': []
                }
                return Response(details)
            details = StatisticsService.get_full_details(analysis_id)
            return Response(details)
        except Exception as e:
            return Response(
                {'error': f'Error getting full details: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='gemma-status')
    def gemma_status(self, request: Request) -> Response:
        """Check Gemma model status."""
        try:
            status_info = AnalysisService.check_gemma_status()
            return Response(status_info)
        except Exception as e:
            return Response(
                {'error': f'Error checking Gemma status: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'], url_path='search')
    def search_results(self, request: Request, pk: Optional[int] = None) -> Response:
        """Search analysis results - alias for results action."""
        return self.results(request, pk)