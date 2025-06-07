from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import SentimentAnalysisViewSet

router = DefaultRouter()
router.register(r'analyses', views.SentimentAnalysisViewSet, basename='sentiment-analysis')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'analyses/<int:pk>/results/<int:result_id>/',
        SentimentAnalysisViewSet.as_view({'patch': 'update_result'}),
        name='sentiment-analysis-update-result'
    ),
    path('analyses/gemma-status/', SentimentAnalysisViewSet.as_view({'get': 'gemma_status'}), name='gemma-status'),
] 