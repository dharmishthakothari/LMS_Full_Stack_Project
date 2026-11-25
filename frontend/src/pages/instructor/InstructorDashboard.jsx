import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import api from '../../services/api';
import { StatCard } from '../../components/StatCard';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { Badge } from '../../components/Badge';
import {
  BookOpen,
  CalendarDays,
  Users,
  FileCheck,
  CheckCircle,
  Clock,
  ArrowRight
} from 'lucide-react';

export const InstructorDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await api.get('/reports/dashboard');
        setData(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) return <LoadingSpinner text="Loading instructor workspace..." />;
  if (!data || !data.kpi) return null;

  const { kpi, recent_submissions } = data;

  return (
    <div className="space-y-8">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          title="Assigned Batches"
          value={kpi.assigned_batches}
          icon={CalendarDays}
          color="indigo"
        />
        <StatCard
          title="Assigned Courses"
          value={kpi.assigned_courses}
          icon={BookOpen}
          color="blue"
        />
        <StatCard
          title="Total Students"
          value={kpi.total_students}
          icon={Users}
          color="emerald"
        />
        <StatCard
          title="Pending Evaluations"
          value={kpi.pending_evaluations}
          icon={FileCheck}
          color="amber"
          subtitle="Submissions to grade"
        />
      </div>

      {/* Quick Action Tiles */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <NavLink
          to="/attendance"
          className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:border-indigo-500 hover:shadow-md transition-all flex items-center justify-between group"
        >
          <div>
            <h4 className="font-bold text-slate-800 text-base">Mark Batch Attendance</h4>
            <p className="text-xs text-slate-500 mt-0.5">Record daily class sessions</p>
          </div>
          <ArrowRight className="w-5 h-5 text-indigo-600 group-hover:translate-x-1 transition-transform" />
        </NavLink>

        <NavLink
          to="/assignments"
          className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:border-indigo-500 hover:shadow-md transition-all flex items-center justify-between group"
        >
          <div>
            <h4 className="font-bold text-slate-800 text-base">Grade Assignments</h4>
            <p className="text-xs text-slate-500 mt-0.5">Evaluate and assign marks</p>
          </div>
          <ArrowRight className="w-5 h-5 text-indigo-600 group-hover:translate-x-1 transition-transform" />
        </NavLink>

        <NavLink
          to="/quizzes"
          className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:border-indigo-500 hover:shadow-md transition-all flex items-center justify-between group"
        >
          <div>
            <h4 className="font-bold text-slate-800 text-base">Manage Quizzes</h4>
            <p className="text-xs text-slate-500 mt-0.5">Create and review MCQ exams</p>
          </div>
          <ArrowRight className="w-5 h-5 text-indigo-600 group-hover:translate-x-1 transition-transform" />
        </NavLink>
      </div>

      {/* Recent Submissions To Review */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
          <h4 className="font-bold text-slate-800 text-base">Recent Submissions for Evaluation</h4>
          <NavLink to="/assignments" className="text-xs font-semibold text-indigo-600 hover:text-indigo-800">
            View All Submissions →
          </NavLink>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-700">
            <thead className="bg-slate-50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200">
              <tr>
                <th className="px-5 py-3">Assignment</th>
                <th className="px-5 py-3">Student</th>
                <th className="px-5 py-3">Submitted At</th>
                <th className="px-5 py-3">Status</th>
                <th className="px-5 py-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {recent_submissions.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-5 py-8 text-center text-slate-400">
                    No submissions currently pending evaluation.
                  </td>
                </tr>
              ) : (
                recent_submissions.map((sub) => (
                  <tr key={sub.id} className="hover:bg-slate-50/50">
                    <td className="px-5 py-3.5 font-semibold text-slate-800">{sub.assignment_title}</td>
                    <td className="px-5 py-3.5">{sub.student_name}</td>
                    <td className="px-5 py-3.5 text-xs text-slate-400">
                      {new Date(sub.submitted_at).toLocaleDateString()}
                    </td>
                    <td className="px-5 py-3.5">
                      <Badge variant={sub.status === 'evaluated' ? 'success' : 'warning'}>
                        {sub.status.replace('_', ' ')}
                      </Badge>
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      <NavLink
                        to="/assignments"
                        className="px-3 py-1 bg-indigo-50 text-indigo-600 hover:bg-indigo-100 rounded-lg text-xs font-semibold transition-colors"
                      >
                        Evaluate
                      </NavLink>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
