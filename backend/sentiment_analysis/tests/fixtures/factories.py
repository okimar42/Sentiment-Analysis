"""
Factory functions for creating test objects using context7 patterns.
"""

from datetime import datetime, timezone

import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User

from ...models import SentimentAnalysis, SentimentResult


class UserFactory(DjangoModelFactory):
    """Factory for creating test users."""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"testuser{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True


class SentimentAnalysisFactory(DjangoModelFactory):
    """Factory for creating test sentiment analyses."""

    class Meta:
        model = SentimentAnalysis

    query = factory.Faker("sentence", nb_words=4)
    source = factory.Iterator(["reddit", "twitter"])
    model = factory.Iterator(["vader", "gemma", "gpt4"])
    status = factory.Iterator(["pending", "processing", "completed", "failed"])
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    user = factory.SubFactory(UserFactory)


class SentimentResultFactory(DjangoModelFactory):
    """Factory for creating test sentiment results."""

    class Meta:
        model = SentimentResult

    sentiment_analysis = factory.SubFactory(SentimentAnalysisFactory)
    content = factory.Faker("text", max_nb_chars=500)
    score = factory.Faker(
        "pyfloat", left_digits=1, right_digits=3, min_value=-1, max_value=1
    )
    post_date = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    perceived_iq = factory.Faker("pyint", min_value=60, max_value=150)
    bot_probability = factory.Faker(
        "pyfloat", left_digits=0, right_digits=2, min_value=0, max_value=1
    )
    source_type = "twitter"
    post_id = factory.Faker("uuid4")
    grok_score = factory.Faker(
        "pyfloat", left_digits=0, right_digits=2, min_value=0, max_value=1
    )


# Specialized factories for specific test scenarios


class RedditAnalysisFactory(SentimentAnalysisFactory):
    """Factory for Reddit-specific analyses."""

    source = "reddit"
    query = factory.Iterator(["AskReddit", "technology", "worldnews", "programming"])


class TwitterAnalysisFactory(SentimentAnalysisFactory):
    """Factory for Twitter-specific analyses."""

    source = "twitter"
    query = factory.Faker("sentence", nb_words=3)


class PositiveSentimentResultFactory(SentimentResultFactory):
    """Factory for positive sentiment results."""

    score = factory.Faker(
        "pyfloat", left_digits=0, right_digits=3, min_value=0.1, max_value=1.0
    )
    perceived_iq = factory.Faker("pyint", min_value=90, max_value=150)


class NegativeSentimentResultFactory(SentimentResultFactory):
    """Factory for negative sentiment results."""

    score = factory.Faker(
        "pyfloat", left_digits=1, right_digits=3, min_value=-1.0, max_value=-0.1
    )
    perceived_iq = factory.Faker("pyint", min_value=60, max_value=90)


class NeutralSentimentResultFactory(SentimentResultFactory):
    """Factory for neutral sentiment results."""

    score = factory.Faker(
        "pyfloat", left_digits=0, right_digits=3, min_value=-0.05, max_value=0.05
    )
    perceived_iq = factory.Faker("pyint", min_value=80, max_value=110)


class HighBotProbabilityResultFactory(SentimentResultFactory):
    """Factory for results with high bot probability."""

    bot_probability = factory.Faker(
        "pyfloat", left_digits=0, right_digits=2, min_value=0.7, max_value=1.0
    )
    content = factory.Iterator(
        [
            "Buy now! Limited time offer!",
            "Click here for amazing deals!",
            "Follow for follow back!",
            "URGENT: This will change your life!",
        ]
    )


# Batch creation helpers


def create_analysis_with_results(num_results=10, **kwargs):
    """Create an analysis with associated results."""
    analysis = SentimentAnalysisFactory(**kwargs)
    results = SentimentResultFactory.create_batch(num_results, sentiment_analysis=analysis)
    return analysis, results


def create_mixed_sentiment_results(sentiment_analysis, num_each=5):
    """Create a mix of positive, negative, and neutral results."""
    positive = PositiveSentimentResultFactory.create_batch(num_each, sentiment_analysis=sentiment_analysis)
    negative = NegativeSentimentResultFactory.create_batch(num_each, sentiment_analysis=sentiment_analysis)
    neutral = NeutralSentimentResultFactory.create_batch(num_each, sentiment_analysis=sentiment_analysis)
    return positive + negative + neutral


def create_completed_analysis_with_mixed_results(num_each=5):
    """Create a completed analysis with diverse results."""
    analysis = SentimentAnalysisFactory(status="completed")
    results = create_mixed_sentiment_results(analysis, num_each)
    return analysis, results

# NOTE: Linter errors for missing stubs in test-only dependencies (factory, django) can be ignored for CI and local test runs. use context7
