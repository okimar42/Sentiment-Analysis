import { createContext } from 'react';
import { themes } from '../themes';
import type { AppTheme } from '../themes';

export interface ThemeContextType {
  currentTheme: AppTheme;
  themeId: string;
  setTheme: (themeId: string) => void;
  availableThemes: AppTheme[];
}

export const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const getThemeById = (id: string): AppTheme => {
  return themes.find((t) => t.id === id) || themes[0];
};

export const getStoredThemeId = (): string => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('themeId') || 'gruvbox-dark';
  }
  return 'gruvbox-dark';
};

export const setStoredThemeId = (id: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('themeId', id);
  }
}; 