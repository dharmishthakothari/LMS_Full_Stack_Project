import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { Modal } from '../../components/Modal';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { Plus, Bell, Calendar } from 'lucide-react';

export const AnnouncementsPage = () => {
  const { role } = useAuth();
  const [announcements, setAnnouncements] = useState([]);
  const [batches, setBatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    target_role: 'all',
    target_batch_id: ''
  });

  const fetchData = async () => {
    setLoading(true);
    try {
      const [annRes, batchRes] = await Promise.all([
        api.get('/announcements'),
        role !== 'student' ? api.get('/batches') : Promise.resolve({ data: [] })
      ]);
      setAnnouncements(annRes.data);
      setBatches(batchRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCreateAnnouncement = async (e) => {
    e.preventDefault();
    try {
      await api.post('/announcements', {
        title: formData.title,
        content: formData.content,
        target_role: formData.target_role,
        target_batch_id: formData.target_batch_id ? parseInt(formData.target_batch_id) : null
      });
      setIsModalOpen(false);
      setFormData({ title: '', content: '', target_role: 'all', target_batch_id: '' });
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to publish announcement');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-bold text-slate-800">Institute Announcements & Notices</h3>
          <p className="text-xs text-slate-500">Official broadcast communications and batch reminders</p>
        </div>
        {['admin', 'instructor'].includes(role) && (
          <button
            onClick={() => setIsModalOpen(true)}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition-colors shadow-sm"
          >
            <Plus className="w-4 h-4" />
            <span>Publish Notice</span>
          </button>
        )}
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : (
        <div className="space-y-4">
          {announcements.map((ann) => (
            <div key={ann.id} className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2.5 py-0.5 rounded">
                  {ann.target_batch_id ? `Batch: ${ann.batch_name}` : `Audience: ${ann.target_role}`}
                </span>
                <span className="text-xs text-slate-400">
                  {new Date(ann.created_at).toLocaleDateString()}
                </span>
              </div>
              <h4 className="text-base font-bold text-slate-800">{ann.title}</h4>
              <p className="text-sm text-slate-600 leading-relaxed">{ann.content}</p>
            </div>
          ))}
        </div>
      )}

      {/* Publish Announcement Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Broadcast Institutional Announcement">
        <form onSubmit={handleCreateAnnouncement} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Notice Title</label>
            <input
              type="text"
              required
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Target Audience</label>
              <select
                value={formData.target_role}
                onChange={(e) => setFormData({ ...formData, target_role: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
              >
                <option value="all">All Users</option>
                <option value="student">Students Only</option>
                <option value="instructor">Instructors Only</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Specific Batch (Optional)</label>
              <select
                value={formData.target_batch_id}
                onChange={(e) => setFormData({ ...formData, target_batch_id: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
              >
                <option value="">None (Broadcast)</option>
                {batches.map((b) => (
                  <option key={b.id} value={b.id}>{b.name}</option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Message Body</label>
            <textarea
              rows="4"
              required
              value={formData.content}
              onChange={(e) => setFormData({ ...formData, content: e.target.value })}
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
            />
          </div>

          <div className="pt-4 flex justify-end gap-2 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setIsModalOpen(false)}
              className="px-4 py-2 border border-slate-200 rounded-lg text-sm text-slate-600 hover:bg-slate-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-semibold"
            >
              Publish Now
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
