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

- **Import Path Guidelines**
  - Use absolute imports for cross-module imports
  - Use relative imports within the same module
  - Avoid deep relative paths (../../../)
  
- **Barrel Exports**
  ```typescript
  // services/index.ts
  export * from './auth.api';
  export * from './analysis.api';
  export * from './results.api';
  ```

- **Type-Only Imports**
  - When `verbatimModuleSyntax` is enabled:
  ```typescript
  import type { ApiError } from './types';
  import { getCachedData } from './cache';
  ```

- **ESLint Configuration**
  - Configure `eslint-plugin-import` for import ordering
  - Enable `no-unused-vars` rule
  - Use `--fix` flag to auto-fix import issues