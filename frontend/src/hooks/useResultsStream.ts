import { useEffect } from 'react';
import type { AnalysisResult } from '../services/types';

interface UseResultsStreamOptions {
  analysisId: string | undefined;
  onMessage: (result: AnalysisResult) => void;
  baseUrl?: string;
}

/**
 * Hook to subscribe to backend SSE endpoint for newly created results.
 */
const useResultsStream = ({ analysisId, onMessage, baseUrl = import.meta.env.VITE_API_URL || '' }: UseResultsStreamOptions) => {
  useEffect(() => {
    if (!analysisId) return;
    const url = `${baseUrl}/analyze/${analysisId}/results-stream/`;
    const es = new EventSource(url);
    es.onmessage = (e) => {
      try {
        const data: AnalysisResult = JSON.parse(e.data);
        onMessage(data);
      } catch {
        // ignore malformed events
      }
    };
    es.onerror = () => {
      es.close();
    };
    return () => {
      es.close();
    };
  }, [analysisId, onMessage, baseUrl]);
};

export default useResultsStream;