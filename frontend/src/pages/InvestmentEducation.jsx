import React, { useState, useEffect } from 'react';
import api from '../api/client';
import { GraduationCap, Sparkles, BookOpen, ShieldAlert, CheckCircle2, HelpCircle, ArrowRight } from 'lucide-react';

export const InvestmentEducation = () => {
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [suggestion, setSuggestion] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const res = await api.get('/education/topics');
        setTopics(res.data);
        if (res.data.length > 0) {
          loadTopicDetail(res.data[0].topic_id);
        }
      } catch (err) {
        console.error("Failed to load investment topics:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchTopics();
  }, []);

  const loadTopicDetail = async (topicId) => {
    try {
      const [tRes, sRes] = await Promise.all([
        api.get(`/education/topics/${topicId}`),
        api.get(`/education/topics/${topicId}/suggestions`)
      ]);
      setSelectedTopic(tRes.data);
      setSuggestion(sRes.data);
    } catch (err) {
      console.error("Error loading topic detail:", err);
    }
  };

  if (loading) {
    return <div className="py-12 text-center text-xs text-slate-400">Loading Wealth Learning Hub...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold mb-2">
          <GraduationCap className="w-3.5 h-3.5" />
          <span>Educational Wealth Hub</span>
        </div>
        <h1 className="text-2xl font-black text-white tracking-tight">Investment Education & Educational Advisory</h1>
        <p className="text-xs text-slate-400 mt-1">Learn fundamental concepts of SIPs, Mutual Funds, Equities, ETFs, Bonds, and Risk Management</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Topic Selector List */}
        <div className="glass-panel p-4 rounded-3xl border border-slate-800 space-y-1">
          <h3 className="text-xs font-bold text-slate-400 uppercase px-3 py-2">Select Topic</h3>
          {topics.map((t) => (
            <button
              key={t.topic_id}
              onClick={() => loadTopicDetail(t.topic_id)}
              className={`w-full text-left px-3.5 py-2.5 rounded-2xl text-xs font-semibold transition ${
                selectedTopic?.topic_id === t.topic_id
                  ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md'
                  : 'text-slate-300 hover:bg-slate-900/60'
              }`}
            >
              {t.title}
            </button>
          ))}
        </div>

        {/* Selected Topic Detailed View */}
        {selectedTopic && (
          <div className="lg:col-span-3 space-y-6">
            <div className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-4">
              <h2 className="text-xl font-black text-white">{selectedTopic.title}</h2>
              <p className="text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-4 rounded-2xl border border-slate-800">
                {selectedTopic.definition}
              </p>

              {/* AI Educational Suggestion Box */}
              {suggestion && (
                <div className="p-5 rounded-2xl bg-indigo-950/40 border border-indigo-500/30 space-y-3">
                  <div className="flex items-center gap-2 text-xs font-bold text-indigo-300">
                    <Sparkles className="w-4 h-4 text-indigo-400" />
                    <span>Personalized Educational Suggestion (Non-Advisory)</span>
                  </div>
                  <div className="space-y-1.5 text-xs text-slate-200">
                    {suggestion.educational_suggestions.map((s, idx) => (
                      <p key={idx}>• {s}</p>
                    ))}
                  </div>
                  <p className="text-[10px] text-slate-400 italic pt-2 border-t border-indigo-500/20">{suggestion.disclaimer}</p>
                </div>
              )}

              {/* Benefits & Risks */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="p-4 rounded-2xl bg-emerald-500/5 border border-emerald-500/20 space-y-2">
                  <h4 className="font-bold text-emerald-400 text-xs flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4" /> Benefits
                  </h4>
                  <ul className="text-xs text-slate-300 space-y-1 list-disc list-inside">
                    {selectedTopic.benefits.map((b, i) => <li key={i}>{b}</li>)}
                  </ul>
                </div>

                <div className="p-4 rounded-2xl bg-rose-500/5 border border-rose-500/20 space-y-2">
                  <h4 className="font-bold text-rose-400 text-xs flex items-center gap-1.5">
                    <ShieldAlert className="w-4 h-4" /> Associated Risks
                  </h4>
                  <ul className="text-xs text-slate-300 space-y-1 list-disc list-inside">
                    {selectedTopic.risks.map((r, i) => <li key={i}>{r}</li>)}
                  </ul>
                </div>
              </div>

              {/* FAQs */}
              <div className="pt-4 border-t border-slate-800">
                <h4 className="font-bold text-white text-xs mb-3 flex items-center gap-1.5">
                  <HelpCircle className="w-4 h-4 text-indigo-400" /> Frequently Asked Questions
                </h4>
                <div className="space-y-3">
                  {selectedTopic.faqs.map((faq, i) => (
                    <div key={i} className="p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800 text-xs">
                      <p className="font-semibold text-white">Q: {faq.q}</p>
                      <p className="text-slate-400 mt-1">A: {faq.a}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
