import React, { useState, useEffect } from 'react';
import { Settings, Cpu, Wrench, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react';
import { api } from '../api';

export default function McpSettingsView() {
  const [mcpTools, setMcpTools] = useState([]);
  const [ollamaStatus, setOllamaStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchStatus = async () => {
    setLoading(true);
    try {
      const [toolsRes, ollamaRes] = await Promise.all([
        api.getMcpTools(),
        api.getOllamaStatus()
      ]);
      setMcpTools(toolsRes.tools || []);
      setOllamaStatus(ollamaRes);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Settings className="w-5 h-5 text-teal-400" /> Model Context Protocol (MCP) & Local Ollama Runtime
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Standardized MCP JSON-RPC 2.0 tool registry and local LLM runtime management.
          </p>
        </div>

        <button
          onClick={fetchStatus}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-200 border border-slate-700 transition"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-teal-400' : ''}`} />
          <span>Refresh Runtime Status</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Ollama Local LLM Status */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
              <Cpu className="w-4 h-4 text-teal-400" /> Local Ollama Server Status
            </h3>
            {ollamaStatus?.is_running ? (
              <span className="flex items-center text-xs text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded border border-emerald-500/30">
                <CheckCircle className="w-3.5 h-3.5 mr-1" /> Active
              </span>
            ) : (
              <span className="flex items-center text-xs text-amber-400 bg-amber-500/10 px-2.5 py-0.5 rounded border border-amber-500/30">
                <AlertCircle className="w-3.5 h-3.5 mr-1" /> Standby (Auto-Fallback)
              </span>
            )}
          </div>

          <div className="mt-4 space-y-3 text-xs">
            <div className="flex justify-between text-slate-400">
              <span>Endpoint:</span>
              <span className="text-slate-200 font-mono">{ollamaStatus?.base_url || 'http://localhost:11434'}</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Selected Model:</span>
              <span className="text-teal-400 font-bold">{ollamaStatus?.selected_model || 'llama3:latest'}</span>
            </div>

            {ollamaStatus?.setup_instructions && (
              <div className="mt-4 p-3 rounded-lg bg-slate-950 border border-slate-800 text-[11px] text-slate-400 whitespace-pre-wrap leading-relaxed">
                <span className="font-bold text-slate-200 block mb-1">Local Ollama Setup:</span>
                {ollamaStatus.setup_instructions}
              </div>
            )}
          </div>
        </div>

        {/* MCP Tool Registry */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow">
          <h3 className="text-xs font-bold text-white uppercase tracking-wider mb-3 flex items-center gap-1.5">
            <Wrench className="w-4 h-4 text-teal-400" /> Exposed MCP Tools ({mcpTools.length})
          </h3>
          <div className="space-y-2.5 max-h-80 overflow-y-auto pr-1 scrollbar-none">
            {mcpTools.map((tool, idx) => (
              <div key={idx} className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-xs space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-teal-400 font-mono">{tool.name}()</span>
                  <span className="text-[10px] bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">JSON-RPC 2.0</span>
                </div>
                <p className="text-slate-300 text-[11px]">{tool.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
