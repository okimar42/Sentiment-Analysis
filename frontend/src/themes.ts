import { createTheme } from '@mui/material/styles';
import type { Theme } from '@mui/material/styles';

export interface AppTheme {
  id: string;
  name: string;
  theme: Theme;
  category: string;
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

// Bloomberg Terminal
const bloombergTerminal = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#00FF41' }, // neon green
    secondary: { main: '#FFD700' }, // yellow
    background: { default: '#101010', paper: '#181818' },
    text: { primary: '#00FF41', secondary: '#FFD700' },
    error: { main: '#FF3131' },
    success: { main: '#00FF41' },
    warning: { main: '#FFD700' },
    info: { main: '#00BFFF' },
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

// Editor Themes
const sublimeText = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#ff9800' },
    secondary: { main: '#272822' },
    background: { default: '#23241f', paper: '#272822' },
    text: { primary: '#f8f8f2', secondary: '#75715e' },
  },
});
const jetBrains = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#ff2c6d' },
    secondary: { main: '#20e3b2' },
    background: { default: '#2b2b2b', paper: '#323232' },
    text: { primary: '#a9b7c6', secondary: '#808080' },
  },
});
const notepadPlus = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#8dc63f' },
    secondary: { main: '#ffffff' },
    background: { default: '#f5f5f5', paper: '#e0e0e0' },
    text: { primary: '#333333', secondary: '#8dc63f' },
  },
});
const emacs = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#7f7fff' },
    secondary: { main: '#ff7f7f' },
    background: { default: '#f6f6f6', paper: '#eaeaea' },
    text: { primary: '#22223b', secondary: '#7f7fff' },
  },
});
const vim = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#019833' },
    secondary: { main: '#f7e017' },
    background: { default: '#282828', paper: '#1d2021' },
    text: { primary: '#ebdbb2', secondary: '#b8bb26' },
  },
});

// OS Themes
const windows = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#0078d7' },
    secondary: { main: '#f3f3f3' },
    background: { default: '#ffffff', paper: '#f3f3f3' },
    text: { primary: '#222222', secondary: '#0078d7' },
  },
});
const macos = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#007aff' },
    secondary: { main: '#f5f5f7' },
    background: { default: '#f5f5f7', paper: '#ffffff' },
    text: { primary: '#222222', secondary: '#007aff' },
  },
});
const ios = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#0a84ff' },
    secondary: { main: '#f2f2f7' },
    background: { default: '#f2f2f7', paper: '#ffffff' },
    text: { primary: '#222222', secondary: '#0a84ff' },
  },
});
const android = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#3ddc84' },
    secondary: { main: '#fafafa' },
    background: { default: '#fafafa', paper: '#ffffff' },
    text: { primary: '#222222', secondary: '#3ddc84' },
  },
});
const ubuntu = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#e95420' },
    secondary: { main: '#77216f' },
    background: { default: '#2c001e', paper: '#77216f' },
    text: { primary: '#ffffff', secondary: '#e95420' },
  },
});
const mint = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#87cf3e' },
    secondary: { main: '#ffffff' },
    background: { default: '#e8f5e9', paper: '#ffffff' },
    text: { primary: '#222222', secondary: '#87cf3e' },
  },
});

// Brand Themes
const facebook = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#1877f3' },
    secondary: { main: '#f5f6fa' },
    background: { default: '#f5f6fa', paper: '#ffffff' },
    text: { primary: '#222222', secondary: '#1877f3' },
  },
});
const twitter = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#1da1f2' },
    secondary: { main: '#e1e8ed' },
    background: { default: '#e1e8ed', paper: '#ffffff' },
    text: { primary: '#222222', secondary: '#1da1f2' },
  },
});
const discord = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#5865f2' },
    secondary: { main: '#23272a' },
    background: { default: '#23272a', paper: '#2c2f33' },
    text: { primary: '#ffffff', secondary: '#5865f2' },
  },
});
const slack = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#611f69' },
    secondary: { main: '#ecb22e' },
    background: { default: '#f8f8f8', paper: '#ffffff' },
    text: { primary: '#222222', secondary: '#611f69' },
  },
});
const spotify = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#1db954' },
    secondary: { main: '#191414' },
    background: { default: '#191414', paper: '#282828' },
    text: { primary: '#ffffff', secondary: '#1db954' },
  },
});
const apple = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#a2aaad' },
    secondary: { main: '#f5f5f7' },
    background: { default: '#f5f5f7', paper: '#ffffff' },
    text: { primary: '#222222', secondary: '#a2aaad' },
  },
});
const google = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#4285f4' },
    secondary: { main: '#fbbc05' },
    background: { default: '#ffffff', paper: '#f8f9fa' },
    text: { primary: '#222222', secondary: '#4285f4' },
  },
});

