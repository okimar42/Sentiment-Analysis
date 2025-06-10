"""
HuggingFace model management utilities.
"""

import os
import time
import gc
import logging
from typing import Optional, Tuple, Any

# Celery logger is great inside tasks but the same module is imported from
# regular Django views as well.  Fallback to standard logging when Celery
# is not configured to avoid noisy import errors in tests or management
# commands executed outside the worker context.

try:
    from celery.utils.log import get_task_logger
    logger = get_task_logger(__name__)
except Exception:  # pragma: no cover
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

def verify_huggingface_token() -> Optional[str]:
    """
    Verify and return HuggingFace token with retry logic.
    
    Returns:
        str: Valid HuggingFace token or None if verification fails
    """
    from huggingface_hub import login, HfFolder
    
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
                logger.error(f"Failed to login to Hugging Face after {max_retries} attempts: {str(e)}")
                raise

    # Fallback return for static type checkers – execution should never reach
    # this line because the function either returns a valid token or raises.
    return None  # pragma: no cover

def load_model_safely() -> Tuple[Any, Any]:
    """
    Load HuggingFace model with safe memory management.
    
    Returns:
        Tuple[Any, Any]: (tokenizer, model) pair
    """
    try:
        import torch
        from transformers import (
            AutoTokenizer,
            AutoModelForCausalLM,
            AutoModelForSequenceClassification,
            BitsAndBytesConfig,
        )
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

        # ---------------------------------------------
        # Tokenizer
        # ---------------------------------------------
        logger.info("[Gemma] Initialising tokenizer (%s)…", model_name)
        try:
            tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                token=hf_token,
                trust_remote_code=True,
                # Use centralised cache directory so that multiple workers
                # share downloads inside the Docker container.
                cache_dir=os.getenv("HF_HOME", "/root/.cache/huggingface"),
                local_files_only=False,
            )
            logger.info("[Gemma] Tokenizer ready")
        except Exception as e:
            logger.error("[Gemma] Unable to load tokenizer: %s", e)
            raise

        # ---------------------------------------------
        # Model
        # ---------------------------------------------
        logger.info("[Gemma] Initialising model (%s)…", model_name)
        try:
            model_cls_preference = [
                AutoModelForSequenceClassification,
                AutoModelForCausalLM,
            ]

            # Select quantisation configuration
            quantization_config: Optional[BitsAndBytesConfig] = None
            torch_dtype = None

            if quantization == "fp16":
                import torch
                torch_dtype = torch.float16
            elif quantization == "8bit":
                quantization_config = BitsAndBytesConfig(
                    load_in_8bit=True,
                    llm_int8_enable_fp32_cpu_offload=True,
                )
            elif quantization == "4bit":
                import torch
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.float16,
                )
            else:
                raise ValueError(f"Unknown quantization type: {quantization}")

            # Attempt to load a sequence-classification checkpoint first. If the
            # model card does not provide a classifier head the attempt will
            # raise a `ValueError: No such configuration class` which we then
            # fall back to the base causal-LM variant.

            exceptions = []
            for model_cls in model_cls_preference:
                try:
                    model = model_cls.from_pretrained(
                        model_name,
                        token=hf_token,
                        trust_remote_code=True,
                        device_map="auto",
                        cache_dir=os.getenv("HF_HOME", "/root/.cache/huggingface"),
                        low_cpu_mem_usage=True,
                        torch_dtype=torch_dtype,
                        quantization_config=quantization_config,
                        local_files_only=False,
                    )
                    logger.info("[Gemma] Model (%s) loaded with %s", model_name, model_cls.__name__)
                    break
                except Exception as exc:
                    exceptions.append(str(exc))
                    model = None
            else:
                # Exhausted both attempts
                for err in exceptions:
                    logger.debug("[Gemma] Loader error: %s", err)
                raise RuntimeError("Failed to load Gemma model – see above for details")

            logger.info("[Gemma] Model ready")
            return tokenizer, model
            
        except Exception as e:
            logger.error("[Gemma] Failed to initialise model: %s", e)
            raise
            
    except Exception as e:
        logger.error("[Gemma] Unhandled error during model load: %s", e)
        raise

    # Unreachable fallback for type-checkers
    return None, None  # pragma: no cover

# Global model cache
_model_cache = {}

def get_model() -> Tuple[Any, Any]:
    """
    Get cached model or load it if not cached.
    
    Returns:
        Tuple[Any, Any]: (tokenizer, model) pair
    """
    global _model_cache
    
    # Honour environment flags for test environments or CPU-only deployments
    if os.environ.get("NO_LOCAL_LLM") == "1" or os.environ.get("CPU_ONLY") == "1":
        logger.warning("Local LLM loading is disabled via env flag – returning (None, None)")
        return None, None

    if 'tokenizer' not in _model_cache or 'model' not in _model_cache:
        logger.info("[Gemma] Loading model for the first time…")
        tokenizer, model = load_model_safely()
        _model_cache['tokenizer'] = tokenizer
        _model_cache['model'] = model
    
    return _model_cache['tokenizer'], _model_cache['model']