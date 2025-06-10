import api from './api.client';
import type { ApiError } from './types';

export interface LoginResponse {
  token: string;
}

export const login = async (username: string, password: string): Promise<LoginResponse> => {
  try {
    const response = await api.post('api-token-auth/', { username, password });
    return response.data;
  } catch (error) {
    const apiError = error as ApiError;
    throw new Error(apiError.response?.data?.detail || 'Login failed');
  }
};