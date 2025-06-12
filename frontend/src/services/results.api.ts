import api from './api.client';
import { getCachedData, setCachedData } from './cache';
import type { AnalysisResult, SearchParams } from './types';

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
  } catch (error) {
    console.error('Failed to fetch analysis results:', error);
    throw new Error('Failed to fetch analysis results');
  }
};

export const updateSentiment = async (
  analysisId: string, 
  resultId: string, 
  sentiment: string, 
  reason: string
): Promise<AnalysisResult> => {
  try {
    const response = await api.patch(`analyze/${analysisId}/results/${resultId}/`, {
      manual_sentiment: sentiment,
      override_reason: reason
    });
    return response.data;
  } catch (error) {
    console.error('Error updating sentiment:', error);
    throw error;
  }
};

export const searchAnalysisResults = async (
  id: string, 
  params: SearchParams
): Promise<{ results: AnalysisResult[]; count: number }> => {
  try {
    const response = await api.get(`analyze/${id}/search/`, { params });
    return response.data;
  } catch (error) {
    console.error('Failed to search analysis results:', error);
    throw new Error('Failed to search analysis results');
  }
};