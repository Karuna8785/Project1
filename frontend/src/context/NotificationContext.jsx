import React, { createContext, useContext, useState, useCallback } from 'react';
import { CheckCircle2, AlertCircle, AlertTriangle, Info, X } from 'lucide-react';

const NotificationContext = createContext(null);

export function NotificationProvider({ children }) {
  const [notifications, setNotifications] = useState([]);

  const addNotification = useCallback(({ type = 'info', title, message, duration = 4000 }) => {
    const id = Date.now() + Math.random().toString();
    setNotifications((prev) => [...prev, { id, type, title, message }]);

    if (duration > 0) {
      setTimeout(() => {
        setNotifications((prev) => prev.filter((n) => n.id !== id));
      }, duration);
    }
  }, []);

  const removeNotification = useCallback((id) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  }, []);

  const notifySuccess = useCallback((message, title = 'Success') => {
    addNotification({ type: 'success', title, message });
  }, [addNotification]);

  const notifyError = useCallback((message, title = 'Error') => {
    addNotification({ type: 'error', title, message: message || 'An unexpected error occurred' });
  }, [addNotification]);

  const notifyWarning = useCallback((message, title = 'Warning') => {
    addNotification({ type: 'warning', title, message });
  }, [addNotification]);

  const notifyInfo = useCallback((message, title = 'Information') => {
    addNotification({ type: 'info', title, message });
  }, [addNotification]);

  return (
    <NotificationContext.Provider
      value={{ notifySuccess, notifyError, notifyWarning, notifyInfo, addNotification }}
    >
      {children}
      {/* Toast container */}
      <div className="fixed top-5 right-5 z-50 flex flex-col space-y-3 pointer-events-none max-w-sm w-full">
        {notifications.map((n) => (
          <div
            key={n.id}
            className={`pointer-events-auto flex items-start p-4 rounded-xl shadow-lg border backdrop-blur-md transition-all duration-300 animate-in fade-in slide-in-from-top-4 ${
              n.type === 'success'
                ? 'bg-emerald-50/95 border-emerald-200 text-emerald-900'
                : n.type === 'error'
                ? 'bg-rose-50/95 border-rose-200 text-rose-900'
                : n.type === 'warning'
                ? 'bg-amber-50/95 border-amber-200 text-amber-900'
                : 'bg-indigo-50/95 border-indigo-200 text-indigo-900'
            }`}
          >
            <div className="flex-shrink-0 mt-0.5 mr-3">
              {n.type === 'success' && <CheckCircle2 className="w-5 h-5 text-emerald-600" />}
              {n.type === 'error' && <AlertCircle className="w-5 h-5 text-rose-600" />}
              {n.type === 'warning' && <AlertTriangle className="w-5 h-5 text-amber-600" />}
              {n.type === 'info' && <Info className="w-5 h-5 text-indigo-600" />}
            </div>
            <div className="flex-1 text-sm">
              {n.title && <div className="font-semibold mb-0.5">{n.title}</div>}
              <div>{n.message}</div>
            </div>
            <button
              onClick={() => removeNotification(n.id)}
              className="flex-shrink-0 ml-3 text-slate-400 hover:text-slate-700 transition"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        ))}
      </div>
    </NotificationContext.Provider>
  );
}

export function useNotification() {
  const ctx = useContext(NotificationContext);
  if (!ctx) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }
  return ctx;
}
