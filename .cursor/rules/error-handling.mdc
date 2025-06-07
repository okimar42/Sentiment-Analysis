- **Error Handling Requirements**
  - All catch blocks must type errors as `unknown`
  - Use type guards to check error types
  - Always provide fallback error messages
  
- **Standard Pattern**
  ```typescript
  try {
    // operation
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : 'Operation failed';
    console.error('Context-specific message:', error);
    // handle error
  }
  ```

- **API Error Interface**
  ```typescript
  interface ApiError {
    response?: {
      data?: {
        detail?: string;
        [key: string]: unknown;
      };
      status?: number;
    };
    message?: string;
  }
  ```

- **❌ DON'T**
  - Use `any` type in catch blocks
  - Access error properties without type guards
  - Leave catch blocks empty

- **✅ DO**
  - Type errors as `unknown`
  - Use instanceof checks
  - Log errors for debugging
  - Provide user-friendly messages

- **Example from Codebase**
  ```typescript
  // From frontend/src/pages/Dashboard.tsx
  } catch (err: unknown) {
    console.error('Failed to fetch analyses:', err);
    const errorMessage = err instanceof Error ? err.message : 'Failed to fetch analyses';
    setError(errorMessage);
  }
  ```