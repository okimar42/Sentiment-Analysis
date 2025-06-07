# Recommended Cursor Rules

Based on the code quality improvements made, here are recommended rules to add to the project:

## 1. Error Handling Rule (`error-handling.mdc`)

```markdown
---
description: Standardized error handling patterns for TypeScript/React
globs: frontend/**/*.ts, frontend/**/*.tsx
alwaysApply: true
---

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
```

## 2. TypeScript Strict Types Rule (`typescript-strict.mdc`)

```markdown
---
description: Enforce strict TypeScript typing across the codebase
globs: frontend/**/*.ts, frontend/**/*.tsx
alwaysApply: true
---

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
```

## 3. File Size Limits Rule (`file-size.mdc`)

```markdown
---
description: Enforce maximum file size to maintain code readability
globs: **/*.ts, **/*.tsx, **/*.py
alwaysApply: true
---

- **Maximum File Size: 300 lines**
  - Excluding test files and generated code
  - Split large files into smaller, focused modules

- **Refactoring Strategies**
  
  ### For React Components
  - Extract sub-components into separate files
  - Move complex logic to custom hooks
  - Separate types/interfaces into `.types.ts` files
  
  ### For API Services
  - Split by domain (auth, analysis, results)
  - Create shared types module
  - Use barrel exports for clean imports
  
  ### For Backend Views/Tasks
  - Use mixins for shared functionality
  - Create service layer for business logic
  - Split by feature area

- **Current Violations** (Reference for refactoring)
  - [api.ts](mdc:frontend/src/services/api.ts) - Split into domain modules
  - [AnalysisResults.tsx](mdc:frontend/src/pages/AnalysisResults.tsx) - Extract chart components
```

## 4. Import Organization Rule (`imports.mdc`)

```markdown
---
description: Maintain clean and organized imports
globs: frontend/**/*.ts, frontend/**/*.tsx
alwaysApply: true
---

- **Import Order**
  1. React and core libraries
  2. Third-party libraries
  3. Internal absolute imports
  4. Internal relative imports
  5. Type imports

- **Remove Unused Imports**
  - No unused variables or imports
  - Use ESLint to catch violations
  
- **Example**
  ```typescript
  // React
  import React, { useState, useEffect } from 'react';
  
  // Third-party
  import { Box, Typography } from '@mui/material';
  import axios from 'axios';
  
  // Internal
  import { api } from '@/services/api';
  import { Button } from '../components';
  
  // Types
  import type { Analysis, User } from '@/types';
  ```
```

## 5. Component Structure Rule (`component-structure.mdc`)

```markdown
---
description: Consistent React component structure
globs: frontend/**/*.tsx
alwaysApply: true
---

- **Component Organization**
  1. Type definitions
  2. Component function
  3. Hooks (useState, useEffect, etc.)
  4. Handler functions
  5. Render logic

- **Naming Conventions**
  - Components: PascalCase
  - Props interfaces: `ComponentNameProps`
  - Event handlers: `handleEventName`

- **Example Structure**
  ```typescript
  interface AnalysisFormProps {
    onSubmit: (data: FormData) => void;
  }
  
  function AnalysisForm({ onSubmit }: AnalysisFormProps) {
    // State
    const [formData, setFormData] = useState<FormData>(initialData);
    
    // Effects
    useEffect(() => {
      // effect logic
    }, [dependencies]);
    
    // Handlers
    const handleSubmit = async (e: React.FormEvent) => {
      // handler logic
    };
    
    // Render
    return (
      <form onSubmit={handleSubmit}>
        {/* JSX */}
      </form>
    );
  }
  ```
```

## Implementation Priority

1. **High Priority**: Error handling and TypeScript strict types (prevents bugs)
2. **Medium Priority**: File size limits (improves maintainability)
3. **Low Priority**: Import organization and component structure (code style)

These rules should be added to `.cursor/rules/` directory following the [cursor_rules.mdc](mdc:.cursor/rules/cursor_rules.mdc) guidelines.