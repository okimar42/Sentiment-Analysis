# Cursor Background Agent Instructions - 5 Agent Parallel Development

## Overview
These instructions are designed for Cursor's background agent system. Each agent will work independently in their own branch and directory to avoid conflicts.

---

# Agent 1: Social Media Data Pipeline Specialist

## Initial Setup
```bash
cd /workspace
git checkout -b agent1-data-pipeline
mkdir -p backend/data_pipeline
cd backend/data_pipeline
```

## Your Mission
Build a complete social media data ingestion pipeline that feeds real-time data to other services.

## Week 1-2 Tasks

### 1. Create Pipeline Architecture
Create `/workspace/backend/data_pipeline/architecture.py`:
```python
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class UnifiedSentimentData:
    """Standard format for all social media data"""
    id: str
    platform: str  # reddit, twitter, stocktwits, discord, tiktok
    ticker: Optional[str]
    content: str
    author: str
    timestamp: datetime
    engagement: Dict  # likes, shares, comments, etc
    metadata: Dict  # platform-specific data
    
    def to_json(self):
        """Convert to JSON for Kafka/Redis"""
        pass
```

### 2. Set Up Kafka Infrastructure
Create `/workspace/backend/data_pipeline/kafka_setup.py`:
- Topic: `sentiment-raw-feed`
- Topic: `sentiment-processed`
- Topic: `sentiment-alerts`

### 3. Reddit Integration
Create `/workspace/backend/data_pipeline/reddit_ingestion.py`:
```python
import praw
from typing import List
import asyncio

class RedditPipeline:
    SUBREDDITS = [
        'wallstreetbets', 'stocks', 'investing', 'stockmarket',
        'options', 'daytrading', 'pennystocks', 'cryptocurrency',
        'thetagang', 'valueinvesting', 'dividends', 'securityanalysis'
    ]
    
    def __init__(self):
        # Initialize PRAW
        pass
    
    async def stream_comments(self):
        """Stream real-time comments"""
        pass
    
    async def stream_posts(self):
        """Stream new posts"""
        pass
    
    def extract_tickers(self, text: str) -> List[str]:
        """Extract stock tickers from text"""
        pass
    
    def detect_dd_quality(self, post) -> float:
        """Score DD (Due Diligence) posts"""
        pass
```

### 4. Multi-Platform Manager
Create `/workspace/backend/data_pipeline/platform_manager.py`:
- Twitter/X streaming
- StockTwits API integration
- Discord webhook listener
- TikTok scraper (if needed)

### 5. Data Quality Service
Create `/workspace/backend/data_pipeline/data_quality.py`:
- Deduplication
- Rate limit management
- Data validation
- Quality metrics

## Deliverables by End of Week 2
1. **API Contract**: `/workspace/contracts/data_pipeline_api.yaml`
2. **Sample Data**: `/workspace/sample_data/unified_format.json`
3. **Kafka Topics**: Created and documented
4. **Basic Reddit Stream**: Working prototype

## Week 3-12 Continuation
- Complete all platform integrations
- Optimize for 10M+ posts/day
- Build monitoring dashboard
- Create data quality reports

## Testing Your Pipeline
```bash
# Test Reddit stream
python -m data_pipeline.reddit_ingestion --test

# Test Kafka producer
python -m data_pipeline.kafka_producer --test

# Monitor data flow
python -m data_pipeline.monitor
```

---

# Agent 2: Mobile App Developer

## Initial Setup
```bash
cd /workspace
git checkout -b agent2-mobile-app
mkdir -p mobile
cd mobile
npx react-native init SentimentTrader --template react-native-template-typescript
```

## Your Mission
Build iOS and Android apps with offline-first architecture and beautiful UX.

## Week 1-2 Tasks

