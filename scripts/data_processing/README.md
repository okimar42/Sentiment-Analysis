# Stand-alone Sentiment Data Processor

This directory contains a **production-ready extraction** of the original
Django/FastAPI web-app data-processing pipeline.  It can be used to collect
social-media data (currently Reddit & Twitter), run multi-model sentiment and
advanced analyses, and export the results **without** running the web
application or requiring a database server.

---

## Features

* Multi-source fetchers (`reddit`, `twitter`) with identical filtering logic
  to the web-app.
* Multi-model sentiment analysis (VADER, GPT-4, Claude, Gemini).
* Sarcasm detection, IQ estimation, bot detection.
* Image sentiment analysis via GPT-4 Vision, Claude Vision, Gemini Vision.
* Export results to **JSON**, **CSV**, or **SQLite** — formats are byte-for-byte
  compatible with the web-app's export endpoints.
* CLI-first design – perfect for cron, Airflow, `docker run`, or CI jobs.

---

## Quick-start

```bash
# 1.  Clone repo / enter workspace (if not already)
cd /workspace

# 2.  Install dependencies (into a virtualenv or the system)
python -m pip install -r backend/requirements.txt  # includes PRAW, tweepy, openai, etc.

# 3.  Set API keys (export as env vars or place in your shell profile)
export REDDIT_CLIENT_ID=xxx        # Reddit creds
export REDDIT_CLIENT_SECRET=xxx
export REDDIT_USER_AGENT="my-app"

export TWITTER_BEARER_TOKEN=xxx    # Twitter v2 creds (optional)

export OPENAI_API_KEY=sk-...       # Needed for GPT-4 & GPT-4 Vision
export ANTHROPIC_API_KEY=...       # Claude / Vision
export GOOGLE_API_KEY=...          # Gemini & Gemini Vision

# 4.  Run the processor (Reddit + Twitter, VADER only, JSON output)
python -m scripts.data_processing.sentiment_processor \
       -q "python,programming" \
       --sources reddit,twitter \
       --models vader \
       --days-back 1 \
       --max-posts 50 \
       --output-format json \
       --output-path ./results
```

The resulting file `results/sentiment_python_programming_<timestamp>.json`
contains the full analysis plus metadata identical to the web-app models.

---

## Directory layout

```text
scripts/data_processing/
├── sentiment_processor.py     # main CLI entrypoint
├── sources/                   # data fetchers (Reddit, Twitter…)
├── analysis/                  # sentiment engine, image analyzer, helpers
├── output/                    # JSON/CSV/SQLite writers
├── utils/                     # small shared helpers
└── docs (this README + API/DEPLOYMENT/TROUBLESHOOTING)
```

---

## Next steps

* See **API.md** for the full option reference.
* See **DEPLOYMENT.md** for Docker and automation examples.
* See **TROUBLESHOOTING.md** if you hit issues with API keys, rate limits, or
  dependency conflicts.