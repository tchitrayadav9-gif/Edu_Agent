import React, { useState } from 'react';
import { GitBranch, Cpu, BarChart3, Settings, Sparkles } from 'lucide-react';
import AlgorithmVisualizerView from './AlgorithmVisualizerView';
import ReasoningView from './ReasoningView';
import EvaluationDashboardView from './EvaluationDashboardView';
import McpSettingsView from './McpSettingsView';

export default function AiLabsView() {
  const [subTab, setSubTab] = useState('search');

  const tabs = [
    { id: 'search', label: 'Classical AI Search', icon: GitBranch, desc: 'BFS, DFS, UCS, A*, Hill Climbing & Beam Search' },
    { id: 'reasoning', label: 'Logic & Reasoning', icon: Cpu, desc: 'Forward/Backward Chaining & Bayesian Career Networks' },
    { id: 'evaluation', label: 'Benchmark (50Q)', icon: BarChart3, desc: 'Automated 50-Question Evaluation & Accuracy Metrics' },
    { id: 'mcp', label: 'MCP & Extensions', icon: Settings, desc: 'Model Context Protocol & External Tool Connectors' },
  ];

  return (
    <div className="space-y-6">
      {/* Sub-Navigation Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-2 shadow-lg flex flex-wrap gap-2">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = subTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setSubTab(tab.id)}
              className={`flex-1 min-w-[200px] flex items-center space-x-3 p-3 rounded-xl text-left transition-all ${
                isActive
                  ? 'bg-gradient-to-r from-teal-500/20 to-emerald-500/10 border border-teal-500/40 text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 border border-transparent'
              }`}
            >
              <div className={`p-2 rounded-lg ${isActive ? 'bg-teal-500 text-slate-950 font-bold' : 'bg-slate-950 text-slate-400'}`}>
                <Icon className="w-4 h-4" />
              </div>
              <div className="truncate">
                <span className="text-xs font-bold block">{tab.label}</span>
                <span className="text-[10px] text-slate-500 block truncate">{tab.desc}</span>
              </div>
            </button>
          );
        })}
      </div>

      {/* Render Selected Sub-View */}
      <div className="transition-opacity duration-200">
        {subTab === 'search' && <AlgorithmVisualizerView />}
        {subTab === 'reasoning' && <ReasoningView />}
        {subTab === 'evaluation' && <EvaluationDashboardView />}
        {subTab === 'mcp' && <McpSettingsView />}
      </div>
    </div>
  );
}
