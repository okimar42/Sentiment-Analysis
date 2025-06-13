# Background Agent Task: Extract Webapp Data Processing into Standalone Scripts

## Mission
Your task is to **extract and replicate** the existing data processing workflows from the Django/FastAPI webapp into **standalone, automatable Python scripts** that can run independently of the web application. These scripts should perform the exact same data processing operations but be suitable for automation, scheduling, and integration into other systems.

## Current Webapp Analysis Summary

Based on the codebase exploration, the webapp currently processes:

### Data Sources
- **Reddit**: Fetches posts from subreddits using PRAW library
- **Twitter**: Processes tweets (implementation in `tasks/twitter.py`)

### Core Processing Pipeline
1. **Data Extraction**: Fetch posts/tweets with metadata
2. **Content Filtering**: Skip emoji-heavy content, ads, etc.
3. **Sentiment Analysis**: Multiple models (VADER, GPT-4, Claude, Gemini, Gemma)
4. **Advanced Analysis**: Bot detection, IQ estimation, sarcasm detection  
5. **Image Processing**: Vision model analysis for posts with images
6. **Data Storage**: Structured storage with comprehensive metadata
7. **Analytics**: Summary statistics, time-series analysis, distributions

### Current Database Schema (Key Models)
```python
# From models.py - replicate this structure
class SentimentAnalysis:
    - query, source, model, selected_llms
    - subreddits, start_date, end_date, status
    - user, include_images, content_summary

class SentimentResult:
    - post_id, content, score, compound_score
    - vader_score, gpt4_score, claude_score, gemini_score, grok_score
    - sarcasm_score, perceived_iq, bot_probability
    - manual_override fields, source_metadata
    - post_date, has_images, is_ad, source_type

class ImageSentimentResult:
    - image_url, image_description, score
    - gpt4_vision_score, claude_vision_score, gemini_vision_score
```

## Required Script Architecture

### 1. Core Processor Script (`sentiment_processor.py`)
Create a main processor that replicates the webapp's functionality:

```python
#!/usr/bin/env python3
"""
Standalone Sentiment Analysis Processor
Replicates webapp functionality for automated execution
"""

import click
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json
import csv
from datetime import datetime, timedelta

@dataclass
class ProcessingConfig:
    """Configuration matching webapp's SentimentAnalysis model"""
    query: str  # Search terms or subreddits
    sources: List[str]  # ['reddit', 'twitter']
    models: List[str]  # ['vader', 'gpt4', 'claude', 'gemini', 'gemma']
    start_date: datetime
    end_date: datetime
    include_images: bool = False
    max_posts: int = 100
    output_format: str = 'json'  # 'json', 'csv', 'sqlite'
    output_path: str = 'results'

@click.command()
@click.option('--config', '-c', help='JSON config file path')
@click.option('--query', '-q', help='Search query or subreddits (comma-separated)')
@click.option('--sources', help='Data sources: reddit,twitter')
@click.option('--models', help='Models: vader,gpt4,claude,gemini,gemma')
@click.option('--days-back', type=int, default=7, help='Days of data to analyze')
@click.option('--max-posts', type=int, default=100, help='Max posts per source')
@click.option('--output-format', type=click.Choice(['json', 'csv', 'sqlite']), default='json')
@click.option('--output-path', default='./results', help='Output directory/file path')
@click.option('--include-images', is_flag=True, help='Include image analysis')
@click.option('--dry-run', is_flag=True, help='Show what would be processed without executing')
def main(...):
    """Main entry point - replicate webapp's analyze_reddit_sentiment/analyze_twitter_sentiment"""
    pass
```

### 2. Data Source Modules

#### Reddit Processor (`sources/reddit_processor.py`)
Extract and enhance the logic from `tasks/reddit.py`:
- **Exact replication**: Use same PRAW configuration, post filtering, metadata extraction
- **Enhanced configuration**: Support multiple subreddits, time ranges, post limits
- **Standalone operation**: No Django dependencies, direct data return
- **Error handling**: Robust retry logic, rate limiting respect

