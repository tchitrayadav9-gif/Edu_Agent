import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import AuthModal from './components/AuthModal';
import ChatView from './components/ChatView';
import DashboardView from './components/DashboardView';
import MemoryManagerView from './components/MemoryManagerView';
import RagVaultView from './components/RagVaultView';
import MockInterviewView from './components/MockInterviewView';
import AlgorithmVisualizerView from './components/AlgorithmVisualizerView';
import ReasoningView from './components/ReasoningView';
import EvaluationDashboardView from './components/EvaluationDashboardView';
import McpSettingsView from './components/McpSettingsView';
import { getStoredAuth, clearStoredAuth, api } from './api';

export default function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [provider, setProvider] = useState('auto');
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [currentUser, setCurrentUser] = useState(() => {
    const { user } = getStoredAuth();
    return user || {
      id: 'chitra_demo_user',
      user_id: 'chitra_demo_user',
      username: 'chitra',
      name: 'Chitra',
      academic_year: '2nd Year',
      branch: 'Computer Science and Engineering',
      career_goal: 'AI Engineer'
    };
  });

  // Verify stored session on mount
  useEffect(() => {
    const verifySession = async () => {
      try {
        const profile = await api.getMe();
        if (profile) {
          setCurrentUser(profile);
        }
      } catch (err) {
        console.debug('No active token session verified, using default/cached profile.');
      }
    };
    verifySession();
  }, []);

  const handleAuthSuccess = (userObj) => {
    setCurrentUser(userObj);
  };

  const handleLogout = () => {
    clearStoredAuth();
    setCurrentUser({
      id: 'chitra_demo_user',
      user_id: 'chitra_demo_user',
      username: 'chitra',
      name: 'Chitra',
      academic_year: '2nd Year',
      branch: 'CSE',
      career_goal: 'AI Engineer'
    });
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        provider={provider}
        setProvider={setProvider}
        currentUser={currentUser}
        onOpenAuth={() => setAuthModalOpen(true)}
        onLogout={handleLogout}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
        {activeTab === 'chat' && <ChatView provider={provider} currentUser={currentUser} />}
        {activeTab === 'dashboard' && <DashboardView currentUser={currentUser} />}
        {activeTab === 'memory' && <MemoryManagerView currentUser={currentUser} />}
        {activeTab === 'rag' && <RagVaultView currentUser={currentUser} />}
        {activeTab === 'interview' && <MockInterviewView currentUser={currentUser} />}
        {activeTab === 'search' && <AlgorithmVisualizerView />}
        {activeTab === 'reasoning' && <ReasoningView />}
        {activeTab === 'evaluation' && <EvaluationDashboardView />}
        {activeTab === 'settings' && <McpSettingsView />}
      </main>

      {/* Auth Registration & Login Modal */}
      <AuthModal
        isOpen={authModalOpen}
        onClose={() => setAuthModalOpen(false)}
        onAuthSuccess={handleAuthSuccess}
      />

      <footer className="py-4 text-center text-xs text-slate-500 border-t border-slate-900">
        EduAgent • Python-Powered Memory-Enabled Multi-Agent RAG System
      </footer>
    </div>
  );
}
