import React from 'react';
import ModuleStubPage from './ModuleStubPage';
import { Briefcase } from 'lucide-react';

export default function PurchasesPage() {
  return (
    <ModuleStubPage
      member="Member 6"
      moduleName="Procurement & Finance"
      description="Suppliers, Purchase Orders, Purchase Invoices, and Expenses. Interacts with Member 4 via add_stock service."
      icon={Briefcase}
    />
  );
}
