import React, { useState } from 'react';
import {
  Brain, Sparkles, BookOpen, Compass, Award,
  BarChart3, Settings, User, LogOut, LogIn, ChevronDown, Flame, CheckCircle
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, provider, setProvider, currentUser, onOpenAuth, onOpenPreferences, onLogout }) {
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'learning', label: 'Learning', icon: BookOpen },
    { id: 'career', label: 'Career Guidance', icon: Compass },
    { id: 'interview', label: 'Mock Interview', icon: Award },
    { id: 'chat', label: 'EduMind AI', icon: Brain },
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  const displayName = currentUser?.name || currentUser?.username || 'Chitra';
  const displayYear = currentUser?.academic_year || '2nd Year';
  const displayBranch = currentUser?.branch || 'CSE';

  return (
    <header className="bg-slate-900 border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-500 via-teal-400 to-emerald-400 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <Brain className="w-6 h-6 text-slate-950 stroke-[2.5]" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-lg tracking-tight text-white">
                  Edu<span className="bg-gradient-to-r from-indigo-400 to-teal-300 bg-clip-text text-transparent">Agent</span>
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/30">
                  AI Platform
                </span>
              </div>
              <p className="text-[11px] text-slate-400 hidden sm:block">Personalized Learning & Career System</p>
            </div>
          </div>

          {/* Model Switcher & User Controls */}
          <div className="flex items-center space-x-2 sm:space-x-3">
            {/* Model Provider */}
            <div className="flex items-center bg-slate-950 border border-slate-800 rounded-xl p-1 text-xs">
              <span className="text-slate-400 px-2 flex items-center gap-1 hidden md:flex">
                <Sparkles className="w-3.5 h-3.5 text-indigo-400" /> Model:
              </span>
              <select
                value={provider}
                onChange={(e) => setProvider(e.target.value)}
                className="bg-slate-900 text-slate-200 border-none rounded-lg px-2.5 py-1 focus:ring-1 focus:ring-indigo-500 text-xs font-semibold cursor-pointer"
              >
                <option value="auto">Auto (Adaptive Engine)</option>
                <option value="openai">OpenAI GPT-4o</option>
                <option value="ollama">Ollama (Local LLM)</option>
              </select>
            </div>

            {/* Auth Button or User Badge */}
            {currentUser ? (
              <div className="relative">
                <button
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  className="flex items-center space-x-2 px-3 py-1.5 rounded-xl bg-slate-800/90 hover:bg-slate-750 border border-slate-700/80 text-xs text-slate-200 transition"
                >
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  <span className="font-bold">{displayName}</span>
                  <span className="text-slate-400 hidden md:inline">({displayYear})</span>
                  <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                </button>

                {dropdownOpen && (
                  <div className="absolute right-0 mt-2 w-56 bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl py-2 text-xs z-50 animate-fadeIn">
                    <div className="px-4 py-2.5 border-b border-slate-800 text-slate-400">
                      <p className="font-bold text-slate-200 text-sm">{displayName}</p>
                      <p className="text-[11px] text-indigo-400 truncate">{currentUser.email || `${currentUser.username || 'chitra'}@eduagent.ai`}</p>
                      <p className="text-[11px] text-slate-500">{displayBranch}</p>
                    </div>

                    <button
                      onClick={() => {
                        setDropdownOpen(false);
                        setActiveTab('profile');
                      }}
                      className="w-full text-left px-4 py-2 text-slate-200 hover:bg-slate-800 flex items-center gap-2"
                    >
                      <User className="w-3.5 h-3.5 text-indigo-400" /> My Profile
                    </button>

                    <button
                      onClick={() => {
                        setDropdownOpen(false);
                        onOpenPreferences();
                      }}
                      className="w-full text-left px-4 py-2 text-indigo-300 hover:bg-slate-800 flex items-center gap-2"
                    >
                      <Settings className="w-3.5 h-3.5 text-indigo-400" /> Guidance Settings
                    </button>

                    <button
                      onClick={() => {
                        setDropdownOpen(false);
                        onOpenAuth();
                      }}
                      className="w-full text-left px-4 py-2 text-slate-300 hover:bg-slate-800 flex items-center gap-2"
                    >
                      <Sparkles className="w-3.5 h-3.5 text-teal-400" /> Switch / Add Account
                    </button>

                    <button
                      onClick={() => {
                        setDropdownOpen(false);
                        onLogout();
                      }}
                      className="w-full text-left px-4 py-2 text-rose-400 hover:bg-slate-800 flex items-center gap-2 border-t border-slate-800/80"
                    >
                      <LogOut className="w-3.5 h-3.5" /> Sign Out
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <button
                onClick={onOpenAuth}
                className="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-indigo-500 to-teal-400 hover:from-indigo-600 hover:to-teal-500 text-slate-950 font-bold text-xs shadow transition"
              >
                <LogIn className="w-3.5 h-3.5" />
                <span>Sign In / Register</span>
              </button>
            )}
          </div>
        </div>

        {/* Navigation Tabs (Removed RAG Notes & Memory Vault) */}
        <nav className="flex space-x-1 overflow-x-auto py-2.5 border-t border-slate-800/50 scrollbar-none">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  if (item.id === 'settings') {
                    onOpenPreferences();
                  } else {
                    setActiveTab(item.id);
                  }
                }}
                className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all duration-150 ${
                  isActive
                    ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
