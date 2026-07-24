import React, { useState } from 'react';
import api from '../api/client';
import { UploadCloud, CheckCircle2, FileText, AlertCircle, Sparkles, ArrowRight } from 'lucide-react';

export const UploadCSV = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError('');
      setSummary(null);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a CSV file first.');
      return;
    }

    setUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await api.post('/transactions/upload-csv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setSummary(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'CSV upload failed.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <h1 className="text-2xl font-black text-white tracking-tight">Bank CSV Upload Wizard</h1>
        <p className="text-xs text-slate-400 mt-1">
          Import statement CSVs from any bank (HDFC, ICICI, SBI, Chase, Revolut). Auto-detects columns and runs AI categorization.
        </p>
      </div>

      <div className="glass-panel p-8 rounded-3xl border border-slate-800 flex flex-col items-center justify-center text-center">
        <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-4">
          <UploadCloud className="w-8 h-8" />
        </div>

        <h3 className="text-lg font-bold text-white mb-1">Select Bank Statement CSV</h3>
        <p className="text-xs text-slate-400 max-w-md mb-6">
          Drag & drop your bank statement file or click to browse. CSV files will be parsed and auto-categorized instantly.
        </p>

        <form onSubmit={handleUpload} className="w-full max-w-md space-y-4">
          <label className="flex flex-col items-center px-4 py-6 bg-slate-900/80 border-2 border-dashed border-slate-800 rounded-2xl cursor-pointer hover:border-indigo-500 transition">
            <FileText className="w-6 h-6 text-indigo-400 mb-2" />
            <span className="text-xs font-semibold text-slate-200">
              {file ? file.name : 'Choose .csv file'}
            </span>
            <span className="text-[10px] text-slate-500 mt-1">Maximum file size 10MB</span>
            <input type="file" accept=".csv" onChange={handleFileChange} className="hidden" />
          </label>

          {error && (
            <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={uploading || !file}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 text-white font-bold text-xs shadow-lg shadow-indigo-500/25 flex items-center justify-center gap-2 transition disabled:opacity-50"
          >
            {uploading ? 'Parsing & Categorizing...' : 'Upload & Process CSV'}
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>
      </div>

      {summary && (
        <div className="glass-panel p-6 rounded-3xl border border-emerald-500/30 space-y-4">
          <div className="flex items-center gap-3">
            <CheckCircle2 className="w-6 h-6 text-emerald-400" />
            <div>
              <h3 className="font-bold text-white text-base">CSV Import Complete</h3>
              <p className="text-xs text-slate-400">Successfully imported {summary.success_count} transactions.</p>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800">
            <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">AI Categorization Summary</h4>
            <div className="flex flex-wrap gap-2">
              {Object.entries(summary.categorization_breakdown).map(([cat, count]) => (
                <span key={cat} className="px-3 py-1 rounded-xl bg-slate-900 border border-slate-800 text-xs text-indigo-300 font-semibold">
                  {cat}: {count}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
