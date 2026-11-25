import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { Modal } from '../../components/Modal';
import { Badge } from '../../components/Badge';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { Plus, Upload, CheckCircle2, FileText, Calendar, Clock, Award } from 'lucide-react';

export const AssignmentList = () => {
  const { role, user } = useAuth();
  const [assignments, setAssignments] = useState([]);
  const [batches, setBatches] = useState([]);
  const [loading, setLoading] = useState(true);

  // Modals state
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isSubmitModalOpen, setIsSubmitModalOpen] = useState(false);
  const [isEvaluateModalOpen, setIsEvaluateModalOpen] = useState(false);
  const [selectedAssignment, setSelectedAssignment] = useState(null);
  const [selectedSubmission, setSelectedSubmission] = useState(null);

  // Forms state
  const [createData, setCreateData] = useState({
    batch_id: '',
    title: '',
    description: '',
    max_marks: 100,
    due_date: ''
  });
  const [submitFile, setSubmitFile] = useState(null);
  const [evalMarks, setEvalMarks] = useState('');
  const [evalFeedback, setEvalFeedback] = useState('');

  const fetchData = async () => {
    setLoading(true);
    try {
      const [assignRes, batchRes] = await Promise.all([
        api.get('/assignments'),
        role !== 'student' ? api.get('/batches') : Promise.resolve({ data: [] })
      ]);
      setAssignments(assignRes.data);
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

  const handleCreateAssignment = async (e) => {
    e.preventDefault();
    try {
      await api.post('/assignments', {
        ...createData,
        batch_id: parseInt(createData.batch_id),
        due_date: new Date(createData.due_date).toISOString()
      });
      setIsCreateModalOpen(false);
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create assignment');
    }
  };

  const handleSubmitAssignment = async (e) => {
    e.preventDefault();
    if (!submitFile || !selectedAssignment) return;
    const form = new FormData();
    form.append('assignment_id', selectedAssignment.id);
    form.append('file', submitFile);

    try {
      await api.post('/submissions', form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setIsSubmitModalOpen(false);
      setSubmitFile(null);
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to submit assignment');
    }
  };

  const handleEvaluate = async (e) => {
    e.preventDefault();
    try {
      await api.post(`/submissions/${selectedSubmission.id}/evaluate`, {
        marks_obtained: parseFloat(evalMarks),
        feedback_text: evalFeedback
      });
      setIsEvaluateModalOpen(false);
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to evaluate submission');
    }
  };

  const openEvaluation = async (assign) => {
    try {
      const res = await api.get(`/assignments/${assign.id}`);
      if (res.data.submissions?.length > 0) {
        setSelectedSubmission(res.data.submissions[0]);
        setEvalMarks(res.data.submissions[0].feedback?.marks_obtained || '');
        setEvalFeedback(res.data.submissions[0].feedback?.feedback_text || '');
        setIsEvaluateModalOpen(true);
      } else {
        alert('No submissions uploaded for this assignment yet.');
      }
    } catch (err) {
      alert('Failed to load submissions');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-bold text-slate-800">Assignments & Project Assessments</h3>
          <p className="text-xs text-slate-500">Author coursework, track submissions, and provide qualitative feedback</p>
        </div>
        {['admin', 'instructor'].includes(role) && (
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition-colors shadow-sm"
          >
            <Plus className="w-4 h-4" />
            <span>Create Assignment</span>
          </button>
        )}
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : (
        <div className="space-y-4">
          {assignments.map((assign) => (
            <div
              key={assign.id}
              className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4"
            >
              <div className="space-y-1.5 max-w-2xl">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2.5 py-0.5 rounded">
                    {assign.batch_name}
                  </span>
                  <span className="text-xs text-slate-400 font-medium">Max Marks: {assign.max_marks}</span>
                </div>
                <h4 className="text-base font-bold text-slate-800">{assign.title}</h4>
                <p className="text-xs text-slate-600">{assign.description}</p>
                <div className="flex items-center gap-4 text-xs text-slate-400 pt-1">
                  <span className="flex items-center gap-1 text-rose-600 font-medium">
                    <Clock className="w-3.5 h-3.5" /> Due: {new Date(assign.due_date).toLocaleDateString()}
                  </span>
                  {['admin', 'instructor'].includes(role) && (
                    <span>Submissions: <strong className="text-slate-700">{assign.submissions_count}</strong></span>
                  )}
                </div>
              </div>

              {/* Action according to role */}
              <div className="flex items-center gap-3">
                {role === 'student' ? (
                  assign.my_submission ? (
                    <div className="text-right">
                      <Badge variant={assign.my_submission.status === 'evaluated' ? 'success' : 'warning'}>
                        {assign.my_submission.status.replace('_', ' ')}
                      </Badge>
                      {assign.my_submission.feedback && (
                        <p className="text-xs font-bold text-emerald-600 mt-1">
                          Score: {assign.my_submission.feedback.marks_obtained}/{assign.max_marks}
                        </p>
                      )}
                    </div>
                  ) : (
                    <button
                      onClick={() => {
                        setSelectedAssignment(assign);
                        setIsSubmitModalOpen(true);
                      }}
                      className="flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold shadow-sm"
                    >
                      <Upload className="w-3.5 h-3.5" /> Submit Work
                    </button>
                  )
                ) : (
                  <button
                    onClick={() => openEvaluation(assign)}
                    className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold"
                  >
                    <Award className="w-3.5 h-3.5 text-indigo-600" /> Review Submissions
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Assignment Modal */}
      <Modal isOpen={isCreateModalOpen} onClose={() => setIsCreateModalOpen(false)} title="Create New Assignment">
        <form onSubmit={handleCreateAssignment} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Target Batch</label>
            <select
              required
              value={createData.batch_id}
              onChange={(e) => setCreateData({ ...createData, batch_id: e.target.value })}
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
            >
              <option value="">Select Batch...</option>
              {batches.map((b) => (
                <option key={b.id} value={b.id}>{b.name} ({b.course_title})</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Assignment Title</label>
            <input
              type="text"
              required
              value={createData.title}
              onChange={(e) => setCreateData({ ...createData, title: e.target.value })}
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Max Marks</label>
              <input
                type="number"
                min="10"
                required
                value={createData.max_marks}
                onChange={(e) => setCreateData({ ...createData, max_marks: parseInt(e.target.value) })}
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Due Date</label>
              <input
                type="datetime-local"
                required
                value={createData.due_date}
                onChange={(e) => setCreateData({ ...createData, due_date: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Instructions & Problem Statement</label>
            <textarea
              rows="3"
              required
              value={createData.description}
              onChange={(e) => setCreateData({ ...createData, description: e.target.value })}
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
            />
          </div>

          <div className="pt-4 flex justify-end gap-2 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setIsCreateModalOpen(false)}
              className="px-4 py-2 border border-slate-200 rounded-lg text-sm text-slate-600 hover:bg-slate-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-semibold"
            >
              Publish Assignment
            </button>
          </div>
        </form>
      </Modal>

      {/* Student Submit Modal */}
      <Modal isOpen={isSubmitModalOpen} onClose={() => setIsSubmitModalOpen(false)} title="Upload Assignment Deliverable">
        <form onSubmit={handleSubmitAssignment} className="space-y-4">
          <p className="text-xs text-slate-500">
            Uploading work for: <strong className="text-slate-800">{selectedAssignment?.title}</strong>
          </p>

          <div className="border-2 border-dashed border-slate-200 rounded-xl p-6 text-center hover:border-indigo-500 transition-colors">
            <Upload className="w-8 h-8 text-indigo-600 mx-auto mb-2" />
            <input
              type="file"
              required
              onChange={(e) => setSubmitFile(e.target.files[0])}
              className="text-xs text-slate-600"
            />
            <p className="text-2xs text-slate-400 mt-2">Supported formats: ZIP, PDF, TAR.GZ (Max 50MB)</p>
          </div>

          <div className="pt-4 flex justify-end gap-2 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setIsSubmitModalOpen(false)}
              className="px-4 py-2 border border-slate-200 rounded-lg text-sm text-slate-600 hover:bg-slate-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-semibold"
            >
              Upload & Submit
            </button>
          </div>
        </form>
      </Modal>

      {/* Evaluate Submission Modal */}
      <Modal isOpen={isEvaluateModalOpen} onClose={() => setIsEvaluateModalOpen(false)} title="Grade Student Submission">
        <form onSubmit={handleEvaluate} className="space-y-4">
          <p className="text-xs text-slate-600">
            Student: <strong className="text-slate-800">{selectedSubmission?.student_name}</strong>
          </p>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Marks Obtained</label>
            <input
              type="number"
              step="0.5"
              min="0"
              required
              value={evalMarks}
              onChange={(e) => setEvalMarks(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Instructor Qualitative Feedback</label>
            <textarea
              rows="3"
              value={evalFeedback}
              onChange={(e) => setEvalFeedback(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
            />
          </div>

          <div className="pt-4 flex justify-end gap-2 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setIsEvaluateModalOpen(false)}
              className="px-4 py-2 border border-slate-200 rounded-lg text-sm text-slate-600 hover:bg-slate-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-semibold"
            >
              Save Evaluation
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
