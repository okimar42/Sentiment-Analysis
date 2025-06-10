"""
Deprecated – kept for backward-compatibility.

This file previously contained a full copy of the Gemma loading logic.  To
avoid diverging behaviour and duplicated maintenance effort it now simply
re-exports the canonical implementation that lives under
`sentiment_analysis.models.huggingface`.
"""

from typing import Any, Tuple

from sentiment_analysis.models.huggingface import (
    verify_huggingface_token,  # re-export for callers that used it
    load_model_safely,
    get_model,
)

# Public re-exports so that `from …model_utils.huggingface import get_model`
# continues to work unchanged.
__all__: Tuple[str, ...] = (
    "verify_huggingface_token",
    "load_model_safely",
    "get_model",
)