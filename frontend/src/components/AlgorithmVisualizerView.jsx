import React, { useState, useEffect } from 'react';
import { GitBranch, Play, CheckCircle2, Clock, Activity, Zap } from 'lucide-react';
import { api } from '../api';

export default function AlgorithmVisualizerView() {
  const [startTopic, setStartTopic] = useState('Python Basics');
  const [goalTopic, setGoalTopic] = useState('AI Engineer Mastery');
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleRunComparison = async () => {
    setLoading(true);
    try {
      const res = await api.compareSearch(startTopic, goalTopic);
      setComparison(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleRunComparison();
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-teal-400" /> Classical AI Search & Curriculum Path Optimization
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Compares 6 pure Python state-space search algorithms (BFS, DFS, UCS, A*, Hill Climbing, Beam Search) on the curriculum prerequisite graph.
          </p>
        </div>

        <button
          onClick={handleRunComparison}
          disabled={loading}
          className="flex items-center space-x-1.5 px-4 py-2 bg-teal-500 hover:bg-teal-600 text-slate-950 font-bold text-xs rounded-lg transition"
        >
          <Play className="w-3.5 h-3.5 fill-slate-950" />
          <span>{loading ? 'Running Benchmark...' : 'Execute All 6 Algorithms'}</span>
        </button>
      </div>

      {/* Comparison Grid */}
      {comparison && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(comparison.algorithms || {}).map(([key, alg]) => {
            const isAStar = key === 'a_star';
            return (
              <div
                key={key}
                className={`bg-slate-900 border rounded-xl p-5 shadow-lg flex flex-col justify-between transition ${
                  isAStar ? 'border-teal-500/60 ring-1 ring-teal-500/20' : 'border-slate-800'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-xs font-bold text-white uppercase tracking-wider">{alg.algorithm}</h3>
                    {isAStar && (
                      <span className="text-[10px] bg-teal-500/20 text-teal-300 font-bold px-2 py-0.5 rounded border border-teal-500/40">
                        Optimal (A*)
                      </span>
                    )}
                  </div>

                  {/* Metrics Row */}
                  <div className="grid grid-cols-3 gap-2 text-center text-[11px] mb-4">
                    <div className="p-2 bg-slate-950 rounded-lg border border-slate-800">
                      <span className="text-slate-500 block text-[10px]">Cost (hrs)</span>
                      <span className="text-white font-bold">{alg.total_cost}</span>
                    </div>
                    <div className="p-2 bg-slate-950 rounded-lg border border-slate-800">
                      <span className="text-slate-500 block text-[10px]">Visited</span>
                      <span className="text-emerald-400 font-bold">{alg.nodes_visited} nodes</span>
                    </div>
                    <div className="p-2 bg-slate-950 rounded-lg border border-slate-800">
                      <span className="text-slate-500 block text-[10px]">Latency</span>
                      <span className="text-cyan-400 font-bold">{alg.execution_time_ms} ms</span>
                    </div>
                  </div>

                  {/* Path Steps */}
                  <div>
                    <span className="text-[10px] text-slate-500 font-semibold uppercase block mb-1.5">Generated Path:</span>
                    <div className="space-y-1">
                      {alg.path?.map((step, idx) => (
                        <div key={idx} className="flex items-center space-x-1.5 text-xs text-slate-300">
                          <span className="w-4 h-4 rounded-full bg-slate-800 text-[9px] flex items-center justify-center font-bold text-teal-400 shrink-0">
                            {idx + 1}
                          </span>
                          <span className="truncate">{step}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
