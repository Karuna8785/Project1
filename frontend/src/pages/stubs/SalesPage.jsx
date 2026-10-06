import React from 'react';
import ModuleStubPage from './ModuleStubPage';
import { ShoppingCart } from 'lucide-react';

export default function SalesPage() {
  return (
    <ModuleStubPage
      member="Member 5"
      moduleName="Sales Management"
      description="Quotations, Sales Orders, Invoices, and Payment Processing. Interacts with Member 4 via deduct_stock service."
      icon={ShoppingCart}
    />
  );
}
