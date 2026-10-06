import { Routes, Route, Navigate } from 'react-router-dom'
import MainLayout from './layouts/MainLayout'
import EmployeeList from './pages/hr/employees/EmployeeList'
import DepartmentList from './pages/hr/departments/DepartmentList'
import AttendanceList from './pages/hr/attendance/AttendanceList'
import LeaveList from './pages/hr/leaves/LeaveList'
import HRDashboard from './pages/hr/HRDashboard'
import ComingSoon from './pages/coming-soon/ComingSoon'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        {/* Default redirect to HR */}
        <Route index element={<Navigate to="/hr" replace />} />

        {/* HR Module (Member 2) */}
        <Route path="hr" element={<HRDashboard />} />
        <Route path="hr/employees" element={<EmployeeList />} />
        <Route path="hr/departments" element={<DepartmentList />} />
        <Route path="hr/attendance" element={<AttendanceList />} />
        <Route path="hr/leaves" element={<LeaveList />} />

        {/* Other modules — Coming Soon (Members 3–7) */}
        <Route path="crm/*" element={<ComingSoon module="CRM" member="Member 3" />} />
        <Route path="inventory/*" element={<ComingSoon module="Inventory" member="Member 4" />} />
        <Route path="sales/*" element={<ComingSoon module="Sales" member="Member 5" />} />
        <Route path="procurement/*" element={<ComingSoon module="Procurement & Finance" member="Member 6" />} />
        <Route path="reports/*" element={<ComingSoon module="Dashboard & Reports" member="Member 7" />} />
      </Route>
    </Routes>
  )
}
