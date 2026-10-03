import React, { useState, useEffect } from 'react';
import { Database, Plus, Trash2, Tag, Star, Clock, RefreshCw } from 'lucide-react';
import { api } from '../api';

export default function MemoryManagerView({ currentUser }) {
  const targetUserId = currentUser?.user_id || currentUser?.id || "chitra_demo_user";
  const [memories, setMemories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newType, setNewType] = useState('important_fact');
  const [newContent, setNewContent] = useState('');
  const [newImportance, setNewImportance] = useState(0.85);

  const fetchMemories = async () => {
    setLoading(true);
    try {
      const res = await api.getMemories(targetUserId);
      setMemories(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMemories();
  }, [targetUserId]);


  const handleAdd = async (e) => {
    e.preventDefault();
    if (!newContent.trim()) return;

    try {
      await api.createMemory({
        memory_type: newType,
        content: newContent,
        importance: parseFloat(newImportance),
        source: 'manual_ui_entry'
      });
      setNewContent('');
      fetchMemories();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.deleteMemory(id);
      setMemories((prev) => prev.filter((m) => m.memory_id !== id && m._id !== id && m.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  const getTypeBadgeColor = (type) => {
    switch (type) {
      case 'career_goal': return 'bg-teal-500/10 text-teal-300 border-teal-500/30';
      case 'skill': return 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30';
      case 'weakness': return 'bg-rose-500/10 text-rose-300 border-rose-500/30';
      case 'preference': return 'bg-purple-500/10 text-purple-300 border-purple-500/30';
      case 'achievement': return 'bg-amber-500/10 text-amber-300 border-amber-500/30';
      default: return 'bg-slate-800 text-slate-300 border-slate-700';
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Database className="w-5 h-5 text-teal-400" /> Persistent Student Long-Term Memory Vault
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Stores permanent facts, career goals, skill proficiencies, weak topics, and preferences stored in MongoDB.
          </p>
        </div>

        <button
          onClick={fetchMemories}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-200 border border-slate-700 transition"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-teal-400' : ''}`} />
          <span>Refresh Memory</span>
        </button>
      </div>

      {/* Add Memory Form */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
        <h3 className="text-xs font-bold text-white uppercase tracking-wider mb-3 flex items-center gap-1.5">
          <Plus className="w-4 h-4 text-teal-400" /> Manually Inject / Store Long-Term Memory
        </h3>
        <form onSubmit={handleAdd} className="grid grid-cols-1 md:grid-cols-4 gap-3">
          <div>
            <label className="text-[11px] text-slate-400 block mb-1">Memory Type</label>
            <select
              value={newType}
              onChange={(e) => setNewType(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-teal-500"
            >
              <option value="career_goal">Career Goal</option>
              <option value="skill">Skill Proficiency</option>
              <option value="weakness">Weakness</option>
              <option value="preference">Study Preference</option>
              <option value="achievement">Achievement / Score</option>
              <option value="important_fact">Important Fact</option>
            </select>
          </div>

          <div className="md:col-span-2">
            <label className="text-[11px] text-slate-400 block mb-1">Memory Content</label>
            <input
              type="text"
              value={newContent}
              onChange={(e) => setNewContent(e.target.value)}
              placeholder="e.g., 'Target Career Goal is AI Engineer', 'Weak in Statistics'..."
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-teal-500"
            />
          </div>

          <div>
            <label className="text-[11px] text-slate-400 block mb-1">Importance (0.0 - 1.0)</label>
            <div className="flex space-x-2">
              <input
                type="number"
                step="0.05"
                min="0.1"
                max="1.0"
                value={newImportance}
                onChange={(e) => setNewImportance(e.target.value)}
                className="w-24 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-teal-500"
              />
              <button
                type="submit"
                className="flex-1 bg-teal-500 hover:bg-teal-600 text-slate-950 font-bold text-xs py-2 px-3 rounded-lg transition"
              >
                Save Memory
              </button>
            </div>
          </div>
        </form>
      </div>

      {/* Memory List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {memories.map((mem) => {
          const memId = mem.memory_id || mem._id || mem.id;
          return (
            <div key={memId} className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow flex flex-col justify-between hover:border-slate-700 transition">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded border ${getTypeBadgeColor(mem.memory_type)}`}>
                    {mem.memory_type?.replace('_', ' ')}
                  </span>
                  <span className="flex items-center text-[11px] text-amber-400">
                    <Star className="w-3 h-3 fill-amber-400 mr-1" />
                    {mem.importance || 0.8}
                  </span>
                </div>
                <p className="text-xs text-slate-200 font-medium leading-relaxed mt-2">{mem.content}</p>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[10px] text-slate-500">
                <span className="flex items-center">
                  <Clock className="w-3 h-3 mr-1" />
                  {mem.updated_at ? new Date(mem.updated_at).toLocaleDateString() : 'Active'}
                </span>
                <button
                  onClick={() => handleDelete(memId)}
                  className="text-slate-500 hover:text-rose-400 p-1 transition"
                  title="Delete Memory"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
