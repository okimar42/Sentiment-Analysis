import { createTheme } from '@mui/material/styles';

export type ThemeKey =
  | 'gruvboxDark'
  | 'gruvboxLight'
  | 'solarizedDark'
  | 'solarizedLight'
  | 'dracula'
  | 'nord'
  | 'oneDark'
  | 'oneLight'
  | 'nightOwl'
  | 'cobalt2'
  | 'materialDark'
  | 'materialLight'
  | 'ayuDark'
  | 'ayuLight'
  | 'synthwave84'
  | 'monokai'
  | 'bullishMeme'
  | 'cryptoNight'
  | 'wallStreetRetro';

export const themes: Record<ThemeKey, ReturnType<typeof createTheme>> = {
  gruvboxDark: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#fabd2f' },
      secondary: { main: '#83a598' },
      background: { default: '#282828', paper: '#3c3836' },
      text: { primary: '#ebdbb2', secondary: '#bdae93' },
    },
  }),
  gruvboxLight: createTheme({
    palette: {
      mode: 'light',
      primary: { main: '#b57614' },
      secondary: { main: '#458588' },
      background: { default: '#fbf1c7', paper: '#f2e5bc' },
      text: { primary: '#3c3836', secondary: '#7c6f64' },
    },
  }),
  solarizedDark: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#268bd2' },
      secondary: { main: '#2aa198' },
      background: { default: '#002b36', paper: '#073642' },
      text: { primary: '#eee8d5', secondary: '#93a1a1' },
    },
  }),
  solarizedLight: createTheme({
    palette: {
      mode: 'light',
      primary: { main: '#268bd2' },
      secondary: { main: '#2aa198' },
      background: { default: '#fdf6e3', paper: '#eee8d5' },
      text: { primary: '#657b83', secondary: '#586e75' },
    },
  }),
  dracula: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#bd93f9' },
      secondary: { main: '#ff79c6' },
      background: { default: '#282a36', paper: '#44475a' },
      text: { primary: '#f8f8f2', secondary: '#6272a4' },
    },
  }),
  nord: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#8fbcbb' },
      secondary: { main: '#88c0d0' },
      background: { default: '#2e3440', paper: '#3b4252' },
      text: { primary: '#eceff4', secondary: '#d8dee9' },
    },
  }),
  oneDark: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#61afef' },
      secondary: { main: '#c678dd' },
      background: { default: '#282c34', paper: '#21252b' },
      text: { primary: '#abb2bf', secondary: '#5c6370' },
    },
  }),
  oneLight: createTheme({
    palette: {
      mode: 'light',
      primary: { main: '#61afef' },
      secondary: { main: '#c678dd' },
      background: { default: '#fafafa', paper: '#e5e5e6' },
      text: { primary: '#383a42', secondary: '#a0a1a7' },
    },
  }),
  nightOwl: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#82aaff' },
      secondary: { main: '#c792ea' },
      background: { default: '#011627', paper: '#1d3b53' },
      text: { primary: '#d6deeb', secondary: '#7e57c2' },
    },
  }),
  cobalt2: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#39d9c8' },
      secondary: { main: '#ff9d00' },
      background: { default: '#193549', paper: '#132738' },
      text: { primary: '#ffffff', secondary: '#ff9d00' },
    },
  }),
  materialDark: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#90caf9' },
      secondary: { main: '#f48fb1' },
      background: { default: '#121212', paper: '#1e1e1e' },
      text: { primary: '#ffffff', secondary: '#b0b0b0' },
    },
  }),
  materialLight: createTheme({
    palette: {
      mode: 'light',
      primary: { main: '#1976d2' },
      secondary: { main: '#d81b60' },
      background: { default: '#fafafa', paper: '#ffffff' },
      text: { primary: '#212121', secondary: '#757575' },
    },
  }),
  ayuDark: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#ffcc66' },
      secondary: { main: '#36a3d9' },
      background: { default: '#0a0e14', paper: '#1f2430' },
      text: { primary: '#b3b1ad', secondary: '#5c6773' },
    },
  }),
  ayuLight: createTheme({
    palette: {
      mode: 'light',
      primary: { main: '#ffcc66' },
      secondary: { main: '#36a3d9' },
      background: { default: '#fcfcfc', paper: '#f8f8f8' },
      text: { primary: '#5c6773', secondary: '#b3b1ad' },
    },
  }),
  synthwave84: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#f92aad' },
      secondary: { main: '#08f7fe' },
      background: { default: '#2a2139', paper: '#1a1626' },
      text: { primary: '#f4f4f4', secondary: '#f92aad' },
    },
  }),
  monokai: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#f92672' },
      secondary: { main: '#a6e22e' },
      background: { default: '#272822', paper: '#383830' },
      text: { primary: '#f8f8f2', secondary: '#75715e' },
    },
  }),
  // Custom themes for Financial Sentiment Analysis
  bullishMeme: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#00ff41' }, // Bright green for gains
      secondary: { main: '#ff0040' }, // Red for losses
      background: { default: '#0d0d0d', paper: '#1a1a1a' }, // Dark like a trading terminal
      text: { primary: '#00ff41', secondary: '#ffff00' }, // Green primary, yellow for highlights (like WSB)
      error: { main: '#ff0040' }, // Red for bearish sentiment
      success: { main: '#00ff41' }, // Green for bullish sentiment
      warning: { main: '#ffa500' }, // Orange for neutral/caution
      info: { main: '#00bfff' }, // Cyan for bot detection
    },
  }),
  cryptoNight: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#f7931a' }, // Bitcoin orange
      secondary: { main: '#627eea' }, // Ethereum blue
      background: { default: '#0a0e27', paper: '#151a3a' }, // Deep space dark
      text: { primary: '#e4e4f0', secondary: '#a0a9d1' }, // Light text with purple tint
      error: { main: '#ff3864' }, // Neon red for negative sentiment
      success: { main: '#00d4aa' }, // Neon teal for positive sentiment
      warning: { main: '#ffb700' }, // Gold for neutral
      info: { main: '#b362ff' }, // Purple for special indicators
    },
  }),
  wallStreetRetro: createTheme({
    palette: {
      mode: 'light',
      primary: { main: '#003366' }, // Classic finance navy
      secondary: { main: '#8b0000' }, // Deep red for contrast
      background: { default: '#f5f5dc', paper: '#fffef7' }, // Beige like old terminals
      text: { primary: '#1a1a1a', secondary: '#4a4a4a' }, // High contrast black
      error: { main: '#8b0000' }, // Deep red for losses
      success: { main: '#006400' }, // Forest green for gains
      warning: { main: '#ff8c00' }, // Dark orange for warnings
      info: { main: '#4682b4' }, // Steel blue for information
    },
  }),
};

export const themeOptions: { key: ThemeKey; label: string }[] = [
  { key: 'gruvboxDark', label: 'Gruvbox Dark' },
  { key: 'gruvboxLight', label: 'Gruvbox Light' },
  { key: 'solarizedDark', label: 'Solarized Dark' },
  { key: 'solarizedLight', label: 'Solarized Light' },
  { key: 'dracula', label: 'Dracula' },
  { key: 'nord', label: 'Nord' },
  { key: 'oneDark', label: 'One Dark' },
  { key: 'oneLight', label: 'One Light' },
  { key: 'nightOwl', label: 'Night Owl' },
  { key: 'cobalt2', label: 'Cobalt2' },
  { key: 'materialDark', label: 'Material Dark' },
  { key: 'materialLight', label: 'Material Light' },
  { key: 'ayuDark', label: 'Ayu Dark' },
  { key: 'ayuLight', label: 'Ayu Light' },
  { key: 'synthwave84', label: "SynthWave '84" },
  { key: 'monokai', label: 'Monokai' },
  { key: 'bullishMeme', label: '🚀 Bullish Meme' },
  { key: 'cryptoNight', label: '₿ Crypto Night' },
  { key: 'wallStreetRetro', label: '📈 Wall Street Retro' },
]; 