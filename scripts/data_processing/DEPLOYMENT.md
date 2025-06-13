# Deployment Guide

This guide shows several ways to run the **stand-alone sentiment processor** in
production-like contexts.

---

## 1. Docker (recommended)

A minimal runtime image is already defined in the repository's root Dockerfile.
You can build a **thin** image containing only the scripts:

```dockerfile
# Dockerfile.dp (in project root)
FROM python:3.11-slim AS base
WORKDIR /app

# copy only what we need for runtime
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/data_processing scripts/data_processing
ENTRYPOINT ["python", "-m", "scripts.data_processing.sentiment_processor"]
```

Build & run:
```bash
docker build -f Dockerfile.dp -t sentiment-processor .

docker run --rm \
  -e REDDIT_CLIENT_ID=$REDDIT_CLIENT_ID \
  -e REDDIT_CLIENT_SECRET=$REDDIT_CLIENT_SECRET \
  -e REDDIT_USER_AGENT="sp-bot" \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  sentiment-processor \
  -q "ai,chatgpt" --sources reddit \"twitter\" --models vader,gpt4 --output-format sqlite
```

### Cron-style scheduling (inside container)
For recurring tasks, wrap the entrypoint with crond or use Kubernetes `CronJob`.

---

## 2. Host-side virtualenv + cron

```bash
python -m venv venv && source venv/bin/activate
pip install -r backend/requirements.txt

# crontab -e  (example: run every day at 03:30 UTC)
30 3 * * * /path/to/venv/bin/python -m scripts.data_processing.sentiment_processor \
           -q "worldnews" --sources reddit --models vader \
           --days-back 1 --output-format csv --output-path /data/sentiment
```

Ensure environment variables are exported from `~/.profile`, or use a wrapper
script that `source`s a `.env` file before invocation.

---

## 3. Airflow / Prefect / Dagster

Simply call the module from a PythonOperator / task:

```python
from airflow.operators.bash import BashOperator

BashOperator(
    task_id="sentiment",
    bash_command="python -m scripts.data_processing.sentiment_processor -q 'stocks' --models vader,gpt4 --output-format json --output-path /tmp/results",
)
```

Because all configuration is via CLI/env-vars there is no additional work.

---

## 4. Resilience & Restart

* Outputs are idempotent – generate to unique timestamped paths.
* Processor exits with non-zero status on unexpected fatal errors so container
  orchestrators restart accordingly.
* For long-running LLM calls consider using a **retry wrapper** such as
  `docker run --restart on-failure`.