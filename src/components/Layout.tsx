import React, { useState } from 'react';
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
  Divider,
  ListSubheader,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Add as AddIcon,
  ExitToApp as LogoutIcon,
  Palette as PaletteIcon,
  Check as CheckIcon,
} from '@mui/icons-material';
import type { ReactNode } from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import { useTheme } from '../contexts/ThemeContext';

const drawerWidth = 240;

interface LayoutProps {
  children?: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [themeMenuAnchor, setThemeMenuAnchor] = useState<null | HTMLElement>(null);
  const navigate = useNavigate();
  const { currentTheme, themeId, setTheme, availableThemes } = useTheme();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleThemeMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setThemeMenuAnchor(event.currentTarget);
  };

  const handleThemeMenuClose = () => {
    setThemeMenuAnchor(null);
  };

  const handleThemeSelect = (selectedThemeId: string) => {
    setTheme(selectedThemeId);
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
            startIcon={<PaletteIcon />}
            onClick={handleThemeMenuOpen}
            sx={{ mr: 1 }}
          >
            {currentTheme.name}
          </Button>
          <Menu
            anchorEl={themeMenuAnchor}
            open={Boolean(themeMenuAnchor)}
            onClose={handleThemeMenuClose}
            PaperProps={{
              sx: { minWidth: 200 }
            }}
          >
            {darkThemes.length > 0 && (
              <>
                <ListSubheader>Dark Themes</ListSubheader>
                {darkThemes.map((theme) => (
                  <MenuItem
                    key={theme.id}
                    onClick={() => handleThemeSelect(theme.id)}
                    selected={theme.id === themeId}
                  >
                    {theme.id === themeId && <CheckIcon fontSize="small" sx={{ mr: 1 }} />}
                    <span style={{ marginLeft: theme.id === themeId ? 0 : 28 }}>
                      {theme.name}
                    </span>
                  </MenuItem>
                ))}
              </>
            )}
            {darkThemes.length > 0 && lightThemes.length > 0 && <Divider />}
            {lightThemes.length > 0 && (
              <>
                <ListSubheader>Light Themes</ListSubheader>
                {lightThemes.map((theme) => (
                  <MenuItem
                    key={theme.id}
                    onClick={() => handleThemeSelect(theme.id)}
                    selected={theme.id === themeId}
                  >
                    {theme.id === themeId && <CheckIcon fontSize="small" sx={{ mr: 1 }} />}
                    <span style={{ marginLeft: theme.id === themeId ? 0 : 28 }}>
                      {theme.name}
                    </span>
                  </MenuItem>
                ))}
              </>
            )}
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
}

export default Layout; 