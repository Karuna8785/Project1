import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi } from '../api/authApi';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      const saved = localStorage.getItem('smarterp_user');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });
  const [token, setToken] = useState(() => localStorage.getItem('smarterp_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function verifyAuth() {
      if (token) {
        try {
          const freshUser = await authApi.getMe();
          setUser(freshUser);
          localStorage.setItem('smarterp_user', JSON.stringify(freshUser));
        } catch {
          logout();
        }
      }
      setLoading(false);
    }
    verifyAuth();
  }, [token]);

  const login = async (usernameOrEmail, password) => {
    const data = await authApi.login(usernameOrEmail, password);
    setToken(data.access_token);
    setUser(data.user);
    localStorage.setItem('smarterp_token', data.access_token);
    localStorage.setItem('smarterp_user', JSON.stringify(data.user));
    return data.user;
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('smarterp_token');
    localStorage.removeItem('smarterp_user');
  };

  const hasPermission = (permissionCode) => {
    if (!user) return false;
    if (user.is_superuser) return true;
    if (!user.permissions) return false;
    return user.permissions.includes('*') || user.permissions.includes(permissionCode);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout, hasPermission }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
