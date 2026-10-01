import React, { useState } from 'react';
import Navbar from './components/Navbar';
import ChatView from './components/ChatView';
import DashboardView from './components/DashboardView';
import MemoryManagerView from './components/MemoryManagerView';
import RagVaultView from './components/RagVaultView';
import MockInterviewView from './components/MockInterviewView';
import AlgorithmVisualizerView from './components/AlgorithmVisualizerView';
import ReasoningView from './components/ReasoningView';
import EvaluationDashboardView from './components/EvaluationDashboardView';
import McpSettingsView from './components/McpSettingsView';

export default function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [provider, setProvider] = useState('auto');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        provider={provider}
        setProvider={setProvider}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
        {activeTab === 'chat' && <ChatView provider={provider} />}
        {activeTab === 'dashboard' && <DashboardView />}
        {activeTab === 'memory' && <MemoryManagerView />}
        {activeTab === 'rag' && <RagVaultView />}
        {activeTab === 'interview' && <MockInterviewView />}
        {activeTab === 'search' && <AlgorithmVisualizerView />}
        {activeTab === 'reasoning' && <ReasoningView />}
        {activeTab === 'evaluation' && <EvaluationDashboardView />}
        {activeTab === 'settings' && <McpSettingsView />}
      </main>

      <footer className="py-4 text-center text-xs text-slate-500 border-t border-slate-900">
        EduAgent • Python-Powered Memory-Enabled Multi-Agent RAG System
      </footer>
    </div>
  );
}
