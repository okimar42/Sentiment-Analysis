- **No Any Types**
  - Replace all `any` types with proper interfaces
  - Use `unknown` for truly unknown types
  - Create specific interfaces for API responses

- **Function Return Types**
  - All exported functions must have explicit return types
  - Async functions should return `Promise<T>`
  
- **Import Meta Types**
  ```typescript
  // For Vite environment variables
  import.meta.env.VITE_API_URL // TypeScript knows about this
  ```

- **Examples from Codebase**
  ```typescript
  // ✅ Good - Explicit types
  export const getAnalyses = async (): Promise<Analysis[]> => {
    // implementation
  };
  
  // ❌ Bad - Any type
  export const getAnalyses = async (): Promise<any> => {
    // implementation
  };
  ```

- **Type Imports**
  - Use `import type` for type-only imports when `verbatimModuleSyntax` is enabled
  ```typescript
  import type { Analysis, User } from './types';
  ```

- **Interface vs Type**
  - Use interfaces for object shapes that might be extended
  - Use types for unions, intersections, and utility types
  
- **Strict Configuration**
  - Ensure `tsconfig.json` has `strict: true`
  - Enable `noUnusedLocals` and `noUnusedParameters`
  - Use `strictNullChecks` for null safety