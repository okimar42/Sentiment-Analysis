import { NotificationProvider, useNotification } from './NotificationContext';
import { renderHook } from '@testing-library/react';

describe('NotificationContext registry', () => {
  it('should provide all required notification methods', () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <NotificationProvider>{children}</NotificationProvider>
    );
    const { result } = renderHook(() => useNotification(), { wrapper });
    const methods = [
      'showNotification',
      'showProcessingStart',
      'showProcessingComplete',
      'hideNotification',
    ];
    for (const method of methods) {
      expect(typeof result.current[method as keyof typeof result.current]).toBe('function');
    }
    const unique = new Set(methods);
    expect(unique.size).toBe(methods.length);
  });
}); 