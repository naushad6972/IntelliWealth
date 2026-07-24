import React, { useEffect, useState } from 'react';
import api from '../api/client';

export const Notifications = () => {
  const [notifs, setNotifs] = useState([]);

  const fetchNotifs = async () => {
    try {
      const res = await api.get('/notifications');
      setNotifs(res.data);
    } catch (err) {
      console.error('Failed to load notifications', err);
    }
  };

  useEffect(() => { fetchNotifs(); }, []);

  const markRead = async (id) => {
    try {
      await api.post(`/notifications/${id}/read`);
      fetchNotifs();
    } catch (err) {
      console.error('Failed to mark read', err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <h1 className="text-2xl font-black text-white">Notifications</h1>
        <p className="text-xs text-slate-400">Real-time alerts and reminders</p>
      </div>

      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        {notifs.length === 0 ? (
          <p className="text-slate-400 text-xs">No notifications.</p>
        ) : (
          <ul className="space-y-3">
            {notifs.map(n => (
              <li key={n.id} className={`p-3 rounded-xl border ${n.is_read ? 'bg-slate-900/60' : 'bg-slate-800/80'} flex justify-between items-start`}>
                <div>
                  <p className="font-semibold text-white text-sm">{n.title}</p>
                  <p className="text-xs text-slate-400 mt-1">{n.message}</p>
                </div>
                <div className="flex flex-col items-end gap-2">
                  <span className="text-[11px] text-slate-500">{new Date(n.created_at).toLocaleString()}</span>
                  {!n.is_read && (<button onClick={() => markRead(n.id)} className="px-3 py-1 text-xs rounded-xl bg-indigo-600 text-white">Mark read</button>)}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};
