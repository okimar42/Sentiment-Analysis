import { themes } from './themes';

describe('themes array', () => {
  it('should have at least 30 themes', () => {
    expect(themes.length).toBeGreaterThanOrEqual(30);
  });

  it('should have unique ids', () => {
    const ids = themes.map(t => t.id);
    const uniqueIds = new Set(ids);
    expect(uniqueIds.size).toBe(ids.length);
  });

  it('should have unique names', () => {
    const names = themes.map(t => t.name);
    const uniqueNames = new Set(names);
    expect(uniqueNames.size).toBe(names.length);
  });

  it('should have a non-empty category for every theme', () => {
    for (const theme of themes) {
      expect(typeof theme.category).toBe('string');
      expect(theme.category.length).toBeGreaterThan(0);
    }
  });

  it('should have all expected categories', () => {
    const expectedCategories = [
      'Classic', 'Editor', 'OS', 'Brand', 'Nature', 'Fun/Trendy', 'High Contrast'
    ];
    const categories = new Set(themes.map(t => t.category));
    for (const cat of expectedCategories) {
      expect(categories.has(cat)).toBe(true);
    }
  });

  it('should not have any theme missing id, name, or category', () => {
    for (const theme of themes) {
      expect(typeof theme.id).toBe('string');
      expect(theme.id.length).toBeGreaterThan(0);
      expect(typeof theme.name).toBe('string');
      expect(theme.name.length).toBeGreaterThan(0);
      expect(typeof theme.category).toBe('string');
      expect(theme.category.length).toBeGreaterThan(0);
    }
  });

  it('debug: print all categories', () => {
    // This will print the categories to the test output
    // Remove or comment out after debugging
    // eslint-disable-next-line no-console
    console.log('CATEGORIES:', [...new Set(themes.map(t => t.category))]);
  });
}); 