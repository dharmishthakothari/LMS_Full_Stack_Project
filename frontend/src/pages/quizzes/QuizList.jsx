import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { Modal } from '../../components/Modal';
import { Badge } from '../../components/Badge';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { Plus, HelpCircle, Clock, CheckCircle2, ArrowRight } from 'lucide-react';

export const QuizList = () => {
  const { role } = useAuth();
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchQuizzes = async () => {
    setLoading(true);
    try {
      const res = await api.get('/quizzes');
      setQuizzes(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuizzes();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-bold text-slate-800">Quizzes & MCQ Examinations</h3>
          <p className="text-xs text-slate-500">Timed assessments with automated server-side evaluation</p>
        </div>
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {quizzes.map((quiz) => (
            <div
              key={quiz.id}
              className="bg-white rounded-2xl border border-slate-200/80 shadow-sm p-6 flex flex-col justify-between overflow-hidden"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-md">
                    {quiz.batch_name}
                  </span>
                  <Badge variant={quiz.is_passed ? 'success' : quiz.my_attempts_count > 0 ? 'warning' : 'neutral'}>
                    {quiz.is_passed ? 'Passed ✓' : quiz.my_attempts_count > 0 ? 'Attempted' : 'Unattempted'}
                  </Badge>
                </div>

                <h4 className="text-lg font-bold text-slate-800 mb-2">{quiz.title}</h4>
                <p className="text-xs text-slate-500 line-clamp-2 mb-4">{quiz.description}</p>

                <div className="space-y-1.5 text-xs text-slate-600 pt-3 border-t border-slate-100">
                  <p className="flex items-center justify-between">
                    <span className="text-slate-400">Duration:</span>
                    <strong>{quiz.duration_minutes} Minutes</strong>
                  </p>
                  <p className="flex items-center justify-between">
                    <span className="text-slate-400">Total Marks:</span>
                    <strong>{quiz.total_marks} Marks</strong>
                  </p>
                  <p className="flex items-center justify-between">
                    <span className="text-slate-400">Passing Criteria:</span>
                    <strong className="text-indigo-600">{quiz.passing_marks} Marks</strong>
                  </p>
                  {quiz.highest_score !== null && (
                    <p className="flex items-center justify-between pt-1 border-t border-slate-100 text-emerald-600">
                      <span>Highest Score:</span>
                      <strong className="font-bold">{quiz.highest_score} / {quiz.total_marks}</strong>
                    </p>
                  )}
                </div>
              </div>

              <div className="mt-6 pt-3 border-t border-slate-100 flex items-center justify-between">
                <span className="text-xs text-slate-400">
                  {quiz.questions_count} Questions
                </span>
                {role === 'student' ? (
                  <NavLink
                    to={`/quizzes/${quiz.id}/attempt`}
                    className="px-4 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition-colors shadow-xs"
                  >
                    Start Exam →
                  </NavLink>
                ) : (
                  <span className="text-xs font-semibold text-slate-500">Instructor Assessment</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
