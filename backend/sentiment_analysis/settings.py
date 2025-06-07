import os
from dotenv import load_dotenv
import threading
import contextvars

# Load environment variables from .env file
load_dotenv()

# ... existing imports and settings ...

# Celery Configuration
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # Disable prefetching
CELERY_WORKER_MAX_TASKS_PER_CHILD = 100  # Restart worker after 100 tasks
CELERY_TASK_ROUTES = {
    'sentiment_analysis.tasks.*': {'queue': 'sentiment_analysis'}
}

# ... rest of the settings ...

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'core.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'sentiment_analysis',
    'drf_spectacular',
    'drf_spectacular_sidecar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sentiment_analysis',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}

# API Keys and External Service Settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', '')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', '')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET', '')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', '')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', '')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', '')

DEBUG = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '')

# Thread-local/contextvar for request_id
_request_id_ctx = contextvars.ContextVar('request_id', default=None)

def get_request_id():
    return _request_id_ctx.get()

class RequestIDLogFilter(logging.Filter):
    def filter(self, record):
        record.request_id = get_request_id() or ''
        return True

# For Celery task_id
_task_id_ctx = contextvars.ContextVar('task_id', default=None)

def get_task_id():
    return _task_id_ctx.get()

class TaskIDLogFilter(logging.Filter):
    def filter(self, record):
        record.task_id = get_task_id() or ''
        return True

# --- JSON Logging ---
from pythonjsonlogger import jsonlogger

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s %(task_id)s',
        },
    },
    'filters': {
        'request_id': {
            '()': 'sentiment_analysis.settings.RequestIDLogFilter',
        },
        'task_id': {
            '()': 'sentiment_analysis.settings.TaskIDLogFilter',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
            'filters': ['request_id', 'task_id'],
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# --- Request ID Middleware (for contextvars) ---
from django.utils.deprecation import MiddlewareMixin
import uuid

class RequestIDMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request_id = str(uuid.uuid4())
        _request_id_ctx.set(request_id)
        request.request_id = request_id
    def process_response(self, request, response):
        if hasattr(request, 'request_id'):
            response['X-Request-ID'] = request.request_id
        _request_id_ctx.set(None)
        return response

MIDDLEWARE = [
    'sentiment_analysis.settings.RequestIDMiddleware',
] + [m for m in MIDDLEWARE if m != 'sentiment_analysis.settings.RequestIDMiddleware']

# --- Celery signals to set task_id contextvar ---
from celery.signals import task_prerun, task_postrun

def set_task_id(sender=None, task_id=None, **kwargs):
    _task_id_ctx.set(task_id)
def clear_task_id(sender=None, task_id=None, **kwargs):
    _task_id_ctx.set(None)
task_prerun.connect(set_task_id)
task_postrun.connect(clear_task_id)

# --- Sentry Integration ---
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

SENTRY_DSN = os.getenv('SENTRY_DSN', '')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), CeleryIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )

# ... rest of the file ... 

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
    INTERNAL_IPS = ['127.0.0.1', 'localhost']

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

def spectacular_preprocessing_hook(endpoints):
    from drf_spectacular.openapi import AutoSchema
    import drf_spectacular.views as spectacular_views
    filtered = []
    for ep in endpoints:
        callback_cls = getattr(ep[3], 'cls', None)
        if callback_cls and callback_cls.__module__.startswith('drf_spectacular.views'):
            continue
        schema = getattr(ep[3], 'schema', None)
        if isinstance(schema, AutoSchema):
            filtered.append(ep)
    return filtered

SPECTACULAR_SETTINGS = {
    'TITLE': 'Sentiment Analysis API',
    'DESCRIPTION': 'API documentation for Sentiment Analysis backend',
    'VERSION': '1.0.0',
    'PREPROCESSING_HOOKS': ['sentiment_analysis.settings.spectacular_preprocessing_hook'],
} 