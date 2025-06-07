// Re-export all types
export type {
  ApiError,
  Analysis,
  AnalysisSummary,
  AnalysisResult,
  BotAnalysis,
  IQDistribution,
  SentimentByDate,
  SearchParams,
  CacheData
} from './types';

// Re-export auth functions
export { login } from './auth.api';
export type { LoginResponse } from './auth.api';

// Re-export analysis functions
export {
  getAnalyses,
  createAnalysis,
  getAnalysis,
  getAnalysisSummary,
  getSentimentByDate,
  getIQDistribution,
  getBotAnalysis,
  getAnalysisFullDetails,
  getGemmaStatus
} from './analysis.api';

// Re-export results functions
export {
  getAnalysisResults,
  updateSentiment,
  searchAnalysisResults
} from './results.api';

// Re-export cache utilities if needed elsewhere
export {
  getCachedData,
  setCachedData,
  clearCache,
  clearAllCache
} from './cache';

// Re-export the api client for direct use if needed
export { default as api } from './api.client';