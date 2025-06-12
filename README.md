# Sentiment Analysis Web Application

A web application that performs sentiment analysis on Reddit and Twitter posts using various AI models. The application features a Django backend and a React frontend.

## Features

- Sentiment analysis of Reddit and Twitter posts
- Support for multiple AI models (VADER, GPT-4, Claude, Gemini, Gemma)
- Customizable date ranges and subreddit selection
- Interactive visualizations of sentiment analysis results
- User authentication and analysis history
- RESTful API for external integration

## Tech Stack

### Backend
- Django 4.2
- Django REST Framework
- PostgreSQL
- Celery for background tasks
- Redis for caching and message broker

### Frontend
- React 18
- Material-UI
- Chart.js for visualizations
- Axios for API communication
- React Router for navigation
- @supabase/supabase-js for Supabase integration (authentication, database, or storage)

## Prerequisites

- Docker (with NVIDIA Container Toolkit for GPU support)
- Docker Compose
- (Optional for development) Python 3.11+, Node.js 18+, PostgreSQL, Redis

## Development Environment

We provide a development environment with hot reloading and optimized builds. To use it:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sentiment-analysis.git
cd sentiment-analysis
```

2. Start the development environment:
```bash
./dev.sh start
```

This will start all services in development mode with:
- Hot reloading for both frontend and backend
- Optimized builds using Docker BuildKit
- Development-specific configurations
- Automatic database migrations

### CPU-Only and No-Local-LLM Modes

The development environment supports two important flags for controlling model and GPU usage:

- `--cpu-only`: Disables all GPU logic and local model downloads. All services run in CPU mode only, and no CUDA or GPU dependencies are used. Local LLMs/models will still be loaded, but only with CPU support.
- `--no-local`: Disables all local LLM/model logic (implies `--cpu-only`). No local models are loaded or downloaded; only remote/cloud LLMs are used if configured. **When this flag is set, the backend is built using a special CPU-only Dockerfile (`Dockerfile.cpu`) that does not install any NVIDIA or CUDA dependencies.** This ensures that no GPU or local model logic is present at build or runtime, and the resulting image is fully CPU-only and cloud-LLM only.

**Example usage:**

```bash
./dev.sh --cpu-only start      # Run everything in CPU-only mode (no GPU/model logic)
./dev.sh --no-local start      # Disable all local LLM/model logic (implies CPU-only, disables all NVIDIA/CUDA at build time)
```

**Note:**
- When `--no-local` is used, the backend Docker image is built without any NVIDIA or CUDA libraries. This is enforced at the Docker build level, so the resulting image is guaranteed to be free of GPU dependencies.
- These options are propagated to all backend services and Celery workers. The backend will detect these flags and skip all GPU/model logic or local LLM/model loading as appropriate.

### Development Commands

The `dev.sh` script provides several useful commands:

```bash
./dev.sh start    # Start the development environment
./dev.sh clean    # Clean up Docker resources
./dev.sh reset    # Reset the database and run migrations
./dev.sh migrate  # Run database migrations
./dev.sh rebuild <service>  # Rebuild a specific service (frontend, backend, celery)
./dev.sh logs <service>     # Show logs for a specific service
./dev.sh --cpu-only start   # Start in CPU-only mode
./dev.sh --no-local start   # Start with all local LLM/model logic disabled
```

### Development URLs

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Admin interface: http://localhost:8000/admin

## Backend Docker Multi-Stage Build (Production & Development)

The backend now uses a multi-stage Docker build for smaller, more secure images and faster builds.

### Build and Run (Development)

```bash
docker compose up --build
```

- Uses `docker-compose.yml` and `docker-compose.dev.yml` for local development.
- Hot-reloading and dev dependencies are included.

### Build and Run (Production)

```bash
docker build -t sentiment-backend:prod -f backend/Dockerfile ./backend
# Run with production compose or directly:
docker run -d -p 8000:8000 sentiment-backend:prod
```

- The production image is minimal, only includes runtime dependencies.
- Healthcheck is included in the Dockerfile and docker-compose for backend service.

### Healthcheck
- The backend container exposes a healthcheck endpoint for Docker orchestration.
- Docker will restart the container if the healthcheck fails.

## API Documentation

The backend uses **drf-spectacular** for OpenAPI 3.0 schema generation. 

- **Swagger UI:** http://localhost:8000/swagger/
- **Redoc UI:** http://localhost:8000/redoc/
- **OpenAPI JSON:** http://localhost:8000/schema/

> **Note:** These documentation endpoints are only available in development/DEBUG mode for security and compatibility. In production, only the API endpoints are exposed.

### Main Endpoints

- `POST /api-token-auth/` - Obtain API token
- `GET /api/analyses/` - List all analyses
- `POST /api/analyses/` - Create new analysis
- `GET /api/analyses/{id}/` - Get analysis details
- `GET /api/analyses/{id}/results/` - Get analysis results
- `GET /api/analyses/{id}/summary/` - Get analysis summary
- `GET /api/analyses/gemma-status/` - Check Gemma model status

## Backend Testing & Quality

- All backend endpoints and features are covered by tests using **pytest** and **pytest-django**.
- Run all backend tests with:
  ```bash
  docker compose exec backend pytest sentiment_analysis/test_sentiment_analysis.py -v
  ```
- Logging is structured (JSON) and includes request/task IDs for traceability.
- Sentry integration is enabled for error monitoring (set `SENTRY_DSN` in `.env`).
- Django Debug Toolbar is available in dev for SQL/profiling at `/__debug__/`.
- Caching is used for LLM results and summaries for performance.
- All packages are regularly checked for minimalism and compatibility.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Setup & Dependency Management

### Installing Dependencies

All backend dependencies are managed in `backend/requirements.txt`.

To install all required Python packages for backend development, run:

```bash
pip install -r backend/requirements.txt
```

### Development Dependencies

For frontend development:
```bash
cd frontend
npm install
```

> Note: The frontend now requires `@supabase/supabase-js` for Supabase integration. This package is already listed in `package.json` and will be installed automatically.

### Keeping Dependencies Up to Date

- **When you add or update a package:**
  1. Install it with pip (e.g., `pip install newpackage`).
  2. Update `requirements.txt` with:
     ```bash
     pip freeze > requirements.txt
     ```
- **For new environments or deployments:**
  - Always use `pip install -r requirements.txt` to ensure consistency.

### Notes
- If you use a virtual environment, activate it before installing dependencies.
- If you encounter missing packages, add them to `requirements.txt` and repeat the above steps.
- For development, use the `dev.sh` script to manage the development environment.

## Frontend (Vite) Migration Notes

- The frontend now uses [Vite](https://vitejs.dev/) for development and builds. All previous Create React App scripts have been replaced.
- The `index.html` file **must be in the `frontend/` root** (not in `public/`).
- All environment variables used in the frontend **must be prefixed with `VITE_`** (e.g., `VITE_API_URL`). Place them in `frontend/.env`.
- The default API URL is `http://localhost:8000/api` unless overridden by `VITE_API_URL`.
- To run the frontend in Docker, the dev server is started automatically. For local dev, use `npm run dev` in the `frontend/` directory.

