"""Health check views for system monitoring."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView as DRFAPIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_206_PARTIAL_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_503_SERVICE_UNAVAILABLE,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from ..services import AnalysisService


class HealthCheckView(DRFAPIView):
    """
    Health check endpoint for system monitoring.
    """

    def get(self, request):
        """
        Get system health status.

        Returns:
            JSON response with health information
        """
        try:
            health_status = AnalysisService.get_health_status()

            # Determine HTTP status based on health
            http_status = HTTP_200_OK
            if health_status.get("status") == "error":
                http_status = HTTP_503_SERVICE_UNAVAILABLE
            elif health_status.get("celery") == "error":
                http_status = HTTP_206_PARTIAL_CONTENT
            # example of 404 usage (not expected here but demonstration)
            if not health_status:
                http_status = HTTP_404_NOT_FOUND

            return Response(health_status, status=http_status)

        except Exception as e:
            return Response(
                {"status": "error", "error": str(e)},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
