import React, { useState, useEffect } from 'react';
import { useParams, NavLink } from 'react-router-dom';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { Modal } from '../../components/Modal';
import { Badge } from '../../components/Badge';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { Users, UserPlus, UserMinus, Calendar, Clock, ArrowLeft } from 'lucide-react';

export const BatchDetail = () => {
  const { id } = useParams();
  const { role } = useAuth();
  const [batch, setBatch] = useState(null);
  const [allStudents, setAllStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isEnrollModalOpen, setIsEnrollModalOpen] = useState(false);
  const [selectedStudentId, setSelectedStudentId] = useState('');

  const fetchBatch = async () => {
    try {
      const [batchRes, stuRes] = await Promise.all([
        api.get(`/batches/${id}`),
        role === 'admin' ? api.get('/students') : Promise.resolve({ data: [] })
      ]);
      setBatch(batchRes.data);
      setAllStudents(stuRes.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBatch();
  }, [id]);

  const handleEnrollStudent = async (e) => {
    e.preventDefault();
    if (!selectedStudentId) return;
    try {
      await api.post(`/batches/${id}/students`, {
        student_id: parseInt(selectedStudentId)
      });
      setIsEnrollModalOpen(false);
      setSelectedStudentId('');
      fetchBatch();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to enroll student');
    }
  };

  const handleRemoveStudent = async (studentId) => {
    if (!confirm('Are you sure you want to drop this student from the batch?')) return;
    try {
      await api.delete(`/batches/${id}/students/${studentId}`);
      fetchBatch();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to remove student');
    }
  };

  if (loading) return <LoadingSpinner text="Loading batch roster..." />;
  if (!batch) return <div className="p-8 text-center text-slate-400">Batch not found.</div>;

  // Filter out students already enrolled
  const enrolledStudentIds = new Set(batch.roster?.map(r => r.student_id));
  const availableStudents = allStudents.filter(s => !enrolledStudentIds.has(s.id));

  return (
    <div className="space-y-6">
      {/* Batch Header */}
      <div className="flex items-center gap-2 mb-2">
        <NavLink to="/batches" className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Batches
        </NavLink>
      </div>

      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col md:flex-row justify-between gap-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-mono font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
              {batch.code}
            </span>
            <Badge variant={batch.status === 'active' ? 'success' : 'neutral'}>
              {batch.status}
            </Badge>
          </div>
          <h2 className="text-2xl font-bold text-slate-800">{batch.name}</h2>
          <p className="text-sm font-semibold text-indigo-600 mt-1">{batch.course_title}</p>

          <div className="flex flex-wrap gap-4 text-xs text-slate-500 mt-4">
            <span className="flex items-center gap-1.5">
              <Calendar className="w-4 h-4 text-slate-400" />
              {batch.class_days}
            </span>
            <span className="flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-slate-400" />
              {batch.class_timing}
            </span>
            <span className="flex items-center gap-1.5">
              <Users className="w-4 h-4 text-slate-400" />
              Faculty: <strong className="text-slate-700">{batch.instructor_name}</strong>
            </span>
          </div>
        </div>

        <div className="flex flex-col justify-between items-end border-t md:border-t-0 md:border-l border-slate-100 pt-4 md:pt-0 md:pl-6">
          <div className="text-right">
            <p className="text-xs text-slate-400">Roster Strength</p>
            <p className="text-2xl font-bold text-slate-800">
              {batch.enrolled_count} / {batch.capacity}
            </p>
          </div>

          {role === 'admin' && (
            <button
              onClick={() => setIsEnrollModalOpen(true)}
              disabled={batch.enrolled_count >= batch.capacity}
              className="mt-4 flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition-colors shadow-sm disabled:opacity-40"
            >
              <UserPlus className="w-4 h-4" />
              <span>Enroll Student</span>
            </button>
          )}
        </div>
      </div>

      {/* Roster Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
          <h4 className="font-bold text-slate-800 text-base">Enrolled Students Roster</h4>
          <span className="text-xs text-slate-400">Total {batch.roster?.length || 0} learners</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-700">
            <thead className="bg-slate-50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200">
              <tr>
                <th className="px-5 py-3">Student Name</th>
                <th className="px-5 py-3">Email Address</th>
                <th className="px-5 py-3">Phone</th>
                <th className="px-5 py-3">Enrolled Date</th>
                <th className="px-5 py-3">Status</th>
                {role === 'admin' && <th className="px-5 py-3 text-right">Action</th>}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {batch.roster?.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-5 py-8 text-center text-slate-400">
                    No students currently enrolled in this batch.
                  </td>
                </tr>
              ) : (
                batch.roster.map((student) => (
                  <tr key={student.student_id} className="hover:bg-slate-50/50">
                    <td className="px-5 py-3.5 font-semibold text-slate-800">{student.name}</td>
                    <td className="px-5 py-3.5 text-slate-600">{student.email}</td>
                    <td className="px-5 py-3.5 text-slate-500">{student.phone || '-'}</td>
                    <td className="px-5 py-3.5 text-xs text-slate-400">
                      {new Date(student.enrolled_at).toLocaleDateString()}
                    </td>
                    <td className="px-5 py-3.5">
                      <Badge variant={student.status === 'active' ? 'success' : 'neutral'}>
                        {student.status}
                      </Badge>
                    </td>
                    {role === 'admin' && (
                      <td className="px-5 py-3.5 text-right">
                        {student.status === 'active' && (
                          <button
                            onClick={() => handleRemoveStudent(student.student_id)}
                            className="p-1.5 text-rose-600 hover:bg-rose-50 rounded-lg text-xs font-semibold"
                            title="Drop Student"
                          >
                            <UserMinus className="w-4 h-4" />
                          </button>
                        )}
                      </td>
                    )}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Enroll Student Modal */}
      <Modal isOpen={isEnrollModalOpen} onClose={() => setIsEnrollModalOpen(false)} title="Enroll Student to Batch">
        <form onSubmit={handleEnrollStudent} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Select Student</label>
            <select
              required
              value={selectedStudentId}
              onChange={(e) => setSelectedStudentId(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
            >
              <option value="">Select a student to enroll...</option>
              {availableStudents.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.email})
                </option>
              ))}
            </select>
          </div>

          <div className="pt-4 flex justify-end gap-2 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setIsEnrollModalOpen(false)}
              className="px-4 py-2 border border-slate-200 rounded-lg text-sm text-slate-600 hover:bg-slate-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-semibold"
            >
              Confirm Enrollment
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
