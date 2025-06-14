import axios from 'axios';
import type { AxiosError, AxiosResponse, InternalAxiosRequestConfig } from 'axios';

const API_URL = import.meta.env.VITE_API_URL || '/api';
console.log('🔧 DEBUG: VITE_API_URL =', import.meta.env.VITE_API_URL);
console.log('🔧 DEBUG: Final API_URL =', API_URL);

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
  // Add these to handle HTTPS self-signed certificates
  withCredentials: false,
  validateStatus: function (status: number) {
    return status >= 200 && status < 300; // default
  },
});

// Add token to requests if it exists
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = localStorage.getItem('token');
  if (token && config.headers) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
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

export default api;

// Export types
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