import { createTheme } from '@mui/material/styles';
import type { Theme } from '@mui/material/styles';

export interface AppTheme {
  id: string;
  name: string;
  theme: Theme;
}

// Gruvbox Dark
const gruvboxDark = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#fb4934', // red
      light: '#fb4934',
      dark: '#cc241d',
    },
    secondary: {
      main: '#b8bb26', // green
      light: '#b8bb26',
      dark: '#98971a',
    },
    background: {
      default: '#282828',
      paper: '#3c3836',
    },
    text: {
      primary: '#ebdbb2',
      secondary: '#d5c4a1',
    },
    error: {
      main: '#fb4934',
    },
    warning: {
      main: '#fabd2f',
    },
    info: {
      main: '#83a598',
    },
    success: {
      main: '#b8bb26',
    },
  },
  typography: {
    fontFamily: '"Fira Code", "Roboto Mono", monospace, system-ui',
  },
});

// Gruvbox Light
const gruvboxLight = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#cc241d', // red
      light: '#fb4934',
      dark: '#9d0006',
    },
    secondary: {
      main: '#98971a', // green
      light: '#b8bb26',
      dark: '#79740e',
    },
    background: {
      default: '#fbf1c7',
      paper: '#ebdbb2',
    },
    text: {
      primary: '#3c3836',
      secondary: '#504945',
    },
    error: {
      main: '#cc241d',
    },
    warning: {
      main: '#d79921',
    },
    info: {
      main: '#458588',
    },
    success: {
      main: '#98971a',
    },
  },
  typography: {
    fontFamily: '"Fira Code", "Roboto Mono", monospace, system-ui',
  },
});

// Dracula
const dracula = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#bd93f9', // purple
      light: '#bd93f9',
      dark: '#8b69c1',
    },
    secondary: {
      main: '#50fa7b', // green
      light: '#50fa7b',
      dark: '#3ec855',
    },
    background: {
      default: '#282a36',
      paper: '#44475a',
    },
    text: {
      primary: '#f8f8f2',
      secondary: '#6272a4',
    },
    error: {
      main: '#ff5555',
    },
    warning: {
      main: '#f1fa8c',
    },
    info: {
      main: '#8be9fd',
    },
    success: {
      main: '#50fa7b',
    },
  },
  typography: {
    fontFamily: '"Fira Code", "Roboto Mono", monospace, system-ui',
  },
});

// Monokai
const monokai = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#f92672', // pink
      light: '#f92672',
      dark: '#c7004a',
    },
    secondary: {
      main: '#a6e22e', // green
      light: '#a6e22e',
      dark: '#7eb006',
    },
    background: {
      default: '#272822',
      paper: '#3e3d32',
    },
    text: {
      primary: '#f8f8f2',
      secondary: '#75715e',
    },
    error: {
      main: '#f92672',
    },
    warning: {
      main: '#e6db74',
    },
    info: {
      main: '#66d9ef',
    },
    success: {
      main: '#a6e22e',
    },
  },
  typography: {
    fontFamily: '"Fira Code", "Roboto Mono", monospace, system-ui',
  },
});

// Solarized Dark
const solarizedDark = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#268bd2', // blue
      light: '#268bd2',
      dark: '#1e6fa0',
    },
    secondary: {
      main: '#2aa198', // cyan
      light: '#2aa198',
      dark: '#227f76',
    },
    background: {
      default: '#002b36',
      paper: '#073642',
    },
    text: {
      primary: '#839496',
      secondary: '#586e75',
    },
    error: {
      main: '#dc322f',
    },
    warning: {
      main: '#b58900',
    },
    info: {
      main: '#268bd2',
    },
    success: {
      main: '#859900',
    },
  },
  typography: {
    fontFamily: '"Fira Code", "Roboto Mono", monospace, system-ui',
  },
});

