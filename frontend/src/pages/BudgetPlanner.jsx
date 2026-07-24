import React, { useState, useEffect } from 'react';
import api from '../api/client';
import { PieChart, Plus, AlertTriangle, CheckCircle, Sparkles, Trash2, Edit } from 'lucide-react';

export const BudgetPlanner = () => {
  const [budgets, setBudgets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    category: 'Food',
    period: 'Monthly',
    amount: 15000,
    alert_threshold: 0.8
  });

  const categoriesList = [
    'Food', 'Shopping', 'Travel', 'Bills', 'Healthcare', 'Entertainment',
    'Education', 'Rent', 'Fuel', 'Insurance', 'Miscellaneous', 'Total Monthly Budget'
  ];

  const fetchBudgets = async () => {
    setLoading(true);
    try {
      const res = await api.get('/budgets');
      setBudgets(res.data);
    } catch (err) {
      console.error("Failed to load budgets:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBudgets();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.post('/budgets', {
        ...formData,
        amount: parseFloat(formData.amount)
      });
      setShowModal(false);
      fetchBudgets();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to create budget.");
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Delete budget?")) {
      try {
        await api.delete(`/budgets/${id}`);
        fetchBudgets();
      } catch (err) {
        alert("Delete failed.");
      }
    }
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-3xl border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Budget Planner & Alert Engine</h1>
          <p className="text-xs text-slate-400 mt-1">Set monthly and category spending limits with live overspending warnings</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 text-white font-bold text-xs shadow-lg shadow-indigo-500/25 flex items-center gap-2 transition"
        >
          <Plus className="w-4 h-4" />
          <span>New Category Budget</span>
        </button>
      </div>

      {loading ? (
        <div className="py-12 text-center text-xs text-slate-400">Loading budgets...</div>
      ) : budgets.length === 0 ? (
        <div className="py-12 text-center text-xs text-slate-400">No budgets set. Click above to create your first budget.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {budgets.map((b) => {
            const isOverspent = b.status === 'OVERSPENT';
            const isWarning = b.status === 'WARNING';
            return (
              <div key={b.id} className="glass-panel p-6 rounded-3xl border border-slate-800 flex flex-col justify-between space-y-4">
                <div className="flex items-center justify-between">
                  <span className="font-extrabold text-white text-base">{b.category}</span>
                  <div className="flex items-center gap-2">
                    <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase ${
                      isOverspent ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' :
                      isWarning ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
                      'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                    }`}>
                      {b.status}
                    </span>
                    <button onClick={() => handleDelete(b.id)} className="p-1 rounded text-slate-500 hover:text-rose-400">
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between text-xs mb-1.5">
                    <span className="text-slate-400">Spent: <strong className="text-white">₹{b.spent_amount?.toLocaleString()}</strong></span>
                    <span className="text-slate-400">Limit: <strong className="text-slate-200">₹{b.amount?.toLocaleString()}</strong></span>
                  </div>
                  {/* Progress Bar */}
                  <div className="w-full h-3 rounded-full bg-slate-900 overflow-hidden border border-slate-800">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${
                        isOverspent ? 'bg-rose-500' : isWarning ? 'bg-amber-500' : 'bg-indigo-500'
                      }`}
                      style={{ width: `${Math.min(100, b.percentage_used)}%` }}
                    ></div>
                  </div>
                  <p className="text-[10px] text-right text-slate-500 mt-1">{b.percentage_used}% Used</p>
                </div>

                <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                  <span className="text-slate-400">Remaining</span>
                  <span className={`font-bold ${isOverspent ? 'text-rose-400' : 'text-emerald-400'}`}>
                    ₹{b.remaining_amount?.toLocaleString()}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-md glass-panel p-6 rounded-3xl border border-slate-800">
            <h3 className="text-lg font-extrabold text-white mb-4">Create Category Budget</h3>
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Category</label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white"
                >
                  {categoriesList.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Monthly Budget Amount (₹)</label>
                <input
                  type="number"
                  required
                  value={formData.amount}
                  onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white"
                />
              </div>
              <div className="flex items-center justify-end gap-3 pt-4">
                <button type="button" onClick={() => setShowModal(false)} className="px-4 py-2 rounded-xl bg-slate-800 text-xs font-semibold text-slate-300">
                  Cancel
                </button>
                <button type="submit" className="px-5 py-2 rounded-xl bg-indigo-600 text-xs font-bold text-white shadow-lg">
                  Save Budget
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
