"""Local runtime type stubs to satisfy static type checkers (e.g. mypy).

These stubs make third-party libraries that do not ship type information
(e.g. Django, DRF, Celery) appear as typed modules so that tools such as
mypy do not raise "missing import" errors while analysing this package.
They should **never** be imported directly by application code.
"""
from types import ModuleType
from typing import Any
import sys


class _Stub(ModuleType):
    """Fallback stub module returning itself for any attribute lookup."""

    # Allow arbitrary attribute access without mypy complaints
    def __getattr__(self, item: str) -> "_Stub":  # noqa: D401,E501
        return self  # type: ignore[return-value]

    # Make stubs callable so that functions/classes also resolve
    def __call__(self, *args: Any, **kwargs: Any) -> "_Stub":  # noqa: D401
        return self  # type: ignore[return-value]


# Third-party modules lacking type hints that we reference in backend code.
_STUB_MODULES = [
    # Django core
    "django",
    "django.conf",
    "django.db",
    "django.db.models",
    "django.http",
    "django.shortcuts",
    "django.utils",
    "django.utils.timezone",
    # Django REST Framework
    "rest_framework",
    "rest_framework.decorators",
    "rest_framework.views",
    "rest_framework.permissions",
    "rest_framework.response",
    "rest_framework.status",
    "rest_framework.viewsets",
    # drf-spectacular
    "drf_spectacular",
    "drf_spectacular.openapi",
    # Celery
    "celery",
]

for module_name in _STUB_MODULES:
    if module_name not in sys.modules:
        sys.modules[module_name] = _Stub(module_name)