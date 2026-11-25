import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { StatCard } from '../../components/StatCard';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import {
  Users,
  GraduationCap,
  BookOpen,
  CalendarDays,
  IndianRupee,
  Clock,
  CheckCircle2,
  TrendingUp,
  FileText
} from 'lucide-react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';

export const AdminDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await api.get('/reports/dashboard');
        setData(res.data);
      } catch (err) {
        console.error('Failed to load dashboard:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) return <LoadingSpinner text="Computing institute analytics..." />;
  if (!data || !data.kpi) return null;

  const { kpi, charts, recent_enrollments } = data;
  const PIE_COLORS = ['#4F46E5', '#F59E0B', '#10B981', '#EF4444'];

  return (
    <div className="space-y-8">
      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          title="Total Students"
          value={kpi.total_students}
          icon={GraduationCap}
          color="indigo"
          trend="+12%"
        />
        <StatCard
          title="Faculty Instructors"
          value={kpi.total_instructors}
          icon={Users}
          color="blue"
        />
        <StatCard
          title="Active Batches"
          value={`${kpi.active_batches} / ${kpi.total_batches}`}
          icon={CalendarDays}
          color="purple"
          subtitle="Batches in session"
        />
        <StatCard
          title="Total Revenue"
          value={`₹${kpi.total_revenue.toLocaleString('en-IN')}`}
          icon={IndianRupee}
          color="emerald"
          trend="+8%"
        />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          title="Total Courses"
          value={kpi.total_courses}
          icon={BookOpen}
          color="blue"
        />
        <StatCard
          title="Active Enrollments"
          value={kpi.total_enrollments}
          icon={CheckCircle2}
          color="indigo"
        />
        <StatCard
          title="Pending Fees"
          value={`₹${kpi.pending_fees.toLocaleString('en-IN')}`}
          icon={Clock}
          color="rose"
        />
        <StatCard
          title="Pending Evaluations"
          value={kpi.pending_evaluations}
          icon={FileText}
          color="amber"
          subtitle="Submissions under review"
        />
      </div>

      {/* Visual Analytics Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Monthly Enrollment Trends Area Chart */}
        <div className="lg:col-span-2 bg-white rounded-xl p-5 border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h4 className="font-bold text-slate-800 text-base">Monthly Enrollment Trends</h4>
              <p className="text-xs text-slate-400">Student enrollment growth across academic terms</p>
            </div>
            <TrendingUp className="w-5 h-5 text-indigo-600" />
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={charts.enrollment_trends}>
                <defs>
                  <linearGradient id="colorEnr" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#4F46E5" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#4F46E5" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip />
                <Area type="monotone" dataKey="enrollments" stroke="#4F46E5" strokeWidth={2} fillOpacity={1} fill="url(#colorEnr)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Payment Distribution Pie Chart */}
        <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm">
          <h4 className="font-bold text-slate-800 text-base mb-1">Fee Payment Distribution</h4>
          <p className="text-xs text-slate-400 mb-4">Paid vs installment collection balance</p>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={charts.payment_distribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {charts.payment_distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend verticalAlign="bottom" height={36} iconSize={8} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Course Enrollment Bar Chart */}
      <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm">
        <h4 className="font-bold text-slate-800 text-base mb-1">Course-Wise Student Enrollment</h4>
        <p className="text-xs text-slate-400 mb-4">Enrollment distribution across active departments</p>
        <div className="h-60">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={charts.course_distribution}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="course" stroke="#94a3b8" fontSize={12} />
              <YAxis stroke="#94a3b8" fontSize={12} />
              <Tooltip />
              <Bar dataKey="students" fill="#3B82F6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Enrollments Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
          <h4 className="font-bold text-slate-800 text-base">Recent Student Enrollments</h4>
          <span className="text-xs text-slate-400">Live database audit feed</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-700">
            <thead className="bg-slate-50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200">
              <tr>
                <th className="px-5 py-3">Student</th>
                <th className="px-5 py-3">Course</th>
                <th className="px-5 py-3">Batch</th>
                <th className="px-5 py-3">Enrolled At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {recent_enrollments.map((enr, idx) => (
                <tr key={idx} className="hover:bg-slate-50/50">
                  <td className="px-5 py-3.5 font-semibold text-slate-800">{enr.student_name}</td>
                  <td className="px-5 py-3.5 text-slate-600">{enr.course_title}</td>
                  <td className="px-5 py-3.5 text-indigo-600 font-medium">{enr.batch_name}</td>
                  <td className="px-5 py-3.5 text-slate-400 text-xs">
                    {new Date(enr.enrolled_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
