import React, { useState, useEffect } from 'react';
import { Compass, Target, Award, Database, FileText, CheckCircle, AlertTriangle, TrendingUp, RefreshCw } from 'lucide-react';
import { api } from '../api';

export default function DashboardView() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchDashboard = async () => {
    setLoading(true);
    try {
      const res = await api.getDashboard();
      setData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        <RefreshCw className="w-6 h-6 animate-spin text-teal-400 mr-2" /> Loading student metrics...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-400 uppercase font-semibold">Target Career</span>
            <Target className="w-5 h-5 text-teal-400" />
          </div>
          <div className="mt-2">
            <h3 className="text-xl font-bold text-white">{data.career_goal}</h3>
            <p className="text-xs text-emerald-400 mt-0.5">82% Bayesian Suitability Match</p>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-400 uppercase font-semibold">Average Skill Score</span>
            <TrendingUp className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="mt-2">
            <h3 className="text-xl font-bold text-white">{data.average_skill_score} / 100</h3>
            <p className="text-xs text-slate-400 mt-0.5">Based on 5 core disciplines</p>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-400 uppercase font-semibold">Interview Readiness</span>
            <Award className="w-5 h-5 text-amber-400" />
          </div>
          <div className="mt-2">
            <h3 className="text-xl font-bold text-white">{data.average_interview_score} / 10</h3>
            <p className="text-xs text-amber-400 mt-0.5">Adaptive Mock Diagnostic</p>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-400 uppercase font-semibold">Memory & Docs</span>
            <Database className="w-5 h-5 text-cyan-400" />
          </div>
          <div className="mt-2">
            <h3 className="text-xl font-bold text-white">{data.memory_count} Facts Stored</h3>
            <p className="text-xs text-slate-400 mt-0.5">{data.document_count} Indexed RAG Document(s)</p>
          </div>
        </div>
      </div>

      {/* Main Grid: Skills & Weaknesses */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Evaluated Skills Breakdown */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-4 flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-teal-400" /> Evaluated Skill Competencies
          </h3>
          <div className="space-y-3.5">
            {Object.entries(data.skills || {}).map(([skill, score]) => (
              <div key={skill} className="space-y-1">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-300">{skill}</span>
                  <span className={score >= 75 ? 'text-emerald-400' : score >= 50 ? 'text-amber-400' : 'text-rose-400'}>
                    {score}% {score >= 75 ? '(Strong)' : score >= 50 ? '(Intermediate)' : '(Weak / Priority)'}
                  </span>
                </div>
                <div className="w-full bg-slate-950 rounded-full h-2 overflow-hidden border border-slate-800">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      score >= 75 ? 'bg-teal-500' : score >= 50 ? 'bg-amber-500' : 'bg-rose-500'
                    }`}
                    style={{ width: `${score}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Weak Topics & Remediation Recommendations */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-4 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" /> Identified Weak Topics & Priority Action
            </h3>
            
            <div className="space-y-2.5">
              {data.weak_skills?.map((weak, idx) => (
                <div key={idx} className="p-3 bg-slate-950/80 border border-amber-500/20 rounded-lg flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="w-2 h-2 rounded-full bg-amber-400"></span>
                    <span className="text-xs font-semibold text-slate-200">{weak}</span>
                  </div>
                  <span className="text-[10px] uppercase font-bold text-amber-300 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/30">
                    Priority {idx + 1}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-5 p-4 rounded-xl bg-teal-500/10 border border-teal-500/30 text-xs text-teal-200">
            <span className="font-bold block mb-1">💡 Agent Recommendation:</span>
            Focus on <strong>{data.recommended_next_skill}</strong> next using the optimized 30-day curriculum roadmap to prepare for AI Engineering interviews.
          </div>
        </div>
      </div>
    </div>
  );
}
