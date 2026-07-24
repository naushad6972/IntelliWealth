import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard, CreditCard, UploadCloud, Building2, PieChart, BarChart3,
  Target, TrendingUp, Activity, Calculator, GraduationCap, Bot, FileText,
  Bell, User, Settings, ShieldCheck, Sparkles
} from 'lucide-react';

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/transactions', label: 'Transactions', icon: CreditCard },
  { path: '/connect-bank', label: 'Bank Integration', icon: Building2 },
  { path: '/upload-csv', label: 'Import CSV', icon: UploadCloud },
  { path: '/budgets', label: 'Budget Planner', icon: PieChart },
  { path: '/analytics', label: 'Deep Analytics', icon: BarChart3 },
  { path: '/goals', label: 'Goal Planner', icon: Target },
  { path: '/forecast', label: 'ML Forecast', icon: TrendingUp },
  { path: '/health', label: 'Health Score', icon: Activity },
  { path: '/emi', label: 'EMI Calculator', icon: Calculator },
  { path: '/education', label: 'Wealth Hub', icon: GraduationCap },
  { path: '/ai-chat', label: 'AI Chat Assistant', icon: Bot, badge: 'AI' },
  { path: '/reports', label: 'Reports Export', icon: FileText },
  { path: '/notifications', label: 'Notifications', icon: Bell },
  { path: '/profile', label: 'My Profile', icon: User },
  { path: '/settings', label: 'Settings', icon: Settings },
];

export const Sidebar = () => {
  return (
    <aside className="w-64 glass-panel border-r border-slate-800/60 hidden md:flex flex-col h-screen sticky top-0 z-30">
      {/* Brand Header */}
      <div className="p-5 flex items-center gap-3 border-b border-slate-800/80">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center shadow-lg shadow-indigo-500/30">
          <ShieldCheck className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="font-extrabold text-lg tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-100 to-indigo-300">
            IntelliWealth
          </h1>
          <p className="text-xs text-indigo-400 font-medium flex items-center gap-1">
            <Sparkles className="w-3 h-3 inline" /> Intelligence Engine
          </p>
        </div>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 text-white shadow-md shadow-indigo-500/20 font-semibold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`
              }
            >
              <div className="flex items-center gap-3">
                <Icon className="w-4 h-4" />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className="px-1.5 py-0.5 text-[10px] font-bold rounded-full bg-gradient-to-r from-pink-500 to-purple-500 text-white uppercase tracking-wider">
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* System Status Footer */}
      <div className="p-4 border-t border-slate-800/80 m-3 rounded-xl bg-slate-900/60 text-xs text-slate-400">
        <div className="flex items-center justify-between mb-1">
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            Bank Sync Active
          </span>
          <span className="text-[10px] text-slate-500 font-mono">v1.0.0</span>
        </div>
        <p className="text-[11px] text-slate-500">Encrypted OAuth2 & AA Connected</p>
      </div>
    </aside>
  );
};