#### Twitter Processor (`sources/twitter_processor.py`) 
Extract from `tasks/twitter.py`:
- **API integration**: Twitter API v2 or scraping methods used in webapp
- **Data normalization**: Match the same metadata structure as Reddit
- **Rate limiting**: Respect Twitter API constraints
- **Content filtering**: Same logic as webapp (emoji detection, spam filtering)

### 3. Analysis Engine (`analysis/sentiment_engine.py`)
Replicate the exact sentiment analysis pipeline:

```python
class SentimentEngine:
    """Replicate webapp's multi-model sentiment analysis"""
    
    def __init__(self, models: List[str]):
        # Initialize all requested models (VADER, LLMs)
        pass
    
    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """Process batch of texts through all models"""
        # Replicate exact scoring logic from webapp
        pass
    
    def analyze_with_vader(self, text: str) -> float:
        """Exact copy from utils/sentiment.py"""
        pass
    
    def analyze_with_llm(self, text: str, model: str) -> float:
        """Replicate LLM analysis from image_tasks.py and model_utils/"""
        pass
    
    def detect_sarcasm(self, text: str) -> Dict:
        """Extract sarcasm detection logic from webapp"""
        pass
    
    def estimate_iq(self, text: str, sentiment: float) -> float:
        """Replicate IQ estimation: 70 + (sentiment * 30)"""
        pass
    
    def detect_bot(self, text: str, metadata: Dict) -> Dict:
        """Extract bot detection logic from webapp"""
        pass
```

### 4. Image Analysis Module (`analysis/image_analyzer.py`)
Extract image processing from `image_tasks.py`:
- **Vision models**: GPT-4 Vision, Claude Vision, Gemini Vision
- **Image extraction**: From post URLs, same logic as webapp
- **Batch processing**: Efficient handling of multiple images
- **Results structure**: Match `ImageSentimentResult` model

### 5. Output Handlers (`output/`)
Create multiple output formats:

#### JSON Output (`output/json_writer.py`)
```python
def save_analysis_json(results: List[Dict], summary: Dict, filepath: str):
    """Save in webapp-compatible JSON format"""
    output = {
        "analysis_summary": summary,
        "results": results,
        "metadata": {
            "processed_at": datetime.now().isoformat(),
            "total_posts": len(results),
            "models_used": [...],
            "sources": [...]
        }
    }
```

#### CSV Export (`output/csv_writer.py`)
Replicate the exact CSV export from webapp's `export_csv` endpoint

#### SQLite Storage (`output/sqlite_writer.py`)
Create local SQLite database with same schema as Django models

### 6. Configuration System (`config/`)
- **Environment**: Load API keys, model endpoints
- **Profiles**: Predefined analysis configurations
- **Validation**: Ensure all required credentials/models available

## Critical Requirements

### 1. Exact Functional Replication
- **Same algorithms**: Use identical sentiment scoring, filtering, and analysis logic
- **Same data structure**: Results must match webapp's model fields exactly
- **Same metadata**: Preserve all source_metadata, timestamps, scores
- **Same filtering**: Emoji detection, ad filtering, content validation

### 2. Standalone Operation
- **No Django dependencies**: Pure Python with minimal external requirements
- **Configuration-driven**: All webapp settings via config files/CLI args
- **Self-contained**: Include all utility functions inline or as modules
- **Docker compatible**: Must run in containers just like webapp

### 3. Production Readiness
- **Error recovery**: Handle API failures, network issues, rate limits
- **Logging**: Structured logging matching webapp's logger usage
- **Monitoring**: Health checks, progress reporting, metrics collection
- **Scalability**: Batch processing, memory management for large datasets

