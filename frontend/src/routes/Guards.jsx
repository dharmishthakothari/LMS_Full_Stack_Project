import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LoadingSpinner } from '../components/LoadingSpinner';

export const ProtectedRoute = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner text="Authenticating session..." />;
  }

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

export const RoleGuard = ({ allowedRoles = [] }) => {
  const { role, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner text="Checking permissions..." />;
  }

  if (!role || !allowedRoles.includes(role)) {
    // Redirect to their default dashboard
    if (role === 'admin') return <Navigate to="/admin/dashboard" replace />;
    if (role === 'instructor') return <Navigate to="/instructor/dashboard" replace />;
    if (role === 'student') return <Navigate to="/student/dashboard" replace />;
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};
