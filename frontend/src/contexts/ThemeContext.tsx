import React, { useContext, useState, useEffect, useMemo } from 'react';
import type { ReactNode } from 'react';
import { ThemeProvider as MuiThemeProvider } from '@mui/material/styles';
import { themes } from '../themes';
import { getThemeById, getStoredThemeId, setStoredThemeId } from './ThemeUtils';
import { ThemeContext } from './ThemeUtils';

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [themeId, setThemeId] = useState(() => getStoredThemeId());
  const currentTheme = useMemo(() => getThemeById(themeId), [themeId]);

  useEffect(() => {
    setStoredThemeId(themeId);
  }, [themeId]);

  const setTheme = (newThemeId: string) => {
    setThemeId(newThemeId);
  };

  const value = {
    currentTheme,
    themeId,
    setTheme,
    availableThemes: themes,
  };

  return (
    <ThemeContext.Provider value={value}>
      <MuiThemeProvider theme={currentTheme.theme}>
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
}; 