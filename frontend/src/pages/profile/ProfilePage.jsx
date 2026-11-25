import React, { useState } from 'react';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { User, Lock, Phone, Mail, ShieldCheck, CheckCircle2 } from 'lucide-react';

export const ProfilePage = () => {
  const { user, role, updateUserProfile } = useAuth();
  const [phone, setPhone] = useState(user?.phone || '');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [profileMsg, setProfileMsg] = useState('');
  const [pwMsg, setPwMsg] = useState('');
  const [pwErr, setPwErr] = useState('');

  const handleUpdateContact = async (e) => {
    e.preventDefault();
    try {
      const res = await api.put(`/users/${user.id}`, { phone });
      updateUserProfile(res.data);
      setProfileMsg('Contact information updated successfully.');
      setTimeout(() => setProfileMsg(''), 4000);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to update profile');
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setPwErr('');
    setPwMsg('');
    try {
      await api.post('/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword
      });
      setPwMsg('Password changed successfully.');
      setCurrentPassword('');
      setNewPassword('');
      setTimeout(() => setPwMsg(''), 4000);
    } catch (err) {
      setPwErr(err.response?.data?.detail || 'Failed to change password');
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h3 className="text-xl font-bold text-slate-800">User Profile & Account Security</h3>
        <p className="text-xs text-slate-500">Manage personal contact preferences and security credentials</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Profile Card */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm text-center space-y-3">
          <div className="w-20 h-20 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold text-2xl mx-auto border-2 border-indigo-100 shadow-inner">
            {user?.first_name ? user.first_name[0] : 'U'}
          </div>
          <div>
            <h4 className="font-bold text-slate-800 text-lg">{user?.first_name} {user?.last_name}</h4>
            <p className="text-xs text-slate-400">{user?.email}</p>
          </div>
          <span className="inline-flex items-center gap-1 px-3 py-1 bg-indigo-50 text-indigo-700 rounded-full text-xs font-bold uppercase tracking-wider">
            <ShieldCheck className="w-3.5 h-3.5" /> {role}
          </span>
        </div>

        {/* Update Forms */}
        <div className="md:col-span-2 space-y-6">
          {/* Contact Details */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <h4 className="font-bold text-slate-800 text-base">Contact Information</h4>
            {profileMsg && (
              <p className="text-xs text-emerald-600 font-semibold">{profileMsg}</p>
            )}

            <form onSubmit={handleUpdateContact} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address (Read-only)</label>
                <input
                  type="email"
                  disabled
                  value={user?.email || ''}
                  className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-100 text-slate-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Phone Number</label>
                <input
                  type="text"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
                />
              </div>

              <button
                type="submit"
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-bold transition-colors shadow-sm"
              >
                Update Contact
              </button>
            </form>
          </div>

          {/* Change Password */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <h4 className="font-bold text-slate-800 text-base">Update Password</h4>
            {pwMsg && <p className="text-xs text-emerald-600 font-semibold">{pwMsg}</p>}
            {pwErr && <p className="text-xs text-rose-600 font-semibold">{pwErr}</p>}

            <form onSubmit={handleChangePassword} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Current Password</label>
                <input
                  type="password"
                  required
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">New Password (Min 6 chars)</label>
                <input
                  type="password"
                  required
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white"
                />
              </div>

              <button
                type="submit"
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-bold transition-colors shadow-sm"
              >
                Save New Password
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};
