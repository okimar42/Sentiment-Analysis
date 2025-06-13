import { renderHook, act } from '@testing-library/react';
import useResultsStream from './useResultsStream';
import type { AnalysisResult } from '../services/types';

describe('useResultsStream', () => {
  it('invokes callback on new SSE message', () => {
    const received: AnalysisResult[] = [];
    const { unmount } = renderHook(() => useResultsStream({ analysisId: '123', onMessage: (r: AnalysisResult) => received.push(r), baseUrl: '' }));
    // access stub instance list exposed in setup
    // @ts-expect-error accessing global test helper
    const es = global.__ES_INSTANCES__[0];
    const mockResult = { id: '1', content: 'hi', score: 0.1, post_date: '2025-06-12T10:00:00Z', perceived_iq: 0.5, bot_probability: 0 };
    act(() => {
      es.emit(JSON.stringify(mockResult));
    });
    expect(received).toHaveLength(1);
    expect(received[0].id).toBe('1');
    unmount();
  });
});