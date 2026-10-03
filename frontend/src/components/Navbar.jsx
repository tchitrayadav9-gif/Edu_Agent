import React, { useState } from 'react';
import { Brain, Sparkles, Database, BookOpen, Compass, Award, Cpu, GitBranch, BarChart3, Settings, User, LogOut, LogIn, ChevronDown } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, provider, setProvider, currentUser, onOpenAuth, onLogout }) {
  const [dropdownOpen, setDropdownOpen] = useState(false);

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

  const displayName = currentUser?.name || currentUser?.username || 'Chitra';
  const displayYear = currentUser?.academic_year || '2nd Yr';
  const displayBranch = currentUser?.branch || 'CSE';

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

          {/* Model Switcher & User Controls */}
          <div className="flex items-center space-x-3">
            {/* Model Provider */}
            <div className="flex items-center bg-slate-950 border border-slate-800 rounded-lg p-1 text-xs">
              <span className="text-slate-400 px-2 flex items-center gap-1 hidden sm:flex">
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

            {/* Auth Button or User Badge */}
            {currentUser ? (
              <div className="relative">
                <button
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-800/90 hover:bg-slate-750 border border-slate-700/80 text-xs text-slate-200 transition"
                >
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  <span className="font-semibold">{displayName}</span>
                  <span className="text-slate-400 hidden md:inline">({displayYear})</span>
                  <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                </button>

                {dropdownOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-slate-900 border border-slate-800 rounded-xl shadow-2xl py-1 text-xs z-50">
                    <div className="px-3 py-2 border-b border-slate-800 text-slate-400">
                      <p className="font-bold text-slate-200">{displayName}</p>
                      <p className="text-[10px] text-teal-400">{currentUser.email || `${currentUser.username}@eduagent.ai`}</p>
                      <p className="text-[10px] text-slate-500">{displayBranch}</p>
                    </div>
                    <button
                      onClick={() => {
                        setDropdownOpen(false);
                        onOpenAuth();
                      }}
                      className="w-full text-left px-3 py-2 text-slate-300 hover:bg-slate-800 flex items-center gap-2"
                    >
                      <User className="w-3.5 h-3.5 text-teal-400" /> Switch / Add Account
                    </button>
                    <button
                      onClick={() => {
                        setDropdownOpen(false);
                        onLogout();
                      }}
                      className="w-full text-left px-3 py-2 text-rose-400 hover:bg-slate-800 flex items-center gap-2"
                    >
                      <LogOut className="w-3.5 h-3.5" /> Sign Out
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <button
                onClick={onOpenAuth}
                className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-teal-500 to-emerald-400 hover:from-teal-600 hover:to-emerald-500 text-slate-950 font-bold text-xs shadow transition"
              >
                <LogIn className="w-3.5 h-3.5" />
                <span>Sign In / Register</span>
              </button>
            )}
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
