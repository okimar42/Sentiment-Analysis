"""
Mock data for external API responses and test scenarios using context7.
"""

from datetime import datetime, timezone
from typing import Dict, List, Any

# Mock Reddit API responses
MOCK_REDDIT_POSTS = [
    {
        'id': 'test_post_1',
        'title': 'This is a positive test post',
        'selftext': 'I love this amazing technology! It makes everything better.',
        'created_utc': 1640995200,  # 2022-01-01
        'ups': 150,
        'downs': 10,
        'num_comments': 25,
        'permalink': '/r/test/comments/test_post_1/',
        'url': 'https://reddit.com/r/test/comments/test_post_1/',
        'author': {'name': 'test_user_positive'},
        'subreddit': {'display_name': 'test_subreddit'}
    },
    {
        'id': 'test_post_2', 
        'title': 'This is a negative test post',
        'selftext': 'This technology is terrible and broken. I hate it.',
        'created_utc': 1640995260,  # 2022-01-01 + 1 min
        'ups': 5,
        'downs': 50,
        'num_comments': 8,
        'permalink': '/r/test/comments/test_post_2/',
        'url': 'https://reddit.com/r/test/comments/test_post_2/',
        'author': {'name': 'test_user_negative'},
        'subreddit': {'display_name': 'test_subreddit'}
    },
    {
        'id': 'test_post_3',
        'title': 'This is a neutral test post',
        'selftext': 'This technology exists and does things.',
        'created_utc': 1640995320,  # 2022-01-01 + 2 min
        'ups': 25,
        'downs': 20,
        'num_comments': 12,
        'permalink': '/r/test/comments/test_post_3/',
        'url': 'https://reddit.com/r/test/comments/test_post_3/',
        'author': {'name': 'test_user_neutral'},
        'subreddit': {'display_name': 'test_subreddit'}
    }
]

