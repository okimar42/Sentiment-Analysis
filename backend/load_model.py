import os
import time
import logging
import sys

if os.environ.get("NO_LOCAL_LLM") == "1":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("NO_LOCAL_LLM mode enabled. Skipping all local LLM/model loading.")
    exit(0)

if os.environ.get("CPU_ONLY") == "1":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("CPU_ONLY mode enabled. Skipping model loading.")
    exit(0)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def verify_huggingface_token():
    """Verify and login to Hugging Face using the token from environment."""
    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            from huggingface_hub import login, HfFolder
            hf_token = os.getenv("HUGGINGFACE_TOKEN")
            if not hf_token:
                if attempt < max_retries - 1:
                    logger.warning(f"HUGGINGFACE_TOKEN not found, retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    continue
                else:
                    raise ValueError("HUGGINGFACE_TOKEN environment variable is not set after multiple attempts")
            
            # Login to Hugging Face
            login(token=hf_token)
            
            # Verify token is valid by checking if we can access the token info
            HfFolder.get_token()
            
            logger.info("Successfully logged in to Hugging Face")
            return hf_token
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Failed to login to Hugging Face, retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries}): {str(e)}")
                time.sleep(retry_delay)
            else:
                logger.error(f"Failed to login to Hugging Face after {max_retries} attempts: {str(e)}")
                raise

def get_free_vram_gb():
    """Returns free VRAM in GB on the first CUDA device."""
    try:
        import torch
        if torch.cuda.is_available():
            stats = torch.cuda.mem_get_info()
            free_bytes = stats[0]
            return free_bytes / (1024 ** 3)
        else:
            logger.warning("CUDA is not available, falling back to nvidia-smi")
            import subprocess
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

def select_gemma_model():
    """Select appropriate Gemma model based on available VRAM."""
    free_gb = get_free_vram_gb()
    logger.info(f"Detected free VRAM: {free_gb:.2f} GB")

    # More conservative VRAM thresholds
    if free_gb >= 32:
        return "google/gemma-3-27b-it", "fp16"
    elif free_gb >= 24:
        return "google/gemma-3-27b-it", "8bit"
    elif free_gb >= 16:
        return "google/gemma-3-27b-it", "4bit"
    elif free_gb >= 14:
        return "google/gemma-3-12b-it", "fp16"
    elif free_gb >= 10:
        return "google/gemma-3-12b-it", "8bit"
    elif free_gb >= 8:
        return "google/gemma-3-12b-it", "4bit"
    elif free_gb >= 6:
        return "google/gemma-3-4b-it", "fp16"
    elif free_gb >= 4:
        return "google/gemma-3-4b-it", "8bit"
    else:
        return "google/gemma-3-4b-it", "4bit"

def load_model_with_retry(max_retries=3, retry_delay=60):
    """Load model with retry logic."""
    for attempt in range(max_retries):
        try:
            # Import torch and transformers only here
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
            # Verify Hugging Face token
            hf_token = verify_huggingface_token()
            
            # Select model and quantization
            model_name, quantization = select_gemma_model()
            logger.info(f"Loading model: {model_name} with quantization: {quantization}")

            # Clear CUDA cache
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

            # Initialize tokenizer with AutoTokenizer
            logger.info("Initializing tokenizer...")
            try:
                tokenizer = AutoTokenizer.from_pretrained(
                    "google/gemma-2b-it",  # Use the 2B model for tokenizer
                    token=hf_token,
                    trust_remote_code=True,
                    force_download=True
                )
                logger.info("Tokenizer initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize tokenizer: {str(e)}")
                raise

            # Initialize model
            logger.info("Initializing model...")
            try:
                if quantization == "fp16":
                    model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        torch_dtype=torch.float16,
                        token=hf_token,
                        trust_remote_code=True,
                        force_download=True,
                        device_map="auto"
                    )
                elif quantization == "8bit":
                    model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        load_in_8bit=True,
                        device_map="auto",
                        token=hf_token,
                        trust_remote_code=True,
                        force_download=True
                    )
                elif quantization == "4bit":
                    model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        device_map="auto",
                        quantization_config=BitsAndBytesConfig(load_in_4bit=True),
                        token=hf_token,
                        trust_remote_code=True,
                        force_download=True
                    )
                else:
                    model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        token=hf_token,
                        trust_remote_code=True,
                        force_download=True,
                        device_map="auto"
                    )
                logger.info("Model initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize model: {str(e)}")
                raise

            logger.info("Model loaded successfully")
            return tokenizer, model

        except Exception as e:
            logger.error(f"Failed to load model (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Failed to load model after all retries")
                raise

def is_running_migrations():
    """Check if we're running Django migrations."""
    return len(sys.argv) > 1 and sys.argv[1] == "migrate"

if __name__ == "__main__":
    if is_running_migrations():
        logger.info("Skipping model loading for migrations")
        sys.exit(0)
        
    try:
        tokenizer, model = load_model_with_retry()
        logger.info("Model loading completed successfully")
    except Exception as e:
        logger.error(f"Model loading failed: {str(e)}")
        exit(1) 