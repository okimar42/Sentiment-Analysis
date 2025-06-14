import * as Charts from './';

describe('Chart component registry', () => {
  it('should export all chart components and have unique names', () => {
    const chartNames = Object.keys(Charts);
    const uniqueNames = new Set(chartNames);
    expect(uniqueNames.size).toBe(chartNames.length);
    for (const name of chartNames) {
      expect(Charts[name]).toBeDefined();
    }
  });
}); 