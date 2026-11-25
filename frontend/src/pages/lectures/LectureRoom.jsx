import React, { useState, useEffect } from 'react';
import { useParams, NavLink } from 'react-router-dom';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { Badge } from '../../components/Badge';
import { PlayCircle, CheckCircle2, Download, FileText, ArrowLeft, Video, Clock } from 'lucide-react';

export const LectureRoom = () => {
  const { id } = useParams();
  const { role } = useAuth();
  const [lecture, setLecture] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isCompleted, setIsCompleted] = useState(false);

  const fetchLecture = async () => {
    try {
      const res = await api.get(`/lectures/${id}`);
      setLecture(res.data);
      setIsCompleted(res.data.is_completed);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLecture();
  }, [id]);

  const handleMarkCompleted = async () => {
    try {
      await api.post(`/lectures/${id}/complete`);
      setIsCompleted(true);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to mark lecture as completed');
    }
  };

  if (loading) return <LoadingSpinner text="Loading classroom environment..." />;
  if (!lecture) return <div className="p-8 text-center text-slate-400">Lecture not found.</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <NavLink to="/courses" className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Curriculum
        </NavLink>
        {role === 'student' && (
          <button
            onClick={handleMarkCompleted}
            disabled={isCompleted}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-sm ${
              isCompleted
                ? 'bg-emerald-50 text-emerald-700 border border-emerald-200 cursor-default'
                : 'bg-indigo-600 hover:bg-indigo-700 text-white'
            }`}
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>{isCompleted ? 'Lecture Completed ✓' : 'Mark as Completed'}</span>
          </button>
        )}
      </div>

      {/* Main Video Stream Player Area */}
      <div className="bg-slate-900 rounded-2xl overflow-hidden shadow-xl border border-slate-800 aspect-video flex items-center justify-center relative">
        {lecture.video_url?.includes('youtube.com') || lecture.video_url?.includes('youtu.be') ? (
          <iframe
            src={`https://www.youtube.com/embed/${lecture.video_url.split('v=')[1] || 'dQw4w9WgXcQ'}`}
            title={lecture.title}
            className="w-full h-full border-0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        ) : (
          <div className="text-center text-slate-400 p-8">
            <Video className="w-16 h-16 mx-auto mb-3 text-indigo-400 animate-pulse" />
            <h4 className="font-bold text-white text-lg">{lecture.title}</h4>
            <p className="text-xs text-slate-500 mt-1">High-Definition Lecture Stream</p>
          </div>
        )}
      </div>

      {/* Details & Notes */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
              Lecture {lecture.sequence_order}
            </span>
            <span className="text-xs text-slate-400 flex items-center gap-1">
              <Clock className="w-3.5 h-3.5" /> {lecture.duration_minutes} minutes
            </span>
          </div>

          <h3 className="text-xl font-bold text-slate-800">{lecture.title}</h3>
          <p className="text-sm text-slate-600 leading-relaxed">
            {lecture.description || 'Detailed academic session notes covering software architecture and hands-on coding.'}
          </p>
        </div>

        {/* Study Materials & Downloads */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
          <h4 className="font-bold text-slate-800 text-base">Study Materials & Notes</h4>

          {lecture.materials?.length === 0 ? (
            <p className="text-xs text-slate-400">No downloadable materials attached to this session.</p>
          ) : (
            <div className="space-y-2">
              {lecture.materials.map((mat) => (
                <div
                  key={mat.id}
                  className="p-3 rounded-xl border border-slate-200 hover:border-indigo-400 bg-slate-50/50 flex items-center justify-between transition-colors"
                >
                  <div className="flex items-center gap-2.5 overflow-hidden">
                    <FileText className="w-5 h-5 text-indigo-600 flex-shrink-0" />
                    <div className="overflow-hidden">
                      <p className="text-xs font-semibold text-slate-800 truncate">{mat.title}</p>
                      <p className="text-2xs text-slate-400">{(mat.file_size_bytes / 1024 / 1024).toFixed(1)} MB • PDF</p>
                    </div>
                  </div>

                  <a
                    href={mat.file_path}
                    download
                    target="_blank"
                    rel="noreferrer"
                    className="p-1.5 text-indigo-600 hover:bg-indigo-50 rounded-lg text-xs font-semibold"
                    title="Download"
                  >
                    <Download className="w-4 h-4" />
                  </a>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