### 1. Project Structure
```
/workspace/mobile/SentimentTrader/
├── src/
│   ├── components/
│   │   ├── SentimentGauge.tsx
│   │   ├── StockCard.tsx
│   │   ├── TrendingList.tsx
│   │   └── MarketMoodRing.tsx
│   ├── screens/
│   │   ├── DashboardScreen.tsx
│   │   ├── StockDetailScreen.tsx
│   │   ├── AlertsScreen.tsx
│   │   └── ScreenerScreen.tsx
│   ├── services/
│   │   ├── api.ts         # Mock API for now
│   │   ├── storage.ts     # Offline storage
│   │   └── notifications.ts
│   ├── store/
│   │   └── sentimentSlice.ts
│   └── utils/
│       └── mockData.ts
```

### 2. Mock Data Service
Create `/workspace/mobile/SentimentTrader/src/utils/mockData.ts`:
```typescript
export const mockTrendingStocks = [
  {
    ticker: 'GME',
    name: 'GameStop',
    sentiment: 0.85,
    momentum: 150,
    platforms: ['reddit', 'twitter'],
    change24h: 45,
    volume: '10.2M'
  },
  // Add 20+ mock stocks
];

export const mockWatchlist = [
  // User's watchlist items
];

export const mockAlerts = [
  // Sample alerts
];
```

### 3. Core Components
Create these components with mock data:
- `SentimentGauge`: Visual sentiment indicator (0-100)
- `StockCard`: Swipeable card with sentiment info
- `TrendingList`: Scrollable list of trending stocks
- `MarketMoodRing`: Overall market sentiment

### 4. Main Dashboard
Create `/workspace/mobile/SentimentTrader/src/screens/DashboardScreen.tsx`:
- Pull-to-refresh
- Trending stocks section
- Watchlist section
- Quick actions (search, scan, alerts)

### 5. Push Notifications Setup
```bash
# iOS
cd ios && pod install

# Configure Firebase
npm install @react-native-firebase/app @react-native-firebase/messaging
```

## Deliverables by End of Week 2
1. **Running App**: Basic navigation working
2. **Mock Screens**: All main screens with mock data
3. **Component Library**: Reusable UI components
4. **Design System**: Colors, fonts, spacing defined

## Week 3-12 Continuation
- Integrate real APIs (when ready)
- Implement offline sync
- Add gamification
- Polish animations
- App store preparation

---

# Agent 3: ML & Sentiment Analysis Expert

## Initial Setup
```bash
cd /workspace
git checkout -b agent3-ml-models
mkdir -p ml/sentiment_models
cd ml/sentiment_models
```

## Your Mission
Build state-of-the-art sentiment models optimized for retail trader language.

## Week 1-2 Tasks

### 1. Model Architecture
Create `/workspace/ml/sentiment_models/architectures.py`:
```python
import torch
from transformers import AutoModel, AutoTokenizer

class WSBSentimentModel(torch.nn.Module):
    """Fine-tuned model for WSB/retail trader language"""
    
    def __init__(self):
        super().__init__()
        self.base_model = AutoModel.from_pretrained('ProsusAI/finbert')
        self.classifier = torch.nn.Sequential(
            torch.nn.Linear(768, 256),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.1),
            torch.nn.Linear(256, 3)  # Positive, Negative, Neutral
        )
    
    def forward(self, input_ids, attention_mask):
        outputs = self.base_model(input_ids, attention_mask)
        pooled = outputs.last_hidden_state.mean(dim=1)
        return self.classifier(pooled)

class MemeStockDetector(torch.nn.Module):
    """Detect meme stock potential"""
    pass

class FOMOIndicator(torch.nn.Module):
    """Measure FOMO levels in text"""
    pass
```

### 2. Training Data Preparation
Create `/workspace/ml/sentiment_models/data_prep.py`:
```python
# Use historical data from existing system
# Augment with WSB-specific language
# Create labeled dataset for:
# - General sentiment
# - Sarcasm detection
# - Position extraction
# - FOMO/hype detection
```

### 3. Model Training Pipeline
Create `/workspace/ml/sentiment_models/train.py`:
```python
def train_wsb_sentiment():
    """Train WSB-specific sentiment model"""
    pass

def train_sarcasm_detector():
    """Train sarcasm detection model"""
    pass

def train_momentum_predictor():
    """Train sentiment momentum model"""
    pass
```

