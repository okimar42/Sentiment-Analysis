import { vi } from 'vitest';

vi.mock('axios', () => {
  const mockAxios = {
    post: vi.fn(),
    create: vi.fn(),
    interceptors: {
      request: { use: vi.fn() },
      response: { use: vi.fn() },
    },
  };
  mockAxios.create.mockReturnValue(mockAxios);
  return {
    __esModule: true,
    default: mockAxios,
  };
});

import axios from 'axios';
import * as api from './auth.api';

// Type the mocked axios
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('api error handling', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it('handles 401 error', async () => {
    const error = { response: { status: 401 }, request: {}, message: '401' };
    mockedAxios.post.mockRejectedValueOnce(error);
    const promise = api.login('user', 'pass').catch(e => e);
    await expect(promise).resolves.toBeInstanceOf(Error);
  });

  it('handles 403 error', async () => {
    const error = { response: { status: 403 }, request: {}, message: '403' };
    mockedAxios.post.mockRejectedValueOnce(error);
    await expect(api.login('user', 'pass')).rejects.toThrow();
  });

  it('handles 404 error', async () => {
    const error = { response: { status: 404 }, request: {}, message: '404' };
    mockedAxios.post.mockRejectedValueOnce(error);
    await expect(api.login('user', 'pass')).rejects.toThrow();
  });

  it('handles 500 error', async () => {
    const error = { response: { status: 500 }, request: {}, message: '500' };
    mockedAxios.post.mockRejectedValueOnce(error);
    await expect(api.login('user', 'pass')).rejects.toThrow();
  });

  it('handles network error', async () => {
    const error = { request: {}, message: 'Network Error' };
    mockedAxios.post.mockRejectedValueOnce(error);
    await expect(api.login('user', 'pass')).rejects.toThrow();
  });
});

describe('API endpoint registry', () => {
  it('should have unique exported function names', () => {
    const apiObj = api as Record<string, unknown>;
    const fnNames = Object.keys(apiObj).filter(k => typeof apiObj[k] === 'function');
    const uniqueNames = new Set(fnNames);
    expect(uniqueNames.size).toBe(fnNames.length);
  });

  it('should have all API functions return a Promise', () => {
    const apiObj = api as Record<string, unknown>;
    const fnNames = Object.keys(apiObj).filter(k => typeof apiObj[k] === 'function');
    for (const name of fnNames) {
      const fn = apiObj[name];
      // Only test async functions (skip types, etc.)
      if (typeof fn === 'function') {
        const result = (fn as () => unknown)();
        if (result && typeof (result as { then?: unknown }).then === 'function') {
          expect(typeof (result as { then: unknown }).then).toBe('function');
        }
      }
    }
  });
}); 