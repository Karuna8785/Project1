/**
 * SmartERP - Axios API Client
 * Member 1 will add JWT token injection when auth is integrated.
 */
import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

// ── Request interceptor (Member 1 adds token here) ──────────────────────────
api.interceptors.request.use((config) => {
  // Member 1 integration: read token from localStorage/context
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ── Response interceptor (global error handling) ────────────────────────────
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Member 1: trigger logout / redirect to login
      console.warn('Unauthorized — redirect to login')
    }
    return Promise.reject(error)
  }
)

export default api
