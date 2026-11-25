import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { GraduationCap, Lock, Mail, ArrowRight, ShieldCheck, AlertCircle } from 'lucide-react';

export const Login = () => {
  const [email, setEmail] = useState('admin@lms.com');
  const [password, setPassword] = useState('Admin@123');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);
    try {
      const user = await login(email, password);
      const role = user.role.name;
      if (role === 'admin') navigate('/admin/dashboard');
      else if (role === 'instructor') navigate('/instructor/dashboard');
      else navigate('/student/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const setDemoAccount = (role) => {
    if (role === 'admin') {
      setEmail('admin@lms.com');
      setPassword('Admin@123');
    } else if (role === 'instructor') {
      setEmail('dr.patel@lms.com');
      setPassword('Instructor@123');
    } else if (role === 'student') {
      setEmail('student1@lms.com');
      setPassword('Student@123');
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-2xl overflow-hidden border border-slate-100">
        {/* Banner */}
        <div className="bg-gradient-to-tr from-indigo-700 via-indigo-600 to-blue-600 p-8 text-white text-center">
          <div className="w-14 h-14 bg-white/10 backdrop-blur-xs rounded-2xl mx-auto flex items-center justify-center mb-4 shadow-inner">
            <GraduationCap className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-2xl font-bold tracking-tight">Welcome to LMS</h2>
          <p className="text-indigo-100 text-sm mt-1">Enterprise Academic Management Platform</p>
        </div>

        <div className="p-8">
          {/* Quick Demo Role Selector */}
          <div className="mb-6 bg-slate-50 p-3 rounded-xl border border-slate-200">
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
              Fast Demo Login:
            </p>
            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => setDemoAccount('admin')}
                className="px-2 py-1.5 text-xs font-semibold bg-white border border-slate-200 rounded-lg text-slate-700 hover:border-indigo-500 hover:text-indigo-600 transition-colors shadow-2xs"
              >
                Admin
              </button>
              <button
                type="button"
                onClick={() => setDemoAccount('instructor')}
                className="px-2 py-1.5 text-xs font-semibold bg-white border border-slate-200 rounded-lg text-slate-700 hover:border-indigo-500 hover:text-indigo-600 transition-colors shadow-2xs"
              >
                Instructor
              </button>
              <button
                type="button"
                onClick={() => setDemoAccount('student')}
                className="px-2 py-1.5 text-xs font-semibold bg-white border border-slate-200 rounded-lg text-slate-700 hover:border-indigo-500 hover:text-indigo-600 transition-colors shadow-2xs"
              >
                Student
              </button>
            </div>
          </div>

          {error && (
            <div className="mb-4 p-3 rounded-lg bg-rose-50 border border-rose-200 flex items-center gap-2 text-rose-700 text-xs">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                Email Address
              </label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3.5" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@lms.com"
                  className="w-full pl-9 pr-3 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                Password
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3.5" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-9 pr-3 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl transition-colors flex items-center justify-center gap-2 text-sm shadow-md shadow-indigo-600/20 disabled:opacity-50"
            >
              <span>{isSubmitting ? 'Authenticating...' : 'Sign In to Portal'}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          <div className="mt-6 text-center text-xs text-slate-400">
            Enterprise LMS • Version 1.1 Production Release
          </div>
        </div>
      </div>
    </div>
  );
};
