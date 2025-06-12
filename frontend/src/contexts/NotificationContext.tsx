/* eslint-disable react-refresh/only-export-components */
import React, { createContext, useContext, useState, useCallback } from 'react';
import type { ReactNode } from 'react';
import { Snackbar, Alert, Slide } from '@mui/material';
import type { SlideProps } from '@mui/material/Slide';
import type { AlertProps } from '@mui/material/Alert';

type AlertColor = AlertProps['severity'];

interface Notification {
  id: string;
  message: string;
  severity: AlertColor;
  duration?: number;
  action?: ReactNode;
}

interface NotificationContextType {
  showNotification: (message: string, severity?: AlertColor, duration?: number, action?: ReactNode) => string;
  showProcessingStart: (processName: string) => string;
  showProcessingComplete: (processName: string, processId?: string, success?: boolean) => void;
  hideNotification: (id: string) => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

function SlideTransition(props: SlideProps) {
  return <Slide {...props} direction="up" />;
}

interface NotificationProviderProps {
  children: ReactNode;
  defaultDuration?: number;
  maxNotifications?: number;
}

export const NotificationProvider: React.FC<NotificationProviderProps> = ({ 
  children, 
  defaultDuration = 4000,
  maxNotifications = 3 
}) => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [processingTasks, setProcessingTasks] = useState<Map<string, string>>(new Map());

  const generateId = () => `notification-${Date.now()}-${Math.random()}`;

  const showNotification = useCallback((
    message: string, 
    severity: AlertColor = 'info', 
    duration?: number,
    action?: ReactNode
  ) => {
    const id = generateId();
    const newNotification: Notification = {
      id,
      message,
      severity,
      duration: duration ?? defaultDuration,
      action
    };

    setNotifications(prev => {
      // Keep only the most recent notifications
      const updated = [...prev, newNotification];
      if (updated.length > maxNotifications) {
        return updated.slice(-maxNotifications);
      }
      return updated;
    });

    return id;
  }, [defaultDuration, maxNotifications]);

  const showProcessingStart = useCallback((processName: string) => {
    const processId = generateId();
    setProcessingTasks(prev => new Map(prev).set(processId, processName));
    
    const notificationId = showNotification(
      `🚀 Started ${processName}...`,
      'info',
      undefined // undefined duration means it stays until explicitly closed
    );
    
    // Store the notification ID with the process ID for later reference
    setProcessingTasks(prev => new Map(prev).set(processId, notificationId));
    
    return processId;
  }, [showNotification]);

  const hideNotification = useCallback((id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  }, []);

  const showProcessingComplete = useCallback((
    processName: string, 
    processId?: string, 
    success: boolean = true
  ) => {
    // If we have a process ID, hide the start notification
    if (processId && processingTasks.has(processId)) {
      const startNotificationId = processingTasks.get(processId);
      if (startNotificationId) {
        hideNotification(startNotificationId);
      }
      setProcessingTasks(prev => {
        const newMap = new Map(prev);
        newMap.delete(processId);
        return newMap;
      });
    }

    showNotification(
      success 
        ? `✅ ${processName} completed successfully!`
        : `❌ ${processName} failed. Please check the logs.`,
      success ? 'success' : 'error',
      success ? 4000 : 6000
    );
  }, [processingTasks, showNotification, hideNotification]);

  const handleClose = (id: string) => (_event?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      return;
    }
    hideNotification(id);
  };

  return (
    <NotificationContext.Provider 
      value={{ 
        showNotification, 
        showProcessingStart, 
        showProcessingComplete, 
        hideNotification 
      }}
    >
      {children}
      {notifications.map((notification, index) => (
        <Snackbar
          key={notification.id}
          open={true}
          autoHideDuration={notification.duration}
          onClose={handleClose(notification.id)}
          TransitionComponent={SlideTransition}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
          sx={{ 
            bottom: (theme) => theme.spacing(3 + index * 9),
            // Stack notifications vertically
            position: 'fixed'
          }}
        >
          <Alert 
            onClose={notification.duration ? handleClose(notification.id) : undefined}
            severity={notification.severity}
            variant="filled"
            elevation={6}
            action={notification.action}
            sx={{ 
              minWidth: '300px',
              boxShadow: 3
            }}
          >
            {notification.message}
          </Alert>
        </Snackbar>
      ))}
    </NotificationContext.Provider>
  );
};

export const useNotification = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }
  return context;
}; 