// Solarized Light
const solarizedLight = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#268bd2', // blue
      light: '#4ca3e8',
      dark: '#1e6fa0',
    },
    secondary: {
      main: '#2aa198', // cyan
      light: '#52b9b0',
      dark: '#227f76',
    },
    background: {
      default: '#fdf6e3',
      paper: '#eee8d5',
    },
    text: {
      primary: '#657b83',
      secondary: '#93a1a1',
    },
    error: {
      main: '#dc322f',
    },
    warning: {
      main: '#b58900',
    },
    info: {
      main: '#268bd2',
    },
    success: {
      main: '#859900',
    },
  },
  typography: {
    fontFamily: '"Fira Code", "Roboto Mono", monospace, system-ui',
  },
});

// Nord
const nord = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#88c0d0', // frost blue
      light: '#88c0d0',
      dark: '#5e99a9',
    },
    secondary: {
      main: '#a3be8c', // green
      light: '#a3be8c',
      dark: '#7b9563',
    },
    background: {
      default: '#2e3440',
      paper: '#3b4252',
    },
    text: {
      primary: '#eceff4',
      secondary: '#d8dee9',
    },
    error: {
      main: '#bf616a',
    },
    warning: {
      main: '#ebcb8b',
    },
    info: {
      main: '#5e81ac',
    },
    success: {
      main: '#a3be8c',
    },
  },
  typography: {
    fontFamily: '"Fira Code", "Roboto Mono", monospace, system-ui',
  },
});

// One Dark
const oneDark = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#61afef', // blue
      light: '#61afef',
      dark: '#3987c7',
    },
    secondary: {
      main: '#98c379', // green
      light: '#98c379',
      dark: '#709b51',
    },
    background: {
      default: '#282c34',
      paper: '#2c323c',
    },
    text: {
      primary: '#abb2bf',
      secondary: '#5c6370',
    },
    error: {
      main: '#e06c75',
    },
    warning: {
      main: '#e5c07b',
    },
    info: {
      main: '#61afef',
    },
    success: {
      main: '#98c379',
    },
  },
  typography: {
    fontFamily: '"Fira Code", "Roboto Mono", monospace, system-ui',
  },
});

// Tokyo Night
const tokyoNight = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#7aa2f7', // blue
      light: '#7aa2f7',
      dark: '#527acf',
    },
    secondary: {
      main: '#9ece6a', // green
      light: '#9ece6a',
      dark: '#76a642',
    },
    background: {
      default: '#1a1b26',
      paper: '#24283b',
    },
    text: {
      primary: '#a9b1d6',
      secondary: '#787c99',
    },
    error: {
      main: '#f7768e',
    },
    warning: {
      main: '#e0af68',
    },
    info: {
      main: '#7aa2f7',
    },
    success: {
      main: '#9ece6a',
    },
  },
  typography: {
    fontFamily: '"Fira Code", "Roboto Mono", monospace, system-ui',
  },
});

// Material Dark (Default)
const materialDark = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

// Material Light (Default)
const materialLight = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

export const themes: AppTheme[] = [
  { id: 'gruvbox-dark', name: 'Gruvbox Dark', theme: gruvboxDark },
  { id: 'gruvbox-light', name: 'Gruvbox Light', theme: gruvboxLight },
  { id: 'dracula', name: 'Dracula', theme: dracula },
  { id: 'monokai', name: 'Monokai', theme: monokai },
  { id: 'solarized-dark', name: 'Solarized Dark', theme: solarizedDark },
  { id: 'solarized-light', name: 'Solarized Light', theme: solarizedLight },
  { id: 'nord', name: 'Nord', theme: nord },
  { id: 'one-dark', name: 'One Dark', theme: oneDark },
  { id: 'tokyo-night', name: 'Tokyo Night', theme: tokyoNight },
  { id: 'material-dark', name: 'Material Dark', theme: materialDark },
  { id: 'material-light', name: 'Material Light', theme: materialLight },
];

export const getThemeById = (id: string): AppTheme => {
  return themes.find(t => t.id === id) || themes[0];
};

export const getStoredThemeId = (): string => {
  return localStorage.getItem('themeId') || 'gruvbox-dark';
};

export const setStoredThemeId = (id: string): void => {
  localStorage.setItem('themeId', id);
}; 