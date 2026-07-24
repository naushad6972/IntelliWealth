import React, { useState, useEffect } from 'react';
import api from '../api/client';
import { Activity, ShieldCheck, CheckCircle2, AlertCircle, Sparkles, TrendingUp, Lightbulb } from 'lucide-react';

export const HealthScore = () => {
  const [healthData, setHealthData] = useState(null);
  const [recData, setRecData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [hRes, rRes] = await Promise.all([
          api.get('/health/score'),
          api.get('/health/savings-recommendations')
        ]);
        setHealthData(hRes.data);
        setRecData(rRes.data);
      } catch (err) {
        console.error("Failed to load health score:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <div className="py-12 text-center text-xs text-slate-400">Calculating Financial Health Score...</div>;
  }

  const scoreColor = healthData?.score >= 80 ? 'text-emerald-400' : healthData?.score >= 65 ? 'text-indigo-400' : healthData?.score >= 50 ? 'text-amber-400' : 'text-rose-400';

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-3xl border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Financial Health Score Audit</h1>
          <p className="text-xs text-slate-400 mt-1">Multi-metric health assessment evaluated from 0 to 100 based on your savings, emergency fund & budget discipline</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Score Gauge Card */}
        <div className="glass-panel p-8 rounded-3xl border border-slate-800 flex flex-col items-center justify-center text-center">
          <div className="relative w-40 h-40 flex items-center justify-center mb-4">
            <div className="w-full h-full rounded-full border-8 border-slate-900 flex items-center justify-center">
              <div className="text-center">
                <span className={`text-5xl font-black ${scoreColor}`}>{healthData?.score}</span>
                <span className="text-xs font-bold text-slate-400 block uppercase tracking-wider mt-1">{healthData?.rating}</span>
              </div>
            </div>
          </div>
          <p className="text-xs text-slate-400 max-w-xs">
            Score based on Savings Rate, Emergency Fund, Investment Habit, Budget Discipline & Discretionary Ratio.
          </p>
        </div>

        {/* Indicator Metrics Audit */}
        <div className="md:col-span-2 glass-panel p-6 rounded-3xl border border-slate-800 space-y-4">
          <h2 className="text-base font-bold text-white mb-2">5 Core Health Indicators</h2>
          <div className="space-y-3 text-xs">
            <div className="flex items-center justify-between p-3 rounded-2xl bg-slate-900/60 border border-slate-800">
              <span className="text-slate-300">Savings Rate Score ({healthData?.metrics.savings_rate_pct}%)</span>
              <strong className="text-white font-mono">{healthData?.metrics.savings_score} / 25 pts</strong>
            </div>
            <div className="flex items-center justify-between p-3 rounded-2xl bg-slate-900/60 border border-slate-800">
              <span className="text-slate-300">Emergency Fund Score</span>
              <strong className="text-white font-mono">{healthData?.metrics.emergency_fund_score} / 20 pts</strong>
            </div>
            <div className="flex items-center justify-between p-3 rounded-2xl bg-slate-900/60 border border-slate-800">
              <span className="text-slate-300">Budget Discipline Score</span>
              <strong className="text-white font-mono">{healthData?.metrics.budget_discipline_score} / 20 pts</strong>
            </div>
            <div className="flex items-center justify-between p-3 rounded-2xl bg-slate-900/60 border border-slate-800">
              <span className="text-slate-300">Investment Ratio Score</span>
              <strong className="text-white font-mono">{healthData?.metrics.investment_score} / 20 pts</strong>
            </div>
            <div className="flex items-center justify-between p-3 rounded-2xl bg-slate-900/60 border border-slate-800">
              <span className="text-slate-300">Discretionary Ratio Score</span>
              <strong className="text-white font-mono">{healthData?.metrics.discretionary_spending_score} / 15 pts</strong>
            </div>
          </div>
        </div>
      </div>

      {/* Actionable Recommendations */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <h2 className="text-base font-bold text-white mb-4 flex items-center gap-2">
          <Lightbulb className="w-5 h-5 text-amber-400" />
          <span>Step-by-Step Improvement Plan</span>
        </h2>
        <div className="space-y-3">
          {healthData?.improvements.map((tip, idx) => (
            <div key={idx} className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 text-xs text-slate-200 flex items-start gap-3">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>{tip}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Savings Recommendation Engine */}
      <div className="glass-panel p-6 rounded-3xl border border-indigo-500/30">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-indigo-400" />
              <span>Automated Savings Recommendation Engine</span>
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">Potential Monthly Savings Opportunity: <strong className="text-emerald-400 font-extrabold text-sm">₹{recData?.total_potential_savings?.toLocaleString()}</strong></p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {recData?.recommendations.map((rec, i) => (
            <div key={i} className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-2">
              <span className="px-2 py-0.5 text-[10px] font-bold rounded-md bg-indigo-500/20 text-indigo-300 uppercase">{rec.category}</span>
              <h4 className="font-bold text-white text-sm">{rec.title}</h4>
              <p className="text-xs text-slate-400 leading-relaxed">{rec.description}</p>
              <div className="pt-2 text-xs font-bold text-emerald-400">
                Potential Savings: ₹{rec.potential_savings?.toLocaleString()}/mo
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
