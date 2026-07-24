import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export const Profile = () => {
  const { user, updateProfile } = useAuth();
  const [form, setForm] = useState({
    name: user?.name || '',
    occupation: user?.occupation || '',
    monthly_income: user?.monthly_income || '',
    risk_preference: user?.risk_preference || '',
    financial_goals: user?.financial_goals || '',
    preferred_currency: user?.preferred_currency || 'INR'
  });
  const [saving, setSaving] = useState(false);

  const save = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await updateProfile(form);
      alert('Profile updated');
    } catch (err) {
      console.error(err);
      alert('Failed to update profile');
    } finally { setSaving(false); }
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <h1 className="text-2xl font-black text-white">My Profile</h1>
        <p className="text-xs text-slate-400">Manage your account information and preferences</p>
      </div>

      <form onSubmit={save} className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-3">
        <div>
          <label className="text-xs text-slate-400">Name</label>
          <input value={form.name} onChange={(e)=>setForm({...form, name: e.target.value})} className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white" />
        </div>
        <div>
          <label className="text-xs text-slate-400">Occupation</label>
          <input value={form.occupation} onChange={(e)=>setForm({...form, occupation: e.target.value})} className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white" />
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-xs text-slate-400">Monthly Income</label>
            <input type="number" value={form.monthly_income} onChange={(e)=>setForm({...form, monthly_income: e.target.value})} className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white" />
          </div>
          <div>
            <label className="text-xs text-slate-400">Preferred Currency</label>
            <input value={form.preferred_currency} onChange={(e)=>setForm({...form, preferred_currency: e.target.value})} className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white" />
          </div>
        </div>
        <div>
          <label className="text-xs text-slate-400">Financial Goals</label>
          <textarea value={form.financial_goals} onChange={(e)=>setForm({...form, financial_goals: e.target.value})} className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white" />
        </div>

        <div className="flex justify-end">
          <button type="submit" disabled={saving} className="px-5 py-2 rounded-xl bg-indigo-600 text-white">Save</button>
        </div>
      </form>
    </div>
  );
};
