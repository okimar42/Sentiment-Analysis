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
    primary: { main: '#fabd2f' },
    secondary: { main: '#83a598' },
    background: { default: '#282828', paper: '#3c3836' },
    text: { primary: '#ebdbb2', secondary: '#bdae93' },
  },
});

// Gruvbox Light
const gruvboxLight = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#b57614' },
    secondary: { main: '#458588' },
    background: { default: '#fbf1c7', paper: '#f2e5bc' },
    text: { primary: '#3c3836', secondary: '#7c6f64' },
  },
});

// Dracula
const dracula = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#bd93f9' },
    secondary: { main: '#ff79c6' },
    background: { default: '#282a36', paper: '#44475a' },
    text: { primary: '#f8f8f2', secondary: '#6272a4' },
  },
});

// Monokai
const monokai = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#f92672' },
    secondary: { main: '#a6e22e' },
    background: { default: '#272822', paper: '#383830' },
    text: { primary: '#f8f8f2', secondary: '#75715e' },
  },
});

// Solarized Dark
const solarizedDark = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#268bd2' },
    secondary: { main: '#2aa198' },
    background: { default: '#002b36', paper: '#073642' },
    text: { primary: '#eee8d5', secondary: '#93a1a1' },
  },
});

// Solarized Light
const solarizedLight = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#268bd2' },
    secondary: { main: '#2aa198' },
    background: { default: '#fdf6e3', paper: '#eee8d5' },
    text: { primary: '#657b83', secondary: '#586e75' },
  },
});

// Nord
const nord = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#8fbcbb' },
    secondary: { main: '#88c0d0' },
    background: { default: '#2e3440', paper: '#3b4252' },
    text: { primary: '#eceff4', secondary: '#d8dee9' },
  },
});

// One Dark
const oneDark = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#61afef' },
    secondary: { main: '#c678dd' },
    background: { default: '#282c34', paper: '#21252b' },
    text: { primary: '#abb2bf', secondary: '#5c6370' },
  },
});

// One Light
const oneLight = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#61afef' },
    secondary: { main: '#c678dd' },
    background: { default: '#fafafa', paper: '#e5e5e6' },
    text: { primary: '#383a42', secondary: '#a0a1a7' },
  },
});

// Night Owl
const nightOwl = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#82aaff' },
    secondary: { main: '#c792ea' },
    background: { default: '#011627', paper: '#1d3b53' },
    text: { primary: '#d6deeb', secondary: '#7e57c2' },
  },
});

// Cobalt2
const cobalt2 = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#39d9c8' },
    secondary: { main: '#ff9d00' },
    background: { default: '#193549', paper: '#132738' },
    text: { primary: '#ffffff', secondary: '#ff9d00' },
  },
});

// Material Dark
const materialDark = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#90caf9' },
    secondary: { main: '#f48fb1' },
    background: { default: '#121212', paper: '#1e1e1e' },
    text: { primary: '#ffffff', secondary: '#b0b0b0' },
  },
});

// Material Light
const materialLight = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#1976d2' },
    secondary: { main: '#d81b60' },
    background: { default: '#fafafa', paper: '#ffffff' },
    text: { primary: '#212121', secondary: '#757575' },
  },
});

// Ayu Dark
const ayuDark = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#ffcc66' },
    secondary: { main: '#36a3d9' },
    background: { default: '#0a0e14', paper: '#1f2430' },
    text: { primary: '#b3b1ad', secondary: '#5c6773' },
  },
});

// Ayu Light
const ayuLight = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#ffcc66' },
    secondary: { main: '#36a3d9' },
    background: { default: '#fcfcfc', paper: '#f8f8f8' },
    text: { primary: '#5c6773', secondary: '#b3b1ad' },
  },
});

// SynthWave '84
const synthwave84 = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#f92aad' },
    secondary: { main: '#08f7fe' },
    background: { default: '#2a2139', paper: '#1a1626' },
    text: { primary: '#f4f4f4', secondary: '#f92aad' },
  },
});

// Bullish Meme
const bullishMeme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#00ff41' },
    secondary: { main: '#ff0040' },
    background: { default: '#0d0d0d', paper: '#1a1a1a' },
    text: { primary: '#00ff41', secondary: '#ffff00' },
    error: { main: '#ff0040' },
    success: { main: '#00ff41' },
    warning: { main: '#ffa500' },
    info: { main: '#00bfff' },
  },
});

// Crypto Night
const cryptoNight = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#f7931a' },
    secondary: { main: '#627eea' },
    background: { default: '#0a0e27', paper: '#151a3a' },
    text: { primary: '#e4e4f0', secondary: '#a0a9d1' },
    error: { main: '#ff3864' },
    success: { main: '#00d4aa' },
    warning: { main: '#ffb700' },
    info: { main: '#b362ff' },
  },
});

// Wall Street Retro
const wallStreetRetro = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#003366' },
    secondary: { main: '#8b0000' },
    background: { default: '#f5f5dc', paper: '#fffef7' },
    text: { primary: '#1a1a1a', secondary: '#4a4a4a' },
    error: { main: '#8b0000' },
    success: { main: '#006400' },
    warning: { main: '#ff8c00' },
    info: { main: '#4682b4' },
  },
});

// VSCode Dark
const vscodeDark = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#569CD6' }, // blue
    secondary: { main: '#D7BA7D' }, // yellow
    background: { default: '#1e1e1e', paper: '#252526' },
    text: { primary: '#d4d4d4', secondary: '#cccccc' },
    error: { main: '#f44747' },
    success: { main: '#608B4E' },
    warning: { main: '#D7BA7D' },
    info: { main: '#9CDCFE' },
  },
});

