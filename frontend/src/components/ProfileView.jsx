import React, { useState, useEffect } from 'react';
import { User, BookOpen, Compass, Award, Database, Save, CheckCircle, RefreshCw, Sliders, Shield, Plus, X } from 'lucide-react';
import { api } from '../api';

export default function ProfileView({ currentUser, onProfileUpdated }) {
  const targetUserId = currentUser?.user_id || currentUser?.id || "chitra_demo_user";
  const [loading, setLoading] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Form state
  const [fullName, setFullName] = useState(currentUser?.name || currentUser?.username || 'Chitra');
  const [educationStatus, setEducationStatus] = useState(currentUser?.academic_year || '2nd Year B.Tech');
  const [college, setCollege] = useState(currentUser?.college || 'Engineering Institute of Technology');
  const [degree, setDegree] = useState(currentUser?.degree || 'Bachelor of Technology (B.Tech)');
  const [branch, setBranch] = useState(currentUser?.branch || 'Computer Science and Engineering');
  const [cgpa, setCgpa] = useState(currentUser?.cgpa || '8.8');
  const [careerGoal, setCareerGoal] = useState(currentUser?.career_goal || 'AI Engineer');
  const [studyStyle, setStudyStyle] = useState(currentUser?.study_style || 'Practical & Code-First');
  const [dailyHours, setDailyHours] = useState(currentUser?.daily_hours || 2.5);

  const [skills, setSkills] = useState({
    "Python": 85,
    "Data Structures": 75,
    "Machine Learning": 70,
    "Deep Learning": 45,
    "SQL": 80,
    "System Design": 60,
    "Cloud & Docker": 50
  });

  const [weakTopics, setWeakTopics] = useState(["Statistics", "Deep Learning Backpropagation"]);
  const [newWeakTopic, setNewWeakTopic] = useState('');

  // Fetch student profile on mount
  useEffect(() => {
    const loadProfile = async () => {
      try {
        const profile = await api.getProfile(targetUserId);
        if (profile) {
          if (profile.name) setFullName(profile.name);
          if (profile.academic_year) setEducationStatus(profile.academic_year);
          if (profile.branch) setBranch(profile.branch);
          if (profile.career_goal) setCareerGoal(profile.career_goal);
          if (profile.skills) setSkills(profile.skills);
          if (profile.weak_topics) setWeakTopics(profile.weak_topics);
          if (profile.cgpa) setCgpa(profile.cgpa);
        }
      } catch (err) {
        console.error("Error loading profile:", err);
      }
    };
    loadProfile();
  }, [targetUserId]);

  const handleSkillChange = (skill, val) => {
    setSkills(prev => ({ ...prev, [skill]: parseInt(val) }));
  };

  const handleAddWeakTopic = (e) => {
    e.preventDefault();
    if (!newWeakTopic.trim()) return;
    if (!weakTopics.includes(newWeakTopic.trim())) {
      setWeakTopics(prev => [...prev, newWeakTopic.trim()]);
    }
    setNewWeakTopic('');
  };

  const handleRemoveWeakTopic = (topicToRemove) => {
    setWeakTopics(prev => prev.filter(t => t !== topicToRemove));
  };

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSaveSuccess(false);

    const payload = {
      name: fullName,
      academic_year: educationStatus,
      college: college,
      degree: degree,
      branch: branch,
      cgpa: cgpa,
      career_goal: careerGoal,
      study_style: studyStyle,
      daily_hours: parseFloat(dailyHours),
      skills: skills,
      weak_topics: weakTopics
    };

    try {
      const res = await api.updateProfile(payload, targetUserId);
      setSaveSuccess(true);
      if (onProfileUpdated) {
        onProfileUpdated({
          ...currentUser,
          ...payload
        });
      }
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err) {
      console.error("Error saving profile:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Hero Header */}
      <div className="bg-gradient-to-r from-slate-900 via-teal-950/30 to-slate-900 border border-teal-500/20 rounded-2xl p-6 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <span className="p-2.5 rounded-xl bg-teal-500/10 text-teal-400 border border-teal-500/30">
              <User className="w-7 h-7" />
            </span>
            <div>
              <h1 className="text-xl font-bold text-white flex items-center gap-2">
                Student Profile & Cognitive Memory
                <span className="text-xs bg-teal-500/20 text-teal-300 border border-teal-500/40 px-2 py-0.5 rounded-full font-medium">
                  MongoDB Atlas
                </span>
              </h1>
              <p className="text-xs text-slate-400">
                Your profile parameters configure Bayesian suitability, A* study roadmaps, and adaptive mock interview difficulty.
              </p>
            </div>
          </div>

          <button
            onClick={handleSaveProfile}
            disabled={loading}
            className="px-6 py-2.5 bg-gradient-to-r from-teal-500 to-emerald-400 hover:from-teal-600 hover:to-emerald-500 text-slate-950 font-bold text-xs rounded-xl shadow-lg shadow-teal-500/20 transition flex items-center gap-2"
          >
            {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
            <span>Save Profile Changes</span>
          </button>
        </div>

        {saveSuccess && (
          <div className="mt-4 p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-emerald-300 text-xs flex items-center gap-2 animate-fadeIn">
            <CheckCircle className="w-4 h-4 text-emerald-400" />
            <span>Profile successfully synced to MongoDB Atlas and shared across all AI agents!</span>
          </div>
        )}
      </div>

      <form onSubmit={handleSaveProfile} className="space-y-6">
        {/* Academic & Personal Details */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2 pb-3 border-b border-slate-800">
            <BookOpen className="w-4 h-4 text-teal-400" /> Academic & Personal Background
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div>
              <label className="text-slate-400 block mb-1 font-medium">Full Name</label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-slate-200 focus:outline-none focus:border-teal-500"
              />
            </div>

            <div>
              <label className="text-slate-400 block mb-1 font-medium">Education Status / Academic Year</label>
              <select
                value={educationStatus}
                onChange={(e) => setEducationStatus(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-slate-200 focus:outline-none focus:border-teal-500"
              >
                <option value="1st Year B.Tech">1st Year B.Tech</option>
                <option value="2nd Year B.Tech">2nd Year B.Tech</option>
                <option value="3rd Year B.Tech">3rd Year B.Tech</option>
                <option value="4th Year B.Tech">4th Year B.Tech</option>
                <option value="B.Tech Graduate">B.Tech Graduate</option>
                <option value="Other Graduate">Other Graduate / MCA / MSc</option>
                <option value="Working Professional">Working Professional</option>
              </select>
            </div>

            <div>
              <label className="text-slate-400 block mb-1 font-medium">Branch / Specialization</label>
              <input
                type="text"
                value={branch}
                onChange={(e) => setBranch(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-slate-200 focus:outline-none focus:border-teal-500"
              />
            </div>

            <div>
              <label className="text-slate-400 block mb-1 font-medium">College / University</label>
              <input
                type="text"
                value={college}
                onChange={(e) => setCollege(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-slate-200 focus:outline-none focus:border-teal-500"
              />
            </div>

            <div>
              <label className="text-slate-400 block mb-1 font-medium">Degree Program</label>
              <input
                type="text"
                value={degree}
                onChange={(e) => setDegree(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-slate-200 focus:outline-none focus:border-teal-500"
              />
            </div>

            <div>
              <label className="text-slate-400 block mb-1 font-medium">Current CGPA / Percentage</label>
              <input
                type="text"
                value={cgpa}
                onChange={(e) => setCgpa(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-slate-200 focus:outline-none focus:border-teal-500"
              />
            </div>
          </div>
        </div>

        {/* Career & Learning Preferences */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2 pb-3 border-b border-slate-800">
            <Compass className="w-4 h-4 text-emerald-400" /> Career Target & Study Preferences
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div>
              <label className="text-slate-400 block mb-1 font-medium">Primary Target Career</label>
              <select
                value={careerGoal}
                onChange={(e) => setCareerGoal(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-slate-200 focus:outline-none focus:border-teal-500"
              >
                <option value="AI Engineer">AI Engineer</option>
                <option value="Data Scientist">Data Scientist</option>
                <option value="Machine Learning Engineer">MLOps / ML Engineer</option>
                <option value="Software Engineer">Software Engineer (Backend/Full Stack)</option>
              </select>
            </div>

            <div>
              <label className="text-slate-400 block mb-1 font-medium">Preferred Learning Style</label>
              <select
                value={studyStyle}
                onChange={(e) => setStudyStyle(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-slate-200 focus:outline-none focus:border-teal-500"
              >
                <option value="Practical & Code-First">Practical & Code-First</option>
                <option value="Theoretical & First-Principles">Theoretical & First-Principles</option>
                <option value="Project-Oriented">Project & Portfolio Oriented</option>
                <option value="Interview-Cracking Focus">Fast Interview-Cracking Focus</option>
              </select>
            </div>

            <div>
              <label className="text-slate-400 block mb-1 font-medium">Available Daily Study (Hours)</label>
              <input
                type="number"
                step="0.5"
                min="0.5"
                max="12"
                value={dailyHours}
                onChange={(e) => setDailyHours(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-slate-200 focus:outline-none focus:border-teal-500"
              />
            </div>
          </div>
        </div>

        {/* Technical Skills Competency Sliders */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Sliders className="w-4 h-4 text-indigo-400" /> Technical Skill Proficiencies (0 - 100%)
            </h3>
            <span className="text-xs text-slate-500">Slide to calibrate agent baseline</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {Object.entries(skills).map(([skill, score]) => (
              <div key={skill} className="space-y-1.5 p-3.5 bg-slate-950 rounded-xl border border-slate-800">
                <div className="flex justify-between text-xs font-semibold">
                  <span className="text-slate-200">{skill}</span>
                  <span className={score >= 75 ? 'text-emerald-400' : score >= 50 ? 'text-amber-400' : 'text-rose-400'}>
                    {score}%
                  </span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={score}
                  onChange={(e) => handleSkillChange(skill, e.target.value)}
                  className="w-full accent-teal-500"
                />
              </div>
            ))}
          </div>
        </div>

        {/* Weak Topics Tag Manager */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2 pb-3 border-b border-slate-800">
            <Shield className="w-4 h-4 text-amber-400" /> Identified Weak Topics for Agent Priority Focus
          </h3>

          <div className="flex flex-wrap gap-2">
            {weakTopics.map((topic, idx) => (
              <span
                key={idx}
                className="px-3 py-1.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-medium flex items-center gap-2"
              >
                <span>{topic}</span>
                <button
                  type="button"
                  onClick={() => handleRemoveWeakTopic(topic)}
                  className="text-amber-400 hover:text-amber-200"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </span>
            ))}
          </div>

          {/* Add Tag */}
          <div className="flex items-center gap-2 pt-2">
            <input
              type="text"
              value={newWeakTopic}
              onChange={(e) => setNewWeakTopic(e.target.value)}
              placeholder="Add another weak area (e.g. Dynamic Programming, Graph Neural Networks)..."
              className="bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-xs text-slate-200 flex-1 focus:outline-none focus:border-teal-500"
            />
            <button
              type="button"
              onClick={handleAddWeakTopic}
              className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs rounded-xl transition flex items-center gap-1.5"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Add Topic</span>
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
