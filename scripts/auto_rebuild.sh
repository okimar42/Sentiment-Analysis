#!/usr/bin/env bash
set -e

# Detect mode from environment or default
USE_GPU=${USE_GPU:-true}
NO_LOCAL_LLM=${NO_LOCAL_LLM:-0}

# Compute a hash of requirements and Dockerfiles for cache busting
REQ_HASH=$(cat backend/requirements*.txt | sha256sum)
DOCKERFILE_HASH=$(cat backend/Dockerfile* | sha256sum)
MODE_HASH="${USE_GPU}_${NO_LOCAL_LLM}"
CACHE_FILE=".last_build_${MODE_HASH}.cache"

# If the hash has changed, or the mode has changed, force rebuild
if [[ ! -f $CACHE_FILE ]] || [[ "$(cat $CACHE_FILE)" != "$REQ_HASH $DOCKERFILE_HASH" ]]; then
  echo "[auto_rebuild.sh] Detected change in requirements, Dockerfile, or build mode. Forcing rebuild..."
  # Pass flags to dev.sh based on mode
  REBUILD_FLAGS=""
  if [[ "$USE_GPU" == "false" ]]; then
    REBUILD_FLAGS="--cpu-only"
  fi
  if [[ "$NO_LOCAL_LLM" == "1" ]]; then
    REBUILD_FLAGS="$REBUILD_FLAGS --no-local"
  fi
  ./dev.sh rebuild all $REBUILD_FLAGS
  echo "$REQ_HASH $DOCKERFILE_HASH" > $CACHE_FILE
else
  echo "[auto_rebuild.sh] No changes detected. Skipping rebuild."
fi 