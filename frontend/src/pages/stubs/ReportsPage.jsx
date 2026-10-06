import React from 'react';
import ModuleStubPage from './ModuleStubPage';
import { BarChart3 } from 'lucide-react';

export default function ReportsPage() {
  return (
    <ModuleStubPage
      member="Member 7"
      moduleName="Dashboard, Reports & Integration"
      description="Cross-module Analytics, Inventory Valuation, and Management Reporting."
      icon={BarChart3}
    />
  );
}