// Nature Themes
const forest = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#228b22' },
    secondary: { main: '#a3c9a8' },
    background: { default: '#183a1d', paper: '#2e5339' },
    text: { primary: '#e6f2e6', secondary: '#a3c9a8' },
  },
});
const ocean = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#1976d2' },
    secondary: { main: '#00bcd4' },
    background: { default: '#0a192f', paper: '#112240' },
    text: { primary: '#e0f7fa', secondary: '#b3e5fc' },
  },
});
const sunset = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#ff7043' },
    secondary: { main: '#ffd54f' },
    background: { default: '#fff3e0', paper: '#ffe0b2' },
    text: { primary: '#6d4c41', secondary: '#ff7043' },
  },
});
const desert = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#e1ad01' },
    secondary: { main: '#f9d29d' },
    background: { default: '#f9e4b7', paper: '#f9d29d' },
    text: { primary: '#7c4700', secondary: '#e1ad01' },
  },
});
const mountain = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#6b7a8f' },
    secondary: { main: '#b8a47e' },
    background: { default: '#2e3c4f', paper: '#3e4c5f' },
    text: { primary: '#e0e6ed', secondary: '#b8a47e' },
  },
});

// Fun/Trendy Themes
const neon = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#39ff14' },
    secondary: { main: '#ff0266' },
    background: { default: '#0f0f0f', paper: '#1a1a1a' },
    text: { primary: '#ffffff', secondary: '#39ff14' },
  },
});
const cyberpunk = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#ff0090' },
    secondary: { main: '#00fff7' },
    background: { default: '#1a0033', paper: '#2d004d' },
    text: { primary: '#fff', secondary: '#ff0090' },
  },
});
const pastel = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#a3c9a8' },
    secondary: { main: '#f7cac9' },
    background: { default: '#f9f6f7', paper: '#fff' },
    text: { primary: '#4a4a4a', secondary: '#a3a3a3' },
  },
});
const vaporwave = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#ff71ce' },
    secondary: { main: '#01cdfe' },
    background: { default: '#232946', paper: '#393e46' },
    text: { primary: '#fff', secondary: '#ff71ce' },
  },
});
const candy = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#ffb6b9' },
    secondary: { main: '#fae3d9' },
    background: { default: '#fff', paper: '#fae3d9' },
    text: { primary: '#6a0572', secondary: '#ffb6b9' },
  },
});
const halloween = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#ff7518' },
    secondary: { main: '#2e2e2e' },
    background: { default: '#2e2e2e', paper: '#1a1a1a' },
    text: { primary: '#fff', secondary: '#ff7518' },
  },
});
const christmas = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#d7263d' },
    secondary: { main: '#a2d5c6' },
    background: { default: '#fff', paper: '#a2d5c6' },
    text: { primary: '#1b1b1b', secondary: '#d7263d' },
  },
});
const valentine = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#ff6f91' },
    secondary: { main: '#ffb6b9' },
    background: { default: '#fff0f3', paper: '#ffb6b9' },
    text: { primary: '#6a0572', secondary: '#ff6f91' },
  },
});
const rainbow = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#ff595e' },
    secondary: { main: '#ffca3a' },
    background: { default: '#8ac926', paper: '#1982c4' },
    text: { primary: '#6a0572', secondary: '#ff595e' },
  },
});
const highContrast = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#ffffff' },
    secondary: { main: '#000000' },
    background: { default: '#000000', paper: '#222222' },
    text: { primary: '#ffffff', secondary: '#ffff00' },
  },
});

