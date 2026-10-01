import React, { useState, useEffect } from 'react';
import { BarChart3, Play, CheckCircle2, ShieldCheck, Zap, DollarSign, RefreshCw } from 'lucide-react';
import { api } from '../api';

export default function EvaluationDashboardView() {
  const [evalData, setEvalData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);

  const fetchLatest = async () => {
    setLoading(true);
    try {
      const res = await api.getLatestEvaluation();
      setEvalData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLatest();
  }, []);

  const handleRunFullBenchmark = async () => {
    setRunning(true);
    try {
      const res = await api.runEvaluation(50, 'auto');
      setEvalData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setRunning(false);
    }
  };

  if (loading && !evalData) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        <RefreshCw className="w-6 h-6 animate-spin text-teal-400 mr-2" /> Loading Evaluation Benchmark...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-teal-400" /> 50-Question Multi-Agent Evaluation Dashboard
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Quantitative evaluation across 50 benchmark questions measuring Accuracy, Relevance, Faithfulness, Context Relevance, Latency, and Token Cost.
          </p>
        </div>

        <button
          onClick={handleRunFullBenchmark}
          disabled={running}
          className="flex items-center space-x-1.5 px-4 py-2 bg-teal-500 hover:bg-teal-600 text-slate-950 font-bold text-xs rounded-lg transition"
        >
          <Play className="w-3.5 h-3.5 fill-slate-950" />
          <span>{running ? 'Executing 50-Q Suite...' : 'Run Live Benchmark (50 Qs)'}</span>
        </button>
      </div>

      {/* Metric Cards */}
      {evalData && (
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3 text-center">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow">
            <span className="text-[11px] text-slate-400 block">Accuracy Score</span>
            <span className="text-xl font-bold text-teal-400 mt-1 block">{(evalData.accuracy_score * 100).toFixed(1)}%</span>
            <span className="text-[10px] text-slate-500">Composite metric</span>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow">
            <span className="text-[11px] text-slate-400 block">Relevance</span>
            <span className="text-xl font-bold text-emerald-400 mt-1 block">{(evalData.relevance_score * 100).toFixed(1)}%</span>
            <span className="text-[10px] text-slate-500">Keyword recall</span>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow">
            <span className="text-[11px] text-slate-400 block">Faithfulness</span>
            <span className="text-xl font-bold text-cyan-400 mt-1 block">{(evalData.faithfulness_score * 100).toFixed(1)}%</span>
            <span className="text-[10px] text-slate-500">Anti-hallucination</span>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow">
            <span className="text-[11px] text-slate-400 block">Context Match</span>
            <span className="text-xl font-bold text-amber-400 mt-1 block">{(evalData.context_relevance_score * 100).toFixed(1)}%</span>
            <span className="text-[10px] text-slate-500">RAG precision</span>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow">
            <span className="text-[11px] text-slate-400 block">Avg Latency</span>
            <span className="text-xl font-bold text-purple-400 mt-1 block">{evalData.avg_latency_ms} ms</span>
            <span className="text-[10px] text-slate-500">Per question</span>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow">
            <span className="text-[11px] text-slate-400 block">Est. Cost</span>
            <span className="text-xl font-bold text-slate-200 mt-1 block">${evalData.estimated_cost_usd}</span>
            <span className="text-[10px] text-slate-500">50-Q benchmark run</span>
          </div>
        </div>
      )}

      {/* Questions Breakdown */}
      {evalData?.results_breakdown?.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow">
          <h3 className="text-xs font-bold text-white uppercase tracking-wider mb-3">
            Benchmark Question Breakdown ({evalData.results_breakdown.length} Evaluated Cases)
          </h3>
          <div className="space-y-2 max-h-96 overflow-y-auto pr-1 scrollbar-none">
            {evalData.results_breakdown.map((r, i) => (
              <div key={i} className="p-3 bg-slate-950 rounded-lg border border-slate-800 flex items-center justify-between text-xs">
                <div className="max-w-[70%]">
                  <span className="text-[10px] text-teal-400 uppercase font-semibold block mb-0.5">
                    #{r.id} [{r.category}]
                  </span>
                  <p className="text-slate-200 font-medium">{r.question}</p>
                </div>
                <div className="text-right space-y-0.5">
                  <span className="text-emerald-400 font-bold block">Relevance: {(r.relevance_score * 100).toFixed(0)}%</span>
                  <span className="text-[10px] text-slate-500">{r.latency_ms} ms</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
