import React from 'react';
import api from '../api/client';

export const Reports = () => {
  const downloadPdf = async () => {
    try {
      const res = await api.get('/reports/download/pdf', { params: { report_type: 'monthly' }, responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
      const a = document.createElement('a');
      a.href = url;
      a.download = 'intelliwealth_monthly_report.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      console.error('Failed to download PDF', err);
    }
  };

  const downloadCsv = async () => {
    try {
      const res = await api.get('/reports/download/csv', { responseType: 'blob' });
      const url = window.URL.createObjectURL(res.data);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'intelliwealth_transactions.csv';
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      console.error('Failed to download CSV', err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <h1 className="text-2xl font-black text-white">Reports & Exports</h1>
        <p className="text-xs text-slate-400">Generate monthly PDF reports or download transactions as CSV.</p>
      </div>

      <div className="glass-panel p-6 rounded-3xl border border-slate-800 flex gap-4">
        <button onClick={downloadPdf} className="px-6 py-3 rounded-xl bg-indigo-600 text-white font-bold">Download Monthly PDF</button>
        <button onClick={downloadCsv} className="px-6 py-3 rounded-xl bg-slate-800 text-slate-200">Download CSV</button>
      </div>
    </div>
  );
};
