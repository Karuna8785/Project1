import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { NotificationProvider } from './context/NotificationContext';
import AppLayout from './components/layout/AppLayout';
import ProtectedRoute from './routes/ProtectedRoute';

// Auth Pages (Member 1)
import Login from './pages/Login';
import Register from './pages/auth/Register';
import Profile from './pages/profile/Profile';

// Dashboard
import Dashboard from './pages/Dashboard';

// Member 4 Inventory Pages
import InventoryLayout from './pages/inventory/InventoryLayout';
import InventoryOverview from './pages/inventory/InventoryOverview';
import ProductsPage from './pages/inventory/ProductsPage';
import CategoriesPage from './pages/inventory/CategoriesPage';
import WarehousesPage from './pages/inventory/WarehousesPage';
import StockOverviewPage from './pages/inventory/StockOverviewPage';
import StockMovementsPage from './pages/inventory/StockMovementsPage';
import LowStockPage from './pages/inventory/LowStockPage';

// Placeholder Pages for Teammates
import ComingSoonPage from './pages/placeholders/ComingSoonPage';
import { Users, UserCheck, ShoppingCart, Briefcase, DollarSign, BarChart3 } from 'lucide-react';

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

              {/* Member 4: Inventory Management Subsystem */}
              <Route path="/inventory" element={<InventoryLayout />}>
                <Route index element={<InventoryOverview />} />
                <Route path="products" element={<ProductsPage />} />
                <Route path="categories" element={<CategoriesPage />} />
                <Route path="warehouses" element={<WarehousesPage />} />
                <Route path="stock" element={<StockOverviewPage />} />
                <Route path="movements" element={<StockMovementsPage />} />
                <Route path="low-stock" element={<LowStockPage />} />
              </Route>

              {/* Teammate Placeholders (Coming Soon) */}
              <Route 
                path="/hr" 
                element={
                  <ComingSoonPage 
                    member="Member 2" 
                    moduleName="Human Resources Management" 
                    description="Employee records, departments, shifts, attendance tracking, and leave management." 
                    icon={Users} 
                  />
                } 
              />
              <Route 
                path="/crm" 
                element={
                  <ComingSoonPage 
                    member="Member 3" 
                    moduleName="Customer Relationship Management" 
                    description="Customers database, lead conversion pipeline, communication logs, and customer history." 
                    icon={UserCheck} 
                  />
                } 
              />
              <Route 
                path="/sales" 
                element={
                  <ComingSoonPage 
                    member="Member 5" 
                    moduleName="Sales Management" 
                    description="Quotations, sales orders, invoices, and payment receipts. Integrates with Inventory via deduct_stock service." 
                    icon={ShoppingCart} 
                  />
                } 
              />
              <Route 
                path="/procurement" 
                element={
                  <ComingSoonPage 
                    member="Member 6" 
                    moduleName="Procurement & Suppliers" 
                    description="Vendor management, purchase orders, goods receipt notes, and purchase invoices. Integrates with Inventory via add_stock service." 
                    icon={Briefcase} 
                  />
                } 
              />
              <Route 
                path="/finance" 
                element={
                  <ComingSoonPage 
                    member="Member 6" 
                    moduleName="Financial Ledger & Expenses" 
                    description="General ledger, chart of accounts, operational expenses, and balance sheets." 
                    icon={DollarSign} 
                  />
                } 
              />
              <Route 
                path="/reports" 
                element={
                  <ComingSoonPage 
                    member="Member 7" 
                    moduleName="Executive Dashboard & Analytics" 
                    description="Cross-module KPI summaries, inventory valuation reports, sales forecasting, and custom reports." 
                    icon={BarChart3} 
                  />
                } 
              />
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </NotificationProvider>
    </BrowserRouter>
  );
}
