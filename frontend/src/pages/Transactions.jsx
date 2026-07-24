import React, { useState, useEffect } from 'react';
import api from '../api/client';
import { Plus, Search, Filter, Trash2, Edit2, ChevronLeft, ChevronRight, Sparkles, AlertCircle, Check } from 'lucide-react';

export const Transactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [type, setType] = useState('');
  const [loading, setLoading] = useState(true);

  // Add / Edit Modal state
  const [showModal, setShowModal] = useState(false);
  const [editingTx, setEditingTx] = useState(null);
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    merchant: '',
    amount: '',
    type: 'Expense',
    category: '',
    payment_method: 'UPI/Bank',
    notes: ''
  });

  const categoriesList = [
    'Food', 'Shopping', 'Travel', 'Bills', 'Healthcare', 'Entertainment',
    'Education', 'Salary', 'Investment', 'Rent', 'Fuel', 'Insurance', 'Miscellaneous'
  ];

  const fetchTransactions = async () => {
    setLoading(true);
    try {
      const res = await api.get('/transactions', {
        params: {
          page,
          limit: 15,
          search: search || undefined,
          category: category || undefined,
          type: type || undefined
        }
      });
      setTransactions(res.data.items);
      setTotal(res.data.total);
      setTotalPages(res.data.total_pages);
    } catch (err) {
      console.error("Failed to fetch transactions:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, [page, search, category, type]);

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      if (editingTx) {
        await api.put(`/transactions/${editingTx.id}`, {
          ...formData,
          amount: parseFloat(formData.amount)
        });
      } else {
        await api.post('/transactions', {
          ...formData,
          amount: parseFloat(formData.amount)
        });
      }
      setShowModal(false);
      setEditingTx(null);
      setFormData({
        date: new Date().toISOString().split('T')[0],
        merchant: '',
        amount: '',
        type: 'Expense',
        category: '',
        payment_method: 'UPI/Bank',
        notes: ''
      });
      fetchTransactions();
    } catch (err) {
      alert("Error saving transaction.");
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this transaction?")) {
      try {
        await api.delete(`/transactions/${id}`);
        fetchTransactions();
      } catch (err) {
        alert("Failed to delete transaction.");
      }
    }
  };

  const openEditModal = (tx) => {
    setEditingTx(tx);
    setFormData({
      date: tx.date,
      merchant: tx.merchant,
      amount: tx.amount,
      type: tx.type,
      category: tx.category,
      payment_method: tx.payment_method || 'UPI/Bank',
      notes: tx.notes || ''
    });
    setShowModal(true);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 glass-panel p-6 rounded-3xl border border-slate-800">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Transaction Management</h1>
          <p className="text-xs text-slate-400 mt-1">Total {total} transactions recorded with AI auto-categorization</p>
        </div>
        <button
          onClick={() => {
            setEditingTx(null);
            setFormData({
              date: new Date().toISOString().split('T')[0],
              merchant: '',
              amount: '',
              type: 'Expense',
              category: '',
              payment_method: 'UPI/Bank',
              notes: ''
            });
            setShowModal(true);
          }}
          className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 text-white font-bold text-xs shadow-lg shadow-indigo-500/25 flex items-center gap-2 transition"
        >
          <Plus className="w-4 h-4" />
          <span>Add Transaction</span>
        </button>
      </div>

      {/* Search & Filter Bar */}
      <div className="glass-panel p-4 rounded-2xl border border-slate-800 flex flex-wrap items-center gap-3">
        <div className="flex-1 min-w-[200px] relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            placeholder="Search merchant, category, notes..."
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPage(1); }}
            className="w-full bg-slate-900/80 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
          />
        </div>

        <select
          value={category}
          onChange={(e) => { setCategory(e.target.value); setPage(1); }}
          className="bg-slate-900/80 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
        >
          <option value="">All Categories</option>
          {categoriesList.map(c => <option key={c} value={c}>{c}</option>)}
        </select>

        <select
          value={type}
          onChange={(e) => { setType(e.target.value); setPage(1); }}
          className="bg-slate-900/80 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
        >
          <option value="">All Types</option>
          <option value="Expense">Expense</option>
          <option value="Income">Income</option>
        </select>
      </div>

      {/* Transactions Table */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        {loading ? (
          <div className="py-12 text-center text-xs text-slate-400">Loading transactions...</div>
        ) : transactions.length === 0 ? (
          <div className="py-12 text-center text-xs text-slate-400">No transactions found.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="text-slate-400 border-b border-slate-800 pb-3 uppercase tracking-wider">
                  <th className="py-3 px-3">Date</th>
                  <th className="py-3 px-3">Merchant</th>
                  <th className="py-3 px-3">Category</th>
                  <th className="py-3 px-3">Type</th>
                  <th className="py-3 px-3">Engine</th>
                  <th className="py-3 px-3 text-right">Amount</th>
                  <th className="py-3 px-3 text-center">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50">
                {transactions.map((t) => (
                  <tr key={t.id} className="hover:bg-slate-900/40 transition">
                    <td className="py-3 px-3 text-slate-300 font-mono">{t.date}</td>
                    <td className="py-3 px-3 font-semibold text-white">
                      {t.merchant}
                      {t.notes && <p className="text-[10px] text-slate-500 font-normal">{t.notes}</p>}
                    </td>
                    <td className="py-3 px-3">
                      <span className="px-2.5 py-1 rounded-lg text-[10px] font-semibold bg-slate-800 text-indigo-300 border border-slate-700">
                        {t.category}
                      </span>
                    </td>
                    <td className="py-3 px-3 font-semibold">
                      <span className={t.type === 'Income' ? 'text-emerald-400' : 'text-slate-200'}>
                        {t.type}
                      </span>
                    </td>
                    <td className="py-3 px-3">
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 text-[9px] rounded-md bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 font-mono uppercase">
                        <Sparkles className="w-2.5 h-2.5 text-indigo-400" />
                        {t.categorizer_type}
                      </span>
                    </td>
                    <td className={`py-3 px-3 text-right font-bold text-sm ${t.type === 'Income' ? 'text-emerald-400' : 'text-white'}`}>
                      {t.type === 'Income' ? '+' : '-'}₹{t.amount?.toLocaleString()}
                    </td>
                    <td className="py-3 px-3 text-center">
                      <div className="flex items-center justify-center gap-2">
                        <button onClick={() => openEditModal(t)} className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition">
                          <Edit2 className="w-3.5 h-3.5" />
                        </button>
                        <button onClick={() => handleDelete(t.id)} className="p-1.5 rounded-lg hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 transition">
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination Controls */}
        <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <span>Page {page} of {totalPages}</span>
          <div className="flex items-center gap-2">
            <button
              disabled={page <= 1}
              onClick={() => setPage(page - 1)}
              className="p-2 rounded-xl bg-slate-900 border border-slate-800 disabled:opacity-40 hover:bg-slate-800 transition"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              disabled={page >= totalPages}
              onClick={() => setPage(page + 1)}
              className="p-2 rounded-xl bg-slate-900 border border-slate-800 disabled:opacity-40 hover:bg-slate-800 transition"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Add / Edit Transaction Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-md glass-panel p-6 rounded-3xl border border-slate-800 shadow-2xl">
            <h3 className="text-lg font-extrabold text-white mb-4">
              {editingTx ? 'Edit Transaction' : 'Add Manual Expense / Income'}
            </h3>
            <form onSubmit={handleSave} className="space-y-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Date</label>
                <input
                  type="date"
                  required
                  value={formData.date}
                  onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Merchant / Payee</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Swiggy, Uber, Starbucks"
                  value={formData.merchant}
                  onChange={(e) => setFormData({ ...formData, merchant: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Amount (₹)</label>
                  <input
                    type="number"
                    step="0.01"
                    required
                    value={formData.amount}
                    onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Type</label>
                  <select
                    value={formData.type}
                    onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white"
                  >
                    <option value="Expense">Expense</option>
                    <option value="Income">Income</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Category (Leave blank for AI Categorization)</label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white"
                >
                  <option value="">Auto-Categorize with AI</option>
                  {categoriesList.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div className="flex items-center justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-xs font-semibold text-slate-300 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-xs font-bold text-white shadow-lg shadow-indigo-500/25"
                >
                  Save Transaction
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
