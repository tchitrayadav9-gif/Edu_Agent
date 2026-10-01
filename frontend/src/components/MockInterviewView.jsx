import React, { useState } from 'react';
import { Award, Play, Send, CheckCircle2, AlertCircle, ArrowRight, RefreshCw, Star } from 'lucide-react';
import { api } from '../api';

export default function MockInterviewView() {
  const [topic, setTopic] = useState('Machine Learning');
  const [session, setSession] = useState(null);
  const [answer, setAnswer] = useState('');
  const [feedbackData, setFeedbackData] = useState(null);
  const [loading, setLoading] = useState(false);

  const startSession = async () => {
    setLoading(true);
    setFeedbackData(null);
    setAnswer('');
    try {
      const res = await api.startInterview('AI Engineer', topic);
      setSession(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async (e) => {
    e.preventDefault();
    if (!answer.trim() || !session?.session_id) return;

    setLoading(true);
    try {
      const res = await api.submitAnswer(session.session_id, answer);
      setFeedbackData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-teal-400" /> Adaptive Mock Technical Interview Arena
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Conducts real-time adaptive questioning, evaluates your explanations (0-10), and permanently saves scores into your memory profile.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <select
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-teal-500"
          >
            <option value="Machine Learning">Machine Learning</option>
            <option value="Python">Python Programming</option>
            <option value="AI Fundamentals">AI & Heuristic Search</option>
            <option value="Data Structures">Data Structures & Algorithms</option>
          </select>
          <button
            onClick={startSession}
            disabled={loading}
            className="flex items-center space-x-1.5 px-4 py-1.5 bg-teal-500 hover:bg-teal-600 text-slate-950 font-bold text-xs rounded-lg transition"
          >
            <Play className="w-3.5 h-3.5 fill-slate-950" />
            <span>Start Mock</span>
          </button>
        </div>
      </div>

      {/* Main Interactive Arena */}
      {session ? (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
          {/* Question Box */}
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-[11px] uppercase font-bold text-teal-400 tracking-wider">
                Topic: {session.topic} • Difficulty: {session.difficulty}
              </span>
              <span className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded">Adaptive Evaluator Active</span>
            </div>
            <p className="text-sm font-semibold text-white leading-relaxed">{session.question}</p>
          </div>

          {/* Answer Input */}
          {!feedbackData && (
            <form onSubmit={submitAnswer} className="space-y-3">
              <label className="text-xs text-slate-400 block font-medium">Your Technical Explanation:</label>
              <textarea
                rows={5}
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Explain the concepts, mathematical formulation, trade-offs, and practical implementations clearly..."
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-teal-500"
              ></textarea>
              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={loading || !answer.trim()}
                  className="flex items-center space-x-1.5 px-5 py-2 bg-teal-500 hover:bg-teal-600 text-slate-950 font-bold text-xs rounded-xl transition"
                >
                  <Send className="w-3.5 h-3.5" />
                  <span>{loading ? 'Evaluating with Rubric...' : 'Submit Answer for Evaluation'}</span>
                </button>
              </div>
            </form>
          )}

          {/* Evaluation & Scoring Feedback */}
          {feedbackData && (
            <div className="space-y-4 p-5 rounded-xl bg-slate-950 border border-slate-800">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div className="flex items-center space-x-2">
                  <div className="p-2 rounded-lg bg-teal-500/10 text-teal-400">
                    <Award className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-white uppercase">Evaluation Score</h4>
                    <p className="text-xs text-slate-400">Logged to Student Long-Term Memory</p>
                  </div>
                </div>

                <div className="flex items-center space-x-1 bg-slate-900 px-3 py-1 rounded-lg border border-slate-800 text-emerald-400 font-bold text-base">
                  <Star className="w-4 h-4 fill-emerald-400 mr-1" />
                  {feedbackData.score} / 10.0
                </div>
              </div>

              <div className="text-xs text-slate-300 leading-relaxed">
                <span className="font-bold text-slate-200 block mb-1">Constructive Feedback:</span>
                {feedbackData.feedback}
              </div>

              {feedbackData.next_question && (
                <div className="mt-4 p-4 rounded-lg bg-slate-900 border border-slate-800 space-y-2">
                  <span className="text-[11px] font-bold text-teal-400 uppercase tracking-wider block">
                    Adaptive Follow-Up Question ({feedbackData.adaptive_next_difficulty} Difficulty):
                  </span>
                  <p className="text-xs text-slate-200">{feedbackData.next_question}</p>
                </div>
              )}

              <div className="flex justify-end pt-2">
                <button
                  onClick={startSession}
                  className="flex items-center space-x-1.5 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg transition"
                >
                  <RefreshCw className="w-3.5 h-3.5 mr-1" />
                  <span>Next Interview Question</span>
                </button>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center text-slate-500">
          <Award className="w-12 h-12 mx-auto mb-3 text-slate-700 stroke-1" />
          <h3 className="text-sm font-semibold text-slate-300">Ready to test your knowledge?</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
            Select a subject and click "Start Mock" to launch an adaptive technical interview session.
          </p>
        </div>
      )}
    </div>
  );
}
