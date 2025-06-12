from rest_framework.routers import DefaultRouter

from django.urls import include, path

from . import views
from .views import HealthCheckView, SentimentAnalysisViewSet

router = DefaultRouter()
router.register(
    r"analyze", views.SentimentAnalysisViewSet, basename="sentiment-analysis"
)

urlpatterns = [
    path("analyze/health/", HealthCheckView.as_view(), name="analyze-health"),
    path("", include(router.urls)),
    path(
        "analyze/<int:pk>/results/<int:result_id>/",
        SentimentAnalysisViewSet.as_view({"patch": "update_result"}),
        name="sentiment-analysis-update-result",
    ),
    path(
        "analyze/gemma-status/",
        SentimentAnalysisViewSet.as_view({"get": "gemma_status"}),
        name="gemma-status",
    ),
]
