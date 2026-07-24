import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Sparkles, Building2, TrendingUp, Cpu, Lock, ArrowRight, CheckCircle2 } from 'lucide-react';

export const Landing = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-indigo-500 selection:text-white">
      {/* Header */}
      <header className="h-20 glass-panel border-b border-slate-800/80 px-8 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center shadow-lg shadow-indigo-500/30">
            <ShieldCheck className="w-6 h-6 text-white" />
          </div>
          <span className="font-extrabold text-xl tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-100 to-indigo-300">
            IntelliWealth
          </span>
        </div>
        <div className="flex items-center gap-4">
          <Link to="/login" className="px-4 py-2 rounded-xl text-sm font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 transition">
            Sign In
          </Link>
          <Link to="/register" className="px-5 py-2.5 rounded-xl text-sm font-semibold bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white shadow-lg shadow-indigo-500/25 transition">
            Get Started Free
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative px-6 pt-20 pb-24 max-w-6xl mx-auto text-center flex flex-col items-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-panel border-indigo-500/30 text-indigo-300 text-xs font-semibold mb-8 animate-bounce">
          <Sparkles className="w-4 h-4 text-indigo-400" />
          <span>Next-Generation Financial Intelligence Agent</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-white max-w-4xl leading-tight">
          Master Your Money with <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">Autonomous AI Intelligence</span>
        </h1>

        <p className="mt-6 text-slate-400 text-base sm:text-lg max-w-2xl leading-relaxed">
          IntelliWealth unifies Open Banking, Account Aggregators, Machine Learning categorizers, spending forecasts, and AI wealth advisory into one high-performance platform.
        </p>

        <div className="mt-10 flex flex-wrap justify-center gap-4">
          <Link to="/register" className="px-8 py-4 rounded-2xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:opacity-95 text-white font-bold text-base shadow-xl shadow-indigo-500/25 flex items-center gap-2 transition transform hover:-translate-y-0.5">
            <span>Explore Live Platform</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link to="/login" className="px-8 py-4 rounded-2xl glass-panel text-slate-200 hover:text-white hover:bg-slate-800/60 font-semibold text-base transition">
            Demo Credentials Access
          </Link>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="px-6 py-16 max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-panel p-6 rounded-2xl border-slate-800/80">
          <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-4">
            <Building2 className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">Modular Bank Integration</h3>
          <p className="text-sm text-slate-400">
            Connect Open Banking APIs and Account Aggregators (India) via secure Provider Adapter Architecture with auto transaction background sync.
          </p>
        </div>

        <div className="glass-panel p-6 rounded-2xl border-slate-800/80">
          <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 mb-4">
            <Cpu className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">ML Categorizer & Forecast</h3>
          <p className="text-sm text-slate-400">
            Naïve Bayes + TF-IDF classification auto-categorizes expenses. Scikit-learn Linear Regression predicts next month spending and cash flows.
          </p>
        </div>

        <div className="glass-panel p-6 rounded-2xl border-slate-800/80">
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mb-4">
            <TrendingUp className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">Health Score & AI Chat</h3>
          <p className="text-sm text-slate-400">
            Audit your Financial Health Score (0-100) across 5 core indicators and chat naturally with your AI Financial Assistant.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-800/80 py-8 px-6 text-center text-xs text-slate-500">
        <p>© 2026 IntelliWealth Platform. Built for precision financial intelligence.</p>
      </footer>
    </div>
  );
};