### 4. Inference Service
Create `/workspace/ml/sentiment_models/inference_service.py`:
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SentimentRequest(BaseModel):
    text: str
    platform: str
    ticker: Optional[str]

@app.post("/analyze")
async def analyze_sentiment(request: SentimentRequest):
    # Run inference
    # Return sentiment scores
    pass
```

### 5. Model Registry
Create `/workspace/ml/sentiment_models/model_registry.py`:
- Track model versions
- A/B testing setup
- Performance metrics

## Deliverables by End of Week 2
1. **Base Models**: FinBERT fine-tuning started
2. **Training Data**: 10K+ labeled examples
3. **API Contract**: `/workspace/contracts/ml_api.yaml`
4. **Inference Service**: Basic FastAPI running

## Week 3-12 Continuation
- Complete all model training
- Optimize for <100ms inference
- Build continuous learning pipeline
- Create model monitoring dashboard

---

# Agent 4: Backend Infrastructure Engineer

## Initial Setup
```bash
cd /workspace
git checkout -b agent4-backend-api
cd backend
# Use existing Django setup
```

## Your Mission
Build robust, scalable APIs that power both mobile and web frontends.

## Week 1-2 Tasks

### 1. API Architecture
Create `/workspace/backend/api/v2/__init__.py`:
```python
# New API version for retail platform
```

### 2. Authentication System
Update `/workspace/backend/api/v2/auth.py`:
```python
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

class RetailUser(AbstractUser):
    subscription_tier = models.CharField(max_length=20)  # free, premium, pro
    watchlist = models.JSONField(default=list)
    settings = models.JSONField(default=dict)
    
    @property
    def is_premium(self):
        return self.subscription_tier in ['premium', 'pro']
```

### 3. Core API Endpoints
Create `/workspace/backend/api/v2/views.py`:
```python
from rest_framework import viewsets
from django.core.cache import cache

class SentimentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/v2/sentiment/{ticker}/
    GET /api/v2/sentiment/trending/
    GET /api/v2/sentiment/watchlist/
    """
    pass

class AlertViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for alerts
    POST /api/v2/alerts/
    GET /api/v2/alerts/history/
    """
    pass

class ScreenerViewSet(viewsets.ViewSet):
    """
    POST /api/v2/screener/run/
    GET /api/v2/screener/strategies/
    """
    pass
```

### 4. WebSocket Support
Create `/workspace/backend/api/v2/consumers.py`:
```python
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class SentimentConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Subscribe to real-time updates
        pass
    
    async def sentiment_update(self, event):
        # Send real-time sentiment updates
        pass
```

### 5. Caching Strategy
Update `/workspace/backend/core/settings.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'sentiment_v2',
        'TIMEOUT': 300,  # 5 minutes default
    }
}

# Cache specific endpoints
CACHE_MIDDLEWARE_SECONDS = 60  # 1 minute for trending
```

## Deliverables by End of Week 2
1. **API Documentation**: OpenAPI/Swagger spec
2. **Auth System**: JWT auth working
3. **Core Endpoints**: Basic CRUD operations
4. **WebSocket**: Real-time connection established

## Week 3-12 Continuation
- Alert engine implementation
- Screening engine optimization
- Payment integration
- Performance optimization

---

# Agent 5: Frontend Web Developer

## Initial Setup
```bash
cd /workspace
git checkout -b agent5-web-frontend
mkdir -p web
cd web
npx create-next-app@latest sentiment-trader --typescript --tailwind --app
```

## Your Mission
Build a responsive, fast web application with stunning visualizations.

## Week 1-2 Tasks

### 1. Project Structure
```
/workspace/web/sentiment-trader/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── dashboard/
│   │   └── page.tsx
│   ├── screener/
│   │   └── page.tsx
│   ├── stock/[ticker]/
│   │   └── page.tsx
│   └── api/
│       └── mock/
├── components/
│   ├── charts/
│   │   ├── SentimentChart.tsx
│   │   ├── HeatMap.tsx
│   │   └── SparkLine.tsx
│   ├── screener/
│   │   ├── FilterBuilder.tsx
│   │   └── ResultsTable.tsx
│   └── common/
│       ├── StockCard.tsx
│       └── Navigation.tsx
├── lib/
│   ├── api.ts
│   └── mockData.ts
└── styles/
    └── globals.css
