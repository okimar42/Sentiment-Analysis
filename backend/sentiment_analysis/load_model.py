import os

if os.environ.get("CPU_ONLY") == "1" or os.environ.get("NO_LOCAL_LLM") == "1":
    raise SystemExit("Model loading skipped due to CPU_ONLY or NO_LOCAL_LLM mode.")

def load_model():
    """Load the sentiment analysis model."""
    try:
        # Load the model
        model = AutoModelForSequenceClassification.from_pretrained(
            "ProsusAI/finbert",
            num_labels=3,
            cache_dir=MODEL_CACHE_DIR
        )
        model.eval()
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise 