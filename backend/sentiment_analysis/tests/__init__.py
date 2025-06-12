"""
Comprehensive test suite for sentiment analysis application.

This package contains modular tests organized by component:
- tasks/: Celery task tests  
- models/: Model and data access tests
- utils/: Utility function tests
- views/: API endpoint tests
- services/: Business logic tests
- integration/: End-to-end integration tests
- fixtures/: Shared test data and fixtures

Using context7 for comprehensive test coverage and quality assurance.
"""

import os

import django
from django.conf import settings

# Configure Django for testing
if not settings.configured:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    django.setup()

# Test configuration constants
TEST_REDDIT_CLIENT_ID = "test_reddit_client"
TEST_REDDIT_CLIENT_SECRET = "test_reddit_secret"
TEST_REDDIT_USER_AGENT = "test_user_agent"

TEST_TWITTER_CONSUMER_KEY = "test_twitter_key"
TEST_TWITTER_CONSUMER_SECRET = "test_twitter_secret"
TEST_TWITTER_ACCESS_TOKEN = "test_access_token"
TEST_TWITTER_ACCESS_TOKEN_SECRET = "test_access_secret"

TEST_OPENAI_API_KEY = "test_openai_key"
TEST_HUGGINGFACE_TOKEN = "test_hf_token"

# Test data paths
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "data")
TEST_MODELS_DIR = os.path.join(TEST_DATA_DIR, "models")

__all__ = [
    "TEST_REDDIT_CLIENT_ID",
    "TEST_REDDIT_CLIENT_SECRET",
    "TEST_REDDIT_USER_AGENT",
    "TEST_TWITTER_CONSUMER_KEY",
    "TEST_TWITTER_CONSUMER_SECRET",
    "TEST_TWITTER_ACCESS_TOKEN",
    "TEST_TWITTER_ACCESS_TOKEN_SECRET",
    "TEST_OPENAI_API_KEY",
    "TEST_HUGGINGFACE_TOKEN",
    "TEST_DATA_DIR",
    "TEST_MODELS_DIR",
]
