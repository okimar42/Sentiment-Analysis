from django.urls import reverse  # type: ignore
from rest_framework.test import APITestCase  # type: ignore
from sentiment_analysis.models import SentimentAnalysis, SentimentResult
from django.contrib.auth.models import User  # type: ignore


class SearchResultsEndpointTests(APITestCase):
    def setUp(self):
        # Create user and analysis
        self.user = User.objects.create(username="tester")
        self.analysis = SentimentAnalysis.objects.create(
            user=self.user,
            query="AAPL",
            source=["reddit"],
            model="vader",
            status="completed",
        )
        # Create 30 results with varying attributes
        for i in range(30):
            SentimentResult.objects.create(
                sentiment_analysis=self.analysis,
                post_id=f"reddit_{i}",
                content=f"Test content {i}",
                score=0.2 if i % 3 == 0 else (-0.2 if i % 3 == 1 else 0.0),
                compound_score=0.2,
                perceived_iq=0.9 if i % 2 == 0 else 0.1,
                is_sarcastic=(i % 5 == 0),
                is_bot=(i % 7 == 0),
            )

    def test_basic_search_returns_paginated_structure(self):
        url = reverse("sentiment-analysis-search", args=[self.analysis.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIn("count", data)
        self.assertEqual(data["count"], 30)
        self.assertTrue(len(data["results"]) <= 20)  # default page_size

    def test_sentiment_filter_positive(self):
        url = reverse("sentiment-analysis-search", args=[self.analysis.id])
        response = self.client.get(url, {"sentiment": "positive"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for res in data["results"]:
            # Positive scores should be >0.05 due to creation logic
            self.assertGreater(res["score"], 0)

    def test_min_iq_filter(self):
        url = reverse("sentiment-analysis-search", args=[self.analysis.id])
        response = self.client.get(url, {"min_iq": 0.8})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for res in data["results"]:
            self.assertGreaterEqual(res["perceived_iq"], 0.8)