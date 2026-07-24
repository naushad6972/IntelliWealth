import React from 'react';

export const StatCard = ({ title, amount, subtitle, icon: Icon, trend, color = 'indigo' }) => {
  const borderGlowMap = {
    indigo: 'hover:border-indigo-500/50 hover:shadow-indigo-500/10',
    emerald: 'hover:border-emerald-500/50 hover:shadow-emerald-500/10',
    rose: 'hover:border-rose-500/50 hover:shadow-rose-500/10',
    purple: 'hover:border-purple-500/50 hover:shadow-purple-500/10',
  };

  const iconBgMap = {
    indigo: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20',
    emerald: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    rose: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
    purple: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
  };

  return (
    <div className={`glass-panel rounded-2xl p-5 border border-slate-800/80 transition-all duration-300 ${borderGlowMap[color] || borderGlowMap.indigo}`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{title}</span>
        {Icon && (
          <div className={`w-9 h-9 rounded-xl border flex items-center justify-center ${iconBgMap[color]}`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>

      <div className="mt-3">
        <h3 className="text-2xl font-extrabold text-white tracking-tight">{amount}</h3>
        {subtitle && <p className="text-xs text-slate-400 mt-1">{subtitle}</p>}
      </div>

      {trend && (
        <div className="mt-3 pt-3 border-t border-slate-800/60 flex items-center justify-between text-xs">
          <span className={`font-semibold ${trend.isPositive ? 'text-emerald-400' : 'text-rose-400'}`}>
            {trend.isPositive ? '+' : ''}{trend.value}
          </span>
          <span className="text-slate-500">{trend.label}</span>
        </div>
      )}
    </div>
  );
};
