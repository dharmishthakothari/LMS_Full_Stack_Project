import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { Clock, AlertTriangle, CheckCircle, ArrowRight, ArrowLeft } from 'lucide-react';

export const QuizAttempt = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [quiz, setQuiz] = useState(null);
  const [attemptId, setAttemptId] = useState(null);
  const [timeLeft, setTimeLeft] = useState(null);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [currentQIndex, setCurrentQIndex] = useState(0);

  useEffect(() => {
    const initQuiz = async () => {
      try {
        const [quizRes, startRes] = await Promise.all([
          api.get(`/quizzes/${id}`),
          api.post(`/quizzes/${id}/start`)
        ]);
        setQuiz(quizRes.data);
        setAttemptId(startRes.data.attempt_id);
        setTimeLeft(startRes.data.duration_minutes * 60);
      } catch (err) {
        alert(err.response?.data?.detail || 'Unable to start quiz attempt');
        navigate('/quizzes');
      } finally {
        setLoading(false);
      }
    };
    initQuiz();
  }, [id]);

  // Live Timer countdown
  useEffect(() => {
    if (timeLeft === null || result) return;
    if (timeLeft <= 0) {
      handleSubmit();
      return;
    }
    const timer = setInterval(() => {
      setTimeLeft((t) => t - 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [timeLeft, result]);

  const handleSelectOption = (questionId, optionId) => {
    setAnswers({ ...answers, [questionId]: optionId });
  };

  const handleSubmit = async () => {
    if (submitting) return;
    setSubmitting(true);
    try {
      const answersPayload = Object.entries(answers).map(([qId, optId]) => ({
        question_id: parseInt(qId),
        selected_option_id: optId ? parseInt(optId) : null
      }));

      const res = await api.post('/quizzes/submit', {
        attempt_id: attemptId,
        answers: answersPayload
      });
      setResult(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || 'Error submitting quiz');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <LoadingSpinner text="Preparing secure examination environment..." />;
  if (!quiz) return null;

  // Format timer
  const formatTime = (secs) => {
    const mins = Math.floor(secs / 60);
    const s = secs % 60;
    return `${mins.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  // Exam Result Screen
  if (result) {
    return (
      <div className="max-w-xl mx-auto bg-white rounded-2xl p-8 border border-slate-200 shadow-xl text-center space-y-6">
        <div className={`w-16 h-16 rounded-2xl mx-auto flex items-center justify-center ${
          result.is_passed ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600'
        }`}>
          {result.is_passed ? <CheckCircle className="w-10 h-10" /> : <AlertTriangle className="w-10 h-10" />}
        </div>

        <div>
          <h3 className="text-2xl font-bold text-slate-800">
            {result.is_passed ? 'Examination Passed!' : 'Passing Threshold Not Met'}
          </h3>
          <p className="text-sm text-slate-500 mt-1">Server-side verified score evaluation</p>
        </div>

        <div className="bg-slate-50 rounded-xl p-5 border border-slate-100 flex items-center justify-around">
          <div>
            <p className="text-xs text-slate-400">Score Obtained</p>
            <p className="text-2xl font-bold text-slate-800">{result.score} / {result.total_marks}</p>
          </div>
          <div>
            <p className="text-xs text-slate-400">Passing Criteria</p>
            <p className="text-2xl font-bold text-indigo-600">{result.passing_marks}</p>
          </div>
        </div>

        <button
          onClick={() => navigate('/quizzes')}
          className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl text-sm transition-colors shadow-md shadow-indigo-600/20"
        >
          Return to Assessments
        </button>
      </div>
    );
  }

  const currentQuestion = quiz.questions[currentQIndex];

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Timer Bar */}
      <div className="bg-slate-900 text-white rounded-2xl p-5 flex items-center justify-between shadow-lg">
        <div>
          <h3 className="font-bold text-base">{quiz.title}</h3>
          <p className="text-xs text-slate-400">Question {currentQIndex + 1} of {quiz.questions.length}</p>
        </div>

        <div className="flex items-center gap-2 bg-slate-800 px-4 py-2 rounded-xl border border-slate-700">
          <Clock className={`w-4 h-4 ${timeLeft < 180 ? 'text-rose-400 animate-pulse' : 'text-indigo-400'}`} />
          <span className={`font-mono text-base font-bold ${timeLeft < 180 ? 'text-rose-400' : 'text-white'}`}>
            {formatTime(timeLeft)}
          </span>
        </div>
      </div>

      {/* Question Card */}
      <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm space-y-6">
        <div>
          <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-md">
            Marks: {currentQuestion.marks}
          </span>
          <h4 className="text-lg font-bold text-slate-800 mt-3 leading-snug">
            {currentQuestion.question_text}
          </h4>
        </div>

        {/* Options */}
        <div className="space-y-3">
          {currentQuestion.options.map((opt) => {
            const isSelected = answers[currentQuestion.id] === opt.id;
            return (
              <label
                key={opt.id}
                onClick={() => handleSelectOption(currentQuestion.id, opt.id)}
                className={`flex items-center gap-3 p-4 rounded-xl border cursor-pointer transition-all ${
                  isSelected
                    ? 'border-indigo-600 bg-indigo-50/60 ring-2 ring-indigo-500/20'
                    : 'border-slate-200 hover:border-slate-300 bg-white'
                }`}
              >
                <input
                  type="radio"
                  name={`question_${currentQuestion.id}`}
                  checked={isSelected}
                  onChange={() => handleSelectOption(currentQuestion.id, opt.id)}
                  className="w-4 h-4 text-indigo-600 focus:ring-indigo-500"
                />
                <span className="text-sm font-medium text-slate-700">{opt.option_text}</span>
              </label>
            );
          })}
        </div>

        {/* Navigation Buttons */}
        <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
          <button
            onClick={() => setCurrentQIndex((i) => Math.max(0, i - 1))}
            disabled={currentQIndex === 0}
            className="flex items-center gap-1 text-xs font-semibold px-3 py-2 border border-slate-200 rounded-lg text-slate-600 disabled:opacity-30"
          >
            <ArrowLeft className="w-3.5 h-3.5" /> Previous
          </button>

          {currentQIndex < quiz.questions.length - 1 ? (
            <button
              onClick={() => setCurrentQIndex((i) => Math.min(quiz.questions.length - 1, i + 1))}
              className="flex items-center gap-1 text-xs font-semibold px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            >
              Next <ArrowRight className="w-3.5 h-3.5" />
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={submitting}
              className="px-6 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold shadow-md shadow-emerald-600/20"
            >
              {submitting ? 'Evaluating...' : 'Submit Final Exam'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
