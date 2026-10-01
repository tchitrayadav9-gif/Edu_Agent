import React from 'react';
import { Brain, Sparkles, Database, BookOpen, Compass, Award, Cpu, GitBranch, BarChart3, Settings } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, provider, setProvider }) {
  const navItems = [
    { id: 'chat', label: 'EduMind Chat', icon: Brain },
    { id: 'dashboard', label: 'Dashboard', icon: Compass },
    { id: 'memory', label: 'Memory Manager', icon: Database },
    { id: 'rag', label: 'RAG Vault', icon: BookOpen },
    { id: 'interview', label: 'Mock Interview', icon: Award },
    { id: 'search', label: 'Search & Path', icon: GitBranch },
    { id: 'reasoning', label: 'Logic & Rules', icon: Cpu },
    { id: 'evaluation', label: 'Evaluation (50Q)', icon: BarChart3 },
    { id: 'settings', label: 'MCP & Models', icon: Settings },
  ];

  return (
    <header className="bg-slate-900 border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('chat')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-500 to-emerald-400 flex items-center justify-center shadow-lg shadow-teal-500/20">
              <Brain className="w-6 h-6 text-slate-950 stroke-[2.5]" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-lg tracking-tight text-white">Edu<span className="text-teal-400">Agent</span></span>
                <span className="text-[10px] uppercase font-semibold tracking-wider px-2 py-0.5 rounded-full bg-teal-500/10 text-teal-300 border border-teal-500/30">
                  Multi-Agent RAG
                </span>
              </div>
              <p className="text-xs text-slate-400 hidden sm:block">Memory-Enabled Cognitive Learning Agent</p>
            </div>
          </div>

          {/* Model Switcher & Student Badge */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center bg-slate-950 border border-slate-800 rounded-lg p-1 text-xs">
              <span className="text-slate-400 px-2 flex items-center gap-1">
                <Sparkles className="w-3.5 h-3.5 text-teal-400" /> Model:
              </span>
              <select
                value={provider}
                onChange={(e) => setProvider(e.target.value)}
                className="bg-slate-900 text-slate-200 border-none rounded px-2 py-1 focus:ring-1 focus:ring-teal-500 text-xs font-medium cursor-pointer"
              >
                <option value="auto">Auto (Adaptive)</option>
                <option value="openai">OpenAI GPT-4o</option>
                <option value="ollama">Ollama (Local)</option>
              </select>
            </div>

            <div className="hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60 text-xs text-slate-300">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="font-medium">Chitra (2nd Yr CSE)</span>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex space-x-1 overflow-x-auto py-2 border-t border-slate-800/50 scrollbar-none">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all duration-150 ${
                  isActive
                    ? 'bg-teal-500/10 text-teal-300 border border-teal-500/30 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-teal-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
