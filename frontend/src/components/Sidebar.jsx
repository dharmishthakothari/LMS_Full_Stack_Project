import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  Users,
  BookOpen,
  CalendarDays,
  FileText,
  HelpCircle,
  CheckSquare,
  Award,
  CreditCard,
  Bell,
  BarChart3,
  User,
  GraduationCap,
  Sparkles
} from 'lucide-react';

export const Sidebar = () => {
  const { role, user } = useAuth();

  const adminNav = [
    { name: 'Dashboard', path: '/admin/dashboard', icon: LayoutDashboard },
    { name: 'User Management', path: '/users', icon: Users },
    { name: 'Courses', path: '/courses', icon: BookOpen },
    { name: 'Batches & Rosters', path: '/batches', icon: CalendarDays },
    { name: 'Assignments', path: '/assignments', icon: FileText },
    { name: 'Quizzes & Exams', path: '/quizzes', icon: HelpCircle },
    { name: 'Attendance', path: '/attendance', icon: CheckSquare },
    { name: 'Certificates', path: '/certificates', icon: Award },
    { name: 'Fee Payments', path: '/payments', icon: CreditCard },
    { name: 'Announcements', path: '/announcements', icon: Bell },
    { name: 'Notifications', path: '/notifications', icon: Bell },
    { name: 'Reports & Analytics', path: '/reports', icon: BarChart3 },
    { name: 'Profile & Settings', path: '/profile', icon: User },
  ];

  const instructorNav = [
    { name: 'Dashboard', path: '/instructor/dashboard', icon: LayoutDashboard },
    { name: 'Assigned Batches', path: '/batches', icon: CalendarDays },
    { name: 'Courses & Syllabus', path: '/courses', icon: BookOpen },
    { name: 'Assignments & Grading', path: '/assignments', icon: FileText },
    { name: 'Quizzes & Exams', path: '/quizzes', icon: HelpCircle },
    { name: 'Mark Attendance', path: '/attendance', icon: CheckSquare },
    { name: 'Student Progress', path: '/progress', icon: Award },
    { name: 'Announcements', path: '/announcements', icon: Bell },
    { name: 'Notifications', path: '/notifications', icon: Bell },
    { name: 'Reports', path: '/reports', icon: BarChart3 },
    { name: 'Profile', path: '/profile', icon: User },
  ];

  const studentNav = [
    { name: 'Dashboard', path: '/student/dashboard', icon: LayoutDashboard },
    { name: 'My Courses & Syllabus', path: '/courses', icon: BookOpen },
    { name: 'My Batches', path: '/batches', icon: CalendarDays },
    { name: 'Assignments', path: '/assignments', icon: FileText },
    { name: 'Quizzes & Tests', path: '/quizzes', icon: HelpCircle },
    { name: 'Attendance History', path: '/attendance', icon: CheckSquare },
    { name: 'Course Progress', path: '/progress', icon: GraduationCap },
    { name: 'My Certificates', path: '/certificates', icon: Award },
    { name: 'Fee Receipts', path: '/payments', icon: CreditCard },
    { name: 'Notifications', path: '/notifications', icon: Bell },
    { name: 'Announcements', path: '/announcements', icon: Bell },
    { name: 'Profile', path: '/profile', icon: User },
  ];

  let navItems = adminNav;
  if (role === 'instructor') navItems = instructorNav;
  else if (role === 'student') navItems = studentNav;

  return (
    <aside className="w-64 bg-slate-900 text-slate-300 min-h-screen flex flex-col border-r border-slate-800">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-800 flex items-center space-x-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-blue-500 flex items-center justify-center text-white shadow-lg shadow-indigo-500/30">
          <GraduationCap className="w-6 h-6" />
        </div>
        <div>
          <h1 className="font-bold text-white text-lg tracking-tight flex items-center gap-1.5">
            LMS Platform
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
          </h1>
          <p className="text-xs text-slate-400 capitalize font-medium">{role || 'Academic'} Portal</p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`
              }
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* User Mini Card */}
      <div className="p-4 border-t border-slate-800 bg-slate-950/40">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold text-sm border border-indigo-500/30">
            {user?.first_name ? user.first_name[0] : 'U'}
          </div>
          <div className="overflow-hidden">
            <p className="text-sm font-semibold text-white truncate">
              {user?.first_name} {user?.last_name}
            </p>
            <p className="text-xs text-slate-400 truncate">{user?.email}</p>
          </div>
        </div>
      </div>
    </aside>
  );
};
