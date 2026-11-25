import React, { useState, useEffect } from 'react';
import api, { downloadAuthenticatedFile } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { Modal } from '../../components/Modal';
import { Badge } from '../../components/Badge';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { Plus, Download, CreditCard, CheckCircle2, Clock } from 'lucide-react';

export const PaymentPage = () => {
  const { role, user } = useAuth();
  const [payments, setPayments] = useState([]);
  const [students, setStudents] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const [formData, setFormData] = useState({
    student_id: '',
    course_id: '',
    paid_amount: '',
    payment_method: 'UPI',
    transaction_reference: '',
    remarks: 'Tuition installment fee'
  });

  const fetchData = async () => {
    setLoading(true);
    try {
      const [payRes, stuRes, courseRes] = await Promise.all([
        api.get('/payments'),
        role === 'admin' ? api.get('/students') : Promise.resolve({ data: [] }),
        role === 'admin' ? api.get('/courses') : Promise.resolve({ data: [] })
      ]);
      setPayments(payRes.data);
      setStudents(stuRes.data || []);
      setCourses(courseRes.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleRecordPayment = async (e) => {
    e.preventDefault();
    try {
      await api.post('/payments', {
        student_id: parseInt(formData.student_id),
        course_id: parseInt(formData.course_id),
        paid_amount: parseFloat(formData.paid_amount),
        payment_method: formData.payment_method,
        transaction_reference: formData.transaction_reference || `TXN-${Date.now()}`,
        remarks: formData.remarks
      });
      setIsModalOpen(false);
      setFormData({
        student_id: '',
        course_id: '',
        paid_amount: '',
        payment_method: 'UPI',
        transaction_reference: '',
        remarks: 'Tuition installment fee'
      });
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to record payment');
    }
  };

  const totalCollected = payments.reduce((acc, p) => acc + p.paid_amount, 0);
  const totalPending = payments.reduce((acc, p) => acc + p.pending_amount, 0);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-bold text-slate-800">Course Fees & Payment Ledger</h3>
          <p className="text-xs text-slate-500">Track tuition installments, pending dues, and download official receipts</p>
        </div>
        {role === 'admin' && (
          <button
            onClick={() => setIsModalOpen(true)}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition-colors shadow-sm"
          >
            <Plus className="w-4 h-4" />
            <span>Record Payment</span>
          </button>
        )}
      </div>

      {/* Financial Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <div className="bg-white p-5 rounded-xl border border-slate-200">
          <p className="text-xs text-slate-400">Total Approved Collections</p>
          <h4 className="text-2xl font-bold text-emerald-600 mt-1">₹{totalCollected.toLocaleString('en-IN')}</h4>
        </div>
        <div className="bg-white p-5 rounded-xl border border-slate-200">
          <p className="text-xs text-slate-400">Remaining Pending Dues</p>
          <h4 className="text-2xl font-bold text-rose-600 mt-1">₹{totalPending.toLocaleString('en-IN')}</h4>
        </div>
        <div className="bg-white p-5 rounded-xl border border-slate-200">
          <p className="text-xs text-slate-400">Total Transactions</p>
          <h4 className="text-2xl font-bold text-slate-800 mt-1">{payments.length}</h4>
        </div>
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="px-5 py-4 border-b border-slate-100 font-bold text-slate-800 text-sm">
            Transaction Entries
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-700">
              <thead className="bg-slate-50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200">
                <tr>
                  <th className="px-5 py-3">Txn Reference</th>
                  <th className="px-5 py-3">Student</th>
                  <th className="px-5 py-3">Course</th>
                  <th className="px-5 py-3">Paid Amount</th>
                  <th className="px-5 py-3">Balance</th>
                  <th className="px-5 py-3">Status</th>
                  <th className="px-5 py-3">Date</th>
                  <th className="px-5 py-3 text-right">Receipt</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {payments.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50/50">
                    <td className="px-5 py-3.5 font-mono text-xs font-bold text-slate-700">
                      {p.transaction_reference}
                    </td>
                    <td className="px-5 py-3.5 font-semibold text-slate-800">{p.student_name}</td>
                    <td className="px-5 py-3.5 text-slate-600">{p.course_title}</td>
                    <td className="px-5 py-3.5 font-bold text-emerald-600">
                      ₹{p.paid_amount.toLocaleString('en-IN')}
                    </td>
                    <td className="px-5 py-3.5 text-xs text-slate-500">
                      ₹{p.pending_amount.toLocaleString('en-IN')}
                    </td>
                    <td className="px-5 py-3.5">
                      <Badge variant={p.status === 'paid' ? 'success' : 'warning'}>
                        {p.status.replace('_', ' ')}
                      </Badge>
                    </td>
                    <td className="px-5 py-3.5 text-xs text-slate-400">
                      {new Date(p.payment_date).toLocaleDateString()}
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      <button
                        onClick={() => downloadAuthenticatedFile(`/payments/${p.id}/receipt`, `Receipt_${p.transaction_reference || p.id}.pdf`)}
                        className="inline-flex items-center gap-1 px-3 py-1 bg-indigo-50 text-indigo-600 hover:bg-indigo-100 rounded-lg text-xs font-bold transition-colors cursor-pointer"
                      >
                        <Download className="w-3.5 h-3.5" /> PDF
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Record Payment Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Record Tuition Payment">
        <form onSubmit={handleRecordPayment} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Student</label>
            <select
              required
              value={formData.student_id}
              onChange={(e) => setFormData({ ...formData, student_id: e.target.value })}
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
            >
              <option value="">Select Student...</option>
              {students.map((s) => (
                <option key={s.id} value={s.id}>{s.name} ({s.email})</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Course</label>
            <select
              required
              value={formData.course_id}
              onChange={(e) => setFormData({ ...formData, course_id: e.target.value })}
              className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
            >
              <option value="">Select Course...</option>
              {courses.map((c) => (
                <option key={c.id} value={c.id}>{c.title} (Fee: ₹{Number(c.fee).toLocaleString('en-IN')})</option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Amount Paid (₹)</label>
              <input
                type="number"
                min="100"
                required
                value={formData.paid_amount}
                onChange={(e) => setFormData({ ...formData, paid_amount: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Payment Method</label>
              <select
                value={formData.payment_method}
                onChange={(e) => setFormData({ ...formData, payment_method: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
              >
                <option value="UPI">UPI</option>
                <option value="NetBanking">Net Banking</option>
                <option value="Card">Debit / Credit Card</option>
                <option value="Cash">Cash / Cheque</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Transaction Reference</label>
            <input
              type="text"
              required
              value={formData.transaction_reference}
              onChange={(e) => setFormData({ ...formData, transaction_reference: e.target.value })}
              placeholder="e.g. TXN-LMS-2026-9901"
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
              Save & Generate Receipt
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
