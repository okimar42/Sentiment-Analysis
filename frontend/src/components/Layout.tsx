import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, Outlet } from 'react-router-dom';
import {
  AppBar,
  Box,
  CssBaseline,
  Drawer,
  IconButton,
  List,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Button,
  Menu,
  MenuItem,
  Tooltip
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Add as AddIcon,
  ExitToApp as LogoutIcon,
  Check as CheckIcon,
  UploadFile as UploadFileIcon,
  Download as DownloadIcon
} from '@mui/icons-material';
import type { ReactNode } from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import { useTheme } from '../contexts/ThemeContext';
import type { AppTheme } from '../themes';
import PaletteIcon from '@mui/icons-material/Palette';
import NightsStayIcon from '@mui/icons-material/NightsStay';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import SearchIcon from '@mui/icons-material/Search';
import StarIcon from '@mui/icons-material/Star';
import StarBorderIcon from '@mui/icons-material/StarBorder';

const drawerWidth = 240;

interface LayoutProps {
  children?: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [themeMenuAnchor, setThemeMenuAnchor] = useState<null | HTMLElement>(null);
  const navigate = useNavigate();
  const { themeId, setTheme, availableThemes } = useTheme();
  const [themeSearch, setThemeSearch] = useState('');
  const [favoriteThemes, setFavoriteThemes] = useState<string[]>(() => {
    try {
      return JSON.parse(localStorage.getItem('favoriteThemes') || '[]');
    } catch {
      return [];
    }
  });

  // Import/export state
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [importError, setImportError] = useState<string | null>(null);
  const [customThemes, setCustomThemes] = useState<AppTheme[]>([]);

  // Preview-on-hover state
  const [hoveredTheme, setHoveredTheme] = useState<AppTheme | null>(null);
  const [lastSelectedThemeId, setLastSelectedThemeId] = useState<string>(themeId);

  // Merge custom themes with available themes
  const allThemes = [...availableThemes, ...customThemes];

  useEffect(() => {
    localStorage.setItem('favoriteThemes', JSON.stringify(favoriteThemes));
  }, [favoriteThemes]);

