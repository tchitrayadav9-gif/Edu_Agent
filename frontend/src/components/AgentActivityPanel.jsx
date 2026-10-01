import React from 'react';
import { Activity, CheckCircle2, Cpu, Database, FileText, Wrench, Users, Clock } from 'lucide-react';

export default function AgentActivityPanel({ activities = [], memoriesRetrieved = [], documentsRetrieved = [], agentsInvoked = [], executionTimeMs = 0 }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col h-full shadow-lg">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <div className="p-1.5 rounded-lg bg-teal-500/10 text-teal-400 border border-teal-500/20">
            <Activity className="w-4 h-4 animate-pulse" />
          </div>
          <div>
            <h3 className="text-xs font-bold text-white uppercase tracking-wider">Agent Execution Telemetry</h3>
            <p className="text-[11px] text-slate-400">Live Cognitive Agent Activity Stream</p>
          </div>
        </div>
        {executionTimeMs > 0 && (
          <span className="flex items-center text-[10px] text-slate-400 bg-slate-950 px-2 py-1 rounded border border-slate-800">
            <Clock className="w-3 h-3 mr-1 text-teal-400" />
            {executionTimeMs} ms
          </span>
        )}
      </div>

      <div className="flex-1 overflow-y-auto mt-3 space-y-2 pr-1 scrollbar-none">
        {activities.length === 0 ? (
          <div className="h-40 flex flex-col items-center justify-center text-center p-4 text-slate-500">
            <Cpu className="w-8 h-8 mb-2 stroke-1 text-slate-600" />
            <p className="text-xs">Agent is standby.</p>
            <p className="text-[11px] text-slate-600">Send a query to observe memory, tools, and sub-agent coordination.</p>
          </div>
        ) : (
          activities.map((act, index) => (
            <div key={index} className="flex items-start space-x-2 text-xs text-slate-300 p-2 rounded-lg bg-slate-950/60 border border-slate-800/60">
              <CheckCircle2 className="w-3.5 h-3.5 text-teal-400 mt-0.5 shrink-0" />
              <span className="leading-tight">{act}</span>
            </div>
          ))
        )}
      </div>

      {/* Badges / Metrics Footer */}
      <div className="pt-3 mt-3 border-t border-slate-800 grid grid-cols-3 gap-2 text-center text-[10px]">
        <div className="p-2 rounded bg-slate-950 border border-slate-800/80">
          <span className="text-slate-400 block flex items-center justify-center gap-1">
            <Database className="w-3 h-3 text-teal-400" /> Memories
          </span>
          <span className="text-white font-bold text-xs">{memoriesRetrieved.length}</span>
        </div>
        <div className="p-2 rounded bg-slate-950 border border-slate-800/80">
          <span className="text-slate-400 block flex items-center justify-center gap-1">
            <FileText className="w-3 h-3 text-emerald-400" /> Docs (RAG)
          </span>
          <span className="text-white font-bold text-xs">{documentsRetrieved.length}</span>
        </div>
        <div className="p-2 rounded bg-slate-950 border border-slate-800/80">
          <span className="text-slate-400 block flex items-center justify-center gap-1">
            <Users className="w-3 h-3 text-cyan-400" /> Sub-Agents
          </span>
          <span className="text-white font-bold text-xs">{agentsInvoked.length}</span>
        </div>
      </div>
    </div>
  );
}