export const themes: AppTheme[] = [
  { id: 'gruvbox-dark', name: 'Gruvbox Dark', theme: gruvboxDark, category: 'Classic' },
  { id: 'gruvbox-light', name: 'Gruvbox Light', theme: gruvboxLight, category: 'Classic' },
  { id: 'dracula', name: 'Dracula', theme: dracula, category: 'Classic' },
  { id: 'monokai', name: 'Monokai', theme: monokai, category: 'Classic' },
  { id: 'solarized-dark', name: 'Solarized Dark', theme: solarizedDark, category: 'Classic' },
  { id: 'solarized-light', name: 'Solarized Light', theme: solarizedLight, category: 'Classic' },
  { id: 'nord', name: 'Nord', theme: nord, category: 'Classic' },
  { id: 'one-dark', name: 'One Dark', theme: oneDark, category: 'Classic' },
  { id: 'one-light', name: 'One Light', theme: oneLight, category: 'Classic' },
  { id: 'night-owl', name: 'Night Owl', theme: nightOwl, category: 'Classic' },
  { id: 'cobalt2', name: 'Cobalt2', theme: cobalt2, category: 'Classic' },
  { id: 'material-dark', name: 'Material Dark', theme: materialDark, category: 'Classic' },
  { id: 'material-light', name: 'Material Light', theme: materialLight, category: 'Classic' },
  { id: 'ayu-dark', name: 'Ayu Dark', theme: ayuDark, category: 'Classic' },
  { id: 'ayu-light', name: 'Ayu Light', theme: ayuLight, category: 'Classic' },
  { id: 'synthwave84', name: "SynthWave '84", theme: synthwave84, category: 'Classic' },
  { id: 'bloomberg-terminal', name: 'Bloomberg Terminal', theme: bloombergTerminal, category: 'Classic' },
  { id: 'bullish-meme', name: '🚀 Bullish Meme', theme: bullishMeme, category: 'Fun/Trendy' },
  { id: 'crypto-night', name: '₿ Crypto Night', theme: cryptoNight, category: 'Fun/Trendy' },
  { id: 'wall-street-retro', name: '📈 Wall Street Retro', theme: wallStreetRetro, category: 'Fun/Trendy' },
  { id: 'vscode-dark', name: 'VSCode Dark', theme: vscodeDark, category: 'Classic' },
  { id: 'vscode-light', name: 'VSCode Light', theme: vscodeLight, category: 'Classic' },
  { id: 'gruvbox-material-dark', name: 'Gruvbox Material Dark', theme: gruvboxMaterialDark, category: 'Classic' },
  { id: 'gruvbox-material-light', name: 'Gruvbox Material Light', theme: gruvboxMaterialLight, category: 'Classic' },
  { id: 'atom-one-dark', name: 'Atom One Dark', theme: atomOneDark, category: 'Classic' },
  { id: 'atom-one-light', name: 'Atom One Light', theme: atomOneLight, category: 'Classic' },
  { id: 'github-dark', name: 'GitHub Dark', theme: githubDark, category: 'Classic' },
  { id: 'github-light', name: 'GitHub Light', theme: githubLight, category: 'Classic' },
  { id: 'tokyo-night', name: 'Tokyo Night', theme: tokyoNight, category: 'Classic' },
  { id: 'tokyo-night-light', name: 'Tokyo Night Light', theme: tokyoNightLight, category: 'Classic' },
  { id: 'sublime-text', name: 'Sublime Text', theme: sublimeText, category: 'Classic' },
  { id: 'jetbrains', name: 'JetBrains', theme: jetBrains, category: 'Classic' },
  { id: 'notepad-plus', name: 'Notepad++', theme: notepadPlus, category: 'Classic' },
  { id: 'emacs', name: 'Emacs', theme: emacs, category: 'Classic' },
  { id: 'vim', name: 'Vim', theme: vim, category: 'Classic' },
  { id: 'windows', name: 'Windows', theme: windows, category: 'OS' },
  { id: 'macos', name: 'macOS', theme: macos, category: 'OS' },
  { id: 'ios', name: 'iOS', theme: ios, category: 'OS' },
  { id: 'android', name: 'Android', theme: android, category: 'OS' },
  { id: 'ubuntu', name: 'Ubuntu', theme: ubuntu, category: 'OS' },
  { id: 'mint', name: 'Mint', theme: mint, category: 'OS' },
  { id: 'facebook', name: 'Facebook', theme: facebook, category: 'Brand' },
  { id: 'twitter', name: 'Twitter', theme: twitter, category: 'Brand' },
  { id: 'discord', name: 'Discord', theme: discord, category: 'Brand' },
  { id: 'slack', name: 'Slack', theme: slack, category: 'Brand' },
  { id: 'spotify', name: 'Spotify', theme: spotify, category: 'Brand' },
  { id: 'apple', name: 'Apple', theme: apple, category: 'Brand' },
  { id: 'google', name: 'Google', theme: google, category: 'Brand' },
  { id: 'forest', name: 'Forest', theme: forest, category: 'Nature' },
  { id: 'ocean', name: 'Ocean', theme: ocean, category: 'Nature' },
  { id: 'sunset', name: 'Sunset', theme: sunset, category: 'Nature' },
  { id: 'desert', name: 'Desert', theme: desert, category: 'Nature' },
  { id: 'mountain', name: 'Mountain', theme: mountain, category: 'Nature' },
  { id: 'neon', name: 'Neon', theme: neon, category: 'Fun/Trendy' },
  { id: 'cyberpunk', name: 'Cyberpunk', theme: cyberpunk, category: 'Fun/Trendy' },
  { id: 'pastel', name: 'Pastel', theme: pastel, category: 'Fun/Trendy' },
  { id: 'vaporwave', name: 'Vaporwave', theme: vaporwave, category: 'Fun/Trendy' },
  { id: 'candy', name: 'Candy', theme: candy, category: 'Fun/Trendy' },
  { id: 'halloween', name: 'Halloween', theme: halloween, category: 'Fun/Trendy' },
  { id: 'christmas', name: 'Christmas', theme: christmas, category: 'Fun/Trendy' },
  { id: 'valentine', name: 'Valentine', theme: valentine, category: 'Fun/Trendy' },
  { id: 'rainbow', name: 'Rainbow', theme: rainbow, category: 'Fun/Trendy' },
  { id: 'high-contrast', name: 'High Contrast', theme: highContrast, category: 'High Contrast' },
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