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
  
  export function AnalysisForm({ onSubmit }: AnalysisFormProps) {
    // State
    const [formData, setFormData] = useState<FormData>(initialData);
    const [error, setError] = useState<string>('');
    
    // Effects
    useEffect(() => {
      // effect logic
    }, [dependencies]);
    
    // Handlers
    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      try {
        await onSubmit(formData);
      } catch (error: unknown) {
        const errorMessage = error instanceof Error ? error.message : 'Submit failed';
        setError(errorMessage);
      }
    };
    
    // Render
    return (
      <form onSubmit={handleSubmit}>
        {error && <Alert severity="error">{error}</Alert>}
        {/* JSX */}
      </form>
    );
  }
  ```

- **Hook Organization**
  - Custom hooks in separate files
  - Prefix with `use` (e.g., `useAnalysisData`)
  - Return typed objects

- **Props Guidelines**
  - Destructure props in function signature
  - Use optional chaining for optional props
  - Provide default values where appropriate

- **State Management**
  - Keep state close to where it's used
  - Lift state only when necessary
  - Consider custom hooks for complex state

- **Performance Considerations**
  - Use `useCallback` for stable handler references
  - Use `useMemo` for expensive computations
  - Avoid inline function definitions in render