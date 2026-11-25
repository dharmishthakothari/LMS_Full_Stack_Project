import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { Badge } from '../../components/Badge';
import { Award, CheckCircle2, AlertCircle, BookOpen, FileText, HelpCircle, CheckSquare } from 'lucide-react';
import { NavLink } from 'react-router-dom';

export const ProgressPage = () => {
  const { role, user } = useAuth();
  const [progressList, setProgressList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProgress = async () => {
      setLoading(true);
      try {
        if (role === 'student' && user?.student_profile) {
          const res = await api.get(`/progress/student/${user.student_profile.id}`);
          setProgressList(res.data);
        } else {
          // If instructor/admin, view student 1 demo progress
          const res = await api.get('/progress/student/1');
          setProgressList(res.data);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchProgress();
  }, [role, user]);

  if (loading) return <LoadingSpinner text="Computing dynamic academic progress..." />;

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-bold text-slate-800">Academic Learning Progress</h3>
        <p className="text-xs text-slate-500">Real-time evaluation based on lectures, assignments, and exam benchmarks</p>
      </div>

      <div className="space-y-6">
        {progressList.map((prog, idx) => (
          <div key={idx} className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
              <div>
                <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider bg-indigo-50 px-2.5 py-1 rounded">
                  Course Track {idx + 1}
                </span>
                <h4 className="text-xl font-bold text-slate-800 mt-1">{prog.course_title}</h4>
                <p className="text-xs text-slate-400">Student: {prog.student_name}</p>
              </div>

              <div className="text-right">
                <span className="text-xs text-slate-400">Weighted Aggregate Score</span>
                <p className="text-3xl font-extrabold text-indigo-600">{prog.overall_progress_percentage}%</p>
              </div>
            </div>

            {/* Sub-Metric Meters */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
              <div className="bg-slate-50 p-4 rounded-xl border border-slate-200/60">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-slate-600 flex items-center gap-1.5">
                    <BookOpen className="w-4 h-4 text-indigo-500" /> Lectures (40%)
                  </span>
                  <span className="text-xs font-bold text-slate-800">{prog.lecture_completion_percentage}%</span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                  <div className="bg-indigo-600 h-2 rounded-full" style={{ width: `${Math.min(prog.lecture_completion_percentage, 100)}%` }} />
                </div>
                <p className="text-2xs text-slate-400 mt-2">{prog.completed_lectures} of {prog.total_lectures} sessions completed</p>
              </div>

              <div className="bg-slate-50 p-4 rounded-xl border border-slate-200/60">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-slate-600 flex items-center gap-1.5">
                    <FileText className="w-4 h-4 text-blue-500" /> Assignments (30%)
                  </span>
                  <span className="text-xs font-bold text-slate-800">{prog.assignment_completion_percentage}%</span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                  <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${Math.min(prog.assignment_completion_percentage, 100)}%` }} />
                </div>
                <p className="text-2xs text-slate-400 mt-2">{prog.evaluated_assignments} of {prog.total_assignments} graded</p>
              </div>

              <div className="bg-slate-50 p-4 rounded-xl border border-slate-200/60">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-slate-600 flex items-center gap-1.5">
                    <HelpCircle className="w-4 h-4 text-purple-500" /> Quizzes (30%)
                  </span>
                  <span className="text-xs font-bold text-slate-800">{prog.quiz_completion_percentage}%</span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                  <div className="bg-purple-600 h-2 rounded-full" style={{ width: `${Math.min(prog.quiz_completion_percentage, 100)}%` }} />
                </div>
                <p className="text-2xs text-slate-400 mt-2">{prog.passed_quizzes} of {prog.total_quizzes} exams passed</p>
              </div>
            </div>

            {/* Certificate Eligibility Banner */}
            <div className={`p-4 rounded-xl border flex items-center justify-between ${
              prog.is_eligible_for_certificate
                ? 'bg-emerald-50 border-emerald-200 text-emerald-800'
                : 'bg-amber-50 border-amber-200 text-amber-800'
            }`}>
              <div className="flex items-center gap-3">
                <Award className="w-6 h-6 flex-shrink-0" />
                <div>
                  <h5 className="font-bold text-sm">
                    {prog.is_eligible_for_certificate
                      ? 'Congratulations! You are eligible for the Course Completion Certificate.'
                      : 'Certificate Requirements in Progress'}
                  </h5>
                  <p className="text-xs mt-0.5 opacity-80">
                    Criteria: Course Progress ≥ 80%, Attendance ≥ 75%, and All Fee Dues Cleared.
                  </p>
                </div>
              </div>

              {prog.is_eligible_for_certificate && (
                <NavLink
                  to="/certificates"
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold transition-colors whitespace-nowrap shadow-xs"
                >
                  Claim Certificate
                </NavLink>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
