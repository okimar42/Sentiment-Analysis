"""
VRAM management and model selection utilities.
"""

import logging
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
        import torch
        import subprocess
        
        if torch.cuda.is_available():
            stats = torch.cuda.mem_get_info()
            free_bytes = stats[0]
            return free_bytes / (1024 ** 3)
        else:
            # Fallback: use nvidia-smi
            try:
                result = subprocess.run(
                    ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,nounits,noheader"],
                    stdout=subprocess.PIPE, check=True, text=True
                )
                free_mb = int(result.stdout.split('\n')[0])
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

    # Use larger instruction-tuned variants when there is ample VRAM
    # Gemma officially provides 2B and 7B checkpoints.
    # We default to the instruction-tuned ("*-it") variants which are
    # better suited for downstream tasks out-of-the-box.

    # >=32 GB — 7B full-precision fp16
    if free_gb >= 32:
        return "google/gemma-7b-it", "fp16"
    # >=24 GB — 7B 8-bit
    elif free_gb >= 24:
        return "google/gemma-7b-it", "8bit"
    # >=16 GB — 7B 4-bit
    elif free_gb >= 16:
        return "google/gemma-7b-it", "4bit"
    # Moderate VRAM uses 2B variant with lighter quantization
    elif free_gb >= 12:
        return "google/gemma-2b-it", "fp16"
    elif free_gb >= 8:
        return "google/gemma-2b-it", "8bit"
    elif free_gb >= 4:
        return "google/gemma-2b-it", "4bit"
    else:
        # Extremely low memory – still attempt 4-bit loading but expect CPU fallback
        return "google/gemma-2b-it", "4bit"