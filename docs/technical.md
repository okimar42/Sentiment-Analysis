# Technical Documentation

## Project Architecture

### Frontend (React + TypeScript)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Library**: Material-UI (MUI)
- **State Management**: React Context/Hooks
- **HTTP Client**: Axios
- **Charts**: Chart.js, Recharts
- **Testing**: Vitest, React Testing Library

### Backend (Django + Python)
- **Framework**: Django 4.x
- **API**: Django REST Framework
- **Task Queue**: Celery with Redis
- **Database**: PostgreSQL
- **Authentication**: Django Auth + Supabase
- **Testing**: Django Test Framework

## Coding Standards

### TypeScript/JavaScript
1. **No Any Types**: All variables must have proper TypeScript types
2. **File Size**: Maximum 300 lines per file
3. **Imports**: Remove all unused imports
4. **Error Handling**: No empty catch blocks
5. **Naming Conventions**:
   - Components: PascalCase
   - Functions/Variables: camelCase
   - Constants: UPPER_SNAKE_CASE
   - Types/Interfaces: PascalCase with 'I' prefix for interfaces

### Python
1. **PEP 8 Compliance**: Follow Python style guide
2. **File Size**: Maximum 300 lines per file (excluding tests)
3. **Docstrings**: All functions and classes must have docstrings
4. **Type Hints**: Use type hints for function parameters and returns
5. **Naming Conventions**:
   - Classes: PascalCase
   - Functions/Variables: snake_case
   - Constants: UPPER_SNAKE_CASE

## File Organization

### Frontend Structure
```
frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/         # Page components (routes)
│   ├── services/      # API services and utilities
│   ├── types/         # TypeScript type definitions
│   ├── hooks/         # Custom React hooks
│   └── utils/         # Helper functions
```

### Backend Structure
```
backend/
├── sentiment_analysis/  # Main app
│   ├── models/        # Database models
│   ├── views/         # API views
│   ├── serializers/   # DRF serializers
│   ├── tasks/         # Celery tasks
│   └── tests/         # Test files
```

## Best Practices

### Component Design
1. Keep components focused and single-purpose
2. Extract complex logic into custom hooks
3. Use composition over inheritance
4. Implement proper error boundaries

### API Design
1. RESTful endpoints with proper HTTP methods
2. Consistent error response format
3. Pagination for list endpoints
4. Proper status codes

### Testing
1. Unit tests for all business logic
2. Integration tests for API endpoints
3. Component tests for UI behavior
4. Minimum 80% code coverage

### Performance
1. Lazy load components where appropriate
2. Implement proper caching strategies
3. Optimize database queries (use select_related/prefetch_related)
4. Use pagination for large datasets

## Security
1. Input validation on both frontend and backend
2. CSRF protection enabled
3. Proper authentication/authorization
4. Sanitize user inputs
5. Use environment variables for sensitive data

## Git Workflow
1. Feature branches from main
2. Meaningful commit messages
3. PR reviews required
4. Run tests before merging
5. Keep commits atomic and focused 