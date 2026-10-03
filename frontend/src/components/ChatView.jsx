import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, Database, FileText, Wrench, RefreshCw } from 'lucide-react';
import { api } from '../api';
import AgentActivityPanel from './AgentActivityPanel';

export default function ChatView({ provider, currentUser }) {
  const studentName = currentUser?.name || currentUser?.username || "Chitra";
  const studentYear = currentUser?.academic_year || "2nd Year";
  const studentBranch = currentUser?.branch || "CSE";
  const targetUserId = currentUser?.user_id || currentUser?.id || "chitra_demo_user";

  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: `Hello ${studentName}! I am **EduMind Agent**, your personalized learning & career AI assistant. I have loaded your academic profile (${studentYear} ${studentBranch}) and active memory context.\n\nHow can I help you today? You can ask me to optimize your study roadmap, evaluate your mock interview answers, analyze skill gaps for AI Engineering, or query your uploaded course notes via RAG.`,
      activities: [`✓ Loaded student profile (${studentName} - ${studentYear})`, "✓ Checked long-term memory", "✓ Initialized EduMind Agent Coordinator"],
      memories: [],
      documents: [],
      agents: ["EduMind Coordinator"]
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentActivities, setCurrentActivities] = useState([]);
  const [currentMemories, setCurrentMemories] = useState([]);
  const [currentDocs, setCurrentDocs] = useState([]);
  const [currentAgents, setCurrentAgents] = useState([]);
  const [executionTime, setExecutionTime] = useState(0);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const quickPrompts = [
    `My name is ${studentName}. I want to become an AI Engineer. I know Python but weak in Machine Learning.`,
    "What should I learn next?",
    "Explain A* search according to my notes.",
    "Create a 30-day plan for AI Engineering.",
    "Test me for an AI interview.",
    "What should I improve based on my previous interview?"
  ];

  const handleSend = async (textToSend) => {
    const query = textToSend || input;
    if (!query.trim() || loading) return;

    const userMsg = { role: 'user', content: query };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await api.chat(query, "conv_" + Date.now(), provider, targetUserId);

      
      setCurrentActivities(res.activities || []);
      setCurrentMemories(res.memories_retrieved || []);
      setCurrentDocs(res.documents_retrieved || []);
      setCurrentAgents(res.agents_invoked || []);
      setExecutionTime(res.execution_time_ms || 0);

      const botMsg = {
        role: 'assistant',
        content: res.response,
        activities: res.activities,
        memories: res.memories_retrieved,
        documents: res.documents_retrieved,
        agents: res.agents_invoked,
        tools: res.tools_executed,
        memorySaved: res.memory_saved,
        timeMs: res.execution_time_ms
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: "⚠️ I encountered an error communicating with the backend. Please ensure the backend server is running on port 8000.",
          activities: ["✕ Connection error to localhost:8000"]
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-140px)]">
      {/* Chat Conversation Column */}
      <div className="lg:col-span-2 flex flex-col bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, index) => {
            const isUser = msg.role === 'user';
            return (
              <div key={index} className={`flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
                  isUser ? 'bg-teal-500 text-slate-950 font-bold' : 'bg-slate-800 text-teal-400 border border-slate-700'
                }`}>
                  {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </div>

                <div className={`max-w-[85%] rounded-2xl p-4 text-sm leading-relaxed ${
                  isUser
                    ? 'bg-teal-600 text-white rounded-tr-none'
                    : 'bg-slate-950/80 border border-slate-800/80 text-slate-200 rounded-tl-none shadow-md'
                }`}>
                  <div className="whitespace-pre-wrap font-sans">
                    {msg.content}
                  </div>

                  {/* Badges / Citations for Assistant */}
                  {!isUser && (msg.memories?.length > 0 || msg.documents?.length > 0 || msg.agents?.length > 0) && (
                    <div className="mt-3 pt-2 border-t border-slate-800/80 flex flex-wrap gap-1.5 text-[11px]">
                      {msg.memories?.length > 0 && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded bg-teal-500/10 text-teal-300 border border-teal-500/20">
                          <Database className="w-3 h-3 mr-1" /> {msg.memories.length} Memory Used
                        </span>
                      )}
                      {msg.documents?.length > 0 && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                          <FileText className="w-3 h-3 mr-1" /> RAG: {msg.documents[0].filename}
                        </span>
                      )}
                      {msg.agents?.length > 0 && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">
                          <Sparkles className="w-3 h-3 mr-1" /> {msg.agents.join(', ')}
                        </span>
                      )}
                      {msg.memorySaved && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20">
                          ✓ Saved to Long-Term Memory
                        </span>
                      )}
                    </div>
                  )}
                </div>
              </div>
            );
          })}

          {loading && (
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 rounded-lg bg-slate-800 text-teal-400 flex items-center justify-center border border-slate-700 shrink-0">
                <Bot className="w-4 h-4 animate-spin" />
              </div>
              <div className="p-3.5 rounded-2xl rounded-tl-none bg-slate-950/80 border border-slate-800 text-slate-400 text-xs flex items-center space-x-2">
                <span className="inline-block w-2 h-2 rounded-full bg-teal-400 animate-pulse"></span>
                <span>EduMind Agent is evaluating context, checking memory, and coordinating sub-agents...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Demo Prompts Chips */}
        <div className="px-4 py-2 border-t border-slate-800/60 bg-slate-950/40 flex items-center space-x-2 overflow-x-auto scrollbar-none">
          <span className="text-[11px] text-slate-500 font-semibold uppercase tracking-wider shrink-0 flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-teal-400" /> Demo:
          </span>
          {quickPrompts.map((prompt, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(prompt)}
              className="text-xs text-slate-300 bg-slate-800/80 hover:bg-slate-700/80 px-2.5 py-1 rounded-full border border-slate-700/50 whitespace-nowrap transition-colors"
            >
              {prompt.length > 38 ? prompt.substring(0, 38) + "..." : prompt}
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <div className="p-3 bg-slate-950 border-t border-slate-800 flex items-center space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask EduMind Agent (e.g. 'What should I learn next?', 'Create 30-day plan')..."
            className="flex-1 bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
          />
          <button
            onClick={() => handleSend()}
            disabled={loading || !input.trim()}
            className="p-2.5 bg-teal-500 hover:bg-teal-600 disabled:opacity-50 disabled:cursor-not-allowed text-slate-950 font-bold rounded-xl transition-colors shadow-lg shadow-teal-500/20"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Right Column: Live Agent Activity Telemetry Panel */}
      <div className="hidden lg:block h-full">
        <AgentActivityPanel
          activities={currentActivities}
          memoriesRetrieved={currentMemories}
          documentsRetrieved={currentDocs}
          agentsInvoked={currentAgents}
          executionTimeMs={executionTime}
        />
      </div>
    </div>
  );
}
