import React, { useState, useEffect } from 'react';
import api, { downloadAuthenticatedFile } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { Download, BarChart3, TrendingUp, Users, Calendar, IndianRupee } from 'lucide-react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

export const ReportsPage = () => {
  const { role } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const res = await api.get('/reports/dashboard');
        setData(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchReports();
  }, []);

  if (loading) return <LoadingSpinner text="Aggregating academic report metrics..." />;
  if (!data) return null;

  const downloadCsv = async (type) => {
    await downloadAuthenticatedFile(`/reports/export/csv?report_type=${type}`, `lms_${type}_report.csv`);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-bold text-slate-800">Operational Reports & Analytics</h3>
          <p className="text-xs text-slate-500">Export tabular audits and inspect institute operational KPIs</p>
        </div>

        {/* Export Buttons */}
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => downloadCsv('students')}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 rounded-lg text-xs font-semibold shadow-2xs"
          >
            <Download className="w-3.5 h-3.5" /> Students CSV
          </button>
          <button
            onClick={() => downloadCsv('payments')}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 rounded-lg text-xs font-semibold shadow-2xs"
          >
            <Download className="w-3.5 h-3.5" /> Payments CSV
          </button>
          <button
            onClick={() => downloadCsv('attendance')}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 rounded-lg text-xs font-semibold shadow-2xs"
          >
            <Download className="w-3.5 h-3.5" /> Attendance CSV
          </button>
        </div>
      </div>

      {data.charts && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Monthly Trends */}
          <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm">
            <h4 className="font-bold text-slate-800 text-sm mb-4">Enrollment Trajectory</h4>
            <div className="h-60">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data.charts.enrollment_trends}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="month" stroke="#94a3b8" fontSize={11} />
                  <YAxis stroke="#94a3b8" fontSize={11} />
                  <Tooltip />
                  <Area type="monotone" dataKey="enrollments" stroke="#4F46E5" fill="#EEF2FF" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Batch Distribution */}
          <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm">
            <h4 className="font-bold text-slate-800 text-sm mb-4">Batch Roster Capacity Utilization</h4>
            <div className="h-60">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.charts.batch_distribution}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="batch" stroke="#94a3b8" fontSize={11} />
                  <YAxis stroke="#94a3b8" fontSize={11} />
                  <Tooltip />
                  <Bar dataKey="enrolled" fill="#4F46E5" radius={[4, 4, 0, 0]} name="Enrolled" />
                  <Bar dataKey="capacity" fill="#E2E8F0" radius={[4, 4, 0, 0]} name="Capacity" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
