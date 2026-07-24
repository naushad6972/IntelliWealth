import React, { useEffect, useState } from 'react';
import api from '../api/client';

export const AIChat = () => {
  const [history, setHistory] = useState([]);
  const [message, setMessage] = useState('');
  const [sending, setSending] = useState(false);

  const loadHistory = async () => {
    try {
      const res = await api.get('/chat/history');
      setHistory(res.data || []);
    } catch (err) {
      console.error('Failed to load chat history', err);
    }
  };

  useEffect(() => { loadHistory(); }, []);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;
    setSending(true);
    try {
      const res = await api.post('/chat', { message });
      setHistory(prev => [...prev, { role: 'user', content: message }, { role: 'assistant', content: res.data.response }]);
      setMessage('');
    } catch (err) {
      console.error('Chat failed', err);
      alert('Failed to send message');
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <h1 className="text-2xl font-black text-white">AI Financial Assistant</h1>
        <p className="text-xs text-slate-400">Ask questions about your finances and receive actionable advice.</p>
      </div>

      <div className="glass-panel p-6 rounded-3xl border border-slate-800 flex flex-col gap-4">
        <div className="max-h-96 overflow-y-auto space-y-3">
          {history.map((m, idx) => (
            <div key={idx} className={`p-3 rounded-lg ${m.role === 'user' ? 'bg-slate-900 text-white self-end' : 'bg-slate-800/80 text-slate-100'}`}>
              <p className="text-sm">{m.content}</p>
            </div>
          ))}
        </div>

        <form onSubmit={sendMessage} className="flex gap-3">
          <input value={message} onChange={(e) => setMessage(e.target.value)} className="flex-1 bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white" placeholder="Ask the AI about budgets, forecasts, or investments..." />
          <button disabled={sending} className="px-4 py-2 rounded-xl bg-indigo-600 text-white">Send</button>
        </form>
      </div>
    </div>
  );
};