// VSCode Light
const vscodeLight = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#0066b8' }, // blue
    secondary: { main: '#b89500' }, // yellow
    background: { default: '#ffffff', paper: '#f3f3f3' },
    text: { primary: '#333333', secondary: '#616161' },
    error: { main: '#e51400' },
    success: { main: '#16825d' },
    warning: { main: '#b89500' },
    info: { main: '#3794ff' },
  },
});

// Gruvbox Material Dark
const gruvboxMaterialDark = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#d8a657' },
    secondary: { main: '#a9b665' },
    background: { default: '#282828', paper: '#32302f' },
    text: { primary: '#ebdbb2', secondary: '#bdae93' },
    error: { main: '#ea6962' },
    success: { main: '#a9b665' },
    warning: { main: '#d8a657' },
    info: { main: '#7daea3' },
  },
});

// Gruvbox Material Light
const gruvboxMaterialLight = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#b47109' },
    secondary: { main: '#a9b665' },
    background: { default: '#fbf1c7', paper: '#f2e5bc' },
    text: { primary: '#3c3836', secondary: '#7c6f64' },
    error: { main: '#ea6962' },
    success: { main: '#a9b665' },
    warning: { main: '#d8a657' },
    info: { main: '#7daea3' },
  },
});

// Atom One Dark
const atomOneDark = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#61afef' },
    secondary: { main: '#98c379' },
    background: { default: '#282c34', paper: '#21252b' },
    text: { primary: '#abb2bf', secondary: '#5c6370' },
    error: { main: '#e06c75' },
    success: { main: '#98c379' },
    warning: { main: '#e5c07b' },
    info: { main: '#56b6c2' },
  },
});

// Atom One Light
const atomOneLight = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#61afef' },
    secondary: { main: '#98c379' },
    background: { default: '#fafafa', paper: '#e5e5e6' },
    text: { primary: '#383a42', secondary: '#a0a1a7' },
    error: { main: '#e06c75' },
    success: { main: '#98c379' },
    warning: { main: '#e5c07b' },
    info: { main: '#56b6c2' },
  },
});

// GitHub Dark
const githubDark = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#539bf5' },
    secondary: { main: '#6cb6ff' },
    background: { default: '#0d1117', paper: '#161b22' },
    text: { primary: '#c9d1d9', secondary: '#8b949e' },
    error: { main: '#ff7b72' },
    success: { main: '#3fb950' },
    warning: { main: '#d29922' },
    info: { main: '#58a6ff' },
  },
});

// GitHub Light
const githubLight = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#0969da' },
    secondary: { main: '#2188ff' },
    background: { default: '#ffffff', paper: '#f6f8fa' },
    text: { primary: '#24292f', secondary: '#57606a' },
    error: { main: '#cf222e' },
    success: { main: '#2da44e' },
    warning: { main: '#bf8700' },
    info: { main: '#0969da' },
  },
});

// Tokyo Night
const tokyoNight = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#7aa2f7' },
    secondary: { main: '#bb9af7' },
    background: { default: '#1a1b26', paper: '#24283b' },
    text: { primary: '#c0caf5', secondary: '#a9b1d6' },
    error: { main: '#f7768e' },
    success: { main: '#9ece6a' },
    warning: { main: '#e0af68' },
    info: { main: '#7dcfff' },
  },
});

// Tokyo Night Light
const tokyoNightLight = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#2e7de9' },
    secondary: { main: '#9854f1' },
    background: { default: '#d5d6db', paper: '#f3f3f3' },
    text: { primary: '#3760bf', secondary: '#6172b0' },
    error: { main: '#b15c6e' },
    success: { main: '#587539' },
    warning: { main: '#8c6c3e' },
    info: { main: '#2e7de9' },
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
  { id: 'one-light', name: 'One Light', theme: oneLight },
  { id: 'night-owl', name: 'Night Owl', theme: nightOwl },
  { id: 'cobalt2', name: 'Cobalt2', theme: cobalt2 },
  { id: 'material-dark', name: 'Material Dark', theme: materialDark },
  { id: 'material-light', name: 'Material Light', theme: materialLight },
  { id: 'ayu-dark', name: 'Ayu Dark', theme: ayuDark },
  { id: 'ayu-light', name: 'Ayu Light', theme: ayuLight },
  { id: 'synthwave84', name: "SynthWave '84", theme: synthwave84 },
  { id: 'bullish-meme', name: '🚀 Bullish Meme', theme: bullishMeme },
  { id: 'crypto-night', name: '₿ Crypto Night', theme: cryptoNight },
  { id: 'wall-street-retro', name: '📈 Wall Street Retro', theme: wallStreetRetro },
  { id: 'vscode-dark', name: 'VSCode Dark', theme: vscodeDark },
  { id: 'vscode-light', name: 'VSCode Light', theme: vscodeLight },
  { id: 'gruvbox-material-dark', name: 'Gruvbox Material Dark', theme: gruvboxMaterialDark },
  { id: 'gruvbox-material-light', name: 'Gruvbox Material Light', theme: gruvboxMaterialLight },
  { id: 'atom-one-dark', name: 'Atom One Dark', theme: atomOneDark },
  { id: 'atom-one-light', name: 'Atom One Light', theme: atomOneLight },
  { id: 'github-dark', name: 'GitHub Dark', theme: githubDark },
  { id: 'github-light', name: 'GitHub Light', theme: githubLight },
  { id: 'tokyo-night', name: 'Tokyo Night', theme: tokyoNight },
  { id: 'tokyo-night-light', name: 'Tokyo Night Light', theme: tokyoNightLight },
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