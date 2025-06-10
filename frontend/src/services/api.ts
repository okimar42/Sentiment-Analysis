import axios, { AxiosError } from 'axios';

const API_URL = (import.meta as any).env.VITE_API_URL || '/api';
console.log('🔧 DEBUG: VITE_API_URL =', (import.meta as any).env.VITE_API_URL);
console.log('🔧 DEBUG: Final API_URL =', API_URL);

// Create cache for GET requests
const cache = new Map();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
  // Add these to handle HTTPS self-signed certificates
  withCredentials: false,
  validateStatus: function (status) {
    return status >= 200 && status < 300; // default
  },
});

// Add token to requests if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    if (error.response) {
      // Handle specific error cases
      console.error('Response error:', error.response.status, error.response.data);
      switch (error.response.status) {
        case 401:
          // Clear token but do not redirect
          localStorage.removeItem('token');
          break;
        case 403:
          console.error('Access forbidden');
          break;
        case 404:
          console.error('Resource not found');
          break;
        case 500:
          console.error('Server error');
          break;
        default:
          console.error('An error occurred');
      }
    } else if (error.request) {
      console.error('No response received', error.request);
    } else {
      console.error('Error setting up request', error.message);
    }
    return Promise.reject(error);
  }
);

// Helper function to get cached data
const getCachedData = (key: string) => {
  const cached = cache.get(key);
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }
  return null;
};

// Helper function to set cached data
const setCachedData = (key: string, data: unknown) => {
  cache.set(key, {
    data,
    timestamp: Date.now(),
  });
};

// TypeScript interfaces for API data structures
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

export type SearchParams = {
  q?: string;
  sentiment?: string;
  sarcasm?: string;
  bot?: string;
  min_iq?: number;
  sort_by?: string;
  sort_order?: string;
  page: number;
  page_size: number;
};

export type SearchResults = {
  results: AnalysisResult[];
  total_count: number;
  page: number;
  page_size: number;
  total_pages: number;
};

export const login = async (username: string, password: string): Promise<any> => {
  try {
    const response = await api.post('api-token-auth/', { username, password });
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Login failed');
  }
};

export const getAnalyses = async (): Promise<Analysis[]> => {
  const cacheKey = 'analyses';
  const cachedData = getCachedData(cacheKey);
  
  if (cachedData) {
    return cachedData as Analysis[];
  }

  try {
    const response = await api.get('analyze/');
    setCachedData(cacheKey, response.data);
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch analyses');
  }
};

export const createAnalysis = async (data: any): Promise<any> => {
  try {
    console.log('Creating analysis with data:', data);
    const response = await api.post('analyze/', data);
    console.log('Analysis creation response:', response.data);
    // Invalidate analyses cache
    cache.delete('analyses');
    return response.data;
  } catch (error: any) {
    console.error('Full error object:', error);
    console.error('Error response:', error.response);
    console.error('Error response data:', error.response?.data);
    console.error('Error response status:', error.response?.status);
    if (error.response?.data) {
      throw new Error(JSON.stringify(error.response.data));
    }
    throw new Error(error.response?.data?.detail || error.message || 'Failed to create analysis');
  }
};

export const getAnalysis = async (id: string): Promise<Analysis> => {
  const cacheKey = `analysis-${id}`;
  const cachedData = getCachedData(cacheKey);
  
  if (cachedData) {
    return cachedData as Analysis;
  }

  try {
    const response = await api.get(`analyze/${id}/`);
    setCachedData(cacheKey, response.data);
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch analysis');
  }
};

export const getAnalysisResults = async (id: string): Promise<AnalysisResult[]> => {
  const cacheKey = `analysis-results-${id}`;
  const cachedData = getCachedData(cacheKey);
  
  if (cachedData) {
    return cachedData as AnalysisResult[];
  }

  try {
    const response = await api.get(`analyze/${id}/results/`);
    setCachedData(cacheKey, response.data);
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch analysis results');
  }
};

export const getAnalysisSummary = async (id: string): Promise<AnalysisSummary> => {
  const cacheKey = `analysis-summary-${id}`;
  const cachedData = getCachedData(cacheKey);
  
  if (cachedData) {
    return cachedData as AnalysisSummary;
  }

  try {
    const response = await api.get(`analyze/${id}/summary/`);
    setCachedData(cacheKey, response.data);
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch analysis summary');
  }
};

export const updateSentiment = async (analysisId: string, resultId: string, sentiment: string, reason: string): Promise<any> => {
  try {
    const response = await api.patch(`analyze/${analysisId}/results/${resultId}/`, {
      manual_sentiment: sentiment,
      override_reason: reason
    });
    return response.data;
  } catch (error: any) {
    console.error('Error updating sentiment:', error);
    throw error;
  }
};

export const getSentimentByDate = async (id: string): Promise<SentimentByDate[]> => {
  try {
    const response = await api.get(`analyze/${id}/sentiment-by-date/`);
    return response.data as SentimentByDate[];
  } catch (error: any) {
    console.error('Error fetching sentiment by date:', error);
    throw error;
  }
};

export const getIQDistribution = async (id: string): Promise<IQDistribution[]> => {
  try {
    const response = await api.get(`analyze/${id}/iq-distribution/`);
    return response.data as IQDistribution[];
  } catch (error: any) {
    console.error('Error fetching IQ distribution:', error);
    throw error;
  }
};

export const getBotAnalysis = async (id: string): Promise<BotAnalysis> => {
  try {
    const response = await api.get(`analyze/${id}/bot-analysis/`);
    return response.data as BotAnalysis;
  } catch (error: any) {
    console.error('Error fetching bot analysis:', error);
    throw error;
  }
};

export const getAnalysisFullDetails = async (id: string): Promise<any> => {
  try {
    // Always fetch fresh data when getting full details
    const response = await api.get(`analyze/${id}/full-details/`);
    return response.data;
  } catch (error: any) {
    console.error('Error fetching full analysis details:', error);
    throw new Error(error.response?.data?.detail || 'Failed to fetch analysis details');
  }
};

export const getGemmaStatus = async (): Promise<any> => {
  try {
    const response = await api.get('analyze/gemma-status/');
    return response.data;
  } catch (error: any) {
    console.error('Error fetching Gemma status:', error);
    throw error;
  }
};

export const searchAnalysisResults = async (id: string, params: SearchParams): Promise<SearchResults> => {
  try {
    const response = await api.get(`analyze/${id}/search/`, { params });
    return response.data;
  } catch (error: any) {
    console.error('Error searching analysis results:', error);
    throw new Error(error.response?.data?.detail || 'Failed to search analysis results');
  }
};

export default api;