#!/bin/bash

# Enable BuildKit for faster builds
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Ensure Buildx uses docker-container driver for cache export support
if ! docker buildx inspect devbuilder &>/dev/null; then
    echo "[dev.sh] Creating buildx builder 'devbuilder' with docker-container driver..."
    docker buildx create --use --name devbuilder
else
    # If not already the current builder, switch to it
    CURRENT_BUILDER=$(docker buildx inspect --bootstrap | grep 'Name:' | awk '{print $2}')
    if [ "$CURRENT_BUILDER" != "devbuilder" ]; then
        echo "[dev.sh] Switching to buildx builder 'devbuilder'..."
        docker buildx use devbuilder
    fi
fi

# Initialize USE_GPU variable
USE_GPU="true"
NO_LOCAL_LLM="0"

# Parse command line arguments
ARGS=()
for arg in "$@"; do
    case $arg in
        --cpu-only)
            USE_GPU="false"
            ;;
        --no-local)
            USE_GPU="false"
            NO_LOCAL_LLM="1"
            ;;
        *)
            ARGS+=("$arg")
            ;;
    esac
done

# Set BACKEND_DOCKERFILE for compose builds
if [ "$NO_LOCAL_LLM" = "1" ]; then
    export BACKEND_DOCKERFILE="Dockerfile.cpu"
else
    export BACKEND_DOCKERFILE="Dockerfile.dev"
fi

# Function to clean up Docker resources
cleanup() {
    echo "Cleaning up Docker resources..."
    docker compose -f docker-compose.dev.yml down -v
    docker system prune -f
}

# Function to reset the database
reset_db() {
    echo "Resetting database..."
    docker compose -f docker-compose.dev.yml down -v
    docker volume rm sentiment-analysis_postgres_data || true
}

# Function to start development environment
start_dev() {
    echo "Starting development environment..."
    # Build using development bake file
    docker buildx bake -f docker-bake.dev.hcl --set "*.args.USE_GPU=${USE_GPU}" --set "*.args.NO_LOCAL_LLM=${NO_LOCAL_LLM}"
    # Start services
    docker compose -f docker-compose.dev.yml up
}

# Function to rebuild a specific service
rebuild_service() {
    local service=$1
    echo "Rebuilding $service..."
    # Build specific target using development bake file
    docker buildx bake -f docker-bake.dev.hcl $service --set "*.args.USE_GPU=${USE_GPU}" --set "*.args.NO_LOCAL_LLM=${NO_LOCAL_LLM}"
    # Restart the service
    docker compose -f docker-compose.dev.yml up -d --no-deps $service
}

# Function to rebuild all services
rebuild_all() {
    echo "Rebuilding all services..."
    docker buildx bake -f docker-bake.dev.hcl --set "*.args.USE_GPU=${USE_GPU}" --set "*.args.NO_LOCAL_LLM=${NO_LOCAL_LLM}"
    docker compose -f docker-compose.dev.yml up -d --build
}

# Function to show logs
show_logs() {
    local service=$1
    if [ -z "$service" ]; then
        docker compose -f docker-compose.dev.yml logs -f
    else
        docker compose -f docker-compose.dev.yml logs -f $service
    fi
}

# Function to run migrations
run_migrations() {
    echo "Running migrations..."
    docker compose -f docker-compose.dev.yml exec backend python manage.py migrate
}

# Function to auto-rebuild containers if requirements or Dockerfiles change
auto_rebuild() {
    echo "Running auto-rebuild check..."
    bash scripts/auto_rebuild.sh
}

# Main script logic
case "${ARGS[0]}" in
    "auto-rebuild")
        auto_rebuild
        ;;
    "clean")
        cleanup
        ;;
    "reset")
        reset_db
        ;;
    "start")
        auto_rebuild
        start_dev
        ;;
    "rebuild")
        if [[ "${ARGS[1]}" == "all" ]]; then
            rebuild_all
        else
            rebuild_service "${ARGS[1]}"
        fi
        ;;
    "logs")
        show_logs "${ARGS[1]}"
        ;;
    "migrate")
        run_migrations
        ;;
    *)
        echo "Usage: $0 {clean|reset|start|rebuild <service>|rebuild all|logs [service]|migrate|auto-rebuild} [--cpu-only] [--no-local]"
        echo "Options:"
        echo "  --cpu-only    Run with CPU-only mode (no GPU/model logic)"
        echo "  --no-local    Disable all local LLM/model logic (implies CPU-only)"
        echo "  auto-rebuild  Automatically rebuild containers if requirements or Dockerfiles change"
        exit 1
        ;;
esac 