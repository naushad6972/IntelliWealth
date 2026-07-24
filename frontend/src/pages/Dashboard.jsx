import React, { useState, useEffect } from 'react';
import { StatCard } from '../components/StatCard';
import { DollarSign, TrendingUp, TrendingDown, Wallet, ArrowUpRight, ArrowDownRight, Sparkles, CreditCard, Building2, Download } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../api/client';
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, ArcElement
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, ArcElement);

export const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await api.get('/analytics/dashboard');
        setData(res.data);
      } catch (err) {
        console.error("Dashboard fetch error:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const cashFlowChartData = {
    labels: data?.monthly_cash_flow.map(m => m.month) || [],
    datasets: [
      {
        label: 'Income',
        data: data?.monthly_cash_flow.map(m => m.income) || [],
        backgroundColor: 'rgba(16, 185, 129, 0.8)',
        borderRadius: 8,
      },
      {
        label: 'Expense',
        data: data?.monthly_cash_flow.map(m => m.expense) || [],
        backgroundColor: 'rgba(244, 63, 94, 0.8)',
        borderRadius: 8,
      }
    ]
  };

  const categoryPieData = {
    labels: data?.category_distribution.map(c => c.category) || [],
    datasets: [
      {
        data: data?.category_distribution.map(c => c.amount) || [],
        backgroundColor: [
          '#6366f1', '#10b981', '#f43f5e', '#a855f7', '#ec4899', '#3b82f6', '#f59e0b', '#14b8a6'
        ],
        borderWidth: 0
      }
    ]
  };

  return (
    <div className="space-y-6">
      {/* Top Banner Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 glass-panel p-6 rounded-3xl border-indigo-500/20 relative overflow-hidden">
        <div className="relative z-10">
          <div className="inline-flex items-center gap-2 text-xs font-semibold text-indigo-400 bg-indigo-500/10 px-3 py-1 rounded-full border border-indigo-500/20 mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Cash Flow Optimization Active</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">Executive Dashboard</h1>
          <p className="text-xs text-slate-400 mt-1">Real-time financial intelligence overview & auto-synced account metrics</p>
        </div>
        <div className="flex items-center gap-3 relative z-10">
          <Link to="/connect-bank" className="px-4 py-2.5 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/30 border border-indigo-500/30 text-indigo-300 font-semibold text-xs flex items-center gap-2 transition">
            <Building2 className="w-4 h-4" />
            <span>Bank Sync</span>
          </Link>
          <Link to="/reports" className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 text-white font-bold text-xs shadow-lg shadow-indigo-500/20 flex items-center gap-2 transition">
            <Download className="w-4 h-4" />
            <span>Export Report</span>
          </Link>
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Monthly Income"
          amount={`₹${data?.total_income?.toLocaleString() || '0'}`}
          subtitle="Salary & Freelance"
          icon={TrendingUp}
          color="emerald"
        />
        <StatCard
          title="Total Expenses"
          amount={`₹${data?.total_expense?.toLocaleString() || '0'}`}
          subtitle="Auto-Categorized"
          icon={TrendingDown}
          color="rose"
        />
        <StatCard
          title="Net Monthly Savings"
          amount={`₹${data?.savings?.toLocaleString() || '0'}`}
          subtitle={`Savings Rate: ${data?.savings_rate || 0}%`}
          icon={DollarSign}
          color="indigo"
        />
        <StatCard
          title="Liquid Balance"
          amount={`₹${data?.current_balance?.toLocaleString() || '0'}`}
          subtitle="Connected Accounts"
          icon={Wallet}
          color="purple"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Cash Flow Bar Chart */}
        <div className="lg:col-span-2 glass-panel p-6 rounded-3xl border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-base font-bold text-white">Monthly Cash Flow Trend</h2>
              <p className="text-xs text-slate-400">Income vs Expenses over recent months</p>
            </div>
          </div>
          <div className="h-72">
            <Bar data={cashFlowChartData} options={{ responsive: true, maintainAspectRatio: false }} />
          </div>
        </div>

        {/* Category Pie Chart */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-800 flex flex-col justify-between">
          <div>
            <h2 className="text-base font-bold text-white">Expense Distribution</h2>
            <p className="text-xs text-slate-400">Category breakdown</p>
          </div>
          <div className="h-56 my-4 flex items-center justify-center">
            <Pie data={categoryPieData} options={{ responsive: true, maintainAspectRatio: false }} />
          </div>
          <div className="pt-3 border-t border-slate-800 text-center">
            <Link to="/analytics" className="text-xs text-indigo-400 hover:underline font-semibold">View Deep Analytics →</Link>
          </div>
        </div>
      </div>

      {/* Recent Transactions Table */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-base font-bold text-white">Recent Transactions</h2>
            <p className="text-xs text-slate-400">Auto-synced and uploaded activities</p>
          </div>
          <Link to="/transactions" className="text-xs font-semibold text-indigo-400 hover:underline">View All ({data?.recent_transactions?.length || 0})</Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="text-slate-400 border-b border-slate-800/80 pb-3 uppercase tracking-wider">
                <th className="py-3 px-3">Date</th>
                <th className="py-3 px-3">Merchant</th>
                <th className="py-3 px-3">Category</th>
                <th className="py-3 px-3">Type</th>
                <th className="py-3 px-3 text-right">Amount</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {data?.recent_transactions?.map((t) => (
                <tr key={t.id} className="hover:bg-slate-900/40 transition">
                  <td className="py-3 px-3 text-slate-300 font-mono">{t.date}</td>
                  <td className="py-3 px-3 font-semibold text-white">{t.merchant}</td>
                  <td className="py-3 px-3">
                    <span className="px-2.5 py-1 rounded-lg text-[10px] font-semibold bg-slate-800 text-indigo-300 border border-slate-700">
                      {t.category}
                    </span>
                  </td>
                  <td className="py-3 px-3">
                    <span className={`inline-flex items-center gap-1 font-semibold ${t.type === 'Income' ? 'text-emerald-400' : 'text-rose-400'}`}>
                      {t.type === 'Income' ? <ArrowUpRight className="w-3.5 h-3.5" /> : <ArrowDownRight className="w-3.5 h-3.5" />}
                      {t.type}
                    </span>
                  </td>
                  <td className={`py-3 px-3 text-right font-bold text-sm ${t.type === 'Income' ? 'text-emerald-400' : 'text-slate-100'}`}>
                    {t.type === 'Income' ? '+' : '-'}₹{t.amount?.toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
