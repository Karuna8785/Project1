import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ requiredPermission, requiredRole }) {
  const { user, loading, hasPermission } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-100">
        <div className="w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (requiredPermission && !hasPermission(requiredPermission)) {
    return (
      <div className="p-8 max-w-lg mx-auto bg-white border border-rose-200 rounded-2xl text-center shadow-sm">
        <h3 className="text-base font-bold text-rose-700 mb-2">Access Forbidden (403)</h3>
        <p className="text-xs text-slate-600 mb-4">
          Your account does not possess the required permission: <code className="font-mono text-indigo-600 font-bold">{requiredPermission}</code>.
        </p>
      </div>
    );
  }

  return <Outlet />;
}
