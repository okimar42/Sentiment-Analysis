# Sentiment Analysis Web Application

[![CI](https://github.com/yourusername/sentiment-analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/sentiment-analysis/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/yourusername/sentiment-analysis/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/sentiment-analysis)

A web application that performs sentiment analysis on Reddit and Twitter posts using various AI models. The application features a Django backend and a React frontend with comprehensive testing, AI-powered development workflows, and advanced deployment capabilities.

## Features

- Sentiment analysis of Reddit and Twitter posts
- Support for multiple AI models (VADER, GPT-4, Claude, Gemini, Gemma, Mistral, xAI, Azure OpenAI, Ollama)
- Customizable date ranges and subreddit selection
- Interactive visualizations of sentiment analysis results
- User authentication and analysis history
- RESTful API for external integration
- Comprehensive test coverage with automated testing
- AI-powered development workflow with Taskmaster integration
- Advanced Docker build system with caching and multi-platform support

## Tech Stack

### Backend
- Django 5.0.2
- Django REST Framework
- PostgreSQL
- Celery for background tasks
- Redis for caching and message broker
- Multiple ML/AI libraries (HuggingFace, Transformers, PyTorch)
- Comprehensive testing with pytest and pytest-django

### Frontend
- React 18 with TypeScript
- Vite for build tooling and development server
- Material-UI (@mui/material, @mui/icons-material, @mui/x-date-pickers)
- Chart.js and Recharts for visualizations
- Axios for API communication
- React Router for navigation
- @supabase/supabase-js for Supabase integration (authentication, database, or storage)
- Comprehensive testing with Vitest, Jest, and React Testing Library
- ESLint for code quality
- date-fns for date manipulation
- **Multi-theme system with persistent, context-based theme picker.**
  - See `frontend/README.md` for details on adding/extending themes and usage.

## Prerequisites

- Docker (with NVIDIA Container Toolkit for GPU support)
- Docker Compose
- (Optional for development) Python 3.11+, Node.js 18+, PostgreSQL, Redis

## Development Environment

We provide a development environment with hot reloading, optimized builds, and intelligent auto-rebuilding. To use it:

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
- Optimized builds using Docker BuildKit with cache management
- Development-specific configurations
- Automatic database migrations
- Intelligent auto-rebuilding when dependencies change

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
./dev.sh start              # Start the development environment
./dev.sh clean              # Clean up Docker resources
./dev.sh reset              # Reset the database and run migrations
./dev.sh migrate            # Run database migrations
./dev.sh rebuild <service>  # Rebuild a specific service (frontend, backend, celery)
./dev.sh rebuild all        # Rebuild all services
./dev.sh logs <service>     # Show logs for a specific service
./dev.sh auto-rebuild       # Automatically rebuild containers if requirements or Dockerfiles change
./dev.sh --cpu-only start   # Start in CPU-only mode
./dev.sh --no-local start   # Start with all local LLM/model logic disabled
```

### Development URLs

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Admin interface: http://localhost:8000/admin

## Backend Docker Multi-Stage Build (Production & Development)

The backend uses a sophisticated multi-stage Docker build system with multiple Dockerfile variants for different use cases:

- `Dockerfile` - Production build with GPU support
- `Dockerfile.dev` - Development build with hot reloading
- `Dockerfile.cpu` - CPU-only build without NVIDIA dependencies

### Advanced Build System with Docker Bake

The project uses Docker Bake for advanced multi-service builds with caching:

```bash
# Development builds with caching
docker buildx bake -f docker-bake.dev.hcl

# Production builds  
docker buildx bake -f docker-bake.hcl

# CPU-only builds
docker buildx bake -f docker-bake.dev.hcl --set "*.args.USE_GPU=false"
```

### Build and Run (Development)

```bash
docker compose up --build
```

- Uses `docker-compose.yml` and `docker-compose.dev.yml` for local development.
- Hot-reloading and dev dependencies are included.
- Intelligent cache management and auto-rebuilding

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

## Testing & Quality Assurance

### Backend Testing
- All backend endpoints and features are covered by tests using **pytest** and **pytest-django**.
- Run all backend tests with:
  ```bash
  docker compose exec backend pytest sentiment_analysis/test_sentiment_analysis.py -v
  ```
- Test analysis utility available: `python analyze_tests.py`

### Frontend Testing
- Comprehensive testing setup with **Vitest**, **Jest**, and **React Testing Library**
- TypeScript support with strict type checking
- ESLint for code quality and consistency
- Run frontend tests with:
  ```bash
  cd frontend
  npm test        # Run tests with Vitest
  npm run lint    # Run ESLint
  npm run lint:fix # Fix ESLint issues automatically
  ```

### Testing Configuration
- **Backend**: `pytest.ini` configuration
- **Frontend**: `vitest.config.ts`, `tsconfig.*.json` for TypeScript
- **Code Quality**: ESLint configuration in `eslint.config.js`

### Quality Assurance Features
- Logging is structured (JSON) and includes request/task IDs for traceability.
- Sentry integration is enabled for error monitoring (set `SENTRY_DSN` in `.env`).
- Django Debug Toolbar is available in dev for SQL/profiling at `/__debug__/`.
- Caching is used for LLM results and summaries for performance.
- All packages are regularly checked for minimalism and compatibility.

## AI Model Support & Configuration

### Supported AI Providers
The application supports multiple AI providers through API integration:

- **OpenAI**: GPT-4, GPT-3.5-turbo models
- **Anthropic**: Claude models  
- **Google**: Gemini models
- **Mistral AI**: Mistral models
- **xAI**: Grok models
- **Azure OpenAI**: Enterprise OpenAI models
- **Ollama**: Local and remote Ollama servers
- **HuggingFace**: Local transformer models

### Environment Variables for AI Models
Configure AI providers by setting the appropriate API keys in your `.env` file:

```bash
# Required for core functionality
ANTHROPIC_API_KEY="sk-ant-api03-..."

# Optional providers
OPENAI_API_KEY="sk-proj-..."
GOOGLE_API_KEY="your_google_api_key_here"
MISTRAL_API_KEY="your_mistral_key_here"
XAI_API_KEY="YOUR_XAI_KEY_HERE"
AZURE_OPENAI_API_KEY="your_azure_key_here"
OLLAMA_API_KEY="your_ollama_api_key_here"  # For authenticated Ollama servers
PERPLEXITY_API_KEY="pplx-..."
```

## Taskmaster AI-Powered Development Workflow

This project integrates with **Taskmaster**, an AI-powered development workflow system that provides:

- Intelligent task breakdown and management
- AI-assisted code generation and refactoring
- Automated dependency analysis
- Project status tracking and reporting

### Taskmaster Configuration
The `.taskmasterconfig` file defines AI models and settings:

```json
{
  "models": {
    "main": { "provider": "openai", "modelId": "gpt-4o" },
    "research": { "provider": "perplexity", "modelId": "sonar-pro" },
    "fallback": { "provider": "anthropic", "modelId": "claude-3-5-sonnet-20240620" }
  },
  "global": {
    "projectName": "Taskmaster",
    "defaultSubtasks": 5,
    "logLevel": "info"
  }
}
```

### Using Taskmaster
Taskmaster commands are available for project management and AI assistance. Refer to the Taskmaster documentation for specific commands and workflows.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Ensure all tests pass (`npm test` for frontend, `pytest` for backend)
5. Run linting (`npm run lint:fix` for frontend)
6. Commit your changes
7. Push to the branch
8. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Setup & Dependency Management

### Installing Dependencies

All backend dependencies are managed in `backend/requirements.txt` with additional variants:
- `requirements.txt` - Full dependencies with GPU support
- `requirements-cpu.txt` - CPU-only dependencies
- `requirements-dev.txt` - Additional development dependencies

#### Core Backend Dependencies
```bash
# Core Framework
Django==5.0.2
djangorestframework==3.14.0
psycopg2-binary==2.9.9

# AI/ML Libraries
torch>=2.2.0                    # PyTorch for deep learning
transformers>=4.41.0            # HuggingFace transformers
huggingface-hub>=0.20.3         # HuggingFace model hub
accelerate>=0.27.2              # Training acceleration
bitsandbytes>=0.41.1            # Model quantization
safetensors>=0.4.1              # Safe tensor format
sentencepiece>=0.1.99           # Text tokenization
einops>=0.7.0                   # Tensor operations

# Analysis Tools
vaderSentiment==3.3.2           # VADER sentiment analysis
nltk==3.8.1                     # Natural language processing
emoji==2.10.1                   # Emoji processing

# API Clients
openai>=1.57.0                  # OpenAI API
google-generativeai==0.3.2     # Google Gemini API
praw==7.8.1                     # Reddit API
tweepy==4.14.0                  # Twitter API

# Task Queue & Caching
celery==5.3.6                   # Background tasks
redis==5.0.1                    # Caching and message broker

# Additional Tools
python-json-logger             # Structured logging
django-debug-toolbar           # Development debugging
drf-spectacular[sidecar]       # API documentation
sentry-sdk                     # Error monitoring
```

To install all required Python packages for backend development, run:

```bash
pip install -r backend/requirements.txt
```

### Frontend Dependencies

#### Core Frontend Dependencies
```bash
# Core Framework
react@^18.2.0                    # React framework
typescript@^5.8.3                # TypeScript support

# Build Tools
vite@^6.3.5                      # Build tool and dev server
@vitejs/plugin-react@^4.2.1      # Vite React plugin

# UI Framework
@mui/material@^5.15.10           # Material-UI components
@mui/icons-material@^5.15.10     # Material-UI icons
@mui/x-date-pickers@^5.0.20      # Material-UI date pickers
@emotion/react@^11.11.3          # CSS-in-JS styling
@emotion/styled@^11.11.0         # Styled components

# Charts & Visualization
chart.js@^4.4.9                  # Chart.js charting library
react-chartjs-2@^5.3.0           # React wrapper for Chart.js
recharts@^2.12.0                 # Alternative charting library

# Utilities
axios@^1.9.0                     # HTTP client
react-router-dom@^6.22.1         # Routing
date-fns@^2.30.0                 # Date manipulation
@supabase/supabase-js@^2.39.7    # Supabase integration

# Testing
vitest@^3.1.4                    # Test runner
@testing-library/react@^16.3.0   # React testing utilities
@testing-library/jest-dom@^6.6.3 # Jest DOM matchers
@testing-library/user-event@^14.6.1 # User interaction testing
jsdom@^26.1.0                    # DOM environment for testing

# Code Quality
eslint@^9.15.0                   # Code linting
typescript-eslint@^8.18.2        # TypeScript ESLint rules
```

For frontend development:
```bash
cd frontend
npm install
```

> Note: The frontend requires Node.js 18+ and includes comprehensive TypeScript and testing configuration.

### Development Dependencies

#### TypeScript Configuration
- `tsconfig.json` - Base TypeScript configuration
- `tsconfig.app.json` - Application-specific settings  
- `tsconfig.node.json` - Node.js-specific settings

#### Testing Configuration
- `vitest.config.ts` - Vitest test runner configuration
- `setupTests.js` - Test environment setup
- Global test timeout: 10 seconds
- JSDOM environment for DOM testing

### Keeping Dependencies Up to Date

- **When you add or update a backend package:**
  1. Install it with pip (e.g., `pip install newpackage`).
  2. Update `requirements.txt` with:
     ```bash
     pip freeze > requirements.txt
     ```

- **When you add or update a frontend package:**
  ```bash
  cd frontend
  npm install <package-name>
  # package.json and package-lock.json are automatically updated
  ```

- **For new environments or deployments:**
  - Always use `pip install -r backend/requirements.txt` for backend
  - Always use `npm install` in the frontend directory

### Notes
- If you use a virtual environment, activate it before installing backend dependencies.
- For development, use the `dev.sh` script to manage the development environment.
- The project includes auto-rebuild functionality that detects dependency changes.

## Frontend (Vite) Migration Notes

- The frontend uses [Vite](https://vitejs.dev/) for development and builds with TypeScript support.
- The `index.html` file **must be in the `frontend/` root** (not in `public/`).
- All environment variables used in the frontend **must be prefixed with `VITE_`** (e.g., `VITE_API_URL`). Place them in `frontend/.env`.
- The default API URL is `http://localhost:8000/api` unless overridden by `VITE_API_URL`.
- Vite configuration includes proxy setup to nginx for API requests.
- TypeScript is fully configured with strict type checking.

### Vite Configuration Features
- **Development server**: Runs on `0.0.0.0:3000` with hot reloading
- **API Proxy**: Automatically proxies `/api` requests to nginx
- **HTTPS**: Disabled in Vite (nginx handles HTTPS termination)
- **Preview mode**: Available for testing production builds

## Nginx SSL/HTTPS Setup

Nginx supports HTTPS with automatic HTTP-to-HTTPS redirection and advanced configuration.

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
- The app is accessible at `https://localhost:8080` (or your configured port).
- All HTTP requests are redirected to HTTPS automatically.
- Nginx configurations available:
  - `nginx.conf` - Production configuration
  - `nginx.dev.conf` - Development configuration

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
- Structured logging with JSON format and request/task IDs.
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

## CI/CD

- Automated tests and linting run on every push via GitHub Actions.
- Code coverage is reported for both backend (pytest-cov) and frontend (Jest) and uploaded to Codecov.