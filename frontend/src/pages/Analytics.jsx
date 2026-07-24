import React, { useState, useEffect } from 'react';
import api from '../api/client';
import { BarChart3, Store, Calendar, Repeat, Flame, ArrowUpRight } from 'lucide-react';
import { Bar } from 'react-chartjs-2';

export const Analytics = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const res = await api.get('/analytics/expense');
        setData(res.data);
      } catch (err) {
        console.error("Failed to load analytics:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) {
    return <div className="py-12 text-center text-xs text-slate-400">Loading analytics...</div>;
  }

  const heatmapChartData = {
    labels: data?.heatmap.map(h => h.day) || [],
    datasets: [
      {
        label: 'Spending Intensity (₹)',
        data: data?.heatmap.map(h => h.amount) || [],
        backgroundColor: 'rgba(99, 102, 241, 0.8)',
        borderRadius: 8
      }
    ]
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <h1 className="text-2xl font-black text-white tracking-tight">Deep Expense Analytics</h1>
        <p className="text-xs text-slate-400 mt-1">Multi-dimensional spending breakdown, top merchants, recurring subscriptions & weekend intensity</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Top Merchants */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-800">
          <h2 className="text-base font-bold text-white mb-4 flex items-center gap-2">
            <Store className="w-4 h-4 text-indigo-400" />
            <span>Top Merchants</span>
          </h2>
          <div className="space-y-3">
            {data?.top_merchants.map((m) => (
              <div key={m.merchant} className="flex items-center justify-between p-3 rounded-2xl bg-slate-900/60 border border-slate-800 text-xs">
                <div>
                  <p className="font-semibold text-white">{m.merchant}</p>
                  <p className="text-[10px] text-slate-500">{m.transactions_count} transactions</p>
                </div>
                <span className="font-bold text-slate-100">₹{m.amount?.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Weekend Spending & Recurring */}
        <div className="space-y-6">
          {/* Weekend vs Weekday Card */}
          <div className="glass-panel p-6 rounded-3xl border border-slate-800">
            <h2 className="text-base font-bold text-white mb-2 flex items-center gap-2">
              <Calendar className="w-4 h-4 text-purple-400" />
              <span>Weekend Spending Intensity</span>
            </h2>
            <div className="mt-4">
              <div className="text-3xl font-black text-white">{data?.weekend_spending.weekend_percentage}%</div>
              <p className="text-xs text-slate-400 mt-1">
                ₹{data?.weekend_spending.weekend_total?.toLocaleString()} spent on Saturdays & Sundays.
              </p>
            </div>
          </div>

          {/* Recurring Expenses */}
          <div className="glass-panel p-6 rounded-3xl border border-slate-800">
            <h2 className="text-base font-bold text-white mb-4 flex items-center gap-2">
              <Repeat className="w-4 h-4 text-emerald-400" />
              <span>Recurring Subscriptions</span>
            </h2>
            <div className="space-y-2">
              {data?.recurring_expenses.map((r) => (
                <div key={r.merchant} className="flex items-center justify-between text-xs py-1.5 border-b border-slate-800/60">
                  <span className="text-slate-300">{r.merchant}</span>
                  <span className="font-bold text-slate-100">₹{r.monthly_amount?.toLocaleString()}/mo</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Day of Week Heatmap Chart */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-800 flex flex-col justify-between">
          <div>
            <h2 className="text-base font-bold text-white mb-1 flex items-center gap-2">
              <Flame className="w-4 h-4 text-pink-400" />
              <span>Day of Week Heatmap</span>
            </h2>
            <p className="text-xs text-slate-400">Weekly spending volume</p>
          </div>
          <div className="h-64 my-4">
            <Bar data={heatmapChartData} options={{ responsive: true, maintainAspectRatio: false }} />
          </div>
        </div>
      </div>
    </div>
  );
};