```

### 2. Mock API Service
Create `/workspace/web/sentiment-trader/lib/mockApi.ts`:
```typescript
export const mockApi = {
  async getTrending() {
    return [
      { ticker: 'GME', sentiment: 0.85, change: 45 },
      // More mock data
    ];
  },
  
  async getSentiment(ticker: string) {
    return {
      current: 0.75,
      history: [/* 7 days of data */],
      platforms: {
        reddit: 0.80,
        twitter: 0.70,
        stocktwits: 0.75
      }
    };
  }
};
```

### 3. Dashboard Components
Create key visualization components:
- `SentimentGauge`: D3.js gauge chart
- `TrendingHeatMap`: Interactive heat map
- `PlatformBreakdown`: Pie/bar chart
- `SentimentTimeline`: Line chart with zoom

### 4. Screener Interface
Create `/workspace/web/sentiment-trader/components/screener/FilterBuilder.tsx`:
- Drag-and-drop filter builder
- Real-time preview
- Save/load strategies

### 5. Responsive Design
- Mobile-first approach
- Touch-friendly interactions
- Progressive enhancement

## Deliverables by End of Week 2
1. **Running Next.js App**: Basic routing working
2. **Component Library**: Reusable chart components
3. **Mock Integration**: All pages using mock data
4. **Responsive Layout**: Works on mobile/tablet/desktop

## Week 3-12 Continuation
- Real API integration
- Advanced visualizations
- SEO optimization
- Performance optimization

---

# Coordination Protocol

## Week 2 Sync Point
All agents must commit and push:
```bash
# Each agent
git add .
git commit -m "Week 2: API contracts and interfaces defined"
git push origin [your-branch]
```

Create these shared contracts in `/workspace/contracts/`:
1. `data_pipeline_api.yaml` - Agent 1
2. `ml_api.yaml` - Agent 3  
3. `backend_api.yaml` - Agent 4
4. `types.ts` - Shared TypeScript types

## Week 6 Integration
1. Agent 1 → Agent 3: Real data flowing
2. Agent 3 → Agent 4: ML models integrated
3. Agent 4 → Agent 2,5: APIs connected

## Daily Standups
Each agent should update `/workspace/agent_status/[agent_name].md`:
```markdown
# Agent 1 Status - [Date]

## Completed Today
- Implemented Reddit streaming
- Set up Kafka topics

## Blockers
- Need API key for Twitter

## Tomorrow's Plan
- Complete Twitter integration
```

## Conflict Resolution
- Each agent works in separate directories
- No direct file conflicts
- Merge to main only after integration testing
- Use feature flags for gradual rollout

---

# Success Criteria

## Week 2
- [ ] All API contracts defined
- [ ] Mock data flowing in all apps
- [ ] Basic UI/UX implemented
- [ ] ML training started

## Week 6
- [ ] Real data pipeline working
- [ ] ML models deployed
- [ ] APIs serving real data
- [ ] Apps consuming real APIs

## Week 12
- [ ] 99.9% uptime achieved
- [ ] <200ms API response time
- [ ] 85%+ sentiment accuracy
- [ ] Apps ready for store submission
- [ ] 100 beta users onboarded

---

# Quick Start Commands

```bash
# Agent 1: Start data pipeline
cd /workspace/backend/data_pipeline
python -m reddit_ingestion

# Agent 2: Start mobile app
cd /workspace/mobile/SentimentTrader
npm run ios  # or npm run android

# Agent 3: Start ML service
cd /workspace/ml/sentiment_models
uvicorn inference_service:app --reload

# Agent 4: Start backend API
cd /workspace/backend
python manage.py runserver

# Agent 5: Start web app
cd /workspace/web/sentiment-trader
npm run dev
```

Each agent should work independently, check in their progress daily, and coordinate only at the defined sync points. This approach maximizes parallel development while minimizing conflicts.