### 4. Output Compatibility
- **Data format**: Results readable by webapp if needed
- **Schema matching**: JSON/CSV exports identical to webapp endpoints
- **Import capability**: Results importable back into webapp database
- **Analytics ready**: Include same summary calculations as webapp

## Implementation Tasks

### Phase 1: Core Extraction
1. **Copy utility functions**: `utils/sentiment.py`, text processing, decorators
2. **Extract Reddit logic**: Replicate `tasks/reddit.py` as standalone function
3. **Extract Twitter logic**: Port `tasks/twitter.py` completely
4. **Create data models**: Python dataclasses matching Django models

### Phase 2: Analysis Pipeline
1. **Sentiment engine**: Combine all model integrations from webapp
2. **Image processing**: Port image analysis capabilities
3. **Batch processing**: Optimize for non-web execution
4. **Results calculation**: Copy summary/analytics functions from `views.py`

### Phase 3: I/O & Integration
1. **Configuration system**: Support all webapp configuration options
2. **Output formats**: JSON, CSV, SQLite matching webapp exports  
3. **CLI interface**: Comprehensive command-line tool
4. **Documentation**: Usage examples, configuration reference

### Phase 4: Automation Features
1. **Scheduling support**: Cron-compatible execution
2. **Incremental processing**: Track processed content, avoid duplicates
3. **Monitoring integration**: Prometheus metrics, health endpoints
4. **Error alerting**: Notification system for failures

## Success Criteria

### Functional Verification
- [ ] Process same Reddit data as webapp with identical results
- [ ] Support all sentiment models used in webapp (VADER, GPT-4, Claude, etc.)
- [ ] Generate identical summary statistics as webapp endpoints
- [ ] Handle image analysis with same accuracy as webapp
- [ ] Export CSV/JSON matching webapp's export format exactly

### Performance Targets
- [ ] Process 1000+ posts in under 5 minutes
- [ ] Handle rate limiting gracefully without failures
- [ ] Use <2GB memory for typical analysis batches
- [ ] Support concurrent processing of multiple sources

### Operational Requirements
- [ ] Run reliably in Docker containers
- [ ] Resume processing after interruption
- [ ] Provide progress feedback for long-running analyses
- [ ] Generate comprehensive logs for debugging
- [ ] Support configuration via environment variables

## Output Deliverables

### Script Structure
```
scripts/data_processing/
├── sentiment_processor.py          # Main CLI tool
├── sources/
│   ├── reddit_processor.py        # Reddit data extraction
│   ├── twitter_processor.py       # Twitter data extraction
│   └── base_processor.py          # Common source functionality
├── analysis/
│   ├── sentiment_engine.py        # Multi-model sentiment analysis
│   ├── image_analyzer.py          # Image processing
│   └── batch_processor.py         # Batch processing optimization
├── output/
│   ├── json_writer.py             # JSON output format
│   ├── csv_writer.py              # CSV export matching webapp
│   └── sqlite_writer.py           # Local database storage
├── config/
│   ├── settings.py                # Configuration management
│   ├── models.py                  # Data structure definitions
│   └── validation.py              # Input validation
├── utils/
│   ├── logging_setup.py           # Structured logging
│   ├── error_handling.py          # Retry logic, exception handling
│   └── api_clients.py             # External API wrappers
└── README.md                      # Comprehensive usage guide
```

### Documentation Requirements
- **README.md**: Installation, configuration, usage examples
- **API.md**: Detailed parameter reference, output formats
- **DEPLOYMENT.md**: Docker setup, automation examples
- **TROUBLESHOOTING.md**: Common issues, debugging guide

### Testing Suite
- **Unit tests**: All processing functions with real/mock data
- **Integration tests**: End-to-end processing with live APIs
- **Performance tests**: Memory usage, processing speed benchmarks
- **Compatibility tests**: Verify output matches webapp exactly

Remember: The goal is to create production-ready scripts that can completely replace the webapp for data processing tasks while maintaining 100% functional compatibility with the existing system. 