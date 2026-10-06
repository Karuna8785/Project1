import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import api from "../services/api";

const AuthContext = createContext(null);
const TOKEN_KEY = "smarterp_access_token";

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const logout = useCallback(async () => {
    try {
      if (localStorage.getItem(TOKEN_KEY)) await api.post("/auth/logout");
    } finally {
      localStorage.removeItem(TOKEN_KEY);
      setUser(null);
    }
  }, []);

  useEffect(() => {
    let active = true;
    const token = localStorage.getItem(TOKEN_KEY);
    if (!token) {
      setLoading(false);
      return () => {
        active = false;
      };
    }
    api
      .get("/auth/me")
      .then(({ data }) => {
        if (active) setUser(data);
      })
      .catch(() => {
        localStorage.removeItem(TOKEN_KEY);
        if (active) setUser(null);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const login = useCallback(async (identifier, password) => {
    const { data } = await api.post("/auth/login", { identifier, password });
    localStorage.setItem(TOKEN_KEY, data.access_token);
    setUser(data.user);
    return data.user;
  }, []);

  const register = useCallback(async (details) => {
    await api.post("/auth/register", details);
  }, []);

  const value = useMemo(
    () => ({ user, loading, login, logout, register }),
    [user, loading, login, logout, register],
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
