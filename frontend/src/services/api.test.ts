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
import * as api from './api';

describe('api error handling', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it('handles 401 error', async () => {
    const error = { response: { status: 401 }, request: {}, message: '401' };
    axios.post.mockRejectedValueOnce(error);
    const promise = api.login('user', 'pass').catch(e => e);
    await expect(promise).resolves.toBeInstanceOf(Error);
  });

  it('handles 403 error', async () => {
    const error = { response: { status: 403 }, request: {}, message: '403' };
    axios.post.mockRejectedValueOnce(error);
    await expect(api.login('user', 'pass')).rejects.toThrow();
  });

  it('handles 404 error', async () => {
    const error = { response: { status: 404 }, request: {}, message: '404' };
    axios.post.mockRejectedValueOnce(error);
    await expect(api.login('user', 'pass')).rejects.toThrow();
  });

  it('handles 500 error', async () => {
    const error = { response: { status: 500 }, request: {}, message: '500' };
    axios.post.mockRejectedValueOnce(error);
    await expect(api.login('user', 'pass')).rejects.toThrow();
  });

  it('handles network error', async () => {
    const error = { request: {}, message: 'Network Error' };
    axios.post.mockRejectedValueOnce(error);
    await expect(api.login('user', 'pass')).rejects.toThrow();
  });
}); 