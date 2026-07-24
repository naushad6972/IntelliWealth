import React, { useState, useEffect } from 'react';
import api from '../api/client';
import { Calculator, DollarSign, Percent, Calendar, ArrowRight } from 'lucide-react';

export const EMICalculator = () => {
  const [loanAmount, setLoanAmount] = useState(1000000);
  const [interestRate, setInterestRate] = useState(8.5);
  const [tenureMonths, setTenureMonths] = useState(60);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const calculateEMI = async () => {
    setLoading(true);
    try {
      const res = await api.post('/emi/calculate', {
        loan_amount: parseFloat(loanAmount),
        interest_rate: parseFloat(interestRate),
        tenure_months: parseInt(tenureMonths)
      });
      setResult(res.data);
    } catch (err) {
      console.error("EMI calculation error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    calculateEMI();
  }, [loanAmount, interestRate, tenureMonths]);

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <h1 className="text-2xl font-black text-white tracking-tight">EMI & Loan Amortization Calculator</h1>
        <p className="text-xs text-slate-400 mt-1">Calculate monthly EMIs, total interest payable, loan comparisons, and complete repayment schedules</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Input Parameters Form */}
        <div className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-4">
          <h2 className="text-base font-bold text-white mb-2 flex items-center gap-2">
            <Calculator className="w-4 h-4 text-indigo-400" />
            <span>Loan Parameters</span>
          </h2>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Loan Principal Amount (₹)</label>
            <input
              type="number"
              value={loanAmount}
              onChange={(e) => setLoanAmount(e.target.value)}
              className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Annual Interest Rate (%)</label>
            <input
              type="number"
              step="0.1"
              value={interestRate}
              onChange={(e) => setInterestRate(e.target.value)}
              className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-white"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Tenure (Months: {tenureMonths} / {(tenureMonths/12).toFixed(1)} years)</label>
            <input
              type="range"
              min="12"
              max="360"
              step="12"
              value={tenureMonths}
              onChange={(e) => setTenureMonths(e.target.value)}
              className="w-full accent-indigo-500"
            />
          </div>
        </div>

        {/* Results Summary Cards */}
        <div className="lg:col-span-2 grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="glass-panel p-6 rounded-3xl border border-indigo-500/30">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Monthly EMI</span>
            <div className="text-3xl font-black text-indigo-400 mt-2">₹{result?.monthly_emi?.toLocaleString()}</div>
            <p className="text-xs text-slate-400 mt-1">Fixed monthly outflow</p>
          </div>

          <div className="glass-panel p-6 rounded-3xl border border-slate-800">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Total Interest Payable</span>
            <div className="text-2xl font-extrabold text-rose-400 mt-2">₹{result?.total_interest?.toLocaleString()}</div>
            <p className="text-xs text-slate-400 mt-1">Interest cost over tenure</p>
          </div>

          <div className="glass-panel p-6 rounded-3xl border border-slate-800">
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Total Repayment Amount</span>
            <div className="text-2xl font-extrabold text-white mt-2">₹{result?.total_payment?.toLocaleString()}</div>
            <p className="text-xs text-slate-400 mt-1">Principal + Interest</p>
          </div>

          {/* Tenure Comparison Table */}
          <div className="sm:col-span-3 glass-panel p-6 rounded-3xl border border-slate-800">
            <h3 className="text-sm font-bold text-white mb-3">Tenure Comparison Matrix</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="text-slate-400 border-b border-slate-800 pb-2 uppercase">
                    <th className="py-2 px-2">Tenure</th>
                    <th className="py-2 px-2">Monthly EMI</th>
                    <th className="py-2 px-2">Total Interest</th>
                    <th className="py-2 px-2 text-right">Total Payment</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/50">
                  {result?.comparison.map((comp) => (
                    <tr key={comp.tenure_months} className={comp.tenure_months === parseInt(tenureMonths) ? 'bg-indigo-500/10 font-bold text-indigo-300' : 'text-slate-300'}>
                      <td className="py-2 px-2">{comp.tenure_years} Years ({comp.tenure_months}m)</td>
                      <td className="py-2 px-2">₹{comp.monthly_emi?.toLocaleString()}</td>
                      <td className="py-2 px-2 text-rose-400">₹{comp.total_interest?.toLocaleString()}</td>
                      <td className="py-2 px-2 text-right">₹{comp.total_payment?.toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      {/* Amortization Schedule Table */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <h2 className="text-base font-bold text-white mb-4">First 12 Months Repayment Amortization Schedule</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="text-slate-400 border-b border-slate-800 pb-3 uppercase">
                <th className="py-2 px-3">Month</th>
                <th className="py-2 px-3">Monthly EMI</th>
                <th className="py-2 px-3">Principal Component</th>
                <th className="py-2 px-3">Interest Component</th>
                <th className="py-2 px-3 text-right">Remaining Balance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {result?.schedule.slice(0, 12).map((s) => (
                <tr key={s.month} className="hover:bg-slate-900/40">
                  <td className="py-2.5 px-3 font-mono text-slate-300">Month {s.month}</td>
                  <td className="py-2.5 px-3 font-semibold text-white">₹{s.emi?.toLocaleString()}</td>
                  <td className="py-2.5 px-3 text-emerald-400">₹{s.principal_paid?.toLocaleString()}</td>
                  <td className="py-2.5 px-3 text-rose-400">₹{s.interest_paid?.toLocaleString()}</td>
                  <td className="py-2.5 px-3 text-right font-mono text-slate-200">₹{s.balance?.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
