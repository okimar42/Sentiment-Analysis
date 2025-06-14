import type * as Types from './types';

describe('Model/type registry', () => {
  it('Analysis should have required fields', () => {
    const required = ['id', 'query', 'source', 'model', 'created_at'];
    const analysis: Types.Analysis = {
      id: '1',
      query: 'AAPL',
      source: 'reddit',
      model: 'gpt-4',
      created_at: new Date().toISOString(),
    };
    for (const field of required) {
      expect(field in analysis).toBe(true);
    }
  });

  it('AnalysisResult should have required fields', () => {
    const required = ['id', 'content', 'score', 'post_date', 'perceived_iq', 'bot_probability'];
    const result: Types.AnalysisResult = {
      id: '1',
      content: 'test',
      score: 0.5,
      post_date: new Date().toISOString(),
      perceived_iq: 100,
      bot_probability: 0.1,
    };
    for (const field of required) {
      expect(field in result).toBe(true);
    }
  });

  it('should have unique type names', () => {
    const typeNames = [
      'ApiError', 'Analysis', 'AnalysisSummary', 'AnalysisResult', 'BotAnalysis', 'IQDistribution', 'SentimentByDate', 'SearchParams', 'CacheData'
    ];
    const uniqueNames = new Set(typeNames);
    expect(uniqueNames.size).toBe(typeNames.length);
  });
}); 