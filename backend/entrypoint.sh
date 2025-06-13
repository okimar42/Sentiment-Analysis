#!/bin/bash
# set -e  # Removed to prevent script from exiting on errors

echo "[entrypoint.sh] Args: $@"

# Function to wait for database
wait_for_db() {
    echo "[entrypoint.sh] Waiting for database to be ready..."
    until python db_connection_check.py > /dev/null 2>&1; do
        echo "[entrypoint.sh] Database not ready, waiting 2 seconds..."
        sleep 2
    done
    echo "[entrypoint.sh] Database is ready!"
}

echo "[entrypoint.sh] Checking for migration command..."
# Check if we're running migrations (match any way the migration command is called)
if [[ "$@" == *"migrate"* ]]; then
    echo "[entrypoint.sh] Migration command detected. Running migrations..."
    wait_for_db
    python manage.py migrate
    exit 0
fi
echo "[entrypoint.sh] Not a migration command. Continuing with normal startup."

# Wait for database before running migrations
wait_for_db

# Run migrations
echo "[entrypoint.sh] Running database migrations..."
python manage.py migrate

# Check GPU configuration
if [ "$USE_GPU" = "false" ]; then
    echo "[entrypoint.sh] GPU disabled. Running in CPU-only mode."
    export CUDA_VISIBLE_DEVICES=""
else
    echo "[entrypoint.sh] GPU enabled. Checking NVIDIA driver..."
    if ! command -v nvidia-smi &> /dev/null; then
        echo "[entrypoint.sh] Warning: NVIDIA driver not found. Falling back to CPU mode."
        export CUDA_VISIBLE_DEVICES=""
    else
        echo "[entrypoint.sh] NVIDIA driver found. GPU mode enabled."
        export CUDA_VISIBLE_DEVICES="all"
    fi
fi

# Check for NO_LOCAL_LLM
if [ "$NO_LOCAL_LLM" = "1" ]; then
    echo "[entrypoint.sh] NO_LOCAL_LLM is set. Disabling all local LLM/model logic."
    export NO_LOCAL_LLM=1
fi

# Start appropriate service
if [ "$SERVICE_ROLE" = "backend" ]; then
    echo "[entrypoint.sh] Starting Django server..."
    exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 2 --timeout 300 --max-requests 1000 --max-requests-jitter 50 --worker-class gthread --worker-tmp-dir /dev/shm --worker-connections 1000 --limit-request-line 4094 --limit-request-fields 100 --limit-request-field_size 8190
elif [ "$SERVICE_ROLE" = "celery" ]; then
    echo "[entrypoint.sh] Starting Celery worker..."
    exec celery -A sentiment_analysis worker --loglevel=info --concurrency=1 --max-tasks-per-child=100 --max-memory-per-child=12288
else
    echo "[entrypoint.sh] Unknown service role: $SERVICE_ROLE"
    exit 1
fi 