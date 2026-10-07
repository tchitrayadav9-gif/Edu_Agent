import React, { useState, useEffect } from 'react';
import { Compass, Target, TrendingUp, Award, CheckCircle, AlertTriangle, ArrowRight, Zap, RefreshCw, Briefcase, ChevronRight, ShieldCheck, Star } from 'lucide-react';
import { api } from '../api';

export default function CareerAgentView({ currentUser, onOpenLearning, onOpenInterview }) {
  const targetUserId = currentUser?.user_id || currentUser?.id || "chitra_demo_user";
  const [selectedRole, setSelectedRole] = useState(currentUser?.career_goal || 'AI Engineer');
  const [loading, setLoading] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);

  const availableRoles = [
    { id: 'AI Engineer', label: 'AI Engineer / LLM Specialist', badge: 'High Demand' },
    { id: 'Data Scientist', label: 'Data Scientist & Analytics', badge: 'Core Tech' },
    { id: 'Machine Learning Engineer', label: 'MLOps & Systems Engineer', badge: 'Advanced' },
    { id: 'Software Engineer', label: 'Full Stack & Backend Engineer', badge: 'Foundation' }
  ];

  const fetchCareerAnalysis = async (role) => {
    setLoading(true);
    try {
      const res = await api.analyzeCareer(role, targetUserId);
      setAnalysisData(res);
    } catch (err) {
      console.error("Error analyzing career path:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCareerAnalysis(selectedRole);
  }, [selectedRole, targetUserId]);

  const bayesianScores = analysisData?.bayesian_suitability || {
    "AI Engineer": 0.82,
    "Data Scientist": 0.74,
    "Machine Learning Engineer": 0.68,
    "Software Engineer": 0.79
  };

  const currentMatchPct = Math.round((bayesianScores[selectedRole] || 0.8) * 100);

  return (
    <div className="space-y-6">
      {/* Hero Header */}
      <div className="bg-gradient-to-r from-slate-900 via-emerald-950/40 to-slate-900 border border-emerald-500/20 rounded-2xl p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <span className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              <Compass className="w-7 h-7" />
            </span>
            <div>
              <h1 className="text-xl font-bold text-white flex items-center gap-2">
                Career Guidance Agent
                <span className="text-xs bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 px-2 py-0.5 rounded-full font-medium">
                  Bayesian Inference Engine
                </span>
              </h1>
              <p className="text-xs text-slate-400">
                Probabilistic suitability calculation, skill-gap decomposition, milestone planning, and portfolio recommendations.
              </p>
            </div>
          </div>

          {/* Role Selector Buttons */}
          <div className="flex flex-wrap gap-2">
            {availableRoles.map((r) => (
              <button
                key={r.id}
                onClick={() => setSelectedRole(r.id)}
                className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition flex items-center gap-1.5 ${
                  selectedRole === r.id
                    ? 'bg-emerald-500 text-slate-950 shadow-lg shadow-emerald-500/20'
                    : 'bg-slate-950 text-slate-400 hover:text-slate-200 border border-slate-800'
                }`}
              >
                <span>{r.id}</span>
                {selectedRole === r.id && <CheckCircle className="w-3 h-3" />}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Top Metrics Banner */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Match Probability */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex items-center justify-between">
          <div className="space-y-1">
            <span className="text-[11px] text-slate-400 uppercase font-bold tracking-wider">Bayesian Match Rate</span>
            <div className="flex items-baseline space-x-2">
              <span className="text-3xl font-black text-white">{currentMatchPct}%</span>
              <span className="text-xs text-emerald-400 font-semibold">
                {currentMatchPct >= 75 ? 'Strong Trajectory' : currentMatchPct >= 50 ? 'Moderate Fit' : 'Requires Upskilling'}
              </span>
            </div>
            <p className="text-[11px] text-slate-500">P({selectedRole} | Evidence, Skills, Weaknesses)</p>
          </div>
          <div className="w-14 h-14 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <Target className="w-7 h-7" />
          </div>
        </div>

        {/* Top Priority Gap */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex items-center justify-between">
          <div className="space-y-1">
            <span className="text-[11px] text-slate-400 uppercase font-bold tracking-wider">Highest Priority Skill Gap</span>
            <h3 className="text-xl font-bold text-amber-400">
              {analysisData?.recommended_focus || 'Statistics / ML'}
            </h3>
            <p className="text-[11px] text-slate-400">Greatest delta to target competency</p>
          </div>
          <div className="w-14 h-14 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
            <AlertTriangle className="w-7 h-7" />
          </div>
        </div>

        {/* Readiness Status */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex items-center justify-between">
          <div className="space-y-1">
            <span className="text-[11px] text-slate-400 uppercase font-bold tracking-wider">Career Readiness Horizon</span>
            <h3 className="text-xl font-bold text-teal-300">~60 - 90 Days</h3>
            <p className="text-[11px] text-slate-400">At 2.0 hours daily study cadence</p>
          </div>
          <div className="w-14 h-14 rounded-2xl bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-400">
            <Zap className="w-7 h-7" />
          </div>
        </div>
      </div>

      {/* Main Grid: Skill Gap Analysis & Bayesian Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Detailed Skill Gap Table */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-emerald-400" /> Skill Gap Matrix for {selectedRole}
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Compares current verified competency levels against industry benchmarks.
              </p>
            </div>
            {loading && <RefreshCw className="w-4 h-4 animate-spin text-emerald-400" />}
          </div>

          <div className="space-y-4">
            {analysisData?.skill_gaps && analysisData.skill_gaps.length > 0 ? (
              analysisData.skill_gaps.map((gap, idx) => (
                <div key={idx} className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <div className="flex items-center space-x-2">
                      <span className="font-bold text-white text-sm">{gap.skill}</span>
                      {gap.is_weak_topic && (
                        <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/30">
                          Identified Weakness
                        </span>
                      )}
                    </div>
                    <div className="flex items-center space-x-2 text-slate-400">
                      <span>Current: <strong className="text-white">{gap.current_level}%</strong></span>
                      <span>•</span>
                      <span>Target: <strong className="text-emerald-400">{gap.target_level}%</strong></span>
                      <span className="text-rose-400 font-bold">(-{gap.gap_delta}%)</span>
                    </div>
                  </div>

                  {/* Dual Bar (Current vs Gap) */}
                  <div className="w-full bg-slate-900 h-2.5 rounded-full overflow-hidden flex border border-slate-800">
                    <div
                      className="bg-emerald-500 h-full transition-all duration-500"
                      style={{ width: `${gap.current_level}%` }}
                    ></div>
                    <div
                      className="bg-rose-500/40 h-full transition-all duration-500"
                      style={{ width: `${gap.gap_delta}%` }}
                    ></div>
                  </div>

                  {/* Learn This Skill Action Button */}
                  <div className="flex justify-end pt-1">
                    <button
                      onClick={() => onOpenLearning && onOpenLearning(gap.skill)}
                      className="px-3 py-1 bg-indigo-600/30 hover:bg-indigo-600 text-indigo-300 hover:text-white border border-indigo-500/40 rounded-lg text-xs font-semibold transition flex items-center gap-1"
                    >
                      <span>Learn {gap.skill}</span>
                      <ArrowRight className="w-3 h-3" />
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <div className="p-6 text-center text-xs text-slate-400 bg-slate-950 rounded-xl border border-slate-800">
                🎉 Excellent! All primary skill requirements for <strong>{selectedRole}</strong> are satisfied at benchmark level.
              </div>
            )}
          </div>
        </div>

        {/* Right Col: Bayesian Roles Comparison & Forward Reasoning */}
        <div className="space-y-6">
          {/* Comparative Role Probabilities */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Compass className="w-4 h-4 text-emerald-400" /> Career Trajectory Probabilities
            </h3>
            <p className="text-xs text-slate-400">
              Evaluated across your skill profile via exact Bayesian network inference:
            </p>

            <div className="space-y-3 pt-1">
              {Object.entries(bayesianScores).map(([role, prob]) => {
                const pct = Math.round(prob * 100);
                const isCurrent = role === selectedRole;
                return (
                  <div
                    key={role}
                    onClick={() => setSelectedRole(role)}
                    className={`p-3 rounded-xl border cursor-pointer transition ${
                      isCurrent
                        ? 'bg-emerald-950/30 border-emerald-500/50'
                        : 'bg-slate-950 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex justify-between text-xs font-semibold mb-1">
                      <span className={isCurrent ? 'text-emerald-300' : 'text-slate-300'}>{role}</span>
                      <span className={isCurrent ? 'text-emerald-400' : 'text-slate-400'}>{pct}%</span>
                    </div>
                    <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${isCurrent ? 'bg-emerald-400' : 'bg-slate-600'}`}
                        style={{ width: `${pct}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Forward Chaining Expert System Output */}
          {analysisData?.logical_reasoning && (
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-3">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-teal-400" /> Rule-Based Logic Inferences
              </h3>
              <div className="space-y-2">
                {analysisData.logical_reasoning.inferred_facts ? (
                  Object.entries(analysisData.logical_reasoning.inferred_facts).map(([k, v], idx) => (
                    <div key={idx} className="p-2.5 bg-slate-950 border border-slate-800/80 rounded-lg text-xs flex justify-between">
                      <span className="text-slate-400">{k}:</span>
                      <span className="text-teal-300 font-semibold">{String(v)}</span>
                    </div>
                  ))
                ) : (
                  <p className="text-xs text-slate-500">No rule conflicts found.</p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Recommended Portfolio Projects & Industry Certifications */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recommended Projects */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Briefcase className="w-4 h-4 text-emerald-400" /> High-Impact Portfolio Projects
          </h3>
          <p className="text-xs text-slate-400">
            Building these specific projects will bridge your highest-delta gaps for technical interview screens:
          </p>

          <div className="space-y-3">
            {[
              {
                title: "Multi-Agent RAG System with MongoDB Atlas & LangGraph",
                skills: ["Python", "LangChain", "Vector Embeddings", "FastAPI"],
                impact: "Proves enterprise agentic architecture and memory persistence skills."
              },
              {
                title: "End-to-End MLOps Pipeline & Model Serving",
                skills: ["PyTorch", "Docker", "FastAPI", "MLflow"],
                impact: "Demonstrates production deployment, monitoring, and automated retraining."
              },
              {
                title: "Transformer-based Question Answering Engine",
                skills: ["HuggingFace", "Attention Mechanisms", "PyTorch"],
                impact: "Validates deep conceptual understanding of modern LLM architectures."
              }
            ].map((p, idx) => (
              <div key={idx} className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
                <h4 className="text-xs font-bold text-white">{p.title}</h4>
                <p className="text-xs text-slate-400">{p.impact}</p>
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {p.skills.map((s, sIdx) => (
                    <span key={sIdx} className="text-[10px] bg-slate-900 text-slate-300 border border-slate-800 px-2 py-0.5 rounded">
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recommended Certifications & Direct Next Actions */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4 flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Award className="w-4 h-4 text-emerald-400" /> Recommended Industry Certifications
            </h3>
            <p className="text-xs text-slate-400 mb-3">
              Recognized credentials to validate competence for recruiter screening:
            </p>

            <div className="space-y-3">
              {[
                { name: "TensorFlow Developer Certificate / PyTorch Deep Learning Specialization", issuer: "DeepLearning.AI" },
                { name: "AWS Certified Machine Learning – Specialty / GCP Professional ML Engineer", issuer: "Cloud Vendors" },
                { name: "DeepLearning.AI LangChain / LangGraph Agentic Systems", issuer: "Andrew Ng / DeepLearning.AI" }
              ].map((c, idx) => (
                <div key={idx} className="p-3 bg-slate-950 border border-slate-800 rounded-xl flex items-center justify-between text-xs">
                  <div>
                    <p className="font-semibold text-slate-200">{c.name}</p>
                    <p className="text-[10px] text-slate-500">{c.issuer}</p>
                  </div>
                  <Star className="w-4 h-4 text-amber-400 fill-amber-400" />
                </div>
              ))}
            </div>
          </div>

          <div className="mt-4 p-4 rounded-xl bg-gradient-to-r from-emerald-950/40 to-teal-950/40 border border-emerald-500/30 flex items-center justify-between gap-4">
            <div className="text-xs">
              <span className="font-bold text-emerald-300 block">Ready to start addressing these gaps?</span>
              <span className="text-slate-400">Launch a personalized study schedule or take a mock interview.</span>
            </div>
            <button
              onClick={onOpenLearning}
              className="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs rounded-xl transition flex items-center gap-1.5 flex-shrink-0"
            >
              <span>View Study Plan</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
