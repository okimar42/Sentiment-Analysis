// API Error type
export interface ApiError {
  response?: {
    data?: {
      detail?: string;
      [key: string]: unknown;
    };
    status?: number;
  };
  request?: unknown;
  message?: string;
}

// Analysis types
export type Analysis = {
  id: string;
  query: string;
  source: string | string[];
  model: string;
  created_at: string;
  status?: string;
  twitter_grok_summary?: string;
  results?: AnalysisResult[];
};

export type AnalysisSummary = {
  total_posts: number;
  average_score: number;
  sentiment_distribution: {
    positive: number;
    negative: number;
    neutral: number;
  };
  sentiment_percentages: {
    positive: number;
    negative: number;
    neutral: number;
  };
};

export type AnalysisResult = {
  id: string;
  content: string;
  score: number;
  post_date: string;
  perceived_iq: number;
  bot_probability: number;
  source_type?: string;
  post_id?: string;
};

export type BotAnalysis = {
  total: number;
  bots: number;
  not_bots: number;
  avg_bot_probability: number;
};

export type IQDistribution = {
  perceived_iq: number;
  count: number;
};

export type SentimentByDate = {
  post_date: string;
  avg_score: number;
  count: number;
};

// Search parameters
export interface SearchParams {
  search?: string;
  ordering?: string;
  sentiment?: string;
  [key: string]: unknown;
}

// Cache types
export interface CacheData {
  data: unknown;
  timestamp: number;
}