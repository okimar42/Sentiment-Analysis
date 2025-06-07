import type { CacheData } from './types';

// Create cache for GET requests
const cache = new Map<string, CacheData>();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

// Helper function to get cached data
export const getCachedData = (key: string): unknown | null => {
  const cached = cache.get(key);
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }
  return null;
};

// Helper function to set cached data
export const setCachedData = (key: string, data: unknown): void => {
  cache.set(key, {
    data,
    timestamp: Date.now(),
  });
};

// Helper function to clear specific cache
export const clearCache = (key: string): void => {
  cache.delete(key);
};

// Helper function to clear all cache
export const clearAllCache = (): void => {
  cache.clear();
};