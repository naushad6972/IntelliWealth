import React from 'react';

export const Settings = () => {
  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <h1 className="text-2xl font-black text-white">Settings</h1>
        <p className="text-xs text-slate-400">Application preferences and integrations.</p>
      </div>

      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <p className="text-slate-400 text-sm">No user-configurable settings yet. Integrations and API keys are configured on the backend `.env`.</p>
      </div>
    </div>
  );
};
