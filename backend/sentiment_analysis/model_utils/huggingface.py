"""
HuggingFace model management utilities.
"""

import gc
import os
import time
from typing import Any, Optional, Tuple

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# Global model cache
_model_cache: dict[str, Any] = {}


def verify_huggingface_token() -> Optional[str]:
    """
    Verify and return HuggingFace token with retry logic.

    Returns:
        str: Valid HuggingFace token or None if verification fails
    """
    from huggingface_hub import HfFolder, login

    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            hf_token = os.getenv("HUGGINGFACE_TOKEN")
            if not hf_token:
                if attempt < max_retries - 1:
                    logger.warning(
                        f"HUGGINGFACE_TOKEN not found, retrying in {retry_delay} seconds... "
                        f"(Attempt {attempt + 1}/{max_retries})"
                    )
                    time.sleep(retry_delay)
                    continue
                else:
                    raise ValueError(
                        "HUGGINGFACE_TOKEN environment variable is not set after multiple attempts"
                    )

            # Login to Hugging Face
            login(token=hf_token)

            # Verify token is valid by checking if we can access the token info
            HfFolder.get_token()

            logger.info("Successfully logged in to Hugging Face")
            return hf_token

        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(
                    f"Failed to login to Hugging Face, retrying in {retry_delay} seconds... "
                    f"(Attempt {attempt + 1}/{max_retries}): {str(e)}"
                )
                time.sleep(retry_delay)
            else:
                logger.error(
                    f"Failed to login to Hugging Face after {max_retries} attempts: {str(e)}"
                )
                raise

    # Fallback return to satisfy type checkers (unreachable if exceptions raised)
    return None


def load_model_safely() -> Tuple[Any, Any]:
    """
    Load HuggingFace model with safe memory management.

    Returns:
        Tuple[Any, Any]: (tokenizer, model) pair
    """
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        from .vram import select_gemma_model

        # Get HuggingFace token
        try:
            hf_token = verify_huggingface_token()
        except Exception as e:
            logger.error(f"Failed to get HuggingFace token: {str(e)}")
            hf_token = None

        model_name, quantization = select_gemma_model()
        logger.info(f"Loading model: {model_name} with quantization: {quantization}")

        # Clear CUDA cache before loading
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            gc.collect()

        # Initialize tokenizer
        logger.info("Initializing tokenizer...")
        try:
            tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                token=hf_token,
                trust_remote_code=True,
                force_download=True,
                cache_dir="/root/.cache/huggingface",
                local_files_only=False,
            )
            logger.info("Tokenizer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize tokenizer: {str(e)}")
            raise

        # Initialize model with appropriate quantization
        logger.info("Initializing model...")
        try:
            if quantization == "fp16":
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16,
                    token=hf_token,
                    trust_remote_code=True,
                    force_download=True,
                    device_map="auto",
                    cache_dir="/root/.cache/huggingface",
                    low_cpu_mem_usage=True,
                    local_files_only=False,
                )
            elif quantization == "8bit":
                quantization_config = BitsAndBytesConfig(
                    load_in_8bit=True, llm_int8_enable_fp32_cpu_offload=True
                )
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    quantization_config=quantization_config,
                    token=hf_token,
                    trust_remote_code=True,
                    device_map="auto",
                    cache_dir="/root/.cache/huggingface",
                    low_cpu_mem_usage=True,
                    local_files_only=False,
                )
            elif quantization == "4bit":
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.float16,
                )
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    quantization_config=quantization_config,
                    token=hf_token,
                    trust_remote_code=True,
                    device_map="auto",
                    cache_dir="/root/.cache/huggingface",
                    low_cpu_mem_usage=True,
                    local_files_only=False,
                )
            else:
                raise ValueError(f"Unknown quantization type: {quantization}")

            logger.info("Model initialized successfully")
            return tokenizer, model

        except Exception as e:
            logger.error(f"Failed to initialize model: {str(e)}")
            raise

    except Exception as e:
        logger.error(f"Failed to load model safely: {str(e)}")
        raise


def get_model() -> Tuple[Any, Any]:
    """
    Get cached model or load it if not cached.

    Returns:
        Tuple[Any, Any]: (tokenizer, model) pair
    """
    if "tokenizer" not in _model_cache or "model" not in _model_cache:
        logger.info("Loading model for the first time...")
        tokenizer, model = load_model_safely()
        _model_cache["tokenizer"] = tokenizer
        _model_cache["model"] = model

    return _model_cache["tokenizer"], _model_cache["model"]