  const toggleFavorite = (themeId: string) => {
    setFavoriteThemes(favs =>
      favs.includes(themeId) ? favs.filter(id => id !== themeId) : [...favs, themeId]
    );
  };

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleThemeMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setThemeMenuAnchor(event.currentTarget);
  };

  const handleThemeMenuClose = () => {
    setThemeMenuAnchor(null);
    setHoveredTheme(null);
  };

  const handleThemeSelect = (selectedThemeId: string) => {
    setTheme(selectedThemeId);
    setHoveredTheme(null);
    handleThemeMenuClose();
  };

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
    { text: 'New Analysis', icon: <AddIcon />, path: '/new-analysis' },
  ];

  const drawer = (
    <div>
      <Toolbar />
      <List>
        {menuItems.map((item) => (
          <ListItemButton
            key={item.text}
            onClick={() => navigate(item.path)}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItemButton>
        ))}
        <ListItemButton onClick={() => navigate('/login')}>
          <ListItemIcon><LogoutIcon /></ListItemIcon>
          <ListItemText primary="Logout" />
        </ListItemButton>
      </List>
    </div>
  );

  // Group themes by light/dark
  const lightThemes = availableThemes.filter(t => t.theme.palette.mode === 'light');
  const darkThemes = availableThemes.filter(t => t.theme.palette.mode === 'dark');
  const currentThemeName = availableThemes.find(t => t.id === themeId)?.name || 'Theme';

  // Filter themes by search
  const filterThemes = (themes: AppTheme[]) =>
    themes.filter(t => t.name.toLowerCase().includes(themeSearch.toLowerCase()));
  const filteredLightThemes = filterThemes(lightThemes);
  const filteredDarkThemes = filterThemes(darkThemes);

  // Add a small color swatch for theme preview
  const ThemeSwatch: React.FC<{ theme: AppTheme }> = ({ theme }) => (
    <span style={{
      display: 'inline-block',
      width: 28,
      height: 18,
      borderRadius: 4,
      marginRight: 8,
      verticalAlign: 'middle',
      boxShadow: '0 0 0 1px #8884',
      background: `linear-gradient(90deg, ${theme.theme.palette.primary.main} 0 33%, ${theme.theme.palette.secondary.main} 33% 66%, ${theme.theme.palette.background.default} 66% 100%)`
    }} />
  );

  // Group themes by category using the new 'category' property
  function groupThemes(themes: AppTheme[]) {
    const groups: { [cat: string]: AppTheme[] } = {};
    for (const t of themes) {
      const cat = t.category || 'Other';
      if (!groups[cat]) groups[cat] = [];
      groups[cat].push(t);
    }
    return groups;
  }

  // Group filtered themes by category
  const groupedLightThemes = groupThemes(filteredLightThemes);
  const groupedDarkThemes = groupThemes(filteredDarkThemes);

  // Get favorite theme objects
  const favoriteThemeObjs = availableThemes.filter(t => favoriteThemes.includes(t.id));

  // Handle import
  const handleImportTheme = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      try {
        const data = JSON.parse(ev.target?.result as string);
        if (!data || !data.theme || !data.id || !data.name) throw new Error('Invalid theme format');
        // Ensure unique id
        const uniqueId = data.id + '-' + Date.now();
        setCustomThemes(ts => [...ts, { ...data, id: uniqueId, name: data.name + ' (Imported)' }]);
        setImportError(null);
      } catch (err: unknown) {
        let message = 'Unknown error';
        if (err instanceof Error) message = err.message;
        setImportError('Failed to import theme: ' + message);
      }
    };
    reader.readAsText(file);
  };

  // Handle export
  const handleExportTheme = () => {
    const theme = allThemes.find(t => t.id === themeId);
    if (!theme) return;
    const blob = new Blob([JSON.stringify(theme, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${theme.name.replace(/\s+/g, '_')}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // When themeId changes (via selection), update lastSelectedThemeId
  useEffect(() => {
    setLastSelectedThemeId(themeId);
  }, [themeId]);

  // Apply preview-on-hover (temporary only)
  useEffect(() => {
    if (hoveredTheme) {
      setTheme(hoveredTheme.id);
    } else {
      // Restore the last selected theme when not hovering
      setTheme(lastSelectedThemeId);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hoveredTheme]);

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            Financial Sentiment Analysis
          </Typography>
          <Button
            color="inherit"
            onClick={handleThemeMenuOpen}
            aria-controls={themeMenuAnchor ? 'theme-menu' : undefined}
            aria-haspopup="true"
            aria-expanded={!!themeMenuAnchor}
            aria-label="Open theme picker"
            startIcon={<CheckIcon sx={{ opacity: 0, width: 0 }} />}
            tabIndex={0}
            onKeyDown={(e: React.KeyboardEvent<HTMLElement>) => {
              if ((e.key === 'Enter' || e.key === ' ') && !themeMenuAnchor) {
                setThemeMenuAnchor(e.currentTarget);
              }
            }}
          >
            {currentThemeName}
          </Button>
          <Menu
            id="theme-menu"
            anchorEl={themeMenuAnchor}
            open={!!themeMenuAnchor}
            onClose={handleThemeMenuClose}
            PaperProps={{ sx: { minWidth: 240 }, 'aria-label': 'Theme selection menu' }}
            MenuListProps={{
              'aria-label': 'Theme selection',
              autoFocus: true,
              tabIndex: 0,
              onKeyDown: (e: React.KeyboardEvent) => {
                if (e.key === 'Escape') handleThemeMenuClose();
              },
            }}
          >
            <Box sx={{ p: 1 }}>
              <TextField
                size="small"
                fullWidth
                placeholder="Search themes..."
                value={themeSearch}
                onChange={e => setThemeSearch(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon fontSize="small" />
                    </InputAdornment>
                  ),
                  'aria-label': 'Search themes',
                }}
              />
            </Box>
            {/* Import/Export Buttons */}
            <Box display="flex" alignItems="center" justifyContent="space-between" px={2} py={1}>
              <Tooltip title="Import Theme">
                <span>
                  <UploadFileIcon
                    fontSize="small"
                    style={{ cursor: 'pointer', marginRight: 8 }}
                    onClick={() => fileInputRef.current?.click()}
                    aria-label="Import Theme"
                    tabIndex={0}
                  />
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="application/json"
                    style={{ display: 'none' }}
                    onChange={handleImportTheme}
                  />
                </span>
              </Tooltip>
              <Tooltip title="Export Current Theme">
                <span>
                  <DownloadIcon
                    fontSize="small"
                    style={{ cursor: 'pointer' }}
                    onClick={handleExportTheme}
                    aria-label="Export Theme"
                    tabIndex={0}
                  />
                </span>
              </Tooltip>
            </Box>
            {importError && <Box color="error.main" px={2} fontSize={12}>{importError}</Box>}
            {/* Favorites Section */}
            {favoriteThemeObjs.length > 0 && (
              <>
                <MenuItem disabled key="favorites-header" style={{ fontWeight: 700, opacity: 0.7 }}>
                  Favorites
                </MenuItem>
                {favoriteThemeObjs.map(theme => (
                  <MenuItem
                    key={theme.id}
                    onClick={() => handleThemeSelect(theme.id)}
                    selected={theme.id === themeId}
                    aria-label={`Select ${theme.name} theme`}
                    onMouseEnter={() => setHoveredTheme(theme)}
                    onMouseLeave={() => setHoveredTheme(null)}
                  >
                    {theme.theme.palette.mode === 'dark' ? <NightsStayIcon fontSize="small" style={{ marginRight: 4 }} /> : <PaletteIcon fontSize="small" style={{ marginRight: 4 }} />}
                    <ThemeSwatch theme={theme} />
                    {theme.name}
                    <span style={{ flex: 1 }} />
                    <span onClick={e => { e.stopPropagation(); toggleFavorite(theme.id); }} style={{ marginLeft: 8, cursor: 'pointer' }} aria-label={favoriteThemes.includes(theme.id) ? 'Unfavorite' : 'Favorite'} tabIndex={0}>
                      {favoriteThemes.includes(theme.id) ? <StarIcon fontSize="small" color="warning" /> : <StarBorderIcon fontSize="small" />}
                    </span>
                  </MenuItem>
                ))}
                <MenuItem disabled divider style={{ margin: '4px 0' }} />
              </>
            )}
            {/* Light Themes by Category */}
            {Object.entries(groupedLightThemes).map(([cat, themes]) => (
              <>
                <MenuItem disabled key={cat + '-light'} style={{ fontWeight: 700, opacity: 0.7 }}>
                  {cat} (Light)
                </MenuItem>
                {themes.map(theme => (
                  <MenuItem
                    key={theme.id}
                    onClick={() => handleThemeSelect(theme.id)}
                    selected={theme.id === themeId}
                    aria-label={`Select ${theme.name} theme`}
                    onMouseEnter={() => setHoveredTheme(theme)}
                    onMouseLeave={() => setHoveredTheme(null)}
                  >
                    {theme.theme.palette.mode === 'dark' ? <NightsStayIcon fontSize="small" style={{ marginRight: 4 }} /> : <PaletteIcon fontSize="small" style={{ marginRight: 4 }} />}
                    <ThemeSwatch theme={theme} />
                    {theme.name}
                    <span style={{ flex: 1 }} />
                    <span onClick={e => { e.stopPropagation(); toggleFavorite(theme.id); }} style={{ marginLeft: 8, cursor: 'pointer' }} aria-label={favoriteThemes.includes(theme.id) ? 'Unfavorite' : 'Favorite'} tabIndex={0}>
                      {favoriteThemes.includes(theme.id) ? <StarIcon fontSize="small" color="warning" /> : <StarBorderIcon fontSize="small" />}
                    </span>
                  </MenuItem>
                ))}
              </>
            ))}
            {/* Dark Themes by Category */}
            {Object.entries(groupedDarkThemes).map(([cat, themes]) => (
              <>
                <MenuItem disabled key={cat + '-dark'} style={{ fontWeight: 700, opacity: 0.7 }}>
                  {cat} (Dark)
                </MenuItem>
                {themes.map(theme => (
                  <MenuItem
                    key={theme.id}
                    onClick={() => handleThemeSelect(theme.id)}
                    selected={theme.id === themeId}
                    aria-label={`Select ${theme.name} theme`}
                    onMouseEnter={() => setHoveredTheme(theme)}
                    onMouseLeave={() => setHoveredTheme(null)}
                  >
                    {theme.theme.palette.mode === 'dark' ? <NightsStayIcon fontSize="small" style={{ marginRight: 4 }} /> : <PaletteIcon fontSize="small" style={{ marginRight: 4 }} />}
                    <ThemeSwatch theme={theme} />
                    {theme.name}
                    <span style={{ flex: 1 }} />
                    <span onClick={e => { e.stopPropagation(); toggleFavorite(theme.id); }} style={{ marginLeft: 8, cursor: 'pointer' }} aria-label={favoriteThemes.includes(theme.id) ? 'Unfavorite' : 'Favorite'} tabIndex={0}>
                      {favoriteThemes.includes(theme.id) ? <StarIcon fontSize="small" color="warning" /> : <StarBorderIcon fontSize="small" />}
                    </span>
                  </MenuItem>
                ))}
              </>
            ))}
          </Menu>
          <Button color="inherit" onClick={() => navigate('/login')}>
            Login
          </Button>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
        }}
      >
        <Toolbar />
        {typeof children !== 'undefined' ? children : null}
        <Outlet />
      </Box>
    </Box>
  );
};

export default Layout; 