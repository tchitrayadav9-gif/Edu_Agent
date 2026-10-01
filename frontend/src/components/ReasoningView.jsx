import React, { useState } from 'react';
import { Cpu, Play, CheckCircle2, ArrowRight, BookOpen } from 'lucide-react';
import { api } from '../api';

export default function ReasoningView() {
  const [facts, setFacts] = useState({
    Python: 'Strong',
    "Machine Learning": 'Strong',
    Statistics: 'Strong',
    "Data Structures": 'Strong',
    Target_Career: 'AI Engineer'
  });
  const [forwardResult, setForwardResult] = useState(null);
  const [backwardResult, setBackwardResult] = useState(null);
  const [loadingForward, setLoadingForward] = useState(false);
  const [loadingBackward, setLoadingBackward] = useState(false);

  const runForward = async () => {
    setLoadingForward(true);
    try {
      const res = await api.runForwardChaining(facts);
      setForwardResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingForward(false);
    }
  };

  const runBackward = async () => {
    setLoadingBackward(true);
    try {
      const res = await api.runBackwardChaining('Career_Recommendation', 'AI Engineer', facts);
      setBackwardResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingBackward(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
        <h2 className="text-base font-bold text-white flex items-center gap-2">
          <Cpu className="w-5 h-5 text-teal-400" /> Classical AI Logical Reasoning & Rule Inference Engines
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Production rule engine executing <strong>Forward Chaining</strong> (data-driven deduction) and <strong>Backward Chaining</strong> (goal-driven verification).
        </p>
      </div>

      {/* Interactive Fact Editor */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow">
        <h3 className="text-xs font-bold text-white uppercase tracking-wider mb-3">
          Configure Known Student Facts Base
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {Object.entries(facts).map(([key, val]) => (
            <div key={key}>
              <label className="text-[11px] text-slate-400 block mb-1">{key}</label>
              <select
                value={val}
                onChange={(e) => setFacts({ ...facts, [key]: e.target.value })}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-teal-500"
              >
                <option value="Strong">Strong</option>
                <option value="Developing">Developing</option>
                <option value="Weak">Weak</option>
                <option value="AI Engineer">AI Engineer</option>
                <option value="Data Scientist">Data Scientist</option>
              </select>
            </div>
          ))}
        </div>

        <div className="flex gap-3 mt-4 pt-3 border-t border-slate-800">
          <button
            onClick={runForward}
            disabled={loadingForward}
            className="px-4 py-2 bg-teal-500 hover:bg-teal-600 text-slate-950 font-bold text-xs rounded-lg transition"
          >
            {loadingForward ? 'Inferring...' : 'Execute Forward Chaining'}
          </button>
          <button
            onClick={runBackward}
            disabled={loadingBackward}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs rounded-lg transition border border-slate-700"
          >
            {loadingBackward ? 'Proving Goal...' : 'Execute Backward Chaining (Prove AI Engineer)'}
          </button>
        </div>
      </div>

      {/* Results Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Forward Chaining Output */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow">
          <h3 className="text-xs font-bold text-teal-400 uppercase tracking-wider mb-3">
            Forward Chaining Trace & Inferred Facts
          </h3>
          {forwardResult ? (
            <div className="space-y-3">
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-xs">
                <span className="text-[11px] text-slate-500 block mb-1">Derived Consequent Facts:</span>
                {Object.entries(forwardResult.derived_facts || {}).map(([k, v]) => (
                  <div key={k} className="text-emerald-400 font-semibold">
                    ✓ {k} = {v}
                  </div>
                ))}
              </div>

              <div className="space-y-2">
                <span className="text-[11px] text-slate-500 font-semibold uppercase block">Step-by-Step Inference Rules:</span>
                {forwardResult.reasoning_trace?.map((trace, idx) => (
                  <div key={idx} className="p-2.5 bg-slate-950/60 rounded border border-slate-800/80 text-xs space-y-1">
                    <span className="text-teal-400 font-bold">Rule: {trace.rule_name}</span>
                    <p className="text-slate-300">{trace.explanation}</p>
                    <span className="text-[10px] text-emerald-400 block font-mono">→ {trace.derived_fact}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <p className="text-xs text-slate-500">Click "Execute Forward Chaining" to view automated rule deduction.</p>
          )}
        </div>

        {/* Backward Chaining Output */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow">
          <h3 className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-3">
            Backward Chaining Goal Proof
          </h3>
          {backwardResult ? (
            <div className="space-y-3">
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-xs flex items-center justify-between">
                <div>
                  <span className="text-slate-400 block text-[11px]">Hypothesized Target Goal:</span>
                  <span className="text-white font-bold">{backwardResult.goal}</span>
                </div>
                <span className={`px-2.5 py-1 rounded text-xs font-bold ${
                  backwardResult.is_proved ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                }`}>
                  {backwardResult.is_proved ? 'PROVED (TRUE)' : 'UNPROVED'}
                </span>
              </div>

              {backwardResult.missing_facts?.length > 0 && (
                <div className="p-3 bg-rose-950/20 border border-rose-500/30 rounded-lg text-xs text-rose-300 space-y-1">
                  <span className="font-bold block">Missing / Unsatisfied Antecedents:</span>
                  {backwardResult.missing_facts.map((mf, i) => (
                    <div key={i}>• {mf}</div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <p className="text-xs text-slate-500">Click "Execute Backward Chaining" to verify prerequisites recursively.</p>
          )}
        </div>
      </div>
    </div>
  );
}
