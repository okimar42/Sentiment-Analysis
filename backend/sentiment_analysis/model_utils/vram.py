"""
Deprecated wrapper – delegates to `sentiment_analysis.models.vram`.
"""

from typing import Tuple

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def get_free_vram_gb() -> float:
    """
    Get available VRAM in gigabytes.

    Returns:
        float: Available VRAM in GB
    """
    try:
        import subprocess

        import torch

        if torch.cuda.is_available():
            stats = torch.cuda.mem_get_info()
            free_bytes = stats[0]
            return free_bytes / (1024**3)
        else:
            # Fallback: use nvidia-smi
            try:
                result = subprocess.run(
                    [
                        "nvidia-smi",
                        "--query-gpu=memory.free",
                        "--format=csv,nounits,noheader",
                    ],
                    stdout=subprocess.PIPE,
                    check=True,
                    text=True,
                )
                free_mb = int(result.stdout.split("\n")[0])
                return free_mb / 1024
            except Exception as e:
                logger.error(f"Failed to get VRAM info from nvidia-smi: {str(e)}")
                return 0
    except Exception as e:
        logger.error(f"Failed to get VRAM info: {str(e)}")
        return 0


def select_gemma_model() -> Tuple[str, str]:
    """
    Select appropriate Gemma model based on available VRAM.

    Returns:
        Tuple[str, str]: (model_name, quantization_type)
    """
    free_gb = get_free_vram_gb()
    logger.info(f"Detected free VRAM: {free_gb:.2f} GB")

    # More conservative VRAM thresholds
    if free_gb >= 32:
        return "google/gemma-2b", "fp16"
    elif free_gb >= 24:
        return "google/gemma-2b", "8bit"
    elif free_gb >= 16:
        return "google/gemma-2b", "4bit"
    elif free_gb >= 14:
        return "google/gemma-2b", "fp16"
    elif free_gb >= 10:
        return "google/gemma-2b", "8bit"
    elif free_gb >= 8:
        return "google/gemma-2b", "4bit"
    elif free_gb >= 6:
        return "google/gemma-2b", "fp16"
    elif free_gb >= 4:
        return "google/gemma-2b", "8bit"
    else:
        return "google/gemma-2b", "4bit"

from sentiment_analysis.models.vram import get_free_vram_gb, select_gemma_model  # re-export

__all__: Tuple[str, ...] = (
    "get_free_vram_gb",
    "select_gemma_model",
)