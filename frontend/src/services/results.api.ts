import api from './api.client';
import { getCachedData, setCachedData } from './cache';
import type { ApiError, AnalysisResult, SearchParams } from './types';

export const getAnalysisResults = async (id: string): Promise<AnalysisResult[]> => {
  const cacheKey = `analysis-results-${id}`;
  const cachedData = getCachedData(cacheKey);
  
  if (cachedData) {
    return cachedData as AnalysisResult[];
  }

  try {
    const response = await api.get(`analyses/${id}/results/`);
    setCachedData(cacheKey, response.data);
    return response.data;
  } catch (error) {
    const apiError = error as ApiError;
    throw new Error(apiError.response?.data?.detail || 'Failed to fetch analysis results');
  }
};

export const updateSentiment = async (
  analysisId: string, 
  resultId: string, 
  sentiment: string, 
  reason: string
): Promise<AnalysisResult> => {
  try {
    const response = await api.patch(`analyses/${analysisId}/results/${resultId}/`, {
      manual_sentiment: sentiment,
      override_reason: reason
    });
    return response.data;
  } catch (error) {
    const apiError = error as ApiError;
    console.error('Error updating sentiment:', error);
    throw error;
  }
};

export const searchAnalysisResults = async (
  id: string, 
  params: SearchParams
): Promise<{ results: AnalysisResult[]; count: number }> => {
  try {
    const response = await api.get(`analyses/${id}/search/`, { params });
    return response.data;
  } catch (error) {
    const apiError = error as ApiError;
    throw new Error(apiError.response?.data?.detail || 'Failed to search analysis results');
  }
};