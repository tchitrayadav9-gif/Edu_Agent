import React, { useState, useEffect } from 'react';
import {
  Compass, Target, Award, Database, FileText, CheckCircle, AlertTriangle, TrendingUp, RefreshCw,
  BookOpen, Play, ArrowRight, Sparkles, Brain, Clock, ShieldCheck, ChevronRight, Flame, Check, Layers
} from 'lucide-react';
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, AreaChart, Area, CartesianGrid
} from 'recharts';
import { api } from '../api';

export default function DashboardView({ currentUser, onNavigate, onLearnSubject }) {
  const targetUserId = currentUser?.user_id || currentUser?.id || "chitra_demo_user";
  const [data, setData] = useState(null);
  const [learningProg, setLearningProg] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchDashboard = async () => {
    setLoading(true);
    try {
      const [dashRes, progRes] = await Promise.all([
        api.getDashboard(targetUserId),
        api.getLearningProgress(null, targetUserId).catch(() => null)
      ]);
      setData(dashRes);
      setLearningProg(progRes);
    } catch (err) {
      console.error("Error fetching dashboard data:", err);
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
        <RefreshCw className="w-8 h-8 animate-spin text-indigo-400" />
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

  const currentSubject = learningProg?.subject || "Python";
  const currentProgressPct = learningProg?.progress_percentage || 40;
  const streakDays = learningProg?.streak_days || 3;
  const nextTopic = learningProg?.next_topic || "Variables & Data Types";
  const completedTopics = learningProg?.completed_topics || [
    "Introduction to Python & Setup",
    "Variables & Data Types",
    "Input and Output in Python",
    "Operators (Arithmetic, Logical, Comparison)"
  ];

  return (
    <div className="space-y-8">
      {/* 1. Student Welcome & Status Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
        <div className="absolute right-0 top-0 w-96 h-96 bg-indigo-500/5 rounded-full blur-3xl pointer-events-none"></div>

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="text-xs uppercase font-bold text-indigo-400 tracking-wider">
                Active Student Workspace • Connected to MongoDB Atlas
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-black text-white">
              Welcome back, <span className="bg-gradient-to-r from-indigo-400 via-teal-300 to-emerald-400 bg-clip-text text-transparent">{currentUser?.name || currentUser?.username || 'Chitra'}</span>
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl leading-relaxed">
              {currentUser?.academic_year || '2nd Year B.Tech'} • {currentUser?.branch || 'Computer Science & Engineering'} • Target Career: <strong className="text-indigo-300">{data.career_goal}</strong>
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => onNavigate('profile')}
              className="px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 hover:border-indigo-500 text-xs font-semibold text-slate-200 transition"
            >
              Edit Profile
            </button>
            <button
              onClick={fetchDashboard}
              className="p-2.5 rounded-xl bg-slate-850 border border-slate-700 hover:border-indigo-500 text-slate-400 hover:text-indigo-300 transition"
              title="Refresh Analytics"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* 2. Real-Time Student Learning Status Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Current Learning Subject */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-lg flex flex-col justify-between space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider">Current Learning</span>
            <BookOpen className="w-4 h-4 text-indigo-400" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-white">{currentSubject}</h3>
            <div className="flex items-center justify-between text-xs text-slate-400 mt-1">
              <span>Progress</span>
              <span className="font-bold text-indigo-300">{currentProgressPct}%</span>
            </div>
            <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800 mt-1.5">
              <div
                className="bg-indigo-500 h-full rounded-full transition-all duration-500"
                style={{ width: `${currentProgressPct}%` }}
              ></div>
            </div>
          </div>
          <button
            onClick={() => onNavigate('learning')}
            className="pt-2 flex items-center justify-between text-xs text-indigo-400 hover:text-indigo-300 font-bold border-t border-slate-800/80"
          >
            <span>Continue Learning</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Today's Target Topic */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-lg flex flex-col justify-between space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-teal-300 uppercase tracking-wider">Today's Topic</span>
            <Clock className="w-4 h-4 text-teal-400" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white line-clamp-1">{nextTopic}</h3>
            <p className="text-xs text-slate-400 mt-1">Estimated: 45 minutes session</p>
          </div>
          <button
            onClick={() => onNavigate('learning')}
            className="w-full py-2 bg-gradient-to-r from-teal-500 to-emerald-400 hover:from-teal-600 hover:to-emerald-500 text-slate-950 font-bold text-xs rounded-xl shadow transition text-center"
          >
            Start Learning →
          </button>
        </div>

        {/* Learning Streak */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-lg flex flex-col justify-between space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-amber-400 uppercase tracking-wider">Learning Streak</span>
            <Flame className="w-4 h-4 fill-amber-400 text-amber-400" />
          </div>
          <div>
            <h3 className="text-2xl font-black text-amber-400 flex items-center gap-1.5">
              <span>🔥 {streakDays}</span>
              <span className="text-sm font-semibold text-slate-300">Days</span>
            </h3>
            <p className="text-xs text-slate-400 mt-1">Keep up your daily study momentum!</p>
          </div>
          <div className="text-[11px] text-emerald-400 font-semibold pt-2 border-t border-slate-800/80">
            ✓ Studied today
          </div>
        </div>

        {/* Recently Completed */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-lg flex flex-col justify-between space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">Recently Mastered</span>
            <CheckCircle className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="space-y-1.5 text-xs text-slate-300">
            {completedTopics.slice(0, 3).map((top, idx) => (
              <div key={idx} className="flex items-center space-x-1.5 truncate">
                <Check className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
                <span className="truncate">{top}</span>
              </div>
            ))}
          </div>
          <div className="text-[11px] text-slate-400 pt-1 border-t border-slate-800/80">
            {completedTopics.length} total topics completed
          </div>
        </div>
      </div>

      {/* 3. Dedicated AI Agent Launch Cards */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-indigo-400" /> Dedicated AI Agents
          </h2>
          <span className="text-xs text-slate-500">Shared MongoDB Atlas Long-Term Memory</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {/* Learning Agent Launch Card */}
          <div className="bg-gradient-to-b from-slate-900 to-indigo-950/30 border border-indigo-500/30 rounded-3xl p-6 shadow-xl hover:border-indigo-500 transition flex flex-col justify-between group">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="p-3 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 group-hover:scale-110 transition-transform">
                  <BookOpen className="w-6 h-6" />
                </span>
                <span className="text-[10px] uppercase font-bold text-indigo-300 bg-indigo-500/20 border border-indigo-500/40 px-2.5 py-0.5 rounded-full">
                  Personalized Roadmap
                </span>
              </div>
              <h3 className="text-lg font-bold text-white group-hover:text-indigo-300 transition">Learning Agent</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Learn any subject (Python, C++, Java, ML, React, SQL) with step-by-step concepts, coding examples, quizzes, verified resources & EduMind AI assistance.
              </p>
            </div>

            <div className="pt-6 border-t border-slate-800/80 mt-6 flex items-center justify-between">
              <span className="text-[11px] text-indigo-300 font-bold">{currentSubject} Path Active</span>
              <button
                onClick={() => onNavigate('learning')}
                className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow-lg shadow-indigo-600/30 transition flex items-center gap-1.5"
              >
                <span>Launch Agent</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Career Guidance Agent Launch Card */}
          <div className="bg-gradient-to-b from-slate-900 to-emerald-950/30 border border-emerald-500/30 rounded-3xl p-6 shadow-xl hover:border-emerald-500 transition flex flex-col justify-between group">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="p-3 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 group-hover:scale-110 transition-transform">
                  <Compass className="w-6 h-6" />
                </span>
                <span className="text-[10px] uppercase font-bold text-emerald-300 bg-emerald-500/20 border border-emerald-500/40 px-2.5 py-0.5 rounded-full">
                  Bayesian Engine
                </span>
              </div>
              <h3 className="text-lg font-bold text-white group-hover:text-emerald-300 transition">Career Guidance Agent</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Probabilistic suitability match, skill-gap decomposition, strategic 90-day placement milestones, and recommended projects with direct "Learn This Skill" links.
              </p>
            </div>

            <div className="pt-6 border-t border-slate-800/80 mt-6 flex items-center justify-between">
              <span className="text-[11px] text-emerald-400 font-bold">82% Match</span>
              <button
                onClick={() => onNavigate('career')}
                className="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/30 transition flex items-center gap-1.5"
              >
                <span>Launch Agent</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Mock Interview Agent Launch Card */}
          <div className="bg-gradient-to-b from-slate-900 to-amber-950/30 border border-amber-500/30 rounded-3xl p-6 shadow-xl hover:border-amber-500 transition flex flex-col justify-between group">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="p-3 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-400 group-hover:scale-110 transition-transform">
                  <Award className="w-6 h-6" />
                </span>
                <span className="text-[10px] uppercase font-bold text-amber-300 bg-amber-500/20 border border-amber-500/40 px-2.5 py-0.5 rounded-full">
                  4-Factor Rubric
                </span>
              </div>
              <h3 className="text-lg font-bold text-white group-hover:text-amber-300 transition">Mock Interview Agent</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Conduct adaptive technical mock interviews with 4-factor FAANG rubric evaluation (Accuracy, Clarity, Problem-Solving, Confidence) and auto-synced weakness tracking.
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

      {/* 4. Analytics: Radar Chart & Current vs Benchmark Gap */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Radar Chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <Brain className="w-4 h-4 text-indigo-400" /> Multidisciplinary Competency Radar
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">Verified skill coverage across core engineering disciplines</p>
            </div>
          </div>

          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="subject" stroke="#94a3b8" tick={{ fontSize: 11, fill: '#94a3b8' }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#475569" />
                <Radar name="Student Skill" dataKey="score" stroke="#6366f1" fill="#6366f1" fillOpacity={0.4} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Skill Gap Bar Chart with "Learn This Skill" Buttons */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-emerald-400" /> Current Competencies vs Placement Benchmark
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">Target benchmark: 85% for top tech readiness</p>
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

      {/* 5. Identified Weak Topics & Direct Remediation */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" /> Identified Weak Topics in Shared Memory
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">Automatically synced from mock interview evaluations & skill gaps</p>
          </div>
          <span className="text-xs text-slate-500">MongoDB Atlas Synced</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
          {data.weak_skills?.map((topic, idx) => (
            <div key={idx} className="p-4 bg-slate-950 border border-amber-500/20 rounded-2xl flex items-center justify-between">
              <div className="space-y-1">
                <div className="flex items-center space-x-2">
                  <span className="w-2 h-2 rounded-full bg-amber-400"></span>
                  <span className="text-xs font-bold text-slate-200">{topic}</span>
                </div>
                <span className="text-[10px] uppercase font-bold text-amber-300 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/30">
                  Priority {idx + 1}
                </span>
              </div>
              <button
                onClick={() => {
                  if (onLearnSubject) onLearnSubject(topic);
                  onNavigate('learning');
                }}
                className="px-3 py-1.5 bg-indigo-600/30 hover:bg-indigo-600 text-indigo-300 hover:text-white border border-indigo-500/40 rounded-xl text-xs font-bold transition flex items-center gap-1"
              >
                <span>Learn Skill</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
