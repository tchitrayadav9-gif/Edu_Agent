import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import AuthModal from './components/AuthModal';
import DashboardView from './components/DashboardView';
import LearningAgentView from './components/LearningAgentView';
import CareerAgentView from './components/CareerAgentView';
import MockInterviewView from './components/MockInterviewView';
import ChatView from './components/ChatView';
import RagVaultView from './components/RagVaultView';
import MemoryManagerView from './components/MemoryManagerView';
import AiLabsView from './components/AiLabsView';
import ProfileView from './components/ProfileView';
import GuidancePreferencesModal from './components/GuidancePreferencesModal';
import { getStoredAuth, clearStoredAuth, api } from './api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [provider, setProvider] = useState('auto');
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [preferencesModalOpen, setPreferencesModalOpen] = useState(false);
  const [currentUser, setCurrentUser] = useState(() => {
    const { user } = getStoredAuth();
    return user || {
      id: 'chitra_demo_user',
      user_id: 'chitra_demo_user',
      username: 'chitra',
      name: 'Chitra',
      academic_year: '2nd Year B.Tech',
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
    // After sign-in/registration, prompt to setup/verify guidance preferences
    setTimeout(() => {
      setPreferencesModalOpen(true);
    }, 400);
  };

  const handleProfileUpdated = (updatedUser) => {
    setCurrentUser(updatedUser);
  };

  const handleLogout = () => {
    clearStoredAuth();
    setCurrentUser({
      id: 'chitra_demo_user',
      user_id: 'chitra_demo_user',
      username: 'chitra',
      name: 'Chitra',
      academic_year: '2nd Year B.Tech',
      branch: 'Computer Science and Engineering',
      career_goal: 'AI Engineer'
    });
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-teal-500/30 selection:text-teal-200">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        provider={provider}
        setProvider={setProvider}
        currentUser={currentUser}
        onOpenAuth={() => setAuthModalOpen(true)}
        onOpenPreferences={() => setPreferencesModalOpen(true)}
        onLogout={handleLogout}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
        {activeTab === 'dashboard' && (
          <DashboardView
            currentUser={currentUser}
            onNavigate={setActiveTab}
          />
        )}
        {activeTab === 'learning' && (
          <LearningAgentView
            currentUser={currentUser}
            onOpenInterview={() => setActiveTab('interview')}
            onOpenCareer={() => setActiveTab('career')}
          />
        )}
        {activeTab === 'career' && (
          <CareerAgentView
            currentUser={currentUser}
            onOpenLearning={() => setActiveTab('learning')}
            onOpenInterview={() => setActiveTab('interview')}
          />
        )}
        {activeTab === 'interview' && (
          <MockInterviewView
            currentUser={currentUser}
            onOpenLearning={() => setActiveTab('learning')}
          />
        )}
        {activeTab === 'chat' && (
          <ChatView
            provider={provider}
            currentUser={currentUser}
            onOpenPreferences={() => setPreferencesModalOpen(true)}
          />
        )}
        {activeTab === 'rag' && <RagVaultView currentUser={currentUser} />}
        {activeTab === 'memory' && <MemoryManagerView currentUser={currentUser} />}
        {activeTab === 'labs' && <AiLabsView />}
        {activeTab === 'profile' && (
          <ProfileView
            currentUser={currentUser}
            onProfileUpdated={handleProfileUpdated}
          />
        )}
      </main>

      {/* Auth Registration & Login Modal */}
      <AuthModal
        isOpen={authModalOpen}
        onClose={() => setAuthModalOpen(false)}
        onAuthSuccess={handleAuthSuccess}
      />

      {/* Guidance Preferences & Profile Setup Modal */}
      <GuidancePreferencesModal
        isOpen={preferencesModalOpen}
        onClose={() => setPreferencesModalOpen(false)}
        currentUser={currentUser}
        onProfileUpdated={handleProfileUpdated}
      />

      <footer className="py-6 text-center text-xs text-slate-500 border-t border-slate-900 flex flex-col sm:flex-row items-center justify-between max-w-7xl mx-auto px-4 w-full gap-2">
        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
          <span>EduAgent Platform • Connected to MongoDB Atlas</span>
        </div>
        <div>
          Multi-Agent System with Learning, Career Guidance & Mock Interview Engines
        </div>
      </footer>
    </div>
  );
}
