import React, { useState, useEffect } from 'react';
import {
  BookOpen, Sparkles, CheckCircle2, Play, ChevronRight, Clock, Target, Award,
  RefreshCw, HelpCircle, ArrowRight, Zap, Layers, ExternalLink, Flame, Check,
  Search, Code, Compass, ShieldAlert, ArrowLeft, MessageSquare, Send, BookMarked,
  Filter, CheckCircle, AlertTriangle
} from 'lucide-react';
import { api } from '../api';

export default function LearningAgentView({ currentUser, initialSubject, onOpenCareer, onOpenInterview }) {
  const targetUserId = currentUser?.user_id || currentUser?.id || "chitra_demo_user";
  
  // URL Param detection (e.g. /learning?subject=Python)
  const getSubjectFromUrl = () => {
    try {
      const params = new URLSearchParams(window.location.search);
      return params.get('subject') || null;
    } catch (e) {
      return null;
    }
  };

  // State Management
  const [subject, setSubject] = useState(initialSubject || getSubjectFromUrl() || "Python");
  const [categoryFilter, setCategoryFilter] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [customSubjectInput, setCustomSubjectInput] = useState("");
  
  // Customization Wizard state
  const [level, setLevel] = useState("Beginner");
  const [goal, setGoal] = useState("Career");
  const [customGoal, setCustomGoal] = useState("");
  const [dailyTime, setDailyTime] = useState("1 hour");
  const [daysPerWeek, setDaysPerWeek] = useState(5);
  const [deadline, setDeadline] = useState("6 weeks");
  const [isConfiguring, setIsConfiguring] = useState(false);

  // Active Plan & Topic view state
  const [planData, setPlanData] = useState(null);
  const [activeTopic, setActiveTopic] = useState(null);
  const [topicContent, setTopicContent] = useState(null);
  const [progressSummary, setProgressSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [topicLoading, setTopicLoading] = useState(false);

  // Quiz state inside Topic View
  const [userQuizAnswers, setUserQuizAnswers] = useState({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [quizScore, setQuizScore] = useState(0);

  // EduMind AI Tutor inside Topic View
  const [edumindQuery, setEdumindQuery] = useState("");
  const [edumindLoading, setEdumindLoading] = useState(false);
  const [edumindHistory, setEdumindHistory] = useState([]);

  // Load Subject Catalog & Active Plan
  const [subjectsList, setSubjectsList] = useState([]);

  useEffect(() => {
    const fetchSubjects = async () => {
      try {
        const subs = await api.getLearningSubjects();
        if (Array.isArray(subs)) setSubjectsList(subs);
      } catch (err) {
        console.error("Error fetching subjects catalog:", err);
      }
    };
    fetchSubjects();
  }, []);

  // Sync when initialSubject changes (e.g. coming from Career Agent "Learn This Skill")
  useEffect(() => {
    if (initialSubject && initialSubject !== subject) {
      setSubject(initialSubject);
      handleGeneratePlan(initialSubject);
    }
  }, [initialSubject]);

  // Load Active Plan & Progress on Mount or Subject Change
  const handleGeneratePlan = async (targetSubj = subject) => {
    setLoading(true);
    try {
      const planReq = {
        subject: targetSubj,
        level: level,
        goal: goal === "Custom" ? customGoal || "Career" : goal,
        daily_minutes: dailyTime === "30 minutes" ? 30 : dailyTime === "1 hour" ? 60 : dailyTime === "2 hours" ? 120 : dailyTime === "3 hours" ? 180 : 240,
        days_per_week: daysPerWeek,
        deadline: deadline
      };
      const plan = await api.createLearningPlan(planReq, targetUserId);
      setPlanData(plan);
      setIsConfiguring(false);
      
      // Also fetch progress summary
      const prog = await api.getLearningProgress(targetSubj, targetUserId);
      setProgressSummary(prog);
    } catch (err) {
      console.error("Error generating learning plan:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleGeneratePlan(subject);
  }, [subject, targetUserId]);

  // Select and Open Topic Detailed Screen
  const handleOpenTopic = async (topicItem) => {
    const topicName = typeof topicItem === 'string' ? topicItem : topicItem.title;
    setActiveTopic(topicName);
    setTopicLoading(true);
    setUserQuizAnswers({});
    setQuizSubmitted(false);
    setQuizScore(0);
    setEdumindHistory([]);

    try {
      const content = await api.getTopicContent(subject, topicName, level);
      setTopicContent(content);
    } catch (err) {
      console.error("Error fetching topic content:", err);
    } finally {
      setTopicLoading(false);
    }
  };

  // Mark Topic Complete & Record Progress in MongoDB Atlas
  const handleCompleteTopic = async () => {
    if (!activeTopic) return;
    try {
      const res = await api.recordTopicProgress(
        subject,
        activeTopic,
        "Completed",
        45,
        quizSubmitted ? quizScore : 5,
        targetUserId
      );
      // Refresh Progress Summary
      const updatedProg = await api.getLearningProgress(subject, targetUserId);
      setProgressSummary(updatedProg);
      
      // Update local plan topic status
      if (planData && planData.weeks) {
        const updatedWeeks = planData.weeks.map(week => ({
          ...week,
          topics: week.topics.map(t => t.title === activeTopic ? { ...t, status: "Completed" } : t)
        }));
        setPlanData({ ...planData, weeks: updatedWeeks });
      }
    } catch (err) {
      console.error("Error recording progress:", err);
    }
  };

  // Submit EduMind Doubt in Topic View
  const handleAskEduMind = async (customMessage = null, actionType = null) => {
    const query = customMessage || edumindQuery;
    if (!query.trim() && !actionType) return;
    
    setEdumindLoading(true);
    const userMsg = query || `Triggered action: ${actionType}`;
    
    // Add user message to thread
    setEdumindHistory(prev => [...prev, { sender: 'user', text: userMsg }]);
    if (!customMessage) setEdumindQuery("");

    try {
      const res = await api.askEduMindDoubt(
        query,
        subject,
        activeTopic || "Core Concepts",
        level,
        goal,
        actionType,
        targetUserId
      );

      setEdumindHistory(prev => [
        ...prev,
        {
          sender: 'edumind',
          text: res.response,
          actions: res.suggested_actions || []
        }
      ]);
    } catch (err) {
      console.error("Error asking EduMind:", err);
      setEdumindHistory(prev => [
        ...prev,
        {
          sender: 'edumind',
          text: "I encountered an issue connecting to the AI learning engine. Please try again."
        }
      ]);
    } finally {
      setEdumindLoading(false);
    }
  };

  // Quiz Option Click
  const handleSelectQuizOption = (qIdx, optIdx) => {
    if (quizSubmitted) return;
    setUserQuizAnswers(prev => ({ ...prev, [qIdx]: optIdx }));
  };

  // Submit Topic Quiz
  const handleSubmitQuiz = () => {
    if (!topicContent?.quiz) return;
    let score = 0;
    topicContent.quiz.forEach((q, idx) => {
      if (userQuizAnswers[idx] === q.answer_index) score += 1;
    });
    setQuizScore(score);
    setQuizSubmitted(true);
  };

  // Filtered Subjects List for Selection Screen
  const filteredSubjects = subjectsList.filter(s => {
    const matchesCategory = categoryFilter === "All" || s.category.toLowerCase() === categoryFilter.toLowerCase();
    const matchesSearch = s.name.toLowerCase().includes(searchQuery.toLowerCase()) || s.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="space-y-6">
      {/* 1. Header & Progress Stats Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-indigo-500/20 rounded-3xl p-6 sm:p-7 shadow-2xl relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-5 relative z-10">
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <span className="p-2 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/30">
                <BookOpen className="w-6 h-6" />
              </span>
              <div>
                <h1 className="text-xl sm:text-2xl font-black text-white flex items-center gap-2">
                  Learning Agent: <span className="text-indigo-400">{subject}</span>
                  <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/40">
                    {level}
                  </span>
                </h1>
                <p className="text-xs text-slate-400">
                  Personalized roadmap, daily schedules, verified references, coding practice & EduMind AI assistance.
                </p>
              </div>
            </div>
          </div>

          {/* Quick Stats & Controls */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center space-x-3 bg-slate-950/80 border border-slate-800 rounded-2xl px-4 py-2.5 text-xs">
              <div className="flex items-center space-x-1.5 text-amber-400 font-bold">
                <Flame className="w-4 h-4 fill-amber-400 text-amber-400 animate-pulse" />
                <span>{progressSummary?.streak_days || 3} Day Streak</span>
              </div>
              <div className="h-4 w-px bg-slate-800"></div>
              <div className="text-slate-300 font-semibold">
                <span className="text-emerald-400 font-bold">{progressSummary?.progress_percentage || 35}%</span> Progress
              </div>
            </div>

            <button
              onClick={() => setIsConfiguring(!isConfiguring)}
              className="px-4 py-2.5 rounded-xl bg-slate-850 hover:bg-slate-800 border border-slate-700 hover:border-indigo-500 text-xs font-semibold text-slate-200 transition"
            >
              {isConfiguring ? "View Roadmap" : "Customize Plan"}
            </button>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mt-5 pt-4 border-t border-slate-800/80 space-y-1.5">
          <div className="flex justify-between text-xs text-slate-400 font-medium">
            <span>
              {progressSummary?.total_topics_count || 12} Topics • <strong className="text-white">{progressSummary?.completed_count || 4} Completed</strong> • {progressSummary?.remaining_count || 8} Remaining
            </span>
            <span className="text-indigo-300 font-bold">{progressSummary?.progress_percentage || 35}%</span>
          </div>
          <div className="w-full bg-slate-950 h-2.5 rounded-full overflow-hidden border border-slate-800">
            <div
              className="bg-gradient-to-r from-indigo-500 via-teal-400 to-emerald-400 h-full rounded-full transition-all duration-500"
              style={{ width: `${progressSummary?.progress_percentage || 35}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* 2. SUBJECT SELECTION & CUSTOMIZATION MODAL / PANEL */}
      {isConfiguring && (
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl space-y-6 animate-fadeIn">
          <div className="flex items-center justify-between pb-4 border-b border-slate-800">
            <div>
              <h2 className="text-base font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <Target className="w-5 h-5 text-indigo-400" /> Configure Your Learning Path
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                Select any subject, set your current level, target goals, and available study hours.
              </p>
            </div>
            <button
              onClick={() => setIsConfiguring(false)}
              className="text-xs text-slate-400 hover:text-white px-3 py-1 bg-slate-950 border border-slate-800 rounded-lg"
            >
              Close
            </button>
          </div>

          {/* Subject Picker */}
          <div className="space-y-4">
            <label className="text-xs font-bold text-white uppercase tracking-wider block">
              1. What do you want to learn?
            </label>

            {/* Category Pills & Search */}
            <div className="flex flex-col sm:flex-row gap-3">
              <div className="relative flex-1">
                <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search programming languages, AI, web frameworks, tools..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2.5 text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex space-x-1.5 overflow-x-auto pb-1 sm:pb-0">
                {["All", "Programming", "Web Development", "Data & AI", "Cloud & DevOps"].map((cat) => (
                  <button
                    key={cat}
                    onClick={() => setCategoryFilter(cat)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-medium whitespace-nowrap transition ${
                      categoryFilter === cat
                        ? "bg-indigo-600 text-white"
                        : "bg-slate-950 text-slate-400 hover:text-slate-200 border border-slate-800"
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>

            {/* Subject Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-5 gap-3 max-h-56 overflow-y-auto pr-1">
              {filteredSubjects.map((s) => (
                <div
                  key={s.id}
                  onClick={() => setSubject(s.id)}
                  className={`p-3 rounded-2xl border cursor-pointer transition flex flex-col justify-between ${
                    subject === s.id
                      ? "bg-indigo-950/40 border-indigo-500 shadow-lg shadow-indigo-500/10"
                      : "bg-slate-950 border-slate-800/80 hover:border-slate-700"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xl">{s.icon || "📚"}</span>
                    {subject === s.id && <CheckCircle className="w-4 h-4 text-indigo-400" />}
                  </div>
                  <div className="mt-2">
                    <h4 className="text-xs font-bold text-white">{s.name}</h4>
                    <span className="text-[10px] text-slate-500">{s.category}</span>
                  </div>
                </div>
              ))}
            </div>

            {/* Custom Subject Entry */}
            <div className="flex items-center gap-2 pt-1">
              <input
                type="text"
                value={customSubjectInput}
                onChange={(e) => setCustomSubjectInput(e.target.value)}
                placeholder="Or enter custom subject (e.g. Rust, PyTorch, Kubernetes, Golang)..."
                className="bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-slate-200 flex-1 focus:outline-none focus:border-indigo-500"
              />
              <button
                onClick={() => {
                  if (customSubjectInput.trim()) {
                    setSubject(customSubjectInput.trim());
                    setCustomSubjectInput("");
                  }
                }}
                disabled={!customSubjectInput.trim()}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 disabled:opacity-50 text-slate-200 text-xs font-bold rounded-xl transition"
              >
                Set Custom
              </button>
            </div>
          </div>

          {/* Level, Goal & Time Configuration */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-5 pt-4 border-t border-slate-800 text-xs">
            {/* Level Selection */}
            <div className="space-y-2">
              <label className="text-slate-300 font-bold uppercase tracking-wider block">
                2. Current Skill Level
              </label>
              <div className="space-y-1.5">
                {["Complete Beginner", "Beginner", "Intermediate", "Advanced"].map((lvl) => (
                  <div
                    key={lvl}
                    onClick={() => setLevel(lvl)}
                    className={`p-2.5 rounded-xl border cursor-pointer transition flex items-center justify-between ${
                      level === lvl
                        ? "bg-indigo-950/40 border-indigo-500 text-white font-bold"
                        : "bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    <span>{lvl}</span>
                    {level === lvl && <Check className="w-3.5 h-3.5 text-indigo-400" />}
                  </div>
                ))}
              </div>
            </div>

            {/* Learning Goal */}
            <div className="space-y-2">
              <label className="text-slate-300 font-bold uppercase tracking-wider block">
                3. Learning Goal
              </label>
              <select
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-slate-200 focus:outline-none focus:border-indigo-500"
              >
                <option value="Career">Career Track Transition</option>
                <option value="Job Preparation">Job & Placement Preparation</option>
                <option value="College/Academic">College / Academic Exam</option>
                <option value="Internship">Internship Readiness</option>
                <option value="Project Development">Project Development</option>
                <option value="Interview Preparation">Interview Prep</option>
                <option value="Certification">Industry Certification</option>
              </select>

              <div className="pt-2">
                <label className="text-slate-400 block mb-1">Target Deadline</label>
                <select
                  value={deadline}
                  onChange={(e) => setDeadline(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-slate-200 focus:outline-none focus:border-indigo-500"
                >
                  <option value="2 weeks">2 Weeks (Intensive)</option>
                  <option value="4 weeks">1 Month (Standard)</option>
                  <option value="6 weeks">6 Weeks (Comprehensive)</option>
                  <option value="8 weeks">2 Months (Mastery)</option>
                </select>
              </div>
            </div>

            {/* Available Time */}
            <div className="space-y-2">
              <label className="text-slate-300 font-bold uppercase tracking-wider block">
                4. Study Commitment
              </label>
              <select
                value={dailyTime}
                onChange={(e) => setDailyTime(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-slate-200 focus:outline-none focus:border-indigo-500 mb-2"
              >
                <option value="30 minutes">30 Minutes / Day</option>
                <option value="1 hour">1 Hour / Day</option>
                <option value="2 hours">2 Hours / Day</option>
                <option value="3 hours">3 Hours / Day</option>
                <option value="4+ hours">4+ Hours / Day</option>
              </select>

              <label className="text-slate-400 block mb-1">Days Per Week</label>
              <div className="grid grid-cols-4 gap-1.5">
                {[3, 5, 6, 7].map((d) => (
                  <button
                    key={d}
                    type="button"
                    onClick={() => setDaysPerWeek(d)}
                    className={`py-2 rounded-xl text-xs font-bold border transition ${
                      daysPerWeek === d
                        ? "bg-indigo-600 text-white border-indigo-500"
                        : "bg-slate-950 text-slate-400 border-slate-800 hover:text-white"
                    }`}
                  >
                    {d} Days
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-slate-800">
            <button
              onClick={() => handleGeneratePlan(subject)}
              disabled={loading}
              className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white font-bold text-xs rounded-xl shadow-lg shadow-indigo-600/30 transition flex items-center gap-2"
            >
              {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Zap className="w-4 h-4" />}
              <span>Generate My Learning Plan</span>
            </button>
          </div>
        </div>
      )}

      {/* 3. MAIN WORKSPACE: DETAILED TOPIC VIEW OR ROADMAP */}
      {activeTopic ? (
        /* ========================================================================= */
        /* DETAILED SUBJECT TOPIC LEARNING SCREEN (e.g. /learning/python/variables)  */
        /* ========================================================================= */
        <div className="space-y-6 animate-fadeIn">
          {/* Top Bar with Back Button */}
          <div className="flex items-center justify-between bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg">
            <button
              onClick={() => setActiveTopic(null)}
              className="flex items-center space-x-2 text-xs font-semibold text-indigo-400 hover:text-indigo-300 transition"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back to {subject} Roadmap</span>
            </button>

            <div className="flex items-center space-x-2">
              <span className="text-xs text-slate-400">Current Topic:</span>
              <span className="text-xs font-bold text-white bg-slate-950 border border-slate-800 px-3 py-1 rounded-xl">
                {activeTopic}
              </span>
            </div>
          </div>

          {topicLoading || !topicContent ? (
            <div className="bg-slate-900 border border-slate-800 rounded-3xl p-16 text-center text-slate-400 space-y-3">
              <RefreshCw className="w-8 h-8 animate-spin mx-auto text-indigo-400" />
              <p className="text-sm font-semibold">Generating comprehensive pedagogical content for {activeTopic}...</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left 2 Cols: Content, Examples, Practice, Quiz & Resources */}
              <div className="lg:col-span-2 space-y-6">
                {/* 1. Simple Explanation */}
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
                  <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                    <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                      <BookMarked className="w-4 h-4 text-indigo-400" /> 1. Concept Intuition & Simple Explanation
                    </h3>
                    <span className="text-[10px] bg-indigo-500/10 text-indigo-300 border border-indigo-500/30 px-2.5 py-0.5 rounded-full font-bold">
                      {topicContent.level} Friendly
                    </span>
                  </div>
                  <p className="text-xs sm:text-sm text-slate-200 leading-relaxed whitespace-pre-line">
                    {topicContent.explanation}
                  </p>
                </div>

                {/* 2. Key Concepts */}
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
                  <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2 pb-3 border-b border-slate-800">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" /> 2. Core Takeaways & Concepts
                  </h3>
                  <ul className="space-y-2.5 text-xs text-slate-300">
                    {topicContent.key_concepts?.map((c, idx) => (
                      <li key={idx} className="flex items-start space-x-2.5 bg-slate-950 p-3 rounded-xl border border-slate-800/80">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 flex-shrink-0"></span>
                        <span>{c}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* 3. Code Example & Walkthrough */}
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
                  <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                    <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                      <Code className="w-4 h-4 text-teal-400" /> 3. Code Example & Syntax
                    </h3>
                    <span className="text-[10px] text-slate-500">Runnable {subject} snippet</span>
                  </div>
                  <pre className="p-4 rounded-2xl bg-slate-950 border border-slate-800 text-emerald-300 text-xs font-mono overflow-x-auto leading-relaxed">
                    <code>{topicContent.code_example}</code>
                  </pre>
                </div>

                {/* 4. Hands-on Practice Questions */}
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
                  <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2 pb-3 border-b border-slate-800">
                    <Zap className="w-4 h-4 text-amber-400" /> 4. Hands-On Practice Questions
                  </h3>
                  <div className="space-y-2.5 text-xs">
                    {topicContent.practice_questions?.map((pq, idx) => (
                      <div key={idx} className="p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                        <span className="text-[10px] uppercase font-bold text-amber-400">Exercise {idx + 1}</span>
                        <p className="text-slate-200">{pq}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* 5. 5-Question Diagnostic Quiz */}
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-5">
                  <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                    <div>
                      <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                        <HelpCircle className="w-4 h-4 text-indigo-400" /> 5. Quick Diagnostic Quiz (5 Questions)
                      </h3>
                      <p className="text-xs text-slate-400 mt-0.5">Test your understanding before marking this topic complete.</p>
                    </div>
                    {quizSubmitted && (
                      <span className={`text-xs font-bold px-3 py-1 rounded-xl border ${
                        quizScore >= 4 ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30" : "bg-amber-500/10 text-amber-400 border-amber-500/30"
                      }`}>
                        Score: {quizScore} / {topicContent.quiz?.length || 5} ({Math.round((quizScore / (topicContent.quiz?.length || 5)) * 100)}%)
                      </span>
                    )}
                  </div>

                  <div className="space-y-4">
                    {topicContent.quiz?.map((q, qIdx) => (
                      <div key={qIdx} className="p-4 bg-slate-950 border border-slate-800 rounded-2xl space-y-3">
                        <p className="text-xs font-semibold text-white">
                          <span className="text-indigo-400 mr-1.5 font-bold">Q{qIdx + 1}.</span>
                          {q.question}
                        </p>

                        <div className="space-y-2">
                          {q.options?.map((opt, optIdx) => {
                            let btnStyle = "bg-slate-900 border-slate-800 text-slate-300 hover:border-indigo-500/50";
                            if (quizSubmitted) {
                              if (optIdx === q.answer_index) {
                                btnStyle = "bg-emerald-500/20 border-emerald-500 text-emerald-300 font-bold";
                              } else if (userQuizAnswers[qIdx] === optIdx) {
                                btnStyle = "bg-rose-500/20 border-rose-500 text-rose-300 font-semibold";
                              } else {
                                btnStyle = "bg-slate-950 border-slate-900 text-slate-600 opacity-60";
                              }
                            } else if (userQuizAnswers[qIdx] === optIdx) {
                              btnStyle = "bg-indigo-600/30 border-indigo-500 text-white font-bold";
                            }

                            return (
                              <button
                                key={optIdx}
                                disabled={quizSubmitted}
                                onClick={() => handleSelectQuizOption(qIdx, optIdx)}
                                className={`w-full text-left p-3 rounded-xl border text-xs transition flex items-center justify-between ${btnStyle}`}
                              >
                                <span>{opt}</span>
                                {quizSubmitted && optIdx === q.answer_index && (
                                  <Check className="w-3.5 h-3.5 text-emerald-400" />
                                )}
                              </button>
                            );
                          })}
                        </div>

                        {quizSubmitted && (
                          <div className="p-3 bg-slate-900 rounded-xl text-[11px] text-slate-400 border border-slate-800">
                            <strong className="text-indigo-300">Explanation: </strong> {q.explanation}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>

                  {!quizSubmitted ? (
                    <div className="flex justify-end pt-2">
                      <button
                        onClick={handleSubmitQuiz}
                        disabled={Object.keys(userQuizAnswers).length === 0}
                        className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-bold text-xs rounded-xl shadow transition"
                      >
                        Submit Quiz Answers
                      </button>
                    </div>
                  ) : (
                    <div className="flex justify-between items-center pt-2">
                      <button
                        onClick={() => {
                          setUserQuizAnswers({});
                          setQuizSubmitted(false);
                          setQuizScore(0);
                        }}
                        className="text-xs text-slate-400 hover:text-white"
                      >
                        Retake Quiz
                      </button>
                      <button
                        onClick={handleCompleteTopic}
                        className="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs rounded-xl shadow transition flex items-center gap-1.5"
                      >
                        <CheckCircle className="w-4 h-4" />
                        <span>Complete Topic & Save Progress</span>
                      </button>
                    </div>
                  )}
                </div>

                {/* 6. Common Mistakes & Mini Task */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Common Mistakes */}
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-xl space-y-3">
                    <h3 className="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center gap-2">
                      <ShieldAlert className="w-4 h-4" /> 6. Common Beginner Mistakes
                    </h3>
                    <div className="space-y-2 text-xs text-slate-300">
                      {topicContent.common_mistakes?.map((m, idx) => (
                        <div key={idx} className="p-2.5 bg-slate-950 border border-rose-500/20 rounded-xl">
                          {m}
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Mini Task */}
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-xl space-y-3 flex flex-col justify-between">
                    <div>
                      <h3 className="text-xs font-bold text-teal-300 uppercase tracking-wider flex items-center gap-2">
                        <Target className="w-4 h-4 text-teal-400" /> 7. Practical Mini Task
                      </h3>
                      <p className="text-xs text-slate-200 mt-2 leading-relaxed">
                        {topicContent.mini_task}
                      </p>
                    </div>
                    <button
                      onClick={() => handleAskEduMind(`Help me plan and write the solution for this mini task: ${topicContent.mini_task}`)}
                      className="mt-3 w-full py-2 bg-slate-950 border border-teal-500/30 hover:border-teal-500 text-teal-300 text-xs font-semibold rounded-xl transition text-center"
                    >
                      Ask EduMind for Hints →
                    </button>
                  </div>
                </div>

                {/* 8. VERIFIED EXTERNAL LEARNING RESOURCES */}
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
                  <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                    <div>
                      <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                        <ExternalLink className="w-4 h-4 text-indigo-400" /> 8. Recommended External Resources & Docs
                      </h3>
                      <p className="text-xs text-slate-400 mt-0.5">Verified official documentation, tutorials, and interactive practice.</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                    {topicContent.resources?.map((res, idx) => (
                      <div key={idx} className="p-4 bg-slate-950 border border-slate-800 hover:border-indigo-500/50 rounded-2xl transition flex flex-col justify-between group space-y-2">
                        <div className="space-y-1">
                          <div className="flex items-center justify-between">
                            <span className="text-[10px] uppercase font-bold text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">
                              {res.type}
                            </span>
                            <span className="text-[10px] text-slate-500">{res.provider}</span>
                          </div>
                          <h4 className="text-xs font-bold text-white group-hover:text-indigo-300 transition">{res.title}</h4>
                          <p className="text-[11px] text-slate-400 leading-relaxed line-clamp-2">{res.description}</p>
                        </div>

                        <a
                          href={res.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="pt-2 flex items-center justify-between text-xs text-indigo-400 hover:text-indigo-300 font-bold border-t border-slate-900"
                        >
                          <span>Open Resource</span>
                          <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Complete Topic Action Button */}
                <div className="p-5 bg-gradient-to-r from-indigo-950/40 via-slate-900 to-emerald-950/40 border border-indigo-500/30 rounded-3xl flex flex-col sm:flex-row items-center justify-between gap-4 shadow-xl">
                  <div className="text-xs">
                    <span className="font-bold text-white block text-sm">Finished studying {activeTopic}?</span>
                    <span className="text-slate-400">Save progress to your MongoDB profile and unlock the next topic in the roadmap.</span>
                  </div>
                  <button
                    onClick={handleCompleteTopic}
                    className="px-6 py-3 bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-bold text-xs rounded-xl shadow-lg shadow-emerald-500/20 transition flex items-center gap-2 flex-shrink-0"
                  >
                    <CheckCircle className="w-4 h-4" />
                    <span>Mark as Completed</span>
                  </button>
                </div>
              </div>

              {/* Right Col: Embedded EduMind AI Learning Assistant */}
              <div className="space-y-6">
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-xl space-y-4 sticky top-20">
                  <div className="flex items-center space-x-2.5 pb-3 border-b border-slate-800">
                    <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-500 to-teal-400 flex items-center justify-center">
                      <Sparkles className="w-4 h-4 text-slate-950" />
                    </div>
                    <div>
                      <h3 className="text-xs font-bold text-white uppercase tracking-wider">EduMind AI Assistant</h3>
                      <p className="text-[10px] text-teal-400">Embedded Tutor for {activeTopic}</p>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex flex-wrap gap-1.5 text-[10px]">
                    {[
                      { label: "Explain Simpler", action: "explain_simpler" },
                      { label: "Give Example", action: "give_example" },
                      { label: "Show Code", action: "show_code" },
                      { label: "Give Practice", action: "give_practice" },
                      { label: "Quiz Me", action: "quiz_me" },
                      { label: "Summarize", action: "summarize" }
                    ].map((btn, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleAskEduMind(null, btn.action)}
                        disabled={edumindLoading}
                        className="px-2.5 py-1 bg-slate-950 border border-slate-800 hover:border-indigo-500/50 text-slate-300 hover:text-indigo-300 rounded-lg transition disabled:opacity-50"
                      >
                        {btn.label}
                      </button>
                    ))}
                  </div>

                  {/* Chat Conversation Thread */}
                  <div className="h-96 overflow-y-auto space-y-3 p-3 bg-slate-950 rounded-2xl border border-slate-800/80 text-xs">
                    {edumindHistory.length === 0 ? (
                      <div className="text-center text-slate-500 py-12 space-y-2">
                        <MessageSquare className="w-8 h-8 mx-auto text-slate-700" />
                        <p className="text-xs font-semibold text-slate-400">Ask EduMind anything about {activeTopic}!</p>
                        <p className="text-[11px] text-slate-600">e.g. "Explain with an analogy", "Why do we need this?", or "Give me code examples".</p>
                      </div>
                    ) : (
                      edumindHistory.map((msg, idx) => (
                        <div
                          key={idx}
                          className={`p-3 rounded-xl leading-relaxed whitespace-pre-line ${
                            msg.sender === 'user'
                              ? 'bg-indigo-600/20 border border-indigo-500/40 text-indigo-200 ml-4'
                              : 'bg-slate-900 border border-slate-800 text-slate-200 mr-2'
                          }`}
                        >
                          <span className="text-[10px] uppercase font-bold text-slate-500 block mb-1">
                            {msg.sender === 'user' ? 'You' : 'EduMind AI Tutor'}
                          </span>
                          {msg.text}
                        </div>
                      ))
                    )}
                    {edumindLoading && (
                      <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-400 flex items-center gap-2">
                        <RefreshCw className="w-3.5 h-3.5 animate-spin text-indigo-400" />
                        <span>EduMind is thinking...</span>
                      </div>
                    )}
                  </div>

                  {/* Input Form */}
                  <form
                    onSubmit={(e) => {
                      e.preventDefault();
                      handleAskEduMind();
                    }}
                    className="flex items-center gap-2 pt-1"
                  >
                    <input
                      type="text"
                      value={edumindQuery}
                      onChange={(e) => setEdumindQuery(e.target.value)}
                      placeholder={`Ask anything about ${activeTopic}...`}
                      className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 flex-1 focus:outline-none focus:border-indigo-500"
                    />
                    <button
                      type="submit"
                      disabled={edumindLoading || !edumindQuery.trim()}
                      className="p-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded-xl transition"
                    >
                      <Send className="w-4 h-4" />
                    </button>
                  </form>
                </div>
              </div>
            </div>
          )}
        </div>
      ) : (
        /* ========================================================================= */
        /* ROADMAP & SCHEDULE VIEW (Default)                                         */
        /* ========================================================================= */
        <div className="space-y-6">
          {/* Active Plan Overview & Action Ribbon */}
          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Layers className="w-5 h-5 text-indigo-400" /> {subject} Learning Roadmap ({level})
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Goal: <strong className="text-indigo-300">{goal}</strong> • Commitment: <strong>{dailyTime}/day</strong> ({daysPerWeek} days/week) • Target: <strong>{deadline}</strong>
              </p>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => setIsConfiguring(true)}
                className="px-4 py-2 bg-slate-950 border border-slate-800 hover:border-indigo-500 text-slate-200 text-xs font-semibold rounded-xl transition"
              >
                Change Subject
              </button>
              <button
                onClick={() => handleGeneratePlan(subject)}
                disabled={loading}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl transition flex items-center gap-1.5 shadow"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Regenerate Plan</span>
              </button>
            </div>
          </div>

          {/* Weekly Modules & Topic Cards */}
          {loading ? (
            <div className="bg-slate-900 border border-slate-800 rounded-3xl p-16 text-center text-slate-400 space-y-3">
              <RefreshCw className="w-8 h-8 animate-spin mx-auto text-indigo-400" />
              <p className="text-sm font-semibold">Generating your personalized {subject} schedule with A* heuristic sequencing...</p>
            </div>
          ) : planData?.weeks ? (
            <div className="space-y-5">
              {planData.weeks.map((week, wIdx) => (
                <div key={wIdx} className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
                  <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                    <div className="flex items-center space-x-3">
                      <span className="px-3 py-1 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 font-bold text-xs">
                        Week {week.week || wIdx + 1}
                      </span>
                      <div>
                        <h3 className="font-bold text-sm text-white">{week.title}</h3>
                        <p className="text-[11px] text-slate-400">{week.focus}</p>
                      </div>
                    </div>
                    <span className="text-xs text-slate-500">{week.topics?.length} Topics</span>
                  </div>

                  {/* Topic Cards Grid */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5 pt-1">
                    {week.topics?.map((top, tIdx) => {
                      const isDone = progressSummary?.completed_topics?.some(
                        ct => ct.toLowerCase().includes(top.title.toLowerCase()) || top.title.toLowerCase().includes(ct.toLowerCase())
                      );

                      return (
                        <div
                          key={tIdx}
                          onClick={() => handleOpenTopic(top)}
                          className={`p-4 rounded-2xl border cursor-pointer transition flex flex-col justify-between group space-y-2.5 ${
                            isDone
                              ? "bg-emerald-950/20 border-emerald-500/40 hover:border-emerald-500"
                              : "bg-slate-950 border-slate-800/80 hover:border-indigo-500/60"
                          }`}
                        >
                          <div className="flex items-start justify-between">
                            <span className="text-[10px] uppercase font-bold text-indigo-400">
                              Module {wIdx + 1}.{tIdx + 1}
                            </span>
                            {isDone ? (
                              <span className="flex items-center space-x-1 text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/30">
                                <Check className="w-3 h-3" />
                                <span>Completed</span>
                              </span>
                            ) : (
                              <span className="text-[10px] text-slate-500 flex items-center gap-1">
                                <Clock className="w-3 h-3" /> {top.estimated_min || 45}m
                              </span>
                            )}
                          </div>

                          <h4 className="text-xs font-bold text-white group-hover:text-indigo-300 transition leading-snug">
                            {top.title}
                          </h4>

                          <div className="flex items-center justify-between text-[11px] pt-1 text-slate-400 group-hover:text-indigo-400">
                            <span>{isDone ? "Review Concept" : "Start Learning"}</span>
                            <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-slate-900 border border-slate-800 rounded-3xl p-12 text-center text-slate-400">
              <p>Click "Generate Plan" to construct your tailored learning roadmap.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
