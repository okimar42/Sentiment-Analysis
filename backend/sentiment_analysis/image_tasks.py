import asyncio
import gc
import json
import logging
import os
import sys
import time
import warnings
from datetime import datetime, timezone
from typing import Any, Dict, List, Union, Optional

import emoji
import praw
import tweepy
from celery import shared_task
from celery.utils.log import get_task_logger
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from django.conf import settings
from django.core.cache import cache

from .models import SentimentAnalysis, SentimentResult

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning)

logger = get_task_logger(__name__)

if os.environ.get("NO_LOCAL_LLM") == "1":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(
        "NO_LOCAL_LLM mode enabled. Skipping all local LLM/model logic in tasks.py."
    )

    # Optionally, define no-op stubs for any model-related functions if needed
    def analyze_reddit_sentiment(*args, **kwargs):
        logger.info("NO_LOCAL_LLM: analyze_reddit_sentiment is a no-op.")

    def get_model(*args, **kwargs):
        logger.info("NO_LOCAL_LLM: get_model is a no-op.")

elif os.environ.get("CPU_ONLY") == "1":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("CPU_ONLY mode enabled. Skipping all model and GPU logic in tasks.py.")

    # Optionally, define no-op stubs for any model-related functions if needed
    def analyze_reddit_sentiment(*args, **kwargs):
        logger.info("CPU_ONLY: analyze_reddit_sentiment is a no-op.")

    def get_model(*args, **kwargs):
        logger.info("CPU_ONLY: get_model is a no-op.")

