import api from './api.client';
import { getCachedData, setCachedData, clearCache } from './cache';
import type { AnalysisSummary, AnalysisResult, BotAnalysis, IQDistribution, SentimentByDate } from './types';
import type { Analysis } from './types';

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
  } catch (error) {
    console.error('Failed to fetch analyses:', error);
    throw new Error('Failed to fetch analyses');
  }
};

export const createAnalysis = async (data: Partial<Analysis>): Promise<Analysis> => {
  try {
    console.log('Creating analysis with data:', data);
    const response = await api.post('analyze/', data);
    console.log('Analysis creation response:', response.data);
    // Invalidate analyses cache
    clearCache('analyses');
    return response.data;
  } catch (error) {
    console.error('Failed to create analysis:', error);
    throw new Error('Failed to create analysis');
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
  } catch (error) {
    console.error('Failed to fetch analysis:', error);
    throw new Error('Failed to fetch analysis');
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
  } catch (error) {
    console.error('Failed to fetch analysis summary:', error);
    throw new Error('Failed to fetch analysis summary');
  }
};

export const getSentimentByDate = async (id: string): Promise<SentimentByDate[]> => {
  try {
    const response = await api.get(`analyze/${id}/sentiment-by-date/`);
    return response.data as SentimentByDate[];
  } catch (error) {
    console.error('Error fetching sentiment by date:', error);
    throw error;
  }
};

export const getIQDistribution = async (id: string): Promise<IQDistribution[]> => {
  try {
    const response = await api.get(`analyze/${id}/iq-distribution/`);
    return response.data as IQDistribution[];
  } catch (error) {
    console.error('Error fetching IQ distribution:', error);
    throw error;
  }
};

export const getBotAnalysis = async (id: string): Promise<BotAnalysis> => {
  try {
    const response = await api.get(`analyze/${id}/bot-analysis/`);
    return response.data as BotAnalysis;
  } catch (error) {
    console.error('Error fetching bot analysis:', error);
    throw error;
  }
};

export const getAnalysisFullDetails = async (id: string): Promise<Analysis & { summary: AnalysisSummary; results: AnalysisResult[] }> => {
  try {
    // Always fetch fresh data when getting full details
    const response = await api.get(`analyze/${id}/full-details/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching full analysis details:', error);
    throw new Error('Failed to fetch analysis details');
  }
};

export const getGemmaStatus = async (): Promise<{ available: boolean; status: string }> => {
  try {
    const response = await api.get('analyze/gemma-status/');
    return response.data;
  } catch (error) {
    console.error('Error fetching Gemma status:', error);
    throw error;
  }
};