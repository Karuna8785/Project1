import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { NotificationProvider } from './context/NotificationContext';
import AppLayout from './components/layout/AppLayout';
import ProtectedRoute from './routes/ProtectedRoute';

// Authentication & Security Subsystem
import Login from './pages/Login';
import Register from './pages/auth/Register';
import Profile from './pages/profile/Profile';

// Dashboard
import Dashboard from './pages/Dashboard';

// Inventory Management Subsystem Pages
import InventoryLayout from './pages/inventory/InventoryLayout';
import InventoryOverview from './pages/inventory/InventoryOverview';
import ProductsPage from './pages/inventory/ProductsPage';
import CategoriesPage from './pages/inventory/CategoriesPage';
import WarehousesPage from './pages/inventory/WarehousesPage';
import StockOverviewPage from './pages/inventory/StockOverviewPage';
import StockMovementsPage from './pages/inventory/StockMovementsPage';
import LowStockPage from './pages/inventory/LowStockPage';

// ── HR Management Subsystem (Member 2) ───────────────────────────────────────
import HRDashboard from './pages/hr/HRDashboard';
import EmployeeList from './pages/hr/employees/EmployeeList';
import DepartmentList from './pages/hr/departments/DepartmentList';
import AttendanceList from './pages/hr/attendance/AttendanceList';
import LeaveList from './pages/hr/leaves/LeaveList';

// Enterprise Subsystem Placeholders
import ComingSoonPage from './pages/placeholders/ComingSoonPage';
import { UserCheck, ShoppingCart, Briefcase, DollarSign, BarChart3 } from 'lucide-react';

export default function App() {
  return (
    <BrowserRouter>
      <NotificationProvider>
        <AuthProvider>
          <Routes>
            {/* Public Auth Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected App Routes */}
            <Route element={<AppLayout />}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/profile" element={<Profile />} />

              {/* Inventory Management Subsystem (Member 4) */}
              <Route path="/inventory" element={<InventoryLayout />}>
                <Route index element={<InventoryOverview />} />
                <Route path="products" element={<ProductsPage />} />
                <Route path="categories" element={<CategoriesPage />} />
                <Route path="warehouses" element={<WarehousesPage />} />
                <Route path="stock" element={<StockOverviewPage />} />
                <Route path="movements" element={<StockMovementsPage />} />
                <Route path="low-stock" element={<LowStockPage />} />
              </Route>

              {/* ── HR Management Subsystem (Member 2) ── */}
              <Route path="/hr" element={<HRDashboard />} />
              <Route path="/hr/employees" element={<EmployeeList />} />
              <Route path="/hr/departments" element={<DepartmentList />} />
              <Route path="/hr/attendance" element={<AttendanceList />} />
              <Route path="/hr/leaves" element={<LeaveList />} />

              {/* Planned Module Placeholders */}
              <Route path="/crm" element={<ComingSoonPage category="Customer" moduleName="Customer Relationship Management" description="Customers database, lead conversion pipeline, communication logs, and customer history." icon={UserCheck} />} />
              <Route path="/sales" element={<ComingSoonPage category="Commerce" moduleName="Sales Management" description="Quotations, sales orders, invoices, and payment receipts." icon={ShoppingCart} />} />
              <Route path="/procurement" element={<ComingSoonPage category="Purchasing" moduleName="Procurement & Suppliers" description="Vendor management, purchase orders, goods receipt notes, and purchase invoices." icon={Briefcase} />} />
              <Route path="/finance" element={<ComingSoonPage category="Finance" moduleName="Financial Ledger & Expenses" description="General ledger, chart of accounts, operational expenses, and balance sheets." icon={DollarSign} />} />
              <Route path="/reports" element={<ComingSoonPage category="Analytics" moduleName="Executive Dashboard & Analytics" description="Cross-module KPI summaries, inventory valuation reports, sales forecasting, and custom reports." icon={BarChart3} />} />
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </NotificationProvider>
    </BrowserRouter>
  );
}
