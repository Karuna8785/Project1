import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authApi } from '../../api/authApi';
import { useNotification } from '../../context/NotificationContext';
import { Layers, User, Mail, Lock, ShieldCheck, ArrowRight } from 'lucide-react';

export default function Register() {
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    username: '',
    password: '',
    confirm_password: '',
  });
  const [loading, setLoading] = useState(false);
  const { notifySuccess, notifyError } = useNotification();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirm_password) {
      notifyError('Passwords do not match');
      return;
    }
    if (formData.password.length < 6) {
      notifyError('Password must be at least 6 characters long');
      return;
    }

    setLoading(true);
    try {
      await authApi.register({
        full_name: formData.full_name,
        email: formData.email,
        username: formData.username,
        password: formData.password,
      });
      notifySuccess('Account registered successfully! Please sign in.');
      navigate('/login');
    } catch (err) {
      notifyError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden">
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none" />

      <div className="sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        <div className="flex items-center justify-center space-x-2 text-white font-extrabold text-3xl tracking-tight">
          <Layers className="w-8 h-8 text-indigo-400" />
          <span>Smart<span className="text-indigo-400">ERP</span></span>
        </div>
        <h2 className="mt-3 text-center text-sm font-medium text-slate-400">
          Enterprise Account Registration
        </h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md relative z-10 px-4">
        <div className="bg-white py-8 px-6 shadow-2xl rounded-2xl sm:px-10 border border-slate-100">
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-semibold text-slate-700">Full Name *</label>
              <div className="mt-1 relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <User className="h-4 w-4 text-slate-400" />
                </div>
                <input
                  type="text"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  placeholder="e.g. John Doe"
                  required
                  className="block w-full pl-9 pr-3 py-2 text-xs border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700">Work Email *</label>
              <div className="mt-1 relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-4 w-4 text-slate-400" />
                </div>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="name@company.com"
                  required
                  className="block w-full pl-9 pr-3 py-2 text-xs border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700">Username *</label>
              <div className="mt-1 relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <User className="h-4 w-4 text-slate-400" />
                </div>
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  placeholder="johndoe"
                  required
                  className="block w-full pl-9 pr-3 py-2 text-xs border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700">Password *</label>
              <div className="mt-1 relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-4 w-4 text-slate-400" />
                </div>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="••••••••"
                  required
                  className="block w-full pl-9 pr-3 py-2 text-xs border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700">Confirm Password *</label>
              <div className="mt-1 relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-4 w-4 text-slate-400" />
                </div>
                <input
                  type="password"
                  name="confirm_password"
                  value={formData.confirm_password}
                  onChange={handleChange}
                  placeholder="••••••••"
                  required
                  className="block w-full pl-9 pr-3 py-2 text-xs border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center items-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition disabled:opacity-50"
            >
              {loading ? (
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
              ) : (
                <>
                  <span>Create Enterprise Account</span>
                  <ArrowRight className="w-4 h-4 ml-1.5" />
                </>
              )}
            </button>
          </form>

          <div className="mt-6 text-center text-xs text-slate-500">
            Already have an enterprise account?{' '}
            <Link to="/login" className="font-semibold text-indigo-600 hover:text-indigo-800">
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
