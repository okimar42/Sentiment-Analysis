import api from './api.client';
import { getCachedData, setCachedData, clearCache } from './cache';
import type { ApiError, Analysis, AnalysisSummary, AnalysisResult, BotAnalysis, IQDistribution, SentimentByDate } from './types';

export const getAnalyses = async (): Promise<Analysis[]> => {
  const cacheKey = 'analyses';
  const cachedData = getCachedData(cacheKey);
  
  if (cachedData) {
    return cachedData as Analysis[];
  }

  try {
    const response = await api.get('analyses/');
    setCachedData(cacheKey, response.data);
    return response.data;
  } catch (error) {
    const apiError = error as ApiError;
    throw new Error(apiError.response?.data?.detail || 'Failed to fetch analyses');
  }
};

export const createAnalysis = async (data: Partial<Analysis>): Promise<Analysis> => {
  try {
    console.log('Creating analysis with data:', data);
    const response = await api.post('analyses/', data);
    console.log('Analysis creation response:', response.data);
    // Invalidate analyses cache
    clearCache('analyses');
    return response.data;
  } catch (error) {
    const apiError = error as ApiError;
    console.error('Full error object:', error);
    console.error('Error response:', apiError.response);
    console.error('Error response data:', apiError.response?.data);
    console.error('Error response status:', apiError.response?.status);
    if (apiError.response?.data) {
      throw new Error(JSON.stringify(apiError.response.data));
    }
    throw new Error(apiError.response?.data?.detail || apiError.message || 'Failed to create analysis');
  }
};

export const getAnalysis = async (id: string): Promise<Analysis> => {
  const cacheKey = `analysis-${id}`;
  const cachedData = getCachedData(cacheKey);
  
  if (cachedData) {
    return cachedData as Analysis;
  }

  try {
    const response = await api.get(`analyses/${id}/`);
    setCachedData(cacheKey, response.data);
    return response.data;
  } catch (error) {
    const apiError = error as ApiError;
    throw new Error(apiError.response?.data?.detail || 'Failed to fetch analysis');
  }
};

export const getAnalysisSummary = async (id: string): Promise<AnalysisSummary> => {
  const cacheKey = `analysis-summary-${id}`;
  const cachedData = getCachedData(cacheKey);
  
  if (cachedData) {
    return cachedData as AnalysisSummary;
  }

  try {
    const response = await api.get(`analyses/${id}/summary/`);
    setCachedData(cacheKey, response.data);
    return response.data;
  } catch (error) {
    const apiError = error as ApiError;
    throw new Error(apiError.response?.data?.detail || 'Failed to fetch analysis summary');
  }
};

export const getSentimentByDate = async (id: string): Promise<SentimentByDate[]> => {
  try {
    const response = await api.get(`analyses/${id}/sentiment-by-date/`);
    return response.data as SentimentByDate[];
  } catch (error) {
    const apiError = error as ApiError;
    console.error('Error fetching sentiment by date:', error);
    throw error;
  }
};

export const getIQDistribution = async (id: string): Promise<IQDistribution[]> => {
  try {
    const response = await api.get(`analyses/${id}/iq-distribution/`);
    return response.data as IQDistribution[];
  } catch (error) {
    const apiError = error as ApiError;
    console.error('Error fetching IQ distribution:', error);
    throw error;
  }
};

export const getBotAnalysis = async (id: string): Promise<BotAnalysis> => {
  try {
    const response = await api.get(`analyses/${id}/bot-analysis/`);
    return response.data as BotAnalysis;
  } catch (error) {
    const apiError = error as ApiError;
    console.error('Error fetching bot analysis:', error);
    throw error;
  }
};

export const getAnalysisFullDetails = async (id: string): Promise<Analysis & { summary: AnalysisSummary; results: AnalysisResult[] }> => {
  try {
    // Always fetch fresh data when getting full details
    const response = await api.get(`analyses/${id}/full-details/`);
    return response.data;
  } catch (error) {
    const apiError = error as ApiError;
    console.error('Error fetching full analysis details:', error);
    throw new Error(apiError.response?.data?.detail || 'Failed to fetch analysis details');
  }
};

export const getGemmaStatus = async (): Promise<{ available: boolean; status: string }> => {
  try {
    const response = await api.get('analyses/gemma-status/');
    return response.data;
  } catch (error) {
    const apiError = error as ApiError;
    console.error('Error fetching Gemma status:', error);
    throw error;
  }
};