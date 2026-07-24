import React, { useState, useEffect } from 'react';
import api from '../api/client';
import { TrendingUp, Cpu, Sparkles, CheckCircle2, ShieldCheck } from 'lucide-react';
import { Line } from 'react-chartjs-2';

export const Forecast = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchForecast = async () => {
      try {
        const res = await api.get('/forecast/predict');
        setData(res.data);
      } catch (err) {
        console.error("Failed to load forecast:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchForecast();
  }, []);

  if (loading) {
    return <div className="py-12 text-center text-xs text-slate-400">Running Scikit-Learn time-series models...</div>;
  }

  const lineChartData = {
    labels: data?.cash_flow_forecast.map(c => c.month) || [],
    datasets: [
      {
        label: 'Predicted Income',
        data: data?.cash_flow_forecast.map(c => c.predicted_income) || [],
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        fill: true,
        tension: 0.4
      },
      {
        label: 'Predicted Expense',
        data: data?.cash_flow_forecast.map(c => c.predicted_expense) || [],
        borderColor: '#f43f5e',
        backgroundColor: 'rgba(244, 63, 94, 0.1)',
        fill: true,
        tension: 0.4
      }
    ]
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-3xl border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-semibold mb-2">
            <Cpu className="w-3.5 h-3.5" />
            <span>Scikit-Learn Machine Learning Engine</span>
          </div>
          <h1 className="text-2xl font-black text-white tracking-tight">Spending & Savings Forecast</h1>
          <p className="text-xs text-slate-400 mt-1">Predictive time-series modeling trained on your historical transaction data</p>
        </div>
        <div className="px-4 py-2 rounded-2xl bg-slate-900 border border-slate-800 text-xs text-slate-300">
          Model Confidence: <strong className="text-emerald-400 font-mono">{(data?.confidence * 100).toFixed(0)}%</strong>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Metric Card 1 */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-800">
          <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Next Month Predicted Spending</span>
          <div className="text-3xl font-black text-white mt-2">₹{data?.next_month_spending?.toLocaleString()}</div>
          <p className="text-xs text-slate-400 mt-1">Estimated total outflow for upcoming month</p>
        </div>

        {/* Metric Card 2 */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-800">
          <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Projected Future Monthly Savings</span>
          <div className="text-3xl font-black text-emerald-400 mt-2">₹{data?.future_savings?.toLocaleString()}</div>
          <p className="text-xs text-slate-400 mt-1">Estimated net investable cash flow</p>
        </div>
      </div>

      {/* Cash Flow Forecast Chart */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <h2 className="text-base font-bold text-white mb-2">3-Month Forward Cash Flow Prediction</h2>
        <div className="h-72 my-4">
          <Line data={lineChartData} options={{ responsive: true, maintainAspectRatio: false }} />
        </div>
      </div>

      {/* Category Forecast Breakdown */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <h2 className="text-base font-bold text-white mb-4">Category-Wise Predictive Breakdown</h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {data?.category_forecast.map((cf) => (
            <div key={cf.category} className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
              <span className="text-xs text-slate-400 font-semibold block">{cf.category}</span>
              <span className="text-base font-extrabold text-white mt-1 block">₹{cf.predicted_amount?.toLocaleString()}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