## Nginx SSL/HTTPS Setup

Nginx now supports HTTPS with automatic HTTP-to-HTTPS redirection.

### Local Development (Self-Signed Certificates)
1. Generate a self-signed certificate:
   ```bash
   mkdir -p nginx/certs
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -keyout nginx/certs/server.key \
     -out nginx/certs/server.crt \
     -subj "/CN=localhost"
   ```
2. The Docker Compose setup will mount `nginx/certs` into the container.

### Production
- Replace `nginx/certs/server.crt` and `server.key` with your real SSL certificate and key.
- Update the Nginx config if your domain or certificate paths differ.

### HTTPS Access
- The app is now accessible at `https://localhost:8080` (or your configured port).
- All HTTP requests are redirected to HTTPS automatically.

## Health Checks & Monitoring

### API Health Check Endpoint
- The backend exposes a health check at `/api/analyses/health/`.
- Checks database and Redis/Celery connectivity.
- Returns 200 and `{ "status": "healthy" }` if all services are up.
- Returns 503 and `{ "status": "unhealthy" }` if any check fails.
- All failures are logged for debugging.

#### Example:
```bash
curl -i https://localhost:8080/api/analyses/health/
```

### Docker Compose Healthchecks
- **Backend:** Docker Compose pings `/api/analyses/health/` to ensure the backend is healthy.
- **Database:** Uses `pg_isready` to check Postgres health.
- **Redis:** Uses `redis-cli ping` to check Redis health.
- **Celery:** Uses `celery -A sentiment_analysis status` for worker health.

### Extending Monitoring
- Timing decorators log duration of key operations.
- For advanced monitoring, consider adding Prometheus metrics or integrating with Grafana, ELK, or other external tools.

## Troubleshooting: Docker Buildx on Arch Linux and Debian/Ubuntu (use context7)

If you encounter errors like `exec format error` or `buildx: command not found` when using Docker Buildx, follow these steps:

1. **Remove any broken or mismatched buildx binaries:**
   ```sh
   sudo rm -f ~/.docker/cli-plugins/docker-buildx
   ```
2. **Install the official docker-buildx package:**
   - **Arch Linux:**
     ```sh
     paru -S docker-buildx --noconfirm
     # or use pacman if you don't use an AUR helper:
     sudo pacman -S docker-buildx
     ```
   - **Debian/Ubuntu (apt-based distros):**
     ```sh
     sudo apt-get update
     sudo apt-get install docker-buildx-plugin
     ```
3. **Verify installation:**
   ```sh
   docker buildx version
   ```
   You should see a version string, not an error.

This is required for advanced Docker workflows, multi-arch builds, and for development scripts that use Buildx features.