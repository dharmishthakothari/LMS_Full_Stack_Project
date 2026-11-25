import React, { useState, useEffect } from 'react';
import { useParams, NavLink } from 'react-router-dom';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { Modal } from '../../components/Modal';
import { Badge } from '../../components/Badge';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { BookOpen, Plus, PlayCircle, Clock, Video, FileText } from 'lucide-react';

export const CourseDetail = () => {
  const { id } = useParams();
  const { role } = useAuth();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isModuleModalOpen, setIsModuleModalOpen] = useState(false);
  const [isLectureModalOpen, setIsLectureModalOpen] = useState(false);
  const [selectedModuleId, setSelectedModuleId] = useState(null);

  const [moduleTitle, setModuleTitle] = useState('');
  const [lectureData, setLectureData] = useState({
    title: '',
    description: '',
    video_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    duration_minutes: 60,
    sequence_order: 1
  });

  const fetchCourse = async () => {
    try {
      const res = await api.get(`/courses/${id}`);
      setCourse(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCourse();
  }, [id]);

  const handleCreateModule = async (e) => {
    e.preventDefault();
    try {
      await api.post('/modules', {
        course_id: parseInt(id),
        title: moduleTitle,
        sequence_order: (course.modules?.length || 0) + 1
      });
      setIsModuleModalOpen(false);
      setModuleTitle('');
      fetchCourse();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create module');
    }
  };

  const handleCreateLecture = async (e) => {
    e.preventDefault();
    try {
      await api.post('/lectures', {
        module_id: selectedModuleId,
        ...lectureData
      });
      setIsLectureModalOpen(false);
      setLectureData({
        title: '',
        description: '',
        video_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        duration_minutes: 60,
        sequence_order: 1
      });
      fetchCourse();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create lecture');
    }
  };

  if (loading) return <LoadingSpinner text="Loading course syllabus..." />;
  if (!course) return <div className="p-8 text-center text-slate-400">Course not found.</div>;

  return (
    <div className="space-y-6">
      {/* Course Overview Banner */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col md:flex-row justify-between gap-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-md">
              {course.category}
            </span>
            <span className="text-xs font-mono text-slate-400">{course.code}</span>
          </div>
          <h2 className="text-2xl font-bold text-slate-800">{course.title}</h2>
          <p className="text-sm text-slate-500 mt-2 max-w-2xl">{course.description}</p>
        </div>

        <div className="flex flex-col justify-between items-end border-t md:border-t-0 md:border-l border-slate-100 pt-4 md:pt-0 md:pl-6">
          <div className="text-right">
            <p className="text-xs text-slate-400">Course Tuition Fee</p>
            <p className="text-2xl font-bold text-slate-800">₹{Number(course.fee).toLocaleString('en-IN')}</p>
          </div>
          {role === 'admin' && (
            <button
              onClick={() => setIsModuleModalOpen(true)}
              className="mt-4 flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition-colors shadow-sm"
            >
              <Plus className="w-4 h-4" />
              <span>Add Module</span>
            </button>
          )}
        </div>
      </div>

      {/* Modules & Lectures List */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold text-slate-800">Course Modules & Curriculum</h3>

        {course.modules?.length === 0 ? (
          <div className="p-12 text-center bg-white rounded-xl border border-slate-200 text-slate-400">
            No modules added to this course yet.
          </div>
        ) : (
          course.modules.map((mod, modIdx) => (
            <div key={mod.id} className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
              <div className="p-4 bg-slate-50/80 border-b border-slate-200 flex items-center justify-between">
                <div>
                  <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider mr-2">
                    Module {modIdx + 1}
                  </span>
                  <span className="font-bold text-slate-800 text-base">{mod.title}</span>
                </div>
                {['admin', 'instructor'].includes(role) && (
                  <button
                    onClick={() => {
                      setSelectedModuleId(mod.id);
                      setIsLectureModalOpen(true);
                    }}
                    className="flex items-center gap-1 text-xs font-semibold text-indigo-600 hover:text-indigo-800 px-2.5 py-1 bg-white rounded-lg border border-slate-200 shadow-2xs"
                  >
                    <Plus className="w-3.5 h-3.5" /> Add Lecture
                  </button>
                )}
              </div>

              {/* Lecture list in module */}
              <div className="divide-y divide-slate-100">
                {mod.lectures?.length === 0 ? (
                  <div className="p-4 text-xs text-slate-400 italic">No lectures in this module.</div>
                ) : (
                  mod.lectures.map((lec) => (
                    <div
                      key={lec.id}
                      className="p-4 flex items-center justify-between hover:bg-slate-50/50 transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <PlayCircle className="w-5 h-5 text-indigo-600 flex-shrink-0" />
                        <div>
                          <p className="font-semibold text-slate-800 text-sm">{lec.title}</p>
                          <p className="text-xs text-slate-400 flex items-center gap-3 mt-0.5">
                            <span className="flex items-center gap-1">
                              <Clock className="w-3 h-3" /> {lec.duration_minutes} mins
                            </span>
                            {lec.video_url && (
                              <span className="flex items-center gap-1 text-emerald-600">
                                <Video className="w-3 h-3" /> Video Ready
                              </span>
                            )}
                          </p>
                        </div>
                      </div>

                      <NavLink
                        to={`/lectures/${lec.id}`}
                        className="px-3 py-1.5 bg-indigo-50 text-indigo-700 hover:bg-indigo-100 rounded-lg text-xs font-bold transition-colors"
                      >
                        Launch Classroom →
                      </NavLink>
                    </div>
                  ))
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Add Module Modal */}
      <Modal isOpen={isModuleModalOpen} onClose={() => setIsModuleModalOpen(false)} title="Add Course Module">
        <form onSubmit={handleCreateModule} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Module Title</label>
            <input
              type="text"
              required
              value={moduleTitle}
              onChange={(e) => setModuleTitle(e.target.value)}
              placeholder="e.g. Module 4: Asynchronous Processing & Task Queues"
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
            />
          </div>
          <div className="pt-4 flex justify-end gap-2 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setIsModuleModalOpen(false)}
              className="px-4 py-2 border border-slate-200 rounded-lg text-sm text-slate-600 hover:bg-slate-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-semibold"
            >
              Save Module
            </button>
          </div>
        </form>
      </Modal>

      {/* Add Lecture Modal */}
      <Modal isOpen={isLectureModalOpen} onClose={() => setIsLectureModalOpen(false)} title="Add Lecture Session">
        <form onSubmit={handleCreateLecture} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Lecture Title</label>
            <input
              type="text"
              required
              value={lectureData.title}
              onChange={(e) => setLectureData({ ...lectureData, title: e.target.value })}
              placeholder="e.g. Session 1: Celery, Redis & Background Workers"
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Video Stream URL</label>
            <input
              type="url"
              value={lectureData.video_url}
              onChange={(e) => setLectureData({ ...lectureData, video_url: e.target.value })}
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Duration (Minutes)</label>
              <input
                type="number"
                min="10"
                value={lectureData.duration_minutes}
                onChange={(e) => setLectureData({ ...lectureData, duration_minutes: parseInt(e.target.value) })}
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Sequence #</label>
              <input
                type="number"
                min="1"
                value={lectureData.sequence_order}
                onChange={(e) => setLectureData({ ...lectureData, sequence_order: parseInt(e.target.value) })}
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
              />
            </div>
          </div>

          <div className="pt-4 flex justify-end gap-2 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setIsLectureModalOpen(false)}
              className="px-4 py-2 border border-slate-200 rounded-lg text-sm text-slate-600 hover:bg-slate-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-semibold"
            >
              Save Lecture
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