# Mock Twitter API responses
MOCK_TWITTER_TWEETS = [
    {
        'id_str': 'tweet_1',
        'full_text': 'Just tried this new app and it\'s absolutely fantastic! 🎉',
        'created_at': datetime(2022, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        'retweet_count': 15,
        'favorite_count': 45,
        'user': {
            'screen_name': 'happy_user',
            'followers_count': 1000,
            'friends_count': 500
        },
        'entities': {
            'hashtags': [{'text': 'awesome'}],
            'user_mentions': [],
            'media': []
        }
    },
    {
        'id_str': 'tweet_2',
        'full_text': 'This service is completely broken and useless. Worst experience ever.',
        'created_at': datetime(2022, 1, 1, 13, 0, 0, tzinfo=timezone.utc),
        'retweet_count': 2,
        'favorite_count': 1,
        'user': {
            'screen_name': 'angry_user',
            'followers_count': 50,
            'friends_count': 100
        },
        'entities': {
            'hashtags': [{'text': 'fail'}],
            'user_mentions': [],
            'media': []
        }
    },
    {
        'id_str': 'tweet_3',
        'full_text': 'The product works as expected. Documentation could be better.',
        'created_at': datetime(2022, 1, 1, 14, 0, 0, tzinfo=timezone.utc),
        'retweet_count': 5,
        'favorite_count': 8,
        'user': {
            'screen_name': 'neutral_user',
            'followers_count': 200,
            'friends_count': 150
        },
        'entities': {
            'hashtags': [],
            'user_mentions': [],
            'media': []
        }
    }
]

# Mock model analysis responses
MOCK_ANALYSIS_RESPONSES = {
    'vader_positive': {
        'compound': 0.8,
        'pos': 0.7,
        'neu': 0.2,
        'neg': 0.1
    },
    'vader_negative': {
        'compound': -0.7,
        'pos': 0.1,
        'neu': 0.2,
        'neg': 0.7
    },
    'vader_neutral': {
        'compound': 0.0,
        'pos': 0.3,
        'neu': 0.4,
        'neg': 0.3
    },
    'gemma_positive': 0.75,
    'gemma_negative': -0.65,
    'gemma_neutral': 0.05,
    'gpt4_positive': {
        'choices': [{
            'message': {
                'content': '{"sentiment": "positive", "score": 0.8, "confidence": 0.9}'
            }
        }]
    },
    'gpt4_negative': {
        'choices': [{
            'message': {
                'content': '{"sentiment": "negative", "score": -0.7, "confidence": 0.85}'
            }
        }]
    }
}

# Mock bot detection responses
MOCK_BOT_DETECTION_RESPONSES = {
    'human_response': {
        'probability': 0.1,
        'is_bot': False,
        'reasoning': 'Natural language patterns and varied content'
    },
    'bot_response': {
        'probability': 0.9,
        'is_bot': True,
        'reasoning': 'Repetitive patterns and promotional content'
    },
    'uncertain_response': {
        'probability': 0.5,
        'is_bot': False,
        'reasoning': 'Mixed signals in content analysis'
    }
}

# Mock model responses for testing different scenarios
MOCK_MODEL_RESPONSES = {
    'huggingface_success': {
        'tokenizer': 'mock_tokenizer',
        'model': 'mock_model'
    },
    'huggingface_failure': None,
    'openai_success': {
        'choices': [{
            'message': {
                'content': '{"sentiment": "positive", "score": 0.8}'
            }
        }]
    },
    'openai_rate_limit': {
        'error': {
            'type': 'rate_limit_exceeded',
            'message': 'Rate limit exceeded'
        }
    },
    'openai_api_error': {
        'error': {
            'type': 'api_error',
            'message': 'API temporarily unavailable'
        }
    }
}

# Mock VRAM information for model selection testing
MOCK_VRAM_INFO = {
    'high_vram': 32.0,    # 32GB
    'medium_vram': 16.0,  # 16GB  
    'low_vram': 8.0,      # 8GB
    'minimal_vram': 4.0,  # 4GB
    'no_vram': 0.0        # No GPU
}

# Mock health check responses
MOCK_HEALTH_RESPONSES = {
    'healthy': {
        'status': 'healthy',
        'database': 'healthy',
        'celery': 'healthy',
        'gemma': {
            'available': True,
            'status': 'operational',
            'test_score': 0.5
        }
    },
    'degraded': {
        'status': 'healthy',
        'database': 'healthy', 
        'celery': 'degraded',
        'gemma': {
            'available': False,
            'status': 'error',
            'error': 'Model not loaded'
        }
    },
    'error': {
        'status': 'error',
        'error': 'Database connection failed'
    }
}

# Test text samples for various scenarios
TEST_TEXT_SAMPLES = {
    'positive': [
        "I absolutely love this product! It's amazing!",
        "This is the best service I've ever used. Fantastic!",
        "Wonderful experience, highly recommended to everyone!",
        "Outstanding quality and excellent customer support."
    ],
    'negative': [
        "This is terrible and completely broken.",
        "Worst experience ever, total waste of money.",
        "Awful service, would not recommend to anyone.",
        "Complete failure, nothing works as advertised."
    ],
    'neutral': [
        "The product works as expected.",
        "Standard service, nothing special about it.",
        "It's okay, meets basic requirements.",
        "Average quality, could be better or worse."
    ],
    'mixed': [
        "Good features but poor documentation.",
        "Great concept but terrible execution.",
        "Love the design, hate the performance.",
        "Excellent support but expensive pricing."
    ],
    'emoji_heavy': [
        "😀😃😄😁😆😅😂🤣",
        "❤️💕💖💗💓💘💞💝",
        "🎉🎊🎈🎁🎀🎂🍰🧁",
        "🔥💯✨⭐🌟💫⚡🌈"
    ],
    'bot_like': [
        "BUY NOW! LIMITED TIME OFFER!!! CLICK HERE!!!",
        "Follow for follow back! Like for like!",
        "URGENT: This will change your life forever!",
        "Amazing deals! Don't miss out! Act now!"
    ]
}

# Mock error responses for testing error handling
MOCK_ERROR_RESPONSES = {
    'reddit_api_error': Exception("Reddit API is temporarily unavailable"),
    'twitter_api_error': Exception("Twitter API rate limit exceeded"),
    'openai_api_error': Exception("OpenAI API key invalid"),
    'huggingface_error': Exception("HuggingFace model loading failed"),
    'database_error': Exception("Database connection lost"),
    'celery_error': Exception("Celery worker unavailable")
}

def get_mock_reddit_post(sentiment='positive', **kwargs):
    """Get a mock Reddit post with specified sentiment."""
    base_post = MOCK_REDDIT_POSTS[0].copy()
    
    if sentiment == 'negative':
        base_post.update(MOCK_REDDIT_POSTS[1])
    elif sentiment == 'neutral':
        base_post.update(MOCK_REDDIT_POSTS[2])
    
    base_post.update(kwargs)
    return base_post

def get_mock_twitter_tweet(sentiment='positive', **kwargs):
    """Get a mock Twitter tweet with specified sentiment."""
    base_tweet = MOCK_TWITTER_TWEETS[0].copy()
    
    if sentiment == 'negative':
        base_tweet.update(MOCK_TWITTER_TWEETS[1])
    elif sentiment == 'neutral':
        base_tweet.update(MOCK_TWITTER_TWEETS[2])
    
    base_tweet.update(kwargs)
    return base_tweet

def get_mock_model_response(model='vader', sentiment='positive'):
    """Get a mock model response for specified model and sentiment."""
    key = f"{model}_{sentiment}"
    return MOCK_ANALYSIS_RESPONSES.get(key, MOCK_ANALYSIS_RESPONSES['vader_neutral'])