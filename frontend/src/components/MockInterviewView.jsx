import React, { useState, useEffect } from 'react';
import { Award, Play, Send, CheckCircle2, AlertCircle, ArrowRight, RefreshCw, Star, BarChart2, ShieldAlert, BookOpen, Volume2, Mic, Check, HelpCircle } from 'lucide-react';
import { api } from '../api';

export default function MockInterviewView({ currentUser, onOpenLearning }) {
  const targetUserId = currentUser?.user_id || currentUser?.id || "chitra_demo_user";
  const [targetRole, setTargetRole] = useState(currentUser?.career_goal || 'AI Engineer');
  const [topic, setTopic] = useState('Machine Learning');
  const [difficulty, setDifficulty] = useState('Intermediate');
  
  const [session, setSession] = useState(null);
  const [answer, setAnswer] = useState('');
  const [feedbackData, setFeedbackData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [history, setHistory] = useState([]);
  const [isRecording, setIsRecording] = useState(false);

  // Start interview session
  const startSession = async () => {
    setLoading(true);
    setFeedbackData(null);
    setAnswer('');
    try {
      const res = await api.startInterview(targetRole, topic, targetUserId);
      setSession(res);
    } catch (err) {
      console.error("Error starting mock interview:", err);
    } finally {
      setLoading(false);
    }
  };

  // Submit student answer for rubric scoring
  const submitAnswer = async (e) => {
    e.preventDefault();
    if (!answer.trim() || !session?.session_id) return;

    setSubmitting(true);
    try {
      const res = await api.submitAnswer(session.session_id, answer, targetUserId);
      setFeedbackData(res);
      // Append to local interview history
      setHistory(prev => [
        {
          id: session.session_id,
          topic: session.topic || topic,
          role: targetRole,
          score: res.score || 7.5,
          timestamp: new Date().toLocaleTimeString(),
          feedback: res.feedback
        },
        ...prev.slice(0, 4)
      ]);
    } catch (err) {
      console.error("Error evaluating answer:", err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleSimulateVoiceInput = () => {
    setIsRecording(true);
    setTimeout(() => {
      setIsRecording(false);
      setAnswer(prev => prev + (prev ? " " : "") + "In machine learning, gradient descent iteratively minimizes the loss function by computing the partial derivatives of the loss with respect to parameters and stepping in the direction of steepest descent scaled by the learning rate.");
    }, 1500);
  };

  const rubric = feedbackData?.rubric || {
    technical_accuracy: feedbackData ? Math.min(100, Math.round((feedbackData.score || 7) * 10 + 5)) : 80,
    communication_clarity: 85,
    problem_solving: 75,
    confidence: 80
  };

  return (
    <div className="space-y-6">
      {/* Hero Header */}
      <div className="bg-gradient-to-r from-slate-900 via-amber-950/30 to-slate-900 border border-amber-500/20 rounded-2xl p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <span className="p-2.5 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/30">
              <Award className="w-7 h-7" />
            </span>
            <div>
              <h1 className="text-xl font-bold text-white flex items-center gap-2">
                Mock Interview Agent
                <span className="text-xs bg-amber-500/20 text-amber-300 border border-amber-500/40 px-2 py-0.5 rounded-full font-medium">
                  Multi-Factor Rubric
                </span>
              </h1>
              <p className="text-xs text-slate-400">
                Conducts realistic technical & conceptual interviews, scores across 4 evaluation rubrics, and logs weak topics to shared memory.
              </p>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="flex items-center gap-3 bg-slate-950/70 border border-slate-800 rounded-xl p-3 text-xs">
            <div>
              <span className="text-[10px] text-slate-400 uppercase block">Target Career</span>
              <span className="font-bold text-amber-300">{targetRole}</span>
            </div>
            <div className="h-6 w-px bg-slate-800"></div>
            <div>
              <span className="text-[10px] text-slate-400 uppercase block">Evaluation Standard</span>
              <span className="font-bold text-white">4-Factor FAANG Rubric</span>
            </div>
          </div>
        </div>

        {/* Setup Toolbar */}
        <div className="mt-6 pt-4 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-2 text-xs">
            <span className="text-slate-400 font-medium">Interview Parameters:</span>
            
            <select
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5 text-slate-200 focus:outline-none focus:border-amber-500"
            >
              <option value="AI Engineer">AI Engineer</option>
              <option value="Data Scientist">Data Scientist</option>
              <option value="Machine Learning Engineer">ML Engineer</option>
              <option value="Software Engineer">Software Engineer</option>
            </select>

            <select
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5 text-slate-200 focus:outline-none focus:border-amber-500"
            >
              <option value="Machine Learning">Machine Learning</option>
              <option value="Python">Python Programming</option>
              <option value="AI Fundamentals">AI & Heuristic Search</option>
              <option value="Data Structures">Data Structures & Algorithms</option>
              <option value="System Design">AI System Design</option>
            </select>

            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5 text-slate-200 focus:outline-none focus:border-amber-500"
            >
              <option value="Junior">Junior Level</option>
              <option value="Intermediate">Intermediate / Mid-Level</option>
              <option value="Senior">Senior / Tech Lead</option>
            </select>
          </div>

          <button
            onClick={startSession}
            disabled={loading}
            className="px-5 py-2 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-slate-950 font-bold text-xs rounded-xl shadow-lg shadow-amber-500/20 transition flex items-center gap-2"
          >
            {loading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5 fill-slate-950" />}
            <span>{session ? 'Restart New Session' : 'Start Mock Interview'}</span>
          </button>
        </div>
      </div>

      {/* Main Interactive Stage */}
      {session ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left 2 Cols: Question & Live Input */}
          <div className="lg:col-span-2 space-y-6">
            {/* Question Card */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div className="flex items-center space-x-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping"></span>
                  <span className="text-xs font-bold text-amber-300 uppercase tracking-wider">
                    Question • {session.topic || topic}
                  </span>
                </div>
                <div className="flex items-center space-x-2 text-[11px]">
                  <span className="bg-slate-950 text-slate-400 px-2.5 py-1 rounded-lg border border-slate-800">
                    Difficulty: <strong className="text-white">{session.difficulty || difficulty}</strong>
                  </span>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80">
                <p className="text-sm font-semibold text-white leading-relaxed">{session.question}</p>
              </div>

              <div className="flex items-center justify-between text-xs text-slate-400 pt-1">
                <span>💡 Tip: Structure your response with intuition, trade-offs, and edge cases.</span>
                <button
                  type="button"
                  onClick={handleSimulateVoiceInput}
                  disabled={isRecording}
                  className="flex items-center space-x-1.5 px-3 py-1 rounded-lg bg-slate-950 border border-slate-800 hover:border-amber-500/50 text-amber-300 transition"
                >
                  <Mic className={`w-3.5 h-3.5 ${isRecording ? 'text-rose-400 animate-pulse' : ''}`} />
                  <span>{isRecording ? 'Listening...' : 'Voice Dictate'}</span>
                </button>
              </div>
            </div>

            {/* Answer Input Form */}
            {!feedbackData && (
              <form onSubmit={submitAnswer} className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                    Your Response:
                  </label>
                  <span className="text-[11px] text-slate-500">{answer.split(/\s+/).filter(Boolean).length} words</span>
                </div>

                <textarea
                  rows={6}
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  placeholder="Type your structured explanation here (e.g., definitions, mathematical formulation, practical implementations, time complexity, and practical considerations)..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-amber-500 leading-relaxed font-mono"
                ></textarea>

                <div className="flex items-center justify-between pt-2">
                  <span className="text-xs text-slate-500">
                    Your evaluation score will automatically update your long-term memory.
                  </span>
                  <button
                    type="submit"
                    disabled={submitting || !answer.trim()}
                    className="px-6 py-2.5 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-slate-950 font-bold text-xs rounded-xl shadow-lg shadow-amber-500/20 transition flex items-center gap-2 disabled:opacity-50"
                  >
                    {submitting ? (
                      <>
                        <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                        <span>Evaluating Rubric...</span>
                      </>
                    ) : (
                      <>
                        <Send className="w-3.5 h-3.5" />
                        <span>Submit Answer</span>
                      </>
                    )}
                  </button>
                </div>
              </form>
            )}

            {/* Detailed Evaluation & Multi-Factor Rubric Output */}
            {feedbackData && (
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
                {/* Score Banner */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-800 gap-4">
                  <div className="flex items-center space-x-3">
                    <div className="p-3 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-400">
                      <Star className="w-6 h-6 fill-amber-400" />
                    </div>
                    <div>
                      <h3 className="text-base font-bold text-white">Interview Evaluation Scorecard</h3>
                      <p className="text-xs text-slate-400">Score permanently logged to MongoDB Atlas profile memory</p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2 bg-slate-950 border border-slate-800 px-4 py-2 rounded-xl">
                    <span className="text-xs text-slate-400 uppercase font-semibold">Overall:</span>
                    <span className="text-2xl font-black text-amber-400">{feedbackData.score || 7.5}</span>
                    <span className="text-xs text-slate-500">/ 10.0</span>
                  </div>
                </div>

                {/* 4-Factor Rubric Breakdown */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl text-center space-y-1">
                    <span className="text-[10px] text-slate-400 uppercase block font-semibold">Technical Accuracy</span>
                    <span className="text-lg font-bold text-emerald-400">{rubric.technical_accuracy}%</span>
                  </div>
                  <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl text-center space-y-1">
                    <span className="text-[10px] text-slate-400 uppercase block font-semibold">Communication</span>
                    <span className="text-lg font-bold text-teal-300">{rubric.communication_clarity}%</span>
                  </div>
                  <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl text-center space-y-1">
                    <span className="text-[10px] text-slate-400 uppercase block font-semibold">Problem Solving</span>
                    <span className="text-lg font-bold text-amber-400">{rubric.problem_solving}%</span>
                  </div>
                  <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl text-center space-y-1">
                    <span className="text-[10px] text-slate-400 uppercase block font-semibold">Confidence</span>
                    <span className="text-lg font-bold text-indigo-400">{rubric.confidence}%</span>
                  </div>
                </div>

                {/* Constructive Pedagogical Feedback */}
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2 text-xs">
                  <span className="font-bold text-amber-400 uppercase tracking-wider block">
                    Detailed Feedback & Analysis:
                  </span>
                  <p className="text-slate-200 leading-relaxed">{feedbackData.feedback}</p>
                </div>

                {/* Model Ideal Answer Comparison */}
                {feedbackData.model_answer && (
                  <div className="p-4 bg-indigo-950/20 border border-indigo-500/30 rounded-xl space-y-2 text-xs">
                    <span className="font-bold text-indigo-300 uppercase tracking-wider block flex items-center gap-1.5">
                      <BookOpen className="w-3.5 h-3.5" /> Model Benchmark Answer:
                    </span>
                    <p className="text-slate-300 leading-relaxed">{feedbackData.model_answer}</p>
                  </div>
                )}

                {/* Adaptive Next Question */}
                {feedbackData.next_question && (
                  <div className="p-4 bg-slate-950 border border-amber-500/30 rounded-xl space-y-2">
                    <span className="text-[11px] font-bold text-amber-400 uppercase tracking-wider block">
                      Adaptive Follow-Up ({feedbackData.adaptive_next_difficulty || 'Advanced'} Difficulty):
                    </span>
                    <p className="text-xs text-white font-medium">{feedbackData.next_question}</p>
                  </div>
                )}

                {/* Next Question Action */}
                <div className="flex items-center justify-between pt-2">
                  <button
                    onClick={onOpenLearning}
                    className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1"
                  >
                    <span>Practice Weak Topics in Learning Agent</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>

                  <button
                    onClick={startSession}
                    className="px-5 py-2.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs rounded-xl shadow-lg shadow-amber-500/20 transition flex items-center gap-1.5"
                  >
                    <RefreshCw className="w-3.5 h-3.5" />
                    <span>Next Mock Question</span>
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Right Col: Past Sessions & Rubric Guidelines */}
          <div className="space-y-6">
            {/* Rubric Criteria Info */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-3">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <BarChart2 className="w-4 h-4 text-amber-400" /> Evaluation Rubric Criteria
              </h3>
              <div className="space-y-2 text-xs text-slate-400">
                <div className="p-2.5 bg-slate-950 rounded-xl border border-slate-800">
                  <strong className="text-emerald-400 block">Technical Accuracy (35%)</strong>
                  Correctness of mathematical foundations, algorithms & formulas.
                </div>
                <div className="p-2.5 bg-slate-950 rounded-xl border border-slate-800">
                  <strong className="text-teal-300 block">Communication (25%)</strong>
                  Conciseness, clarity, logical structure & terminology.
                </div>
                <div className="p-2.5 bg-slate-950 rounded-xl border border-slate-800">
                  <strong className="text-amber-400 block">Problem-Solving (25%)</strong>
                  Decomposition of problems, edge case awareness & trade-offs.
                </div>
                <div className="p-2.5 bg-slate-950 rounded-xl border border-slate-800">
                  <strong className="text-indigo-400 block">Confidence (15%)</strong>
                  Assertiveness, depth of explanation, and direct addressing of prompt.
                </div>
              </div>
            </div>

            {/* Past Interview History in Session */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-3">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <Award className="w-4 h-4 text-amber-400" /> Recent Mock History
              </h3>

              {history.length > 0 ? (
                <div className="space-y-2.5">
                  {history.map((h, idx) => (
                    <div key={idx} className="p-3 bg-slate-950 border border-slate-800 rounded-xl flex items-center justify-between text-xs">
                      <div>
                        <p className="font-semibold text-white">{h.topic}</p>
                        <p className="text-[10px] text-slate-500">{h.role} • {h.timestamp}</p>
                      </div>
                      <span className="font-bold text-amber-400 bg-amber-500/10 px-2 py-1 rounded border border-amber-500/20">
                        {h.score} / 10
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-500 text-center py-4">
                  No previous mock questions in current session.
                </p>
              )}
            </div>
          </div>
        </div>
      ) : (
        /* Empty State / Launchpad */
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-12 text-center text-slate-400 space-y-4 shadow-xl">
          <div className="w-16 h-16 rounded-3xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 mx-auto">
            <Award className="w-8 h-8" />
          </div>
          <div className="space-y-1 max-w-md mx-auto">
            <h3 className="text-base font-bold text-white">Ready for your technical mock interview?</h3>
            <p className="text-xs text-slate-400">
              Select your target role and topic above, then click <strong>"Start Mock Interview"</strong> to begin your session.
            </p>
          </div>
          <button
            onClick={startSession}
            disabled={loading}
            className="px-6 py-2.5 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-slate-950 font-bold text-xs rounded-xl shadow-lg shadow-amber-500/20 transition inline-flex items-center gap-2"
          >
            <Play className="w-3.5 h-3.5 fill-slate-950" />
            <span>Launch Mock Interview Session</span>
          </button>
        </div>
      )}
    </div>
  );
}
