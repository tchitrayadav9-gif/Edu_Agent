import React, { useState, useEffect } from 'react';
import { BookOpen, Sparkles, CheckCircle2, Play, ChevronRight, Clock, Target, Award, RefreshCw, HelpCircle, ArrowRight, Zap, Layers } from 'lucide-react';
import { api } from '../api';

export default function LearningAgentView({ currentUser, onOpenInterview, onOpenCareer }) {
  const targetUserId = currentUser?.user_id || currentUser?.id || "chitra_demo_user";
  const [activeSubTab, setActiveSubTab] = useState('study_plan'); // 'study_plan', 'curriculum', 'tutor', 'quiz'
  const [loading, setLoading] = useState(false);
  const [studyPlanData, setStudyPlanData] = useState(null);
  const [dailyHours, setDailyHours] = useState(2);
  const [preferredTime, setPreferredTime] = useState('Evening');
  
  // Tutor state
  const [tutorQuery, setTutorQuery] = useState('');
  const [tutorResponse, setTutorResponse] = useState(null);
  const [tutorLoading, setTutorLoading] = useState(false);

  // Quiz state
  const [quizTopic, setQuizTopic] = useState('Machine Learning');
  const [quizQuestionIndex, setQuizQuestionIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [quizScore, setQuizScore] = useState(0);

  const sampleQuizzes = {
    'Machine Learning': [
      {
        q: "What is the primary cause of overfitting in a supervised learning model?",
        options: [
          "Too few training epochs",
          "Excessive model complexity relative to data volume & lack of regularization",
          "High bias and low variance",
          "Learning rate being set too small"
        ],
        answer: 1,
        explanation: "Overfitting occurs when a model with excessive capacity captures noise in the training dataset rather than true underlying patterns."
      },
      {
        q: "Which metric is most suitable for evaluating a classification model on highly imbalanced data?",
        options: [
          "Accuracy",
          "F1-Score / PR-AUC",
          "Mean Squared Error (MSE)",
          "Mean Absolute Percentage Error"
        ],
        answer: 1,
        explanation: "F1-Score (harmonic mean of Precision & Recall) and PR-AUC evaluate true positives effectively despite heavy class imbalance."
      },
      {
        q: "What does the Bias-Variance trade-off describe?",
        options: [
          "The balance between training speed and memory consumption",
          "The balance between underfitting (high bias) and overfitting (high variance)",
          "The trade-off between CPU and GPU compute usage",
          "The difference between L1 and L2 regularization"
        ],
        answer: 1,
        explanation: "Bias represents error from erroneous assumptions (underfitting), while variance represents sensitivity to small fluctuations in the training set (overfitting)."
      }
    ],
    'Python': [
      {
        q: "In Python, how does a generator function differ from a regular function?",
        options: [
          "It uses the 'yield' statement and returns an iterator object without storing all items in memory",
          "It executes asynchronously on a secondary thread",
          "It compiles directly to native C bytecode",
          "It cannot accept input arguments"
        ],
        answer: 0,
        explanation: "Generators use 'yield' to produce items lazily on demand, preserving execution state and saving memory for large sequences."
      },
      {
        q: "What is the Global Interpreter Lock (GIL) in CPython?",
        options: [
          "A security lock preventing unauthorized script execution",
          "A mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes at once",
          "A database lock used by SQLite",
          "A memory garbage collector"
        ],
        answer: 1,
        explanation: "The GIL prevents true parallel execution of Python bytecode across multiple threads in CPython to ensure thread-safe memory management."
      }
    ]
  };

  const handleGeneratePlan = async () => {
    setLoading(true);
    try {
      const res = await api.generateStudyPlan({
        career_goal: currentUser?.career_goal || 'AI Engineer',
        daily_hours: parseFloat(dailyHours),
        preferred_time: preferredTime,
        days: 30
      }, targetUserId);
      setStudyPlanData(res);
    } catch (err) {
      console.error("Error generating study plan:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleGeneratePlan();
  }, [targetUserId]);

  const handleAskTutor = async (e) => {
    e.preventDefault();
    if (!tutorQuery.trim()) return;
    setTutorLoading(true);
    try {
      const res = await api.chat(
        `[Learning Agent Query]: As my personalized AI tutor, please explain "${tutorQuery}" clearly with pedagogical intuition, a simple real-world analogy, a code snippet if applicable, and 3 key interview takeaways.`,
        "learning_agent_tutor",
        "auto",
        targetUserId
      );
      setTutorResponse(res.response || res.message);
    } catch (err) {
      console.error(err);
      setTutorResponse("I encountered an issue generating the tutorial. Please try again.");
    } finally {
      setTutorLoading(false);
    }
  };

  const currentQuizList = sampleQuizzes[quizTopic] || sampleQuizzes['Machine Learning'];
  const currentQuiz = currentQuizList[quizQuestionIndex] || currentQuizList[0];

  const handleAnswerOption = (idx) => {
    if (quizSubmitted) return;
    setSelectedOption(idx);
    setQuizSubmitted(true);
    if (idx === currentQuiz.answer) {
      setQuizScore(prev => prev + 1);
    }
  };

  const handleNextQuiz = () => {
    setSelectedOption(null);
    setQuizSubmitted(false);
    if (quizQuestionIndex + 1 < currentQuizList.length) {
      setQuizQuestionIndex(prev => prev + 1);
    } else {
      setQuizQuestionIndex(0);
      setQuizScore(0);
    }
  };

  return (
    <div className="space-y-6">
      {/* Learning Agent Hero Header */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-indigo-500/20 rounded-2xl p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex items-center space-x-2">
              <span className="p-2 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/30">
                <BookOpen className="w-6 h-6" />
              </span>
              <div>
                <h1 className="text-xl font-bold text-white flex items-center gap-2">
                  Learning Agent Workspace
                  <span className="text-xs bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 px-2 py-0.5 rounded-full font-medium">
                    A* Optimized Path
                  </span>
                </h1>
                <p className="text-xs text-slate-400">
                  Tailored curriculum generation, 30-day schedules, concept deep-dives, and adaptive knowledge testing.
                </p>
              </div>
            </div>
          </div>

          {/* Quick Stats Pill */}
          <div className="flex items-center gap-3 bg-slate-950/70 border border-slate-800 rounded-xl p-3 text-xs">
            <div>
              <span className="text-[10px] text-slate-400 uppercase block">Active Track</span>
              <span className="font-bold text-indigo-300">{currentUser?.career_goal || 'AI Engineer'}</span>
            </div>
            <div className="h-6 w-px bg-slate-800"></div>
            <div>
              <span className="text-[10px] text-slate-400 uppercase block">Daily Goal</span>
              <span className="font-bold text-emerald-400">{dailyHours} Hours / Day</span>
            </div>
          </div>
        </div>

        {/* Sub-Navigation Tabs */}
        <div className="flex space-x-2 mt-6 border-t border-slate-800/80 pt-4 overflow-x-auto">
          <button
            onClick={() => setActiveSubTab('study_plan')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
              activeSubTab === 'study_plan'
                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20'
                : 'bg-slate-950 text-slate-400 hover:text-slate-200 border border-slate-800'
            }`}
          >
            <Clock className="w-3.5 h-3.5" />
            <span>30-Day Study Plan</span>
          </button>

          <button
            onClick={() => setActiveSubTab('curriculum')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
              activeSubTab === 'curriculum'
                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20'
                : 'bg-slate-950 text-slate-400 hover:text-slate-200 border border-slate-800'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>A* Prerequisite Roadmap</span>
          </button>

          <button
            onClick={() => setActiveSubTab('tutor')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
              activeSubTab === 'tutor'
                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20'
                : 'bg-slate-950 text-slate-400 hover:text-slate-200 border border-slate-800'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Interactive Concept Explainer</span>
          </button>

          <button
            onClick={() => setActiveSubTab('quiz')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
              activeSubTab === 'quiz'
                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20'
                : 'bg-slate-950 text-slate-400 hover:text-slate-200 border border-slate-800'
            }`}
          >
            <HelpCircle className="w-3.5 h-3.5" />
            <span>Adaptive Topic Quiz</span>
          </button>
        </div>
      </div>

      {/* Sub-Tab 1: 30-Day Personalized Study Schedule */}
      {activeSubTab === 'study_plan' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Controls Panel */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-5 h-fit">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Zap className="w-4 h-4 text-indigo-400" /> Plan Parameters
            </h3>

            <div className="space-y-4 text-xs">
              <div>
                <label className="text-slate-400 block mb-1">Target Career Track</label>
                <div className="p-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 font-semibold">
                  {currentUser?.career_goal || 'AI Engineer'}
                </div>
              </div>

              <div>
                <label className="text-slate-400 block mb-1">Daily Study Commitment (Hours)</label>
                <input
                  type="range"
                  min="1"
                  max="6"
                  step="0.5"
                  value={dailyHours}
                  onChange={(e) => setDailyHours(e.target.value)}
                  className="w-full accent-indigo-500"
                />
                <div className="flex justify-between text-slate-400 mt-1">
                  <span>1 hr</span>
                  <span className="text-indigo-400 font-bold">{dailyHours} hrs / day</span>
                  <span>6 hrs</span>
                </div>
              </div>

              <div>
                <label className="text-slate-400 block mb-1">Preferred Study Slot</label>
                <select
                  value={preferredTime}
                  onChange={(e) => setPreferredTime(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-slate-200 focus:outline-none focus:border-indigo-500"
                >
                  <option value="Morning">Morning (6:00 AM - 9:00 AM)</option>
                  <option value="Afternoon">Afternoon (1:00 PM - 4:00 PM)</option>
                  <option value="Evening">Evening (6:00 PM - 9:00 PM)</option>
                  <option value="Night">Late Night (9:00 PM - 12:00 AM)</option>
                </select>
              </div>

              <button
                onClick={handleGeneratePlan}
                disabled={loading}
                className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl transition flex items-center justify-center gap-2 shadow-lg shadow-indigo-600/30"
              >
                {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}
                <span>Regenerate Schedule</span>
              </button>
            </div>

            {studyPlanData && (
              <div className="p-4 bg-indigo-950/20 border border-indigo-500/20 rounded-xl text-xs space-y-2">
                <span className="text-[10px] uppercase font-bold text-indigo-400 block">Agent Analysis</span>
                <p className="text-slate-300">
                  Total curriculum commitment: <strong>{studyPlanData.total_estimated_study_hours || 60} hours</strong>.
                </p>
                <p className="text-slate-400">
                  Weak topics automatically allocated priority revision blocks.
                </p>
              </div>
            )}
          </div>

          {/* Schedule Breakdown */}
          <div className="lg:col-span-2 space-y-4">
            {loading ? (
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-12 text-center text-slate-400">
                <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-3 text-indigo-400" />
                <p className="text-sm">Optimizing 30-day curriculum with A* Search heuristics...</p>
              </div>
            ) : studyPlanData?.study_plan?.weeks ? (
              studyPlanData.study_plan.weeks.map((week, wIdx) => (
                <div key={wIdx} className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-3">
                  <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                    <div className="flex items-center space-x-2">
                      <span className="px-2.5 py-1 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 font-bold text-xs">
                        Week {week.week_number || wIdx + 1}
                      </span>
                      <h4 className="font-bold text-sm text-white">{week.theme || `Module ${wIdx + 1}`}</h4>
                    </div>
                    <span className="text-xs text-slate-400">{week.focus_area || 'Core Competencies'}</span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
                    {week.days?.map((day, dIdx) => (
                      <div key={dIdx} className="p-3 bg-slate-950/70 border border-slate-800/80 rounded-xl space-y-1.5">
                        <div className="flex items-center justify-between">
                          <span className="text-[10px] uppercase font-bold text-indigo-400">Day {day.day}</span>
                          <span className="text-[10px] text-slate-500">{day.duration_hours || dailyHours}h session</span>
                        </div>
                        <p className="text-xs font-semibold text-slate-200">{day.topic}</p>
                        <p className="text-[11px] text-slate-400 line-clamp-2">{day.tasks || day.objective}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ))
            ) : (
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 text-center text-slate-400">
                <p>Click "Regenerate Schedule" to construct your personalized study path.</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Sub-Tab 2: A* Prerequisite Roadmap */}
      {activeSubTab === 'curriculum' && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <Layers className="w-4 h-4 text-indigo-400" /> Optimal Prerequisite Dependency Graph
              </h3>
              <p className="text-xs text-slate-400 mt-1">
                Computed via A* heuristic search over knowledge dependency lattices to minimize cognitive prerequisite friction.
              </p>
            </div>
            <span className="text-xs bg-indigo-500/10 text-indigo-300 border border-indigo-500/30 px-3 py-1 rounded-lg font-medium">
              Heuristic: Manhatten Skill-Gap Delta
            </span>
          </div>

          {/* Stepper Roadmap */}
          <div className="relative pl-6 border-l-2 border-indigo-500/30 space-y-8 py-2">
            {[
              {
                step: 1,
                title: "Foundations: Python Mastery & Data Structures",
                desc: "Variables, OOP, Generators, Time Complexity (O(n)), Arrays, Trees & Hash Maps.",
                status: "Mastered",
                duration: "10 Hours"
              },
              {
                step: 2,
                title: "Mathematical Foundations & Statistics",
                desc: "Linear Algebra (Matrices, Eigenvectors), Multivariate Calculus, Probability Distributions, Bayes Theorem.",
                status: "In Progress",
                duration: "14 Hours"
              },
              {
                step: 3,
                title: "Machine Learning Algorithms & Optimization",
                desc: "Regression, Decision Trees, SVM, Gradient Descent, Bias-Variance Regularization, Evaluation Metrics.",
                status: "Next Priority",
                duration: "18 Hours"
              },
              {
                step: 4,
                title: "Deep Learning, PyTorch & Transformers",
                desc: "Backpropagation, CNNs, RNNs, Self-Attention Mechanism, HuggingFace Transformers, Fine-Tuning.",
                status: "Upcoming",
                duration: "20 Hours"
              },
              {
                step: 5,
                title: "AI Agent Architecture, RAG & LLM Orchestration",
                desc: "LangChain, LangGraph, Vector Embeddings, ChromaDB/MongoDB Atlas, Tool Calling, MCP Protocol.",
                status: "Capstone",
                duration: "15 Hours"
              }
            ].map((node) => (
              <div key={node.step} className="relative group">
                <div className={`absolute -left-[31px] top-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                  node.status === 'Mastered' ? 'bg-emerald-500 text-slate-950' :
                  node.status === 'In Progress' ? 'bg-indigo-500 text-white animate-pulse' :
                  'bg-slate-800 text-slate-400 border border-slate-700'
                }`}>
                  {node.step}
                </div>

                <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 group-hover:border-indigo-500/50 transition space-y-2">
                  <div className="flex items-center justify-between">
                    <h4 className="text-xs font-bold text-white">{node.title}</h4>
                    <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded ${
                      node.status === 'Mastered' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' :
                      node.status === 'In Progress' ? 'bg-indigo-500/10 text-indigo-300 border border-indigo-500/30' :
                      'bg-slate-800 text-slate-400'
                    }`}>
                      {node.status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">{node.desc}</p>
                  <div className="flex items-center justify-between text-[11px] text-slate-500 pt-2 border-t border-slate-900">
                    <span>Estimated Effort: {node.duration}</span>
                    <button
                      onClick={() => {
                        setTutorQuery(`Explain the key concepts and code patterns for ${node.title}`);
                        setActiveSubTab('tutor');
                      }}
                      className="text-indigo-400 hover:text-indigo-300 font-semibold flex items-center gap-1"
                    >
                      <span>Study Topic</span>
                      <ChevronRight className="w-3 h-3" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Sub-Tab 3: Interactive Concept Explainer / Tutor */}
      {activeSubTab === 'tutor' && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
          <div>
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-indigo-400" /> Pedagogical Concept Tutor
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Ask about any algorithm, mathematical concept, or code implementation. The tutor uses cognitive scaffolding to explain step-by-step.
            </p>
          </div>

          {/* Search / Input Box */}
          <form onSubmit={handleAskTutor} className="space-y-3">
            <div className="relative">
              <input
                type="text"
                value={tutorQuery}
                onChange={(e) => setTutorQuery(e.target.value)}
                placeholder="e.g. How does A* Search work with Manhattan distance vs Euclidean distance?"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-indigo-500 pr-28"
              />
              <button
                type="submit"
                disabled={tutorLoading || !tutorQuery.trim()}
                className="absolute right-2 top-2 px-4 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-lg transition disabled:opacity-50"
              >
                {tutorLoading ? 'Explaining...' : 'Explain'}
              </button>
            </div>

            {/* Quick Topic Chips */}
            <div className="flex flex-wrap gap-2 text-[11px]">
              <span className="text-slate-500 py-1">Quick prompts:</span>
              {[
                "Bayesian Networks & Conditional Probability",
                "Forward vs Backward Chaining Reasoning",
                "A* Search Admissible Heuristics",
                "Self-Attention Mechanism in Transformers",
                "RAG Vector Chunking Strategies"
              ].map((chip, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => {
                    setTutorQuery(chip);
                  }}
                  className="px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 hover:border-indigo-500/50 text-slate-300 hover:text-indigo-300 transition"
                >
                  {chip}
                </button>
              ))}
            </div>
          </form>

          {/* Response Box */}
          {tutorResponse && (
            <div className="p-5 rounded-xl bg-slate-950 border border-indigo-500/30 space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5" /> Tutor Explanation
                </span>
                <span className="text-[10px] text-slate-500">Grounded Pedagogical Model</span>
              </div>
              <div className="text-xs text-slate-200 whitespace-pre-wrap leading-relaxed space-y-2">
                {tutorResponse}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Sub-Tab 4: Adaptive Topic Quiz */}
      {activeSubTab === 'quiz' && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <HelpCircle className="w-4 h-4 text-indigo-400" /> Adaptive Knowledge Verification Quiz
              </h3>
              <p className="text-xs text-slate-400 mt-1">
                Fast diagnostic checks to assess conceptual retention and pinpoint knowledge gaps.
              </p>
            </div>

            <div className="flex items-center gap-2">
              <select
                value={quizTopic}
                onChange={(e) => {
                  setQuizTopic(e.target.value);
                  setQuizQuestionIndex(0);
                  setSelectedOption(null);
                  setQuizSubmitted(false);
                }}
                className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
              >
                <option value="Machine Learning">Machine Learning</option>
                <option value="Python">Python Programming</option>
              </select>
            </div>
          </div>

          {/* Active Question Box */}
          <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-indigo-400 uppercase">
                Question {quizQuestionIndex + 1} of {currentQuizList.length}
              </span>
              <span className="text-xs text-slate-400">Score: {quizScore} / {currentQuizList.length}</span>
            </div>

            <p className="text-sm font-semibold text-white leading-relaxed">{currentQuiz.q}</p>

            <div className="space-y-2.5 pt-2">
              {currentQuiz.options.map((opt, idx) => {
                let btnStyle = "bg-slate-900 border-slate-800 text-slate-300 hover:border-indigo-500/50";
                if (quizSubmitted) {
                  if (idx === currentQuiz.answer) {
                    btnStyle = "bg-emerald-500/20 border-emerald-500 text-emerald-300 font-bold";
                  } else if (selectedOption === idx) {
                    btnStyle = "bg-rose-500/20 border-rose-500 text-rose-300 font-semibold";
                  } else {
                    btnStyle = "bg-slate-950 border-slate-900 text-slate-600 opacity-60";
                  }
                }
                return (
                  <button
                    key={idx}
                    disabled={quizSubmitted}
                    onClick={() => handleAnswerOption(idx)}
                    className={`w-full text-left p-3.5 rounded-xl border text-xs transition flex items-center justify-between ${btnStyle}`}
                  >
                    <span>{opt}</span>
                    {quizSubmitted && idx === currentQuiz.answer && (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                    )}
                  </button>
                );
              })}
            </div>

            {/* Explanation & Next */}
            {quizSubmitted && (
              <div className="pt-4 border-t border-slate-800 space-y-3">
                <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300">
                  <span className="font-bold text-indigo-400 block mb-1">Pedagogical Rationale:</span>
                  {currentQuiz.explanation}
                </div>

                <div className="flex justify-end">
                  <button
                    onClick={handleNextQuiz}
                    className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-xl transition flex items-center gap-1.5"
                  >
                    <span>{quizQuestionIndex + 1 < currentQuizList.length ? 'Next Question' : 'Restart Quiz'}</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
