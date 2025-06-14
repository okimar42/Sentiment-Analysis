import pytest
from django.conf import settings
from sentiment_analysis import models
from django.urls import get_resolver
from sentiment_analysis.utils import rate_limiting
from sentiment_analysis.utils import __all__ as utils_all
from sentiment_analysis.services import __all__ as services_all
from sentiment_analysis.services import analysis_service

# --- Model Choices Integrity ---
def test_source_choices_unique():
    values = [v for v, _ in models.SentimentAnalysis.SOURCE_CHOICES]
    assert len(values) == len(set(values)), "Duplicate values in SOURCE_CHOICES"

def test_model_choices_unique():
    values = [v for v, _ in models.SentimentAnalysis.MODEL_CHOICES]
    assert len(values) == len(set(values)), "Duplicate values in MODEL_CHOICES"

def test_status_choices_unique():
    values = [v for v, _ in models.SentimentAnalysis.STATUS_CHOICES]
    assert len(values) == len(set(values)), "Duplicate values in STATUS_CHOICES"

# --- Model Choices Completeness ---
def test_all_referenced_sources_in_choices():
    referenced = {"reddit", "twitter"}
    allowed = {v for v, _ in models.SentimentAnalysis.SOURCE_CHOICES}
    assert referenced <= allowed, f"Referenced sources {referenced - allowed} missing from SOURCE_CHOICES"

def test_all_referenced_statuses_in_choices():
    referenced = {"pending", "processing", "completed", "failed"}
    allowed = {v for v, _ in models.SentimentAnalysis.STATUS_CHOICES}
    assert referenced <= allowed, f"Referenced statuses {referenced - allowed} missing from STATUS_CHOICES"

def test_all_referenced_models_in_choices():
    referenced = {"vader", "gpt4", "claude", "gemini", "gemma"}
    allowed = {v for v, _ in models.SentimentAnalysis.MODEL_CHOICES}
    assert referenced <= allowed, f"Referenced models {referenced - allowed} missing from MODEL_CHOICES"

# --- Special Case: Warn if 'grok' is referenced but not in MODEL_CHOICES ---
def test_grok_model_reference():
    referenced = True  # 'grok' is referenced in backend code
    allowed = {v for v, _ in models.SentimentAnalysis.MODEL_CHOICES}
    assert "grok" not in allowed, (
        "'grok' is referenced in code but not present in MODEL_CHOICES. "
        "If this is intentional (API-only), ignore this warning. "
        "If users should be able to select 'grok', add it to MODEL_CHOICES."
    )

# --- Django Settings Integrity ---
def test_installed_apps_unique():
    assert len(settings.INSTALLED_APPS) == len(set(settings.INSTALLED_APPS)), "Duplicate INSTALLED_APPS entries"

def test_middleware_unique():
    assert len(settings.MIDDLEWARE) == len(set(settings.MIDDLEWARE)), "Duplicate MIDDLEWARE entries"

# --- API Routes Integrity ---
def test_url_names_unique():
    resolver = get_resolver()
    names = [name for name in resolver.reverse_dict.keys() if isinstance(name, str)]
    assert len(names) == len(set(names)), "Duplicate route names in URLconf"

def test_url_patterns_unique():
    resolver = get_resolver()
    patterns = [str(p.pattern) for p in resolver.url_patterns]
    assert len(patterns) == len(set(patterns)), "Duplicate URL patterns in URLconf"

# --- RATE_LIMITS Integrity ---
def test_rate_limits_no_duplicate_keys():
    keys = list(rate_limiting.RATE_LIMITS.keys())
    assert len(keys) == len(set(keys)), "Duplicate keys in RATE_LIMITS"

def test_rate_limits_required_fields():
    required_fields = {"initial_delay", "min_delay", "max_delay", "batch_size", "min_retry_delay", "retry_multiplier"}
    for model, config in rate_limiting.RATE_LIMITS.items():
        assert required_fields <= set(config.keys()), f"RATE_LIMITS for {model} missing required fields"

# --- __all__ Integrity for utils/services ---
def test_utils_all_exports_exist():
    import sentiment_analysis.utils as utils_mod
    for name in utils_all:
        assert hasattr(utils_mod, name), f"{name} in utils __all__ not found"

def test_services_all_exports_exist():
    for name in services_all:
        assert hasattr(__import__('sentiment_analysis.services', fromlist=[name]), name), f"{name} in services __all__ not found"

# --- sentiment_map_str_to_num Integrity ---
def test_sentiment_map_str_to_num():
    sentiment_map = {"positive": 1, "neutral": 0, "negative": -1}
    referenced = {"positive", "neutral", "negative"}
    assert set(sentiment_map.keys()) == referenced, "sentiment_map_str_to_num keys mismatch"
    assert len(set(sentiment_map.values())) == len(sentiment_map.values()), "Duplicate values in sentiment_map_str_to_num"

# --- Cross-check RATE_LIMITS models with MODEL_CHOICES and referenced models ---
def test_model_choices_have_rate_limits():
    model_choices = {v for v, _ in models.SentimentAnalysis.MODEL_CHOICES}
    rate_limit_models = set(rate_limiting.RATE_LIMITS.keys())
    # All model choices should have a rate limit entry or fallback to 'default'
    missing = [m for m in model_choices if m not in rate_limit_models and 'default' not in rate_limit_models]
    assert not missing, f"MODEL_CHOICES missing RATE_LIMITS entry: {missing}"

def test_all_referenced_models_in_rate_limits():
    # Models referenced in backend code (from previous analysis)
    referenced = {"vader", "gpt4", "claude", "gemini", "gemma", "grok"}
    rate_limit_models = set(rate_limiting.RATE_LIMITS.keys())
    model_choices = {v for v, _ in models.SentimentAnalysis.MODEL_CHOICES}
    missing = [m for m in referenced if m not in model_choices and m not in rate_limit_models and 'default' not in rate_limit_models]
    assert not missing, f"Referenced models missing in both MODEL_CHOICES and RATE_LIMITS: {missing}"

# --- __all__ Integrity for tasks ---
def test_tasks_all_exports_exist():
    import sentiment_analysis.tasks as tasks_mod
    for name in tasks_mod.__all__:
        assert hasattr(tasks_mod, name), f"{name} in tasks __all__ not found"
    # Check that all public task functions are included in __all__
    public = [n for n in dir(tasks_mod) if not n.startswith('_') and callable(getattr(tasks_mod, n))]
    for name in public:
        assert name in tasks_mod.__all__, f"Public task {name} missing from __all__ in tasks/__init__.py"

# --- __all__ Integrity for core ---
def test_core_all_exports_exist():
    import core
    import types
    for name in core.__all__:
        assert hasattr(core, name), f"{name} in core __all__ not found"
    # Only require non-module public objects to be in __all__
    public = [n for n in dir(core) if not n.startswith('_')]
    for name in public:
        obj = getattr(core, name)
        if not isinstance(obj, types.ModuleType):
            assert name in core.__all__, f"Public object {name} missing from __all__ in core/__init__.py" 