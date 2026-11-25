import React, { useState, useEffect } from 'react';
import { useSearchParams, NavLink } from 'react-router-dom';
import api from '../../services/api';
import { ShieldCheck, Search, CheckCircle, AlertTriangle, ArrowLeft } from 'lucide-react';

export const VerifyCertificate = () => {
  const [searchParams] = useSearchParams();
  const [verificationId, setVerificationId] = useState(searchParams.get('id') || 'V-LMS-984712');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleVerify = async (e) => {
    if (e) e.preventDefault();
    if (!verificationId.trim()) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const res = await api.get(`/certificates/verify/${verificationId.trim()}`);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid certificate or verification ID not found in institutional registry.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (searchParams.get('id')) {
      handleVerify();
    }
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-center p-4">
      <div className="max-w-xl w-full bg-white rounded-2xl shadow-2xl p-8 border border-slate-100 space-y-6">
        <div className="text-center">
          <div className="w-14 h-14 bg-indigo-50 text-indigo-600 rounded-2xl mx-auto flex items-center justify-center mb-3">
            <ShieldCheck className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold text-slate-800">Certificate Verification Portal</h2>
          <p className="text-xs text-slate-500 mt-1">
            Authenticate officially issued academic credentials against institute database records
          </p>
        </div>

        <form onSubmit={handleVerify} className="space-y-3">
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
            Verification ID / Code
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              required
              value={verificationId}
              onChange={(e) => setVerificationId(e.target.value)}
              placeholder="e.g. V-LMS-984712"
              className="flex-1 px-4 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-xl font-mono focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
            />
            <button
              type="submit"
              disabled={loading}
              className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition-colors shadow-sm disabled:opacity-50"
            >
              {loading ? 'Verifying...' : 'Verify Now'}
            </button>
          </div>
        </form>

        {error && (
          <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {result && (
          <div className="p-6 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-3 text-slate-800">
            <div className="flex items-center gap-2 text-emerald-700 font-bold text-sm">
              <CheckCircle className="w-5 h-5" />
              <span>Valid & Authentic Credential</span>
            </div>

            <div className="space-y-1.5 text-xs pt-2 border-t border-emerald-200/60">
              <p><span className="text-slate-500">Student Name:</span> <strong className="text-slate-900 text-sm">{result.student_name}</strong></p>
              <p><span className="text-slate-500">Course Track:</span> <strong className="text-indigo-700">{result.course_title}</strong></p>
              <p><span className="text-slate-500">Certificate Number:</span> <span className="font-mono">{result.certificate_number}</span></p>
              <p><span className="text-slate-500">Issue Date:</span> {new Date(result.issue_date).toLocaleDateString()}</p>
              <p><span className="text-slate-500">Issuing Authority:</span> {result.issuing_institute}</p>
            </div>
          </div>
        )}

        <div className="text-center pt-2">
          <NavLink to="/login" className="inline-flex items-center gap-1 text-xs text-indigo-600 hover:text-indigo-800 font-semibold">
            <ArrowLeft className="w-3.5 h-3.5" /> Back to LMS Login
          </NavLink>
        </div>
      </div>
    </div>
  );
};
