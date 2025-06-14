# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

## Theme System (Multi-Theme, Persistent, Context-Based)

This project features a robust theme system with the following capabilities:

- **Multiple Editor Themes:** Gruvbox, Dracula, Monokai, Solarized, Nord, VSCode Dark, and more (see `frontend/src/themes.ts`).
- **Context-Based:** Uses a `ThemeContext` (`frontend/src/contexts/ThemeContext.tsx`) for global theme management.
- **Persistent Selection:** Remembers the user's last selected theme using `localStorage`.
- **Grouped Menu:** Theme picker groups themes by light/dark, shows checkmarks for the active theme, and is accessible from the app bar.
- **Easy Extension:** Add new themes by extending the `themes` array in `frontend/src/themes.ts`.
- **Visual Theme Previews:** The theme picker now shows a color swatch preview for each theme, displaying its primary, secondary, and background colors for quick visual selection.

### Usage

- The theme picker is available in the app bar. Click the current theme name to open the menu and select from grouped light/dark themes.
- Each theme in the menu displays a color swatch preview of its palette.
- The selected theme is applied instantly and will persist across reloads.
- To add a new theme, add a new entry to the `themes` array in `frontend/src/themes.ts` with an `id`, `name`, and a Material-UI theme object.

### Example: Adding a New Theme

```ts
import { createTheme } from '@mui/material/styles';

const myCustomTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#123456' },
    // ...
  },
});

export const themes = [
  // ...existing themes
  { id: 'my-custom-theme', name: 'My Custom Theme', theme: myCustomTheme },
];
```

### Technical Details
- See `frontend/src/contexts/ThemeContext.tsx` for the context/provider implementation.
- See `frontend/src/components/Layout.tsx` for the grouped menu UI logic.
- All theme switching is handled via context; no prop drilling is required.
- **AI Assistance:** This project uses context7 for AI-powered development and documentation improvements.

---

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default tseslint.config({
  extends: [
    // Remove ...tseslint.configs.recommended and replace with this
    ...tseslint.configs.recommendedTypeChecked,
    // Alternatively, use this for stricter rules
    ...tseslint.configs.strictTypeChecked,
    // Optionally, add this for stylistic rules
    ...tseslint.configs.stylisticTypeChecked,
  ],
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config({
  plugins: {
    // Add the react-x and react-dom plugins
    'react-x': reactX,
    'react-dom': reactDom,
  },
  rules: {
    // other rules...
    // Enable its recommended typescript rules
    ...reactX.configs['recommended-typescript'].rules,
    ...reactDom.configs.recommended.rules,
  },
})
```