else:
    # Only import VADER and other non-model libraries here
    import logging

    # ... rest of the non-model logic ...
    # Initialize VADER
    vader = SentimentIntensityAnalyzer()

    # --- Helper Functions ---
    def compute_vader_score(text: str) -> float:
        """Compute VADER sentiment score for a given text."""
        return vader.polarity_scores(text)["compound"]

    def verify_huggingface_token():
        import os
        import time

        from huggingface_hub import HfFolder, login

        max_retries = 3
        retry_delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                hf_token = os.getenv("HUGGINGFACE_TOKEN")
                if not hf_token:
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"HUGGINGFACE_TOKEN not found, retrying in {retry_delay} "
                            f"seconds... (Attempt {attempt + 1}/{max_retries})"
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
                        f"Failed to login to Hugging Face, retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries}): {str(e)}"
                    )
                    time.sleep(retry_delay)
                else:
                    logger.error(
                        f"Failed to login to Hugging Face after {max_retries} attempts: {str(e)}"
                    )
                    raise

    # Initialize Hugging Face token with retry logic
    try:
        hf_token = verify_huggingface_token()
    except Exception as e:
        logger.error(f"Failed to initialize Hugging Face token: {str(e)}")
        hf_token = None  # Set to None to allow the application to start, but model loading will fail

    def get_free_vram_gb():
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

    def select_gemma_model():
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

    def load_model_safely():
        try:
            import torch
            from transformers import (
                AutoModelForCausalLM,
                AutoTokenizer,
                BitsAndBytesConfig,
            )

            model_name, quantization = select_gemma_model()
            logger.info(
                f"Loading model: {model_name} with quantization: {quantization}"
            )

            # Clear CUDA cache before loading
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()

            # Initialize tokenizer with AutoTokenizer
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
                    model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        load_in_8bit=True,
                        device_map="auto",
                        token=hf_token,
                        trust_remote_code=True,
                        force_download=True,
                        cache_dir="/root/.cache/huggingface",
                        low_cpu_mem_usage=True,
                        local_files_only=False,
                    )
                elif quantization == "4bit":
                    model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        device_map="auto",
                        quantization_config=BitsAndBytesConfig(
                            load_in_4bit=True,
                            bnb_4bit_compute_dtype=torch.float16,
                            bnb_4bit_use_double_quant=True,
                            bnb_4bit_quant_type="nf4",
                        ),
                        token=hf_token,
                        trust_remote_code=True,
                        force_download=True,
                        cache_dir="/root/.cache/huggingface",
                        low_cpu_mem_usage=True,
                        local_files_only=False,
                    )
                else:
                    model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        token=hf_token,
                        trust_remote_code=True,
                        force_download=True,
                        device_map="auto",
                        cache_dir="/root/.cache/huggingface",
                        low_cpu_mem_usage=True,
                        local_files_only=False,
                    )
                logger.info("Model initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize model: {str(e)}")
                raise

            model.eval()  # Set to evaluation mode
            return tokenizer, model

        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            # If loading fails, try with a smaller model
            if "27b" in model_name:
                logger.info("Retrying with 12B model...")
                return load_model_safely()
            elif "12b" in model_name:
                logger.info("Retrying with 4B model...")
                return load_model_safely()
            else:
                raise

    # Initialize model and tokenizer as None
    gemma_tokenizer = None
    gemma_model = None

    def get_model():
        global gemma_tokenizer, gemma_model
        if gemma_tokenizer is None or gemma_model is None:
            try:
                logger.info("[Gemma] Starting model load with timeout...")
                import concurrent.futures

                future = concurrent.futures.ThreadPoolExecutor(max_workers=1).submit(
                    load_model_safely
                )
                try:
                    gemma_tokenizer, gemma_model = future.result(
                        timeout=300
                    )  # 5 minutes
                    logger.info("[Gemma] Model loaded successfully.")
                    logger.info("[Gemma] Model and tokenizer are ready for inference.")
                except concurrent.futures.TimeoutError:
                    logger.error("[Gemma] Model loading timed out after 5 minutes!")
                    logger.warning(
                        "[Gemma] Continuing without model - will use fallback sentiment analysis."
                    )
                    return None, None
            except Exception as e:
                logger.error(f"Failed to initialize model after all retries: {str(e)}")
                logger.warning(
                    "[Gemma] Continuing without model - will use fallback sentiment analysis."
                )
                return None, None
        return gemma_tokenizer, gemma_model

    # Rate limiting settings
    INITIAL_DELAY = 3  # Start with 3 seconds between requests
    MIN_DELAY = 2  # Minimum delay between requests
    MAX_DELAY = 10  # Maximum delay between requests
    BATCH_SIZE = 3  # Process 3 requests at a time
    MAX_RETRIES = 5

    # Model-specific rate limiting settings
    RATE_LIMITS = {
        "gpt4": {
            "initial_delay": 2.0,
            "min_delay": 1.0,
            "max_delay": 10.0,
            "batch_size": 2,
            "min_retry_delay": 2.0,
            "retry_multiplier": 2.0,
        },
        "gemini": {
            "initial_delay": 1.5,
            "min_delay": 0.8,
            "max_delay": 6.0,
            "batch_size": 3,
            "min_retry_delay": 1.5,
            "retry_multiplier": 1.5,
        },
        "grok": {
            "initial_delay": 2.0,
            "min_delay": 1.0,
            "max_delay": 8.0,
            "batch_size": 2,
            "min_retry_delay": 2.0,
            "retry_multiplier": 2.0,
        },
        "default": {
            "initial_delay": 2.0,
            "min_delay": 1.0,
            "max_delay": 8.0,
            "batch_size": 2,
            "min_retry_delay": 2.0,
            "retry_multiplier": 2.0,
        },
    }

    class ModelRateLimiter:
        def __init__(self, model_name: str):
            self.model_name = model_name
            self.settings = RATE_LIMITS.get(model_name, RATE_LIMITS["default"])
            self.current_delay = self.settings["initial_delay"]
            self.lock = asyncio.Lock()
            self.last_request_time = 0
            self.consecutive_failures = 0

        async def wait(self):
            async with self.lock:
                now = time.time()
                time_since_last = now - self.last_request_time
                if time_since_last < self.current_delay:
                    wait_time = self.current_delay - time_since_last
                    await asyncio.sleep(wait_time)
                self.last_request_time = time.time()

        def increase_delay(self):
            # Increase delay more aggressively if we've had consecutive failures
            self.consecutive_failures += 1
            multiplier = self.settings["retry_multiplier"] * (
                1.5 ** (self.consecutive_failures - 1)
            )
            new_delay = self.current_delay * multiplier
            self.current_delay = min(
                max(new_delay, self.settings["min_retry_delay"]),
                self.settings["max_delay"],
            )
            logger.info(
                f"Increased {self.model_name} delay to {self.current_delay:.1f}s after {self.consecutive_failures} consecutive failures"
            )

        def decrease_delay(self):
            # Reset consecutive failures on success
            self.consecutive_failures = 0
            self.current_delay = max(
                self.current_delay * 0.8, self.settings["min_delay"]
            )
            logger.info(
                f"Decreased {self.model_name} delay to {self.current_delay:.1f}s due to successful request"
            )

        @property
        def batch_size(self):
            # Reduce batch size if we've had failures
            return max(1, self.settings["batch_size"] - self.consecutive_failures)

    # Initialize rate limiters for each model
    rate_limiters = {
        "gpt4": ModelRateLimiter("gpt4"),
        "gemini": ModelRateLimiter("gemini"),
        "gemma": ModelRateLimiter("gemma"),
        "grok": ModelRateLimiter("grok"),
    }

    async def make_api_request(client, messages, model_name: str, retry_count=0):
        rate_limiter = rate_limiters.get(model_name, rate_limiters["gpt4"])
        try:
            await rate_limiter.wait()
            if model_name == "gpt4":
                pass

                result = await client.chat.completions.create(
                    model="gpt-4", messages=messages, temperature=0.3
                )
            elif model_name == "gemini":
                import google.generativeai as genai

                model = genai.GenerativeModel("gemini-pro")
                result = await model.generate_content(messages[1]["content"])
            elif model_name == "grok":
                import aiohttp

                url = "https://api.x.ai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {settings.GROK_API_KEY}",
                    "Content-Type": "application/json",
                }
                data = {
                    "model": "grok-beta",
                    "messages": messages,
                    "stream": False,
                    "temperature": 0,
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=data) as resp:
                        if resp.status != 200:
                            raise Exception(
                                f"Grok API error: {resp.status} {await resp.text()}"
                            )
                        result = await resp.json()

                class GrokResult:
                    class Choice:
                        def __init__(self, content):
                            self.message = type("msg", (), {"content": content})

                    def __init__(self, content):
                        self.choices = [self.Choice(content)]

                result = GrokResult(result["choices"][0]["message"]["content"])
            else:
                raise ValueError(f"Unknown model: {model_name}")
            rate_limiter.decrease_delay()
            return result
        except Exception as e:
            if retry_count >= MAX_RETRIES:
                logger.error(
                    f"Max retries ({MAX_RETRIES}) exceeded for {model_name} request: {str(e)}"
                )
                raise e
            rate_limiter.increase_delay()
            logger.warning(
                f"Rate limit hit for {model_name}, retrying with increased delay (Attempt {retry_count + 1}/{MAX_RETRIES})"
            )
            return await make_api_request(client, messages, model_name, retry_count + 1)

    async def analyze_batch_with_model(
        texts: List[str], model_name: str
    ) -> List[Dict[str, Any]]:
        client = None
        try:
            if model_name == "gpt4":
                import os

                import openai

                try:
                    client = openai.AsyncOpenAI(
                        api_key=os.getenv("OPENAI_API_KEY"), http_client=None
                    )
                except TypeError:
                    client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            rate_limiter = rate_limiters[model_name]
            results = []
            for i in range(0, len(texts), rate_limiter.batch_size):
                batch_texts = texts[i : i + rate_limiter.batch_size]
                tasks = []
                for text in batch_texts:
                    messages = [
                        {
                            "role": "system",
                            "content": """You are a sentiment analysis assistant. \nYou must respond with a valid JSON object containing a 'score' field.\nThe score should be a number between -1 and 1.\nExample response: {\"score\": 0.75}""",
                        },
                        {"role": "user", "content": text},
                    ]
                    tasks.append(make_api_request(client, messages, model_name))
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                for result in batch_results:
                    if isinstance(result, Exception):
                        logger.error(f"Error in {model_name} analysis: {str(result)}")
                        results.append({"score": 0})
                    else:
                        try:
                            if model_name in ["gpt4", "grok"]:
                                parsed = json.loads(result.choices[0].message.content)
                            elif model_name == "gemini":
                                parsed = json.loads(result.text)
                            results.append({"score": float(parsed.get("score", 0))})
                        except (json.JSONDecodeError, ValueError) as e:
                            logger.error(
                                f"Invalid JSON response from {model_name}: {str(e)}"
                            )
                            results.append({"score": 0})
            return results
        except Exception as e:
            logger.error(f"Error in analyze_batch_with_model: {str(e)}")
            return [{"score": 0} for _ in texts]

    def analyze_with_gemma(text: str) -> float:
        try:
            if "migrate" in sys.argv:
                return 0.0
            if os.getenv("SERVICE_ROLE") != "backend":
                logger.info("Not in backend service, skipping model loading")
                return 0.0
            tokenizer, model = get_model()
            if tokenizer is None or model is None:
                logger.info("[Gemma] Using VADER as fallback for sentiment analysis")
                return vader.polarity_scores(text)["compound"]
            import torch

            inputs = tokenizer(
                text, return_tensors="pt", truncation=True, max_length=512
            )
            with torch.no_grad():
                outputs = model(**inputs)
                scores = torch.softmax(outputs.logits, dim=1)
            sentiment_score = float(scores[0][1] - scores[0][0])
            return sentiment_score
        except Exception as e:
            logger.error(f"Error in analyze_with_gemma: {str(e)}")
            logger.info("[Gemma] Falling back to VADER due to error")
            return vader.polarity_scores(text)["compound"]

    async def detect_bots_batch(
        texts: List[str], model_name: str = "gpt4"
    ) -> List[Dict[str, Any]]:
        try:
            results = []
            for text in texts:
                messages = [
                    {
                        "role": "system",
                        "content": """You are a bot detection assistant. \
                    Analyze the given text for bot-like behavior and respond with a JSON object containing:\
                    - probability: A number between 0 and 1 indicating the likelihood of the text being from a bot\
                    - is_bot: A boolean indicating if the text is likely from a bot (true if probability > 0.7)\
                    - reasoning: A brief explanation of your analysis\
                    \n                    Example response: {\"probability\": 0.85, \"is_bot\": true, \"reasoning\": \"Text shows repetitive patterns and lacks natural language variation\"}""",
                    },
                    {"role": "user", "content": text},
                ]
                try:
                    if model_name == "gpt4":
                        import os

                        import openai

                        try:
                            client = openai.AsyncOpenAI(
                                api_key=os.getenv("OPENAI_API_KEY"), http_client=None
                            )
                        except TypeError:
                            client = openai.AsyncOpenAI(
                                api_key=os.getenv("OPENAI_API_KEY")
                            )
                        response = await client.chat.completions.create(
                            model="gpt-4", messages=messages, temperature=0.3
                        )
                        result = json.loads(response.choices[0].message.content)
                    elif model_name == "gemini":
                        import google.generativeai as genai

                        model = genai.GenerativeModel("gemini-pro")
                        response = await model.generate_content(messages[1]["content"])
                        result = json.loads(response.text)
                    elif model_name == "gemma":
                        import torch

                        tokenizer, model = get_model()
                        if tokenizer is not None and model is not None:
                            inputs = tokenizer(
                                text,
                                return_tensors="pt",
                                truncation=True,
                                max_length=512,
                            )
                            with torch.no_grad():
                                outputs = model(**inputs)
                                scores = torch.softmax(outputs.logits, dim=1)
                            bot_prob = float(scores[0][1])
                            result = {
                                "probability": bot_prob,
                                "is_bot": bot_prob > 0.7,
                                "reasoning": f"Model confidence: {bot_prob:.2f}",
                            }
                        else:
                            raise ValueError("Gemma model not available")
                    elif model_name == "grok":
                        result = await make_api_request(None, messages, model_name)
                    else:
                        raise ValueError(f"Unsupported model: {model_name}")
                    results.append(
                        {
                            "probability": float(result.get("probability", 0)),
                            "is_bot": bool(result.get("is_bot", False)),
                            "reasoning": str(
                                result.get("reasoning", "No reasoning provided")
                            ),
                        }
                    )
                except Exception as e:
                    logger.error(
                        f"Error in bot detection for text using {model_name}: {str(e)}"
                    )
                    results.append(
                        {
                            "probability": 0,
                            "is_bot": False,
                            "reasoning": f"Error in analysis: {str(e)}",
                        }
                    )
            return results
        except Exception as e:
            logger.error(f"Error in detect_bots_batch: {str(e)}")
            return [
                {
                    "probability": 0,
                    "is_bot": False,
                    "reasoning": f"Error in batch processing: {str(e)}",
                }
                for _ in texts
            ]

    def timing_decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            logger.info(f"[TIMING] {func.__name__} took {duration:.2f}s")
            return result

        return wrapper

    async def async_timing_decorator(func):
        async def wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)
            duration = time.time() - start
            logger.info(f"[TIMING] {func.__name__} took {duration:.2f}s (async)")
            return result

        return wrapper

    # Apply to Celery tasks
    @shared_task(bind=True, max_retries=3, default_retry_delay=60)
    def analyze_reddit_sentiment(self, analysis_id: int) -> str:
        start_time = time.time()
        logger.info("[TIMING] analyze_reddit_sentiment started")
        try:
            analysis = SentimentAnalysis.objects.get(id=analysis_id)
            selected_llms = getattr(analysis, "selected_llms", [])
            selected_features = []
            analysis.status = "processing"
            analysis.save()
            logger.info(
                f"Analysis status set to processing for analysis_id={analysis_id}"
            )

            # Initialize Reddit client
            reddit = praw.Reddit(
                client_id=settings.REDDIT_CLIENT_ID,
                client_secret=settings.REDDIT_CLIENT_SECRET,
                user_agent=settings.REDDIT_USER_AGENT,
            )
            logger.info("Reddit client initialized")

            # Get subreddits to analyze
            subreddits = analysis.query.split(",")
            texts_to_analyze = []
            text_to_result_map = []
            sentiment_results = []
            subreddit_list = []  # List to store subreddit names for each text

            logger.info(
                f"Processing {len(subreddits)} subreddits: {', '.join(subreddits)}"
            )
            logger.info("Starting processing of posts...")
            for subreddit_name in subreddits:
                try:
                    logger.info(f"Fetching posts from subreddit: {subreddit_name}")
                    subreddit = reddit.subreddit(subreddit_name.strip())
                    posts = list(subreddit.hot(limit=100))  # Convert to list once
                    post_count = 0
                    logger.info(
                        f"Found {len(posts)} posts in subreddit {subreddit_name}"
                    )
                    for post in posts:
                        # Skip posts without text content
                        if not post.selftext and not post.title:
                            continue
                        post_count += 1
                        # Combine title and text
                        content = (
                            f"{post.title}\n{post.selftext}"
                            if post.selftext
                            else post.title
                        )
                        # Get VADER score
                        vader_scores = vader.polarity_scores(content)
                        # Store text and metadata for batch processing
                        texts_to_analyze.append(content)
                        subreddit_list.append(
                            subreddit_name.strip()
                        )  # Store subreddit name for this text
                        text_to_result_map.append(
                            {
                                "post_id": post.id,
                                "vader_score": vader_scores["compound"],
                                "has_images": bool(
                                    post.url
                                    and post.url.endswith(
                                        (".jpg", ".jpeg", ".png", ".gif")
                                    )
                                ),
                                "post_date": datetime.fromtimestamp(
                                    post.created_utc, tz=timezone.utc
                                ),
                                "source_metadata": {
                                    "author": post.author.name if post.author else None,
                                    "subreddit": post.subreddit.display_name,
                                    "upvotes": post.ups,
                                    "downvotes": post.downs,
                                    "num_comments": post.num_comments,
                                    "permalink": post.permalink,
                                    "url": post.url,
                                },
                            }
                        )
                    logger.info(
                        f"Processed {post_count} posts from subreddit {subreddit_name}"
                    )
                except Exception as e:
                    logger.error(
                        f"Error processing subreddit {subreddit_name}: {str(e)}"
                    )
                    continue

            # Process all texts in batches
            if texts_to_analyze:
                logger.info(f"Starting analysis for {len(texts_to_analyze)} posts")
                # Create event loop and run async function
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                # Use all user-selected LLMs for all features
                selected_features = []
                # Check if we have any actual LLM models (not just VADER)
                llm_models = [
                    model
                    for model in selected_llms
                    if model in ["gpt4", "gemini", "gemma", "grok", "claude"]
                ]
                # Only include sarcasm if explicitly requested and we have LLM models
                if "sarcasm" in selected_llms and llm_models:
                    selected_features.append("sarcasm")

                logger.info(
                    f"Starting analysis with LLM models: {selected_llms} and features: {selected_features}"
                )

            # Always run analysis (even for VADER-only) to get consistent result structure
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            llm_results = loop.run_until_complete(
                analyze_with_llms(
                    texts_to_analyze,
                    selected_llms,
                    selected_features,
                    None,
                    subreddit_list,  # Pass the list of subreddits
                )
            )
            loop.close()
            logger.info("Analysis completed")

            # Create sentiment results
            logger.info("Creating sentiment results")
            for i, (text, result_map, llm_result) in enumerate(
                zip(texts_to_analyze, text_to_result_map, llm_results)
            ):
                # Determine the primary score based on the selected model
                primary_score = result_map["vader_score"]  # Default to VADER
                if analysis.model == "vader":
                    primary_score = llm_result.get(
                        "vader_score", result_map["vader_score"]
                    )
                elif analysis.model == "gpt4" and "gpt4_score" in llm_result:
                    primary_score = llm_result["gpt4_score"]
                elif analysis.model == "gemini" and "gemini_score" in llm_result:
                    primary_score = llm_result["gemini_score"]
                elif analysis.model == "gemma" and "gemma_score" in llm_result:
                    primary_score = llm_result["gemma_score"]
                elif analysis.model == "grok" and "grok_score" in llm_result:
                    primary_score = llm_result["grok_score"]

                sentiment_result = SentimentResult(
                    sentiment_analysis_id=analysis.id,
                    post_id=result_map["post_id"],
                    content=text,
                    score=primary_score,
                    compound_score=primary_score,
                    has_images=result_map.get("has_images", False),
                    vader_score=result_map["vader_score"],
                    gpt4_score=llm_result.get("gpt4_score", 0),
                    gemini_score=llm_result.get("gemini_score", 0),
                    sarcasm_score=llm_result.get("sarcasm_score", 0),
                    is_sarcastic=llm_result.get("is_sarcastic")
                    if llm_result.get("is_sarcastic") is not None
                    else False,
                    perceived_iq=llm_result.get("perceived_iq"),
                    bot_probability=llm_result.get("bot_probability"),
                    is_bot=llm_result.get("bot_probability", 0) > 0.7
                    if llm_result.get("bot_probability") is not None
                    else False,
                    post_date=result_map.get("post_date"),
                    source_type="reddit",
                    source_metadata=result_map.get("source_metadata", {}),
                    grok_score=llm_result.get("grok_score", 0),
                )
                sentiment_results.append(sentiment_result)
                if (i + 1) % 10 == 0:
                    logger.info(f"Processed {i + 1}/{len(texts_to_analyze)} posts")

            # Bulk create results
            if sentiment_results:
                logger.info(
                    f"Saving {len(sentiment_results)} sentiment results to database"
                )
                SentimentResult.objects.bulk_create(sentiment_results, batch_size=100)
                logger.info(
                    f"Successfully saved {len(sentiment_results)} sentiment results"
                )
                # Refresh analysis from db to ensure related results are available
                analysis.refresh_from_db()

            # Generate content summary - temporarily disabled due to OpenAI client compatibility issues
            try:
                try:
                    all_contents = [
                        r.content
                        for r in SentimentResult.objects.filter(
                            sentiment_analysis=analysis
                        )
                    ]
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        content_summary = loop.run_until_complete(
                            summarize_contents_async(all_contents)
                        )
                        analysis.content_summary = content_summary
                    except Exception as e:
                        logger.error(f"Error in content summary: {e}")
                        analysis.content_summary = "Content summary temporarily unavailable due to API compatibility issues."
                    finally:
                        analysis.save(update_fields=["content_summary"])
                        loop.close()
                except Exception as e:
                    logger.error(f"Outer error in content summary: {e}")
                    analysis.content_summary = "Content summary temporarily unavailable due to API compatibility issues."
                    analysis.save(update_fields=["content_summary"])
            except Exception as e:
                logger.error(f"Final fallback error in content summary: {e}")
                analysis.content_summary = "Content summary temporarily unavailable due to API compatibility issues."
                analysis.save(update_fields=["content_summary"])

            # Update analysis status
            analysis.status = "completed"
            analysis.save(update_fields=["status"])
            logger.info(f"Analysis {analysis_id} completed successfully")

            return f"Analysis completed for {analysis.query}"
        except Exception as e:
            logger.error(f"Error in analyze_reddit_sentiment: {str(e)}")
            analysis.status = "failed"
            analysis.save(update_fields=["status"])
            raise
        finally:
            duration = time.time() - start_time
            logger.info(f"[TIMING] analyze_reddit_sentiment took {duration:.2f}s")

    @shared_task
    def analyze_twitter_sentiment(analysis_id):
        start_time = time.time()
        logger.info("[TIMING] analyze_twitter_sentiment started")
        try:
            analysis = SentimentAnalysis.objects.get(id=analysis_id)
            analysis.status = "processing"
            analysis.save()
            try:
                # Initialize Twitter client
                client = tweepy.Client(
                    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
                    consumer_key=os.getenv("TWITTER_API_KEY"),
                    consumer_secret=os.getenv("TWITTER_API_SECRET"),
                    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
                    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
                )
                # Search tweets
                tweets = client.search_recent_tweets(
                    query=analysis.query,
                    max_results=100,
                    tweet_fields=["created_at", "text"],
                )
                if not tweets.data:
                    analysis.status = "completed"
                    analysis.save()
                    return
                # Process tweets
                for tweet in tweets.data:
                    selected_llms = analysis.selected_llms
                    # For VADER-only analyses, don't include any additional features that require LLM calls
                    selected_features = []
                    # Check if we have any actual LLM models (not just VADER)
                    llm_models = [
                        model
                        for model in selected_llms
                        if model in ["gpt4", "gemini", "gemma", "grok", "claude"]
                    ]
                    # Only include sarcasm if explicitly requested and we have LLM models
                    if "sarcasm" in analysis.selected_llms and llm_models:
                        selected_features.append("sarcasm")
                    logger.info(
                        f"Starting analysis with LLM models: {selected_llms} and features: {selected_features}"
                    )
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    results = loop.run_until_complete(
                        analyze_with_llms(
                            tweet.text, selected_llms, selected_features, None, None
                        )
                    )
                    loop.close()
                    SentimentResult.objects.create(
                        sentiment_analysis=analysis,
                        content=tweet.text,
                        score=results["vader_score"],
                        compound_score=results["gpt4_score"]
                        if "gpt4_score" in results
                        else results["vader_score"],
                        source_type="twitter",
                        post_id=tweet.id,
                        source_metadata={
                            "created_at": tweet.created_at.isoformat()
                            if tweet.created_at
                            else None,
                        },
                        vader_score=results["vader_score"],
                        gpt4_score=results.get("gpt4_score", 0),
                        gemini_score=results.get("gemini_score", 0),
                        sarcasm_score=results.get("sarcasm_score", 0),
                        is_sarcastic=results.get("is_sarcastic", False),
                        perceived_iq=results.get("perceived_iq"),
                        bot_probability=results.get("bot_probability"),
                        is_bot=results.get("bot_probability", 0) > 0.7
                        if results.get("bot_probability") is not None
                        else False,
                        grok_score=results.get("grok_score", 0),
                    )
                # Generate content summary - temporarily disabled due to OpenAI client compatibility issues
                try:
                    all_contents = [
                        r.content
                        for r in SentimentResult.objects.filter(
                            sentiment_analysis=analysis
                        )
                    ]
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        content_summary = loop.run_until_complete(
                            summarize_contents_async(all_contents)
                        )
                        analysis.content_summary = content_summary
                    except Exception as e:
                        logger.error(f"Error in content summary: {e}")
                        analysis.content_summary = "Content summary temporarily unavailable due to API compatibility issues."
                    finally:
                        analysis.save(update_fields=["content_summary"])
                        loop.close()
                    analysis.content_summary = content_summary
                    analysis.save(update_fields=["content_summary"])
                except Exception as e:
                    logger.warning(
                        f"Content summarization failed (OpenAI client issue): {str(e)}"
                    )
                    analysis.content_summary = "Content summary temporarily unavailable due to API compatibility issues."
                    analysis.save(update_fields=["content_summary"])
                analysis.status = "completed"
                analysis.save()
            except Exception as e:
                logger.error(f"Error in analyze_twitter_sentiment: {str(e)}")
                analysis.status = "failed"
                analysis.save()
                return  # Ensure function exits after failure
        except Exception as e:
            logger.error(f"Error in analyze_twitter_sentiment: {str(e)}")
            try:
                analysis.status = "failed"
                analysis.save()
            except Exception:
                pass
            return  # Ensure function exits after failure
        finally:
            duration = time.time() - start_time
            logger.info(f"[TIMING] analyze_twitter_sentiment took {duration:.2f}s")

    def is_mostly_emojis(text: str) -> bool:
        """Check if the text consists mostly of emojis."""
        if not text:
            return False

        # Count emoji characters
        emoji_count = sum(1 for char in text if char in emoji.EMOJI_DATA)

        # Calculate emoji ratio
        emoji_ratio = emoji_count / len(text)

        # Consider text mostly emojis if more than 50% are emojis
        return emoji_ratio > 0.5

    async def detect_sarcasm_batch(
        texts: List[str], model_name: str = "gpt4", subreddits: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        try:
            results = []
            for text in texts:
                messages = [
                    {
                        "role": "system",
                        "content": """You are a sarcasm detection assistant. \
                    Analyze the text and respond with a JSON object containing:\
                    - confidence: A number between 0 and 1 indicating confidence in the detection\
                    - sarcastic: A boolean indicating if the text is sarcastic\
                    - reasoning: A brief explanation of the analysis\
                    \n                    Example response: {\"confidence\": 0.9, \"sarcastic\": true, \"reasoning\": \"The text uses obvious sarcastic markers\"}""",
                    },
                    {"role": "user", "content": text},
                ]
                try:
                    if model_name == "gpt4":
                        import os

                        import openai

                        try:
                            client = openai.AsyncOpenAI(
                                api_key=os.getenv("OPENAI_API_KEY"), http_client=None
                            )
                        except TypeError:
                            client = openai.AsyncOpenAI(
                                api_key=os.getenv("OPENAI_API_KEY")
                            )
                        response = await client.chat.completions.create(
                            model="gpt-4", messages=messages, temperature=0.3
                        )
                        result = json.loads(response.choices[0].message.content)
                    elif model_name == "gemini":
                        import google.generativeai as genai

                        model = genai.GenerativeModel("gemini-pro")
                        response = await model.generate_content(messages[1]["content"])
                        result = json.loads(response.text)
                    elif model_name == "gemma":
                        import torch

                        tokenizer, model = get_model()
                        if tokenizer is not None and model is not None:
                            inputs = tokenizer(
                                text,
                                return_tensors="pt",
                                truncation=True,
                                max_length=512,
                            )
                            with torch.no_grad():
                                outputs = model(**inputs)
                                scores = torch.softmax(outputs.logits, dim=1)
                            # Generate sarcasm detection based on model output
                            sarcasm_score = float(scores[0][1])
                            result = {
                                "confidence": sarcasm_score,
                                "sarcastic": sarcasm_score > 0.5,
                                "reasoning": f"Model confidence: {sarcasm_score:.2f}",
                            }
                        else:
                            raise ValueError("Gemma model not available")
                    elif model_name == "grok":
                        result = await make_api_request(None, messages, model_name)
                    else:
                        raise ValueError(f"Unsupported model: {model_name}")
                    results.append(
                        {
                            "confidence": float(result.get("confidence", 0)),
                            "sarcastic": bool(result.get("sarcastic", False)),
                            "reasoning": str(
                                result.get("reasoning", "No reasoning provided")
                            ),
                        }
                    )
                except Exception as e:
                    logger.error(
                        f"Error in sarcasm detection for text using {model_name}: {str(e)}"
                    )
                    results.append(
                        {
                            "confidence": 0.0,
                            "sarcastic": False,
                            "reasoning": f"Error in analysis: {str(e)}",
                        }
                    )
            return results
        except Exception as e:
            logger.error(f"Error in detect_sarcasm_batch: {str(e)}")
            return [
                {
                    "confidence": 0.0,
                    "sarcastic": False,
                    "reasoning": f"Error in batch processing: {str(e)}",
                }
                for _ in texts
            ]

    async def analyze_iq_batch(
        texts: List[str], model_name: str = "gpt4"
    ) -> List[Dict[str, Any]]:
        try:
            results = []
            for text in texts:
                messages = [
                    {
                        "role": "system",
                        "content": """You are an IQ analysis assistant. \
                    Analyze the text and respond with a JSON object containing:\
                    - iq_score: A number between 0 and 1 indicating the perceived intelligence\
                    - raw_iq: A number between 55 and 145 representing the estimated IQ\
                    - confidence: A number between 0 and 1 indicating confidence in the analysis\
                    - reasoning: A brief explanation of the analysis\
                    \n                    Example response: {\"iq_score\": 0.8, \"raw_iq\": 120, \"confidence\": 0.9, \"reasoning\": \"The text shows high analytical ability\"}""",
                    },
                    {"role": "user", "content": text},
                ]
                try:
                    if model_name == "gpt4":
                        import os

                        import openai

                        try:
                            client = openai.AsyncOpenAI(
                                api_key=os.getenv("OPENAI_API_KEY"), http_client=None
                            )
                        except TypeError:
                            client = openai.AsyncOpenAI(
                                api_key=os.getenv("OPENAI_API_KEY")
                            )
                        response = await client.chat.completions.create(
                            model="gpt-4", messages=messages, temperature=0.3
                        )
                        result = json.loads(response.choices[0].message.content)
                    elif model_name == "gemini":
                        import google.generativeai as genai

                        model = genai.GenerativeModel("gemini-pro")
                        response = await model.generate_content(messages[1]["content"])
                        result = json.loads(response.text)
                    elif model_name == "gemma":
                        import torch

                        tokenizer, model = get_model()
                        if tokenizer is not None and model is not None:
                            inputs = tokenizer(
                                text,
                                return_tensors="pt",
                                truncation=True,
                                max_length=512,
                            )
                            with torch.no_grad():
                                outputs = model(**inputs)
                                scores = torch.softmax(outputs.logits, dim=1)
                            # Generate reasonable IQ scores based on model output
                            iq_score = float(scores[0][1])
                            raw_iq = 55 + (iq_score * 90)  # Scale to 55-145 range
                            result = {
                                "iq_score": iq_score,
                                "raw_iq": raw_iq,
                                "confidence": iq_score,
                                "reasoning": f"Model confidence: {iq_score:.2f}",
                            }
                        else:
                            raise ValueError("Gemma model not available")
                    elif model_name == "grok":
                        result = await make_api_request(None, messages, model_name)
                    else:
                        raise ValueError(f"Unsupported model: {model_name}")
                    results.append(
                        {
                            "iq_score": float(result.get("iq_score", 0.5)),
                            "raw_iq": float(result.get("raw_iq", 100)),
                            "confidence": float(result.get("confidence", 0)),
                            "reasoning": str(
                                result.get("reasoning", "No reasoning provided")
                            ),
                        }
                    )
                except Exception as e:
                    logger.error(
                        f"Error in IQ analysis for text using {model_name}: {str(e)}"
                    )
                    results.append(
                        {
                            "iq_score": 0.5,
                            "raw_iq": 100,
                            "confidence": 0.0,
                            "reasoning": f"Error in analysis: {str(e)}",
                        }
                    )
            return results
        except Exception as e:
            logger.error(f"Error in analyze_iq_batch: {str(e)}")
            return [
                {
                    "iq_score": 0.5,
                    "raw_iq": 100,
                    "confidence": 0.0,
                    "reasoning": f"Error in batch processing: {str(e)}",
                }
                for _ in texts
            ]

    async def analyze_image(image_url: str, selected_llms: list) -> Dict[str, Any]:
        client = None
        try:
            import requests

            response = requests.get(image_url)
            if response.status_code != 200:
                raise ValueError(f"Failed to download image: {response.status_code}")
            import base64

            image_data = base64.b64encode(response.content).decode("utf-8")
            results = {}
            for model in selected_llms:
                try:
                    if model == "gpt4":
                        import os

                        import openai

                        try:
                            client = openai.AsyncOpenAI(
                                api_key=os.getenv("OPENAI_API_KEY"), http_client=None
                            )
                        except TypeError:
                            client = openai.AsyncOpenAI(
                                api_key=os.getenv("OPENAI_API_KEY")
                            )
                        try:
                            response = await client.chat.completions.create(
                                model="gpt-4-vision-preview",
                                messages=[
                                    {
                                        "role": "system",
                                        "content": """Analyze this image and respond with a JSON object containing:\n                                        - sentiment_score: A number between -1 and 1 indicating the overall sentiment\n                                        - content_description: A brief description of the image content\n                                        - emotional_impact: A brief analysis of the emotional impact\n                                        \n                                        Example response: {\"sentiment_score\": 0.8, \"content_description\": \"A happy family at the beach\", \"emotional_impact\": \"Positive and uplifting\"}""",
                                    },
                                    {
                                        "role": "user",
                                        "content": [
                                            {
                                                "type": "text",
                                                "text": "Analyze this image",
                                            },
                                            {
                                                "type": "image_url",
                                                "image_url": {
                                                    "url": f"data:image/jpeg;base64,{image_data}"
                                                },
                                            },
                                        ],
                                    },
                                ],
                                max_tokens=300,
                            )
                            result = json.loads(response.choices[0].message.content)
                            results["gpt4_image"] = {
                                "sentiment_score": float(
                                    result.get("sentiment_score", 0)
                                ),
                                "content_description": str(
                                    result.get("content_description", "")
                                ),
                                "emotional_impact": str(
                                    result.get("emotional_impact", "")
                                ),
                            }
                        finally:
                            await client.aclose()
                    elif model == "gemini":
                        import google.generativeai as genai

                        model = genai.GenerativeModel("gemini-pro-vision")
                        response = await model.generate_content(
                            [
                                "Analyze this image and provide sentiment, content description, and emotional impact",
                                {"mime_type": "image/jpeg", "data": image_data},
                            ]
                        )
                        content = response.text
                        sentiment_score = 0.0
                        if "positive" in content.lower():
                            sentiment_score = 0.5
                        elif "negative" in content.lower():
                            sentiment_score = -0.5
                        results["gemini_image"] = {
                            "sentiment_score": sentiment_score,
                            "content_description": content,
                            "emotional_impact": content,
                        }
                    elif model == "gemma":
                        continue
                except Exception as e:
                    logger.error(f"Error in {model} image analysis: {str(e)}")
                    results[f"{model}_image"] = {
                        "sentiment_score": 0,
                        "content_description": f"Error in analysis: {str(e)}",
                        "emotional_impact": "Analysis failed",
                    }
            return results
        except Exception as e:
            logger.error(f"Error in analyze_image: {str(e)}")
            return {
                "error": str(e),
                "sentiment_score": 0,
                "content_description": "Failed to analyze image",
                "emotional_impact": "Analysis failed",
            }

    async def analyze_with_llms(
        texts: Union[str, List[str]],
        selected_llms: list,
        selected_features: Optional[list] = None,
        image_url: Optional[str] = None,
        subreddits: Optional[List[str]] = None,
    ) -> Union[dict, List[dict]]:
        """Analyze text(s) using selected LLMs and features with model-specific rate limiting. Caches LLM results."""
        logger.info(
            f"Starting analysis with LLMs: {selected_llms} and features: {selected_features}"
        )
        is_single = isinstance(texts, str)
        cache_key = f"llm_result:{str(texts)}:{str(selected_llms)}:{str(selected_features)}:{str(image_url)}:{str(subreddits)}"
        cached = cache.get(cache_key)
        if cached:
            logger.info(f"[CACHE] Returning cached LLM result for key: {cache_key}")
            return cached

        # Convert single text to list for consistent processing
        if is_single:
            texts = [texts]
            if subreddits:
                subreddits = [subreddits]

        results = []

        try:
            # Step 1: Do sentiment analysis first for all texts with each selected model
            logger.info("Starting sentiment analysis for all texts")
            sentiment_results = {}

            # Process each selected model
            for model in selected_llms:
                logger.info(f"Starting {model} analysis")
                if model == "vader":
                    model_results = []
                    for text in texts:
                        score = vader.polarity_scores(text)["compound"]
                        model_results.append({"score": score})
                    sentiment_results["vader"] = model_results
                elif model == "gemma":
                    import torch

                    gemma_results = []
                    for text in texts:
                        try:
                            tokenizer, model = get_model()
                            if tokenizer is not None and model is not None:
                                inputs = tokenizer(
                                    text,
                                    return_tensors="pt",
                                    truncation=True,
                                    max_length=512,
                                )
                                with torch.no_grad():
                                    outputs = model(**inputs)
                                    scores = torch.softmax(outputs.logits, dim=1)
                                score = float(scores[0][1] - scores[0][0])
                            else:
                                logger.warning(
                                    "[Gemma] Model not available, skipping analysis"
                                )
                                score = 0.0
                        except Exception as e:
                            logger.error(f"Error in Gemma analysis: {str(e)}")
                            score = 0.0
                        gemma_results.append({"score": score})
                    sentiment_results["gemma"] = gemma_results
                elif model in ["gpt4", "gemini"]:
                    model_results = await analyze_batch_with_model(texts, model)
                    sentiment_results[model] = model_results
                elif model == "grok":
                    grok_results = []
                    for text in texts:
                        try:
                            model_results = await analyze_batch_with_model(
                                [text], "grok"
                            )
                            score = model_results[0]["score"]
                        except Exception as e:
                            logger.error(f"Error in Grok analysis: {str(e)}")
                            score = 0.0
                        grok_results.append({"score": score})
                    sentiment_results["grok"] = grok_results

            # Step 2: Process each text's additional features sequentially
            for i, text in enumerate(texts):
                text_results = {
                    "vader_score": sentiment_results["vader"][i]["score"]
                    if "vader" in sentiment_results
                    else 0,
                    "gpt4_score": sentiment_results["gpt4"][i]["score"]
                    if "gpt4" in sentiment_results
                    else 0,
                    "gemini_score": sentiment_results["gemini"][i]["score"]
                    if "gemini" in sentiment_results
                    else 0,
                    "gemma_score": sentiment_results["gemma"][i]["score"]
                    if "gemma" in sentiment_results
                    else 0,
                    "grok_score": sentiment_results["grok"][i]["score"]
                    if "grok" in sentiment_results
                    else 0,
                }

                current_subreddit = (
                    subreddits[i] if subreddits and i < len(subreddits) else None
                )

                # Set N/A values for features not available with current model selection
                # (e.g., when using VADER only, IQ and bot detection are not available)
                if "iq" not in selected_features:
                    text_results.update(
                        {
                            "perceived_iq": -1,  # -1 indicates N/A
                            "raw_iq": -1,
                            "iq_confidence": -1,
                            "iq_reasoning": "Not available with VADER model",
                        }
                    )

                if "bot" not in selected_features:
                    text_results.update(
                        {
                            "bot_probability": -1,  # -1 indicates N/A
                            "is_bot": None,
                            "bot_reasoning": "Not available with VADER model",
                        }
                    )

                if "sarcasm" not in selected_features:
                    text_results.update(
                        {
                            "sarcasm_score": -1,  # -1 indicates N/A
                            "is_sarcastic": None,
                            "sarcasm_reasoning": "Not available with VADER model",
                        }
                    )

                # Process additional features only if selected
                if selected_features:
                    # Sarcasm detection
                    if "sarcasm" in selected_features:
                        logger.info(
                            f"Starting sarcasm detection for text {i+1}/{len(texts)}"
                        )
                        try:
                            # Use the first available model from selected_llms for sarcasm detection
                            sarcasm_model = next(
                                (
                                    model
                                    for model in selected_llms
                                    if model in ["gpt4", "gemini", "gemma", "grok"]
                                ),
                                "gpt4",
                            )
                            sarcasm_results = await detect_sarcasm_batch(
                                [text],
                                sarcasm_model,
                                [current_subreddit] if current_subreddit else [],
                            )
                            text_results.update(
                                {
                                    "sarcasm_score": sarcasm_results[0]["confidence"],
                                    "is_sarcastic": sarcasm_results[0]["sarcastic"],
                                    "sarcasm_reasoning": sarcasm_results[0][
                                        "reasoning"
                                    ],
                                }
                            )
                        except Exception as e:
                            logger.error(f"Error in sarcasm detection: {str(e)}")
                            text_results.update(
                                {
                                    "sarcasm_score": 0.0,
                                    "is_sarcastic": False,
                                    "sarcasm_reasoning": "Error in analysis",
                                }
                            )

                    # IQ analysis
                    if "iq" in selected_features:
                        logger.info(f"Starting IQ analysis for text {i+1}/{len(texts)}")
                        try:
                            if is_mostly_emojis(text):
                                text_results.update(
                                    {
                                        "perceived_iq": 0.5,
                                        "raw_iq": 100,
                                        "iq_confidence": 0,
                                        "iq_reasoning": "Skipped analysis - post is mostly emojis",
                                    }
                                )
                            else:
                                # Use the first available model from selected_llms for IQ analysis
                                iq_model = next(
                                    (
                                        model
                                        for model in selected_llms
                                        if model in ["gpt4", "gemini", "gemma", "grok"]
                                    ),
                                    "gpt4",
                                )
                                iq_results = await analyze_iq_batch([text], iq_model)
                                text_results.update(
                                    {
                                        "perceived_iq": iq_results[0]["iq_score"],
                                        "raw_iq": iq_results[0]["raw_iq"],
                                        "iq_confidence": iq_results[0]["confidence"],
                                        "iq_reasoning": iq_results[0]["reasoning"],
                                    }
                                )
                        except Exception as e:
                            logger.error(f"Error in IQ analysis: {str(e)}")
                            text_results.update(
                                {
                                    "perceived_iq": 0.5,
                                    "raw_iq": 100,
                                    "iq_confidence": 0.0,
                                    "iq_reasoning": "Error in analysis",
                                }
                            )

                    # Bot detection
                    if "bot" in selected_features:
                        logger.info(
                            f"Starting bot detection for text {i+1}/{len(texts)}"
                        )
                        try:
                            # Use the first available model from selected_llms for bot detection
                            bot_model = next(
                                (
                                    model
                                    for model in selected_llms
                                    if model in ["gpt4", "gemini", "gemma", "grok"]
                                ),
                                "gpt4",
                            )
                            bot_results = await detect_bots_batch([text], bot_model)
                            text_results.update(
                                {
                                    "bot_probability": bot_results[0]["probability"],
                                    "is_bot": bot_results[0]["is_bot"],
                                    "bot_reasoning": bot_results[0]["reasoning"],
                                }
                            )
                        except Exception as e:
                            logger.error(f"Error in bot detection: {str(e)}")
                            text_results.update(
                                {
                                    "bot_probability": 0.0,
                                    "is_bot": False,
                                    "bot_reasoning": "Error in analysis",
                                }
                            )

                results.append(text_results)

            # Image analysis if URL provided (only for single text)
            if image_url and is_single:
                logger.info(f"Starting image analysis for URL: {image_url}")
                try:
                    image_results = await analyze_image(image_url, selected_llms)
                    results[0].update(image_results)
                    logger.info("Image analysis completed successfully")
                except Exception as e:
                    logger.error(f"Error in image analysis: {str(e)}")

            logger.info("Analysis completed successfully")
            if results:
                cache.set(
                    cache_key, results[0] if is_single else results, timeout=60 * 60
                )  # 1 hour
            return results[0] if is_single else results

        except Exception as e:
            logger.error(f"Error in analyze_with_llms: {str(e)}")
            return results[0] if is_single else results

    # --- Content summarization helper ---
    async def summarize_contents_async(texts):
        if not texts:
            return "No content to summarize."
        cache_key = f"content_summary:{hash(tuple(texts))}"
        cached = cache.get(cache_key)
        if cached:
            logger.info(
                f"[CACHE] Returning cached content summary for key: {cache_key}"
            )
            return cached
        # Limit to first 50 posts to avoid token limits
        sample_texts = texts[:50]
        joined = "\n".join(sample_texts)
        prompt = f"Summarize the main topics, themes, and trends in the following social media posts. Be concise and focus on what people are talking about, not sentiment:\n{joined}\nSummary:"
        import os

        import openai

        # Initialize OpenAI client with simpler configuration to avoid proxy issues
        try:
            # Try the simplest initialization first
            client = openai.AsyncOpenAI()
        except TypeError:
            try:
                # Try with explicit API key
                client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            except Exception:
                # Return simple fallback if OpenAI is not available
                logger.warning(
                    "OpenAI client initialization failed, returning fallback summary"
                )
                return "Content summary unavailable - OpenAI client error."

        try:
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
            )
            summary = response.choices[0].message.content.strip()
            cache.set(cache_key, summary, timeout=60 * 60)  # 1 hour
            return summary
        except Exception as e:
            logger.error(f"Error summarizing content: {str(e)}")
            return "Content summary unavailable due to an error."
        finally:
            try:
                await client.aclose()
            except Exception:
                pass  # Ignore client close errors
