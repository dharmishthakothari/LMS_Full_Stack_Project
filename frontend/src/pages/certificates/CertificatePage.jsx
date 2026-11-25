import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import api, { downloadAuthenticatedFile } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { Award, Download, ShieldCheck, CheckCircle2 } from 'lucide-react';

export const CertificatePage = () => {
  const { role, user } = useAuth();
  const [certificates, setCertificates] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchCertificates = async () => {
    setLoading(true);
    try {
      const res = await api.get('/certificates');
      setCertificates(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCertificates();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-bold text-slate-800">Accredited Course Certificates</h3>
          <p className="text-xs text-slate-500">Download high-resolution verified credentials with cryptographic tamper detection</p>
        </div>
        <NavLink
          to="/verify-certificate"
          className="flex items-center gap-1.5 px-4 py-2 border border-indigo-200 text-indigo-600 hover:bg-indigo-50 rounded-xl text-xs font-bold transition-colors shadow-2xs"
        >
          <ShieldCheck className="w-4 h-4" />
          <span>Public Verification Tool</span>
        </NavLink>
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : certificates.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-xl border border-slate-200 text-slate-400">
          No certificates issued yet. Complete course benchmarks (≥80%) to generate credentials.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {certificates.map((cert) => (
            <div
              key={cert.id}
              className="bg-white rounded-2xl border-2 border-indigo-100 shadow-sm p-6 space-y-4 hover:shadow-md transition-shadow relative overflow-hidden"
            >
              <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-br from-indigo-500/10 to-blue-500/0 rounded-bl-full pointer-events-none" />

              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded">
                  {cert.certificate_number}
                </span>
                <span className="inline-flex items-center gap-1 text-xs font-bold text-emerald-600">
                  <CheckCircle2 className="w-3.5 h-3.5" /> Verified
                </span>
              </div>

              <div>
                <p className="text-xs text-slate-400">Recipient</p>
                <h4 className="text-lg font-bold text-slate-800">{cert.student_name}</h4>
                <p className="text-sm font-semibold text-indigo-600 mt-1">{cert.course_title}</p>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <span>Issued: {new Date(cert.issue_date).toLocaleDateString()}</span>
                <span>Verification ID: <strong className="font-mono text-slate-700">{cert.verification_id}</strong></span>
              </div>

              <div className="pt-2 flex items-center justify-between">
                <NavLink
                  to={`/verify-certificate?id=${cert.verification_id}`}
                  className="text-xs font-semibold text-indigo-600 hover:text-indigo-800"
                >
                  Verify Authenticity →
                </NavLink>

                <button
                  onClick={() => downloadAuthenticatedFile(`/certificates/${cert.id}/download`, `Certificate_${cert.certificate_number}.pdf`)}
                  className="flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition-colors shadow-sm cursor-pointer"
                >
                  <Download className="w-3.5 h-3.5" /> Download PDF
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
