import React from 'react';

export const StatCard = ({ title, value, icon: Icon, trend, color = 'indigo', subtitle }) => {
  const colorMap = {
    indigo: 'bg-indigo-500 text-white shadow-indigo-500/20',
    blue: 'bg-blue-500 text-white shadow-blue-500/20',
    emerald: 'bg-emerald-500 text-white shadow-emerald-500/20',
    amber: 'bg-amber-500 text-white shadow-amber-500/20',
    rose: 'bg-rose-500 text-white shadow-rose-500/20',
    purple: 'bg-purple-500 text-white shadow-purple-500/20',
  };

  return (
    <div className="bg-white rounded-xl p-5 border border-slate-200/80 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{title}</p>
          <h3 className="text-2xl font-bold text-slate-800 mt-1">{value}</h3>
          {subtitle && <p className="text-xs text-slate-500 mt-0.5">{subtitle}</p>}
        </div>
        <div className={`w-12 h-12 rounded-xl flex items-center justify-center shadow-lg ${colorMap[color] || colorMap.indigo}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
      {trend && (
        <div className="mt-3 pt-3 border-t border-slate-100 flex items-center text-xs">
          <span className="text-emerald-600 font-semibold">{trend}</span>
          <span className="text-slate-400 ml-1.5">vs last month</span>
        </div>
      )}
    </div>
  );
};
