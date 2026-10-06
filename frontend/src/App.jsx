import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { NotificationProvider } from './context/NotificationContext';
import AppLayout from './components/layout/AppLayout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import HRPage from './pages/stubs/HRPage';
import CRMPage from './pages/stubs/CRMPage';
import SalesPage from './pages/stubs/SalesPage';
import PurchasesPage from './pages/stubs/PurchasesPage';
import ReportsPage from './pages/stubs/ReportsPage';

export default function App() {
  return (
    <BrowserRouter>
      <NotificationProvider>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<Login />} />

            <Route element={<AppLayout />}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/hr" element={<HRPage />} />
              <Route path="/crm" element={<CRMPage />} />
              <Route path="/sales" element={<SalesPage />} />
              <Route path="/procurement" element={<PurchasesPage />} />
              <Route path="/reports" element={<ReportsPage />} />

              {/* Inventory routes will be mounted here */}
              <Route path="/inventory/*" element={<Navigate to="/" replace />} />
            </Route>

            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </NotificationProvider>
    </BrowserRouter>
  );
}
