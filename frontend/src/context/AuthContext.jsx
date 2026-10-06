/**
 * SmartERP - Auth Context Stub
 * Member 1 will replace this with real JWT authentication.
 *
 * Current behavior: Mock logged-in admin user for HR module development.
 */
import { createContext, useContext, useState } from 'react'

const AuthContext = createContext(null)

// Mock admin user — replace when Member 1 integrates
const MOCK_USER = {
  id: 1,
  full_name: 'Admin User',
  email: 'admin@smarterp.com',
  username: 'admin',
  role: 'ADMIN',
}

export function AuthProvider({ children }) {
  const [user] = useState(MOCK_USER)
  // Member 1 will manage: token, login(), logout(), loading state, etc.

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: true }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}
