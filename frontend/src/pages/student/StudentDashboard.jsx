import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { StatCard } from '../../components/StatCard';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import {
  BookOpen,
  CalendarCheck,
  FileText,
  HelpCircle,
  GraduationCap,
  Award,
  ArrowRight,
  CheckCircle2
} from 'lucide-react';

export const StudentDashboard = () => {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [progressData, setProgressData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [dashRes, progRes] = await Promise.all([
          api.get('/reports/dashboard'),
          user?.student_profile ? api.get(`/progress/student/${user.student_profile.id}`) : Promise.resolve({ data: [] })
        ]);
        setData(dashRes.data);
        setProgressData(progRes.data || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [user]);

  if (loading) return <LoadingSpinner text="Loading student learning portal..." />;
  if (!data || !data.kpi) return null;

  const { kpi } = data;

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-indigo-700 to-blue-600 rounded-2xl p-6 text-white shadow-lg shadow-indigo-600/10 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold">Hello, {user?.first_name}!</h2>
          <p className="text-indigo-100 text-sm mt-1">
            Track your course progress, attend scheduled lectures, and complete upcoming assessments.
          </p>
        </div>
        <NavLink
          to="/progress"
          className="px-4 py-2.5 bg-white text-indigo-700 hover:bg-indigo-50 font-semibold text-sm rounded-xl transition-colors shadow-sm whitespace-nowrap"
        >
          View Full Progress
        </NavLink>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          title="Enrolled Batches"
          value={kpi.enrolled_courses}
          icon={BookOpen}
          color="indigo"
        />
        <StatCard
          title="Attendance Rate"
          value={`${kpi.attendance_percentage}%`}
          icon={CalendarCheck}
          color="emerald"
          subtitle="Target: >= 75%"
        />
        <StatCard
          title="Pending Assignments"
          value={kpi.pending_assignments}
          icon={FileText}
          color="amber"
          subtitle="Awaiting submission"
        />
        <StatCard
          title="Available Quizzes"
          value={kpi.available_quizzes}
          icon={HelpCircle}
          color="purple"
        />
      </div>

      {/* Active Course Progress Cards */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-bold text-slate-800">My Enrolled Courses & Progress</h3>
          <NavLink to="/courses" className="text-xs font-semibold text-indigo-600 hover:text-indigo-800">
            Browse All Courses →
          </NavLink>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {progressData.map((prog, idx) => (
            <div key={idx} className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider bg-indigo-50 px-2.5 py-1 rounded-md">
                    Course {idx + 1}
                  </span>
                  <span className="text-sm font-bold text-slate-700">
                    {prog.overall_progress_percentage}% Overall
                  </span>
                </div>
                <h4 className="font-bold text-slate-800 text-base mb-3">{prog.course_title}</h4>

                {/* Progress bar */}
                <div className="w-full bg-slate-100 rounded-full h-2.5 mb-4 overflow-hidden">
                  <div
                    className="bg-indigo-600 h-2.5 rounded-full transition-all duration-500"
                    style={{ width: `${Math.min(prog.overall_progress_percentage, 100)}%` }}
                  />
                </div>

                <div className="grid grid-cols-3 gap-2 text-center text-xs border-t border-slate-100 pt-3">
                  <div>
                    <p className="text-slate-400">Lectures</p>
                    <p className="font-bold text-slate-700 mt-0.5">{prog.completed_lectures}/{prog.total_lectures}</p>
                  </div>
                  <div>
                    <p className="text-slate-400">Assignments</p>
                    <p className="font-bold text-slate-700 mt-0.5">{prog.evaluated_assignments}/{prog.total_assignments}</p>
                  </div>
                  <div>
                    <p className="text-slate-400">Attendance</p>
                    <p className="font-bold text-slate-700 mt-0.5">{prog.attendance_percentage}%</p>
                  </div>
                </div>
              </div>

              <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between">
                {prog.is_eligible_for_certificate ? (
                  <span className="inline-flex items-center gap-1 text-xs font-semibold text-emerald-600">
                    <CheckCircle2 className="w-4 h-4" /> Certificate Eligible
                  </span>
                ) : (
                  <span className="text-xs text-slate-400">Complete 80% to earn certificate</span>
                )}
                <NavLink
                  to={`/courses/${prog.course_id}`}
                  className="inline-flex items-center gap-1 text-xs font-bold text-indigo-600 hover:text-indigo-800"
                >
                  Enter Course <ArrowRight className="w-3.5 h-3.5" />
                </NavLink>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
