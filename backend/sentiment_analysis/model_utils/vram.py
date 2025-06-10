"""
Deprecated wrapper – delegates to `sentiment_analysis.models.vram`.
"""

from typing import Tuple

from sentiment_analysis.models.vram import get_free_vram_gb, select_gemma_model  # re-export

__all__: Tuple[str, ...] = (
    "get_free_vram_gb",
    "select_gemma_model",
)