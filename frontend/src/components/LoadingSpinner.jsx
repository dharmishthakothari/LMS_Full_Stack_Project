import React from 'react';
import { Loader2 } from 'lucide-react';

export const LoadingSpinner = ({ text = 'Loading data...' }) => (
  <div className="flex flex-col items-center justify-center p-12 text-slate-500">
    <Loader2 className="w-8 h-8 animate-spin text-indigo-600 mb-3" />
    <p className="text-sm font-medium">{text}</p>
  </div>
);

export const EmptyState = ({ title = 'No Data Available', message = 'There are no records to display at this time.', icon: Icon }) => (
  <div className="flex flex-col items-center justify-center p-12 text-center bg-white rounded-xl border border-slate-200">
    {Icon && (
      <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center text-slate-400 mb-3">
        <Icon className="w-6 h-6" />
      </div>
    )}
    <h4 className="font-bold text-slate-700 text-base">{title}</h4>
    <p className="text-sm text-slate-400 max-w-sm mt-1">{message}</p>
  </div>
);
