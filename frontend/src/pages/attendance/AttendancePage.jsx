import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { Badge } from '../../components/Badge';
import { Calendar, CheckCircle2, XCircle, Save, CheckSquare } from 'lucide-react';

export const AttendancePage = () => {
  const { role, user } = useAuth();
  const [batches, setBatches] = useState([]);
  const [selectedBatchId, setSelectedBatchId] = useState('');
  const [sessionDate, setSessionDate] = useState(new Date().toISOString().split('T')[0]);
  const [roster, setRoster] = useState([]);
  const [attendanceMap, setAttendanceMap] = useState({});
  const [studentSummary, setStudentSummary] = useState(null);
  const [studentHistory, setStudentHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const initAttendance = async () => {
      setLoading(true);
      try {
        if (role === 'student' && user?.student_profile) {
          const res = await api.get(`/attendance/student/${user.student_profile.id}`);
          setStudentSummary(res.data.summary);
          setStudentHistory(res.data.history);
        } else {
          const res = await api.get('/batches');
          setBatches(res.data);
          if (res.data.length > 0) {
            setSelectedBatchId(res.data[0].id.toString());
          }
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    initAttendance();
  }, [role, user]);

  // Load roster when batch or date changes for instructor/admin
  useEffect(() => {
    if (role === 'student' || !selectedBatchId) return;

    const loadBatchRoster = async () => {
      try {
        const [batchRes, attRes] = await Promise.all([
          api.get(`/batches/${selectedBatchId}`),
          api.get(`/attendance/batch/${selectedBatchId}?session_date=${sessionDate}`)
        ]);
        setRoster(batchRes.data.roster || []);

        const existingMap = {};
        attRes.data.forEach((r) => {
          existingMap[r.student_id] = r.status;
        });
        setAttendanceMap(existingMap);
      } catch (err) {
        console.error(err);
      }
    };
    loadBatchRoster();
  }, [selectedBatchId, sessionDate, role]);

  const toggleStatus = (studentId) => {
    const current = attendanceMap[studentId] || 'absent';
    const next = current === 'present' ? 'absent' : 'present';
    setAttendanceMap({ ...attendanceMap, [studentId]: next });
  };

  const handleSaveAttendance = async () => {
    setSaving(true);
    try {
      const records = roster.map((s) => ({
        student_id: s.student_id,
        status: attendanceMap[s.student_id] || 'present'
      }));

      await api.post('/attendance', {
        batch_id: parseInt(selectedBatchId),
        session_date: sessionDate,
        records
      });
      alert('Attendance saved successfully!');
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to save attendance');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <LoadingSpinner text="Loading attendance records..." />;

  // Student Attendance View
  if (role === 'student') {
    return (
      <div className="space-y-6">
        <div>
          <h3 className="text-xl font-bold text-slate-800">My Attendance History</h3>
          <p className="text-xs text-slate-500">Track recorded session participation across batches</p>
        </div>

        {studentSummary && (
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
            <div className="bg-white p-5 rounded-xl border border-slate-200">
              <p className="text-xs text-slate-400">Total Sessions</p>
              <h4 className="text-2xl font-bold text-slate-800 mt-1">{studentSummary.total_sessions}</h4>
            </div>
            <div className="bg-white p-5 rounded-xl border border-slate-200">
              <p className="text-xs text-slate-400">Present Sessions</p>
              <h4 className="text-2xl font-bold text-emerald-600 mt-1">{studentSummary.present_sessions}</h4>
            </div>
            <div className="bg-white p-5 rounded-xl border border-slate-200">
              <p className="text-xs text-slate-400">Absent Sessions</p>
              <h4 className="text-2xl font-bold text-rose-600 mt-1">{studentSummary.absent_sessions}</h4>
            </div>
            <div className="bg-white p-5 rounded-xl border border-slate-200">
              <p className="text-xs text-slate-400">Attendance Rate</p>
              <h4 className="text-2xl font-bold text-indigo-600 mt-1">{studentSummary.attendance_percentage}%</h4>
            </div>
          </div>
        )}

        {/* History Table */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="px-5 py-4 border-b border-slate-100 font-bold text-slate-800 text-sm">
            Session History Log
          </div>
          <table className="w-full text-left text-sm text-slate-700">
            <thead className="bg-slate-50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200">
              <tr>
                <th className="px-5 py-3">Session Date</th>
                <th className="px-5 py-3">Batch Name</th>
                <th className="px-5 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {studentHistory.map((h) => (
                <tr key={h.id} className="hover:bg-slate-50/50">
                  <td className="px-5 py-3.5 font-medium">{new Date(h.session_date).toLocaleDateString()}</td>
                  <td className="px-5 py-3.5 text-slate-600">{h.batch_name}</td>
                  <td className="px-5 py-3.5">
                    <Badge variant={h.status === 'present' ? 'success' : 'danger'}>
                      {h.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

  // Instructor / Admin Attendance Entry View
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-bold text-slate-800">Batch Attendance Management</h3>
          <p className="text-xs text-slate-500">Record and audit daily attendance for scheduled cohorts</p>
        </div>

        <button
          onClick={handleSaveAttendance}
          disabled={saving || roster.length === 0}
          className="flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition-colors shadow-sm disabled:opacity-40"
        >
          <Save className="w-4 h-4" />
          <span>{saving ? 'Saving...' : 'Save Attendance Session'}</span>
        </button>
      </div>

      {/* Selectors Bar */}
      <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-sm flex flex-wrap gap-4">
        <div className="w-64">
          <label className="block text-xs font-semibold text-slate-700 mb-1">Select Batch</label>
          <select
            value={selectedBatchId}
            onChange={(e) => setSelectedBatchId(e.target.value)}
            className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50"
          >
            {batches.map((b) => (
              <option key={b.id} value={b.id}>{b.name}</option>
            ))}
          </select>
        </div>

        <div className="w-48">
          <label className="block text-xs font-semibold text-slate-700 mb-1">Session Date</label>
          <input
            type="date"
            value={sessionDate}
            onChange={(e) => setSessionDate(e.target.value)}
            className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50"
          />
        </div>
      </div>

      {/* Roster Attendance Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
          <h4 className="font-bold text-slate-800 text-sm">Student Attendance Checklist</h4>
          <span className="text-xs text-slate-400">Click button to toggle Present / Absent</span>
        </div>

        <table className="w-full text-left text-sm text-slate-700">
          <thead className="bg-slate-50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200">
            <tr>
              <th className="px-5 py-3">Student Name</th>
              <th className="px-5 py-3">Email Address</th>
              <th className="px-5 py-3 text-right">Attendance Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {roster.length === 0 ? (
              <tr>
                <td colSpan={3} className="px-5 py-8 text-center text-slate-400">
                  No students enrolled in this batch.
                </td>
              </tr>
            ) : (
              roster.map((student) => {
                const status = attendanceMap[student.student_id] || 'present';
                const isPresent = status === 'present';
                return (
                  <tr key={student.student_id} className="hover:bg-slate-50/50">
                    <td className="px-5 py-3.5 font-semibold text-slate-800">{student.name}</td>
                    <td className="px-5 py-3.5 text-slate-500">{student.email}</td>
                    <td className="px-5 py-3.5 text-right">
                      <button
                        onClick={() => toggleStatus(student.student_id)}
                        className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 ml-auto transition-colors ${
                          isPresent
                            ? 'bg-emerald-50 text-emerald-700 border border-emerald-200 hover:bg-emerald-100'
                            : 'bg-rose-50 text-rose-700 border border-rose-200 hover:bg-rose-100'
                        }`}
                      >
                        {isPresent ? <CheckCircle2 className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
                        <span>{isPresent ? 'Present' : 'Absent'}</span>
                      </button>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
