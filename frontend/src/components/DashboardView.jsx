import React, { useState, useEffect } from 'react';
import {
  Compass, Target, Award, Database, FileText, CheckCircle, AlertTriangle, TrendingUp, RefreshCw,
  BookOpen, Play, ArrowRight, Sparkles, Brain, Clock, ShieldCheck, ChevronRight
} from 'lucide-react';
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, AreaChart, Area, CartesianGrid
} from 'recharts';
import { api } from '../api';

export default function DashboardView({ currentUser, onNavigate }) {
  const targetUserId = currentUser?.user_id || currentUser?.id || "chitra_demo_user";
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchDashboard = async () => {
    setLoading(true);
    try {
      const res = await api.getDashboard(targetUserId);
      setData(res);
    } catch (err) {
      console.error("Error fetching dashboard:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, [targetUserId]);

  if (loading || !data) {
    return (
      <div className="flex flex-col items-center justify-center h-80 text-slate-400 space-y-3">
        <RefreshCw className="w-8 h-8 animate-spin text-teal-400" />
        <p className="text-sm font-medium">Syncing student intelligence from MongoDB Atlas...</p>
      </div>
    );
  }

  // Format skills for Recharts
  const skillsList = data.skills || {
    "Python": 85,
    "Data Structures": 75,
    "Machine Learning": 70,
    "Deep Learning": 45,
    "SQL / Databases": 80,
    "System Design": 60
  };

  const radarData = Object.entries(skillsList).map(([skill, score]) => ({
    subject: skill,
    score: score,
    target: 85,
    fullMark: 100
  }));

  const comparisonData = Object.entries(skillsList).map(([skill, score]) => ({
    name: skill.length > 12 ? skill.substring(0, 10) + '..' : skill,
    current: score,
    target: 85,
    gap: Math.max(0, 85 - score)
  }));

  const studyProgressTrend = [
    { day: 'Mon', hours: 2.0, completed: 3 },
    { day: 'Tue', hours: 2.5, completed: 4 },
    { day: 'Wed', hours: 1.5, completed: 2 },
    { day: 'Thu', hours: 3.0, completed: 5 },
    { day: 'Fri', hours: 2.0, completed: 3 },
    { day: 'Sat', hours: 4.0, completed: 6 },
    { day: 'Sun', hours: 3.5, completed: 5 },
  ];

  return (
    <div className="space-y-8">
      {/* Student Welcome & Profile Status Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-850 to-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
        <div className="absolute right-0 top-0 w-96 h-96 bg-teal-500/5 rounded-full blur-3xl pointer-events-none"></div>

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="text-xs uppercase font-bold text-teal-400 tracking-wider">
                Active Student Workspace • Connected to MongoDB Atlas
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-black text-white">
              Welcome back, <span className="bg-gradient-to-r from-teal-400 to-emerald-300 bg-clip-text text-transparent">{currentUser?.name || currentUser?.username || 'Chitra'}</span>
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl leading-relaxed">
              {currentUser?.academic_year || '2nd Year B.Tech'} • {currentUser?.branch || 'Computer Science & Engineering'} • Target Career: <strong className="text-teal-300">{data.career_goal}</strong>
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => onNavigate('profile')}
              className="px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 hover:border-teal-500 text-xs font-semibold text-slate-200 transition"
            >
              Edit Profile
            </button>
            <button
              onClick={fetchDashboard}
              className="p-2.5 rounded-xl bg-slate-850 border border-slate-700 hover:border-teal-500 text-slate-400 hover:text-teal-300 transition"
              title="Refresh Analytics"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* 3 Dedicated AI Agent Hero Launch Cards */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-teal-400" /> Dedicated AI Agents
          </h2>
          <span className="text-xs text-slate-500">Shared MongoDB Atlas Long-Term Memory</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {/* 1. Learning Agent Launch Card */}
          <div className="bg-gradient-to-b from-slate-900 to-indigo-950/20 border border-indigo-500/30 rounded-2xl p-6 shadow-xl hover:border-indigo-500 transition-all duration-200 flex flex-col justify-between group">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="p-3 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 group-hover:scale-110 transition-transform">
                  <BookOpen className="w-6 h-6" />
                </span>
                <span className="text-[10px] uppercase font-bold text-indigo-300 bg-indigo-500/20 border border-indigo-500/40 px-2 py-0.5 rounded-full">
                  A* Curriculum
                </span>
              </div>
              <h3 className="text-lg font-bold text-white group-hover:text-indigo-300 transition">Learning Agent</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                30-day personalized schedules, A* prerequisite path optimization, step-by-step concept tutorials, and diagnostic quizzes.
              </p>
            </div>

            <div className="pt-6 border-t border-slate-800/80 mt-6 flex items-center justify-between">
              <span className="text-[11px] text-slate-400">30-Day Plan Ready</span>
              <button
                onClick={() => onNavigate('learning')}
                className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow-lg shadow-indigo-600/30 transition flex items-center gap-1.5"
              >
                <span>Launch Agent</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* 2. Career Guidance Agent Launch Card */}
          <div className="bg-gradient-to-b from-slate-900 to-emerald-950/20 border border-emerald-500/30 rounded-2xl p-6 shadow-xl hover:border-emerald-500 transition-all duration-200 flex flex-col justify-between group">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="p-3 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 group-hover:scale-110 transition-transform">
                  <Compass className="w-6 h-6" />
                </span>
                <span className="text-[10px] uppercase font-bold text-emerald-300 bg-emerald-500/20 border border-emerald-500/40 px-2 py-0.5 rounded-full">
                  Bayesian Engine
                </span>
              </div>
              <h3 className="text-lg font-bold text-white group-hover:text-emerald-300 transition">Career Guidance Agent</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Probabilistic suitability match, skill-gap matrix, strategic 90-day placement milestones, and project recommendations.
              </p>
            </div>

            <div className="pt-6 border-t border-slate-800/80 mt-6 flex items-center justify-between">
              <span className="text-[11px] text-emerald-400 font-bold">82% Bayesian Match</span>
              <button
                onClick={() => onNavigate('career')}
                className="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/30 transition flex items-center gap-1.5"
              >
                <span>Launch Agent</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* 3. Mock Interview Agent Launch Card */}
          <div className="bg-gradient-to-b from-slate-900 to-amber-950/20 border border-amber-500/30 rounded-2xl p-6 shadow-xl hover:border-amber-500 transition-all duration-200 flex flex-col justify-between group">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="p-3 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-400 group-hover:scale-110 transition-transform">
                  <Award className="w-6 h-6" />
                </span>
                <span className="text-[10px] uppercase font-bold text-amber-300 bg-amber-500/20 border border-amber-500/40 px-2 py-0.5 rounded-full">
                  4-Factor Rubric
                </span>
              </div>
              <h3 className="text-lg font-bold text-white group-hover:text-amber-300 transition">Mock Interview Agent</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Live adaptive interview arena, multi-factor rubric evaluation (Accuracy, Clarity, Problem-Solving, Confidence), and instant memory updates.
              </p>
            </div>

            <div className="pt-6 border-t border-slate-800/80 mt-6 flex items-center justify-between">
              <span className="text-[11px] text-amber-300 font-bold">{data.average_interview_score} / 10 Score</span>
              <button
                onClick={() => onNavigate('interview')}
                className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs shadow-lg shadow-amber-500/30 transition flex items-center gap-1.5"
              >
                <span>Launch Agent</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>Career Goal</span>
            <Target className="w-4 h-4 text-teal-400" />
          </div>
          <p className="text-lg font-bold text-white mt-1">{data.career_goal}</p>
          <p className="text-[11px] text-emerald-400">82% Suitability</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>Average Skill Score</span>
            <TrendingUp className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-lg font-bold text-white mt-1">{data.average_skill_score} / 100</p>
          <p className="text-[11px] text-slate-400">Verified competencies</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>Interview Score</span>
            <Award className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-lg font-bold text-white mt-1">{data.average_interview_score} / 10</p>
          <p className="text-[11px] text-amber-400">Adaptive diagnostic</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>Persistent Memory</span>
            <Database className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-lg font-bold text-white mt-1">{data.memory_count} Facts</p>
          <p className="text-[11px] text-slate-400">{data.document_count} Indexed RAG doc(s)</p>
        </div>
      </div>

      {/* Recharts Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recharts Radar Chart: Multi-Disciplinary Competencies */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <Brain className="w-4 h-4 text-teal-400" /> Competency Radar Profile
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">Verified skill coverage across core AI disciplines</p>
            </div>
            <span className="text-[10px] bg-teal-500/10 text-teal-300 border border-teal-500/30 px-2 py-0.5 rounded">
              Recharts Active
            </span>
          </div>

          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="subject" stroke="#94a3b8" tick={{ fontSize: 11, fill: '#94a3b8' }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#475569" />
                <Radar name="Student Skill" dataKey="score" stroke="#14b8a6" fill="#14b8a6" fillOpacity={0.4} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recharts Bar Chart: Current vs Benchmark Gap */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-emerald-400" /> Current Competencies vs Target Benchmark
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">Target score: 85% for placement readiness</p>
            </div>
          </div>

          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={comparisonData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#64748b" tick={{ fontSize: 10, fill: '#94a3b8' }} />
                <YAxis domain={[0, 100]} stroke="#64748b" tick={{ fontSize: 10, fill: '#94a3b8' }} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
                <Bar dataKey="current" fill="#10b981" name="Current Level" radius={[4, 4, 0, 0]} />
                <Bar dataKey="gap" fill="#f43f5e" opacity={0.5} name="Skill Gap" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Identified Weaknesses & Shared Memory Sync */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Identified Weak Topics Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" /> Identified Weak Topics in Shared Memory
            </h3>
            <span className="text-xs text-slate-400">Synced from Mock Interviews</span>
          </div>

          <div className="space-y-2.5">
            {data.weak_skills?.map((topic, idx) => (
              <div key={idx} className="p-3.5 bg-slate-950 border border-amber-500/20 rounded-xl flex items-center justify-between">
                <div className="flex items-center space-x-2.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-amber-400"></span>
                  <span className="text-xs font-semibold text-slate-200">{topic}</span>
                </div>
                <button
                  onClick={() => onNavigate('learning')}
                  className="text-[11px] text-indigo-400 hover:text-indigo-300 font-bold flex items-center gap-1"
                >
                  <span>Remediate in Study Agent</span>
                  <ChevronRight className="w-3 h-3" />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Weekly Study Progression Area Chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Clock className="w-4 h-4 text-teal-400" /> Weekly Study Cadence & Topics Mastered
            </h3>
            <span className="text-xs text-teal-400 font-bold">18.5 Hours Logged</span>
          </div>

          <div className="h-44 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={studyProgressTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="day" stroke="#64748b" tick={{ fontSize: 10, fill: '#94a3b8' }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 10, fill: '#94a3b8' }} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
                <Area type="monotone" dataKey="hours" stroke="#14b8a6" fill="#14b8a6" fillOpacity={0.2} name="Study Hours" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
