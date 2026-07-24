import React, { useState, useEffect } from 'react';
import api from '../api/client';
import { Target, Plus, CheckCircle2, Calendar, Sparkles, DollarSign } from 'lucide-react';

export const Goals = () => {
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [contribModal, setContribModal] = useState(null);
  const [contribAmount, setContribAmount] = useState(5000);

  const [formData, setFormData] = useState({
    title: '',
    category: 'Emergency Fund',
    target_amount: 300000,
    current_amount: 50000,
    deadline: '2027-12-31'
  });

  const categories = ['Emergency Fund', 'Vacation', 'Bike', 'Car', 'House', 'Education', 'Marriage', 'Retirement'];

  const fetchGoals = async () => {
    setLoading(true);
    try {
      const res = await api.get('/goals');
      setGoals(res.data);
    } catch (err) {
      console.error("Failed to fetch goals:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGoals();
  }, []);

  const handleCreateGoal = async (e) => {
    e.preventDefault();
    try {
      await api.post('/goals', {
        ...formData,
        target_amount: parseFloat(formData.target_amount),
        current_amount: parseFloat(formData.current_amount)
      });
      setShowModal(false);
      fetchGoals();
    } catch (err) {
      alert("Failed to create goal.");
    }
  };

  const handleContribute = async (e) => {
    e.preventDefault();
    if (!contribModal) return;
    try {
      await api.post(`/goals/${contribModal.id}/contribute`, {
        amount: parseFloat(contribAmount)
      });
      setContribModal(null);
      fetchGoals();
    } catch (err) {
      alert("Failed to record deposit.");
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Delete goal?")) {
      try {
        await api.delete(`/goals/${id}`);
        fetchGoals();
      } catch (err) {
        alert("Failed to delete goal.");
      }
    }
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-3xl border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Financial Goal Planner</h1>
          <p className="text-xs text-slate-400 mt-1">Track target milestones, deadlines & AI recommended monthly deposit contributions</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 text-white font-bold text-xs shadow-lg flex items-center gap-2 transition"
        >
          <Plus className="w-4 h-4" />
          <span>Create New Goal</span>
        </button>
      </div>

      {loading ? (
        <div className="py-12 text-center text-xs text-slate-400">Loading goals...</div>
      ) : goals.length === 0 ? (
        <div className="py-12 text-center text-xs text-slate-400">No active goals. Create one above!</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {goals.map((g) => (
            <div key={g.id} className="glass-panel p-6 rounded-3xl border border-slate-800 flex flex-col justify-between space-y-4">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 font-bold">
                    <Target className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-extrabold text-white text-base">{g.title}</h3>
                    <p className="text-xs text-slate-400">{g.category} • Target Deadline: {g.deadline}</p>
                  </div>
                </div>
                <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase ${
                  g.status === 'COMPLETED' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20'
                }`}>
                  {g.status}
                </span>
              </div>

              <div>
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="text-slate-400">Saved: <strong className="text-white">₹{g.current_amount?.toLocaleString()}</strong></span>
                  <span className="text-slate-400">Target: <strong className="text-slate-200">₹{g.target_amount?.toLocaleString()}</strong></span>
                </div>
                <div className="w-full h-3 rounded-full bg-slate-900 overflow-hidden border border-slate-800">
                  <div
                    className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full transition-all duration-500"
                    style={{ width: `${g.progress_percentage}%` }}
                  ></div>
                </div>
                <p className="text-[10px] text-right text-slate-400 mt-1">{g.progress_percentage}% Completed</p>
              </div>

              <div className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800 text-xs text-indigo-300 flex items-center justify-between">
                <span className="flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                  AI Monthly Savings Suggestion:
                </span>
                <strong className="text-white font-mono">₹{g.ai_monthly_saving_suggestion?.toLocaleString()}/mo</strong>
              </div>

              <div className="pt-3 border-t border-slate-800 flex items-center justify-between">
                <button
                  onClick={() => setContribModal(g)}
                  className="px-4 py-1.5 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 text-xs font-bold transition"
                >
                  + Add Deposit
                </button>
                <button onClick={() => handleDelete(g.id)} className="text-xs text-slate-500 hover:text-rose-400">
                  Delete Goal
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-md glass-panel p-6 rounded-3xl border border-slate-800">
            <h3 className="text-lg font-extrabold text-white mb-4">Create Financial Goal</h3>
            <form onSubmit={handleCreateGoal} className="space-y-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Goal Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Electric Bike, Emergency Fund"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Target Amount (₹)</label>
                  <input
                    type="number"
                    required
                    value={formData.target_amount}
                    onChange={(e) => setFormData({ ...formData, target_amount: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Current Saved (₹)</label>
                  <input
                    type="number"
                    value={formData.current_amount}
                    onChange={(e) => setFormData({ ...formData, current_amount: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Target Deadline Date</label>
                <input
                  type="date"
                  required
                  value={formData.deadline}
                  onChange={(e) => setFormData({ ...formData, deadline: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white"
                />
              </div>
              <div className="flex items-center justify-end gap-3 pt-4">
                <button type="button" onClick={() => setShowModal(false)} className="px-4 py-2 rounded-xl bg-slate-800 text-xs font-semibold text-slate-300">
                  Cancel
                </button>
                <button type="submit" className="px-5 py-2 rounded-xl bg-indigo-600 text-xs font-bold text-white shadow-lg">
                  Save Goal
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Deposit Modal */}
      {contribModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-sm glass-panel p-6 rounded-3xl border border-slate-800">
            <h3 className="text-base font-extrabold text-white mb-2">Deposit to '{contribModal.title}'</h3>
            <form onSubmit={handleContribute} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Deposit Amount (₹)</label>
                <input
                  type="number"
                  required
                  value={contribAmount}
                  onChange={(e) => setContribAmount(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white"
                />
              </div>
              <div className="flex items-center justify-end gap-3">
                <button type="button" onClick={() => setContribModal(null)} className="px-4 py-2 rounded-xl bg-slate-800 text-xs font-semibold text-slate-300">
                  Cancel
                </button>
                <button type="submit" className="px-5 py-2 rounded-xl bg-emerald-600 text-xs font-bold text-white shadow-lg">
                  Confirm Deposit
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
