import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ProtectedRoute, RoleGuard } from './routes/Guards';
import { DashboardLayout } from './layouts/DashboardLayout';

// Pages
import { Login } from './pages/auth/Login';
import { ForgotPassword } from './pages/auth/ForgotPassword';
import { ResetPassword } from './pages/auth/ResetPassword';
import { AdminDashboard } from './pages/admin/AdminDashboard';
import { InstructorDashboard } from './pages/instructor/InstructorDashboard';
import { StudentDashboard } from './pages/student/StudentDashboard';
import { UserManagement } from './pages/users/UserManagement';
import { CourseList } from './pages/courses/CourseList';
import { CourseDetail } from './pages/courses/CourseDetail';
import { BatchList } from './pages/batches/BatchList';
import { BatchDetail } from './pages/batches/BatchDetail';
import { LectureRoom } from './pages/lectures/LectureRoom';
import { AssignmentList } from './pages/assignments/AssignmentList';
import { QuizList } from './pages/quizzes/QuizList';
import { QuizAttempt } from './pages/quizzes/QuizAttempt';
import { AttendancePage } from './pages/attendance/AttendancePage';
import { ProgressPage } from './pages/progress/ProgressPage';
import { CertificatePage } from './pages/certificates/CertificatePage';
import { VerifyCertificate } from './pages/certificates/VerifyCertificate';
import { PaymentPage } from './pages/payments/PaymentPage';
import { AnnouncementsPage } from './pages/communications/AnnouncementsPage';
import { NotificationsPage } from './pages/communications/NotificationsPage';
import { ReportsPage } from './pages/reports/ReportsPage';
import { ProfilePage } from './pages/profile/ProfilePage';

// Root redirect component
const RootRedirect = () => {
  const { role, isAuthenticated, loading } = useAuth();
  if (loading) return null;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (role === 'admin') return <Navigate to="/admin/dashboard" replace />;
  if (role === 'instructor') return <Navigate to="/instructor/dashboard" replace />;
  return <Navigate to="/student/dashboard" replace />;
};

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/verify-certificate" element={<VerifyCertificate />} />
          <Route path="/" element={<RootRedirect />} />

          {/* Protected Routes inside Dashboard Layout */}
          <Route element={<ProtectedRoute />}>
            <Route element={<DashboardLayout />}>
              {/* Role-Specific Dashboards */}
              <Route element={<RoleGuard allowedRoles={['admin']} />}>
                <Route path="/admin/dashboard" element={<AdminDashboard />} />
                <Route path="/users" element={<UserManagement />} />
              </Route>

              <Route element={<RoleGuard allowedRoles={['instructor']} />}>
                <Route path="/instructor/dashboard" element={<InstructorDashboard />} />
              </Route>

              <Route element={<RoleGuard allowedRoles={['student']} />}>
                <Route path="/student/dashboard" element={<StudentDashboard />} />
                <Route path="/quizzes/:id/attempt" element={<QuizAttempt />} />
              </Route>

              {/* Shared Academic & Management Modules */}
              <Route path="/courses" element={<CourseList />} />
              <Route path="/courses/:id" element={<CourseDetail />} />
              <Route path="/batches" element={<BatchList />} />
              <Route path="/batches/:id" element={<BatchDetail />} />
              <Route path="/lectures/:id" element={<LectureRoom />} />
              <Route path="/assignments" element={<AssignmentList />} />
              <Route path="/quizzes" element={<QuizList />} />
              <Route path="/attendance" element={<AttendancePage />} />
              <Route path="/progress" element={<ProgressPage />} />
              <Route path="/certificates" element={<CertificatePage />} />
              <Route path="/payments" element={<PaymentPage />} />
              <Route path="/announcements" element={<AnnouncementsPage />} />
              <Route path="/notifications" element={<NotificationsPage />} />
              <Route path="/reports" element={<ReportsPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Route>
          </Route>

          {/* Catch all fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
