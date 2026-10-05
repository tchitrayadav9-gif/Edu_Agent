import React, { useState, useEffect } from 'react';
import { Target, Sparkles, BookOpen, Clock, Brain, CheckCircle2, X, Sliders, AlertCircle, Compass } from 'lucide-react';
import { api } from '../api';

export default function GuidancePreferencesModal({ isOpen, onClose, currentUser, onProfileUpdated }) {
  const targetUserId = currentUser?.user_id || currentUser?.id || "chitra_demo_user";

  const [formData, setFormData] = useState({
    name: currentUser?.name || '',
    academic_year: currentUser?.academic_year || '2nd Year',
    branch: currentUser?.branch || 'Computer Science and Engineering',
    career_goal: currentUser?.career_goal || 'AI Engineer',
    skills: {
      Python: 80,
      SQL: 65,
      'Machine Learning': 40,
      'Data Structures': 70,
      Statistics: 45
    },
    weak_topics: ['Statistics', 'Deep Learning', 'System Design'],
    daily_hours: 2.0,
    preferred_time: 'Evening',
    learning_style: 'Hands-on projects & Code examples'
  });

  const [weakInput, setWeakInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setSuccess(false);
      // Load current profile from server
      const loadData = async () => {
        try {
          const prof = await api.getProfile(targetUserId);
          if (prof) {
            setFormData({
              name: prof.name || currentUser?.name || '',
              academic_year: prof.academic_year || '2nd Year',
              branch: prof.branch || 'Computer Science and Engineering',
              career_goal: prof.career_goal || 'AI Engineer',
              skills: prof.skills || { Python: 80, 'Machine Learning': 40, SQL: 60, Statistics: 45 },
              weak_topics: prof.weak_topics || ['Machine Learning', 'Statistics'],
              daily_hours: prof.study_preferences?.daily_hours || 2.0,
              preferred_time: prof.study_preferences?.preferred_time || 'Evening',
              learning_style: prof.study_preferences?.learning_style || 'Hands-on projects & Code examples'
            });
          }
        } catch (err) {
          console.debug('Failed to load profile for preferences modal, using cached.');
        }
      };
      loadData();
    }
  }, [isOpen, targetUserId, currentUser]);

  if (!isOpen) return null;

  const handleSkillChange = (skillName, val) => {
    setFormData((prev) => ({
      ...prev,
      skills: {
        ...prev.skills,
        [skillName]: parseInt(val, 10)
      }
    }));
  };

  const addWeakTopic = () => {
    if (!weakInput.trim()) return;
    if (!formData.weak_topics.includes(weakInput.trim())) {
      setFormData((prev) => ({
        ...prev,
        weak_topics: [...prev.weak_topics, weakInput.trim()]
      }));
    }
    setWeakInput('');
  };

  const removeWeakTopic = (topic) => {
    setFormData((prev) => ({
      ...prev,
      weak_topics: prev.weak_topics.filter((t) => t !== topic)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {
        name: formData.name.trim() || 'Student',
        academic_year: formData.academic_year,
        branch: formData.branch,
        career_goal: formData.career_goal,
        target_role: formData.career_goal,
        skills: formData.skills,
        weak_topics: formData.weak_topics,
        study_preferences: {
          daily_hours: parseFloat(formData.daily_hours),
          preferred_time: formData.preferred_time,
          learning_style: formData.learning_style
        }
      };

      await api.updateProfile(payload, targetUserId);

      // Save updated career goal & preference memories into long-term memory
      await api.createMemory({
        memory_type: 'career_goal',
        content: `Target Career Goal is ${formData.career_goal}.`,
        importance: 1.0,
        source: 'guidance_preferences'
      }, targetUserId);

      await api.createMemory({
        memory_type: 'preference',
        content: `Prefers studying during ${formData.preferred_time} (${formData.daily_hours} hrs/day) with ${formData.learning_style}.`,
        importance: 0.85,
        source: 'guidance_preferences'
      }, targetUserId);

      setSuccess(true);
      if (onProfileUpdated) {
        onProfileUpdated({
          ...currentUser,
          name: formData.name.trim() || currentUser?.name,
          academic_year: formData.academic_year,
          branch: formData.branch,
          career_goal: formData.career_goal
        });
      }
      setTimeout(() => {
        onClose();
      }, 700);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-2xl p-6 shadow-2xl relative my-6 max-h-[90vh] overflow-y-auto">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="flex items-center space-x-3 mb-5 pb-4 border-b border-slate-800">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-500 to-emerald-400 flex items-center justify-center text-slate-950 font-bold shadow-lg shadow-teal-500/20 shrink-0">
            <Sliders className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white tracking-tight">
              Personalized Guidance & Learning Preferences
            </h2>
            <p className="text-xs text-slate-400">
              Configure your academic details, target career track, and study preferences to calibrate the AI Agents.
            </p>
          </div>
        </div>

        {success && (
          <div className="mb-4 p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span>Preferences updated & saved to MongoDB Atlas cluster! Agents are calibrated.</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          {/* Section 1: Academic & Target Career */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="text-slate-400 font-semibold block mb-1">Full Name</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="e.g. Chitra Yadav"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200 focus:outline-none focus:border-teal-500"
              />
            </div>

            <div>
              <label className="text-slate-400 font-semibold block mb-1">Target Career Goal</label>
              <select
                value={formData.career_goal}
                onChange={(e) => setFormData({ ...formData, career_goal: e.target.value })}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200 focus:outline-none focus:border-teal-500"
              >
                <option value="AI Engineer">Artificial Intelligence Engineer</option>
                <option value="Machine Learning Engineer">Machine Learning Engineer</option>
                <option value="Data Scientist">Data Scientist & Analyst</option>
                <option value="Full Stack Developer">Full Stack Software Developer</option>
                <option value="Cloud & DevOps Engineer">Cloud & DevOps Engineer</option>
                <option value="Cybersecurity Analyst">Cybersecurity Analyst</option>
              </select>
            </div>

            <div>
              <label className="text-slate-400 font-semibold block mb-1">Academic Year / Status</label>
              <select
                value={formData.academic_year}
                onChange={(e) => setFormData({ ...formData, academic_year: e.target.value })}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200 focus:outline-none focus:border-teal-500"
              >
                <option value="1st Year">1st Year Undergraduate</option>
                <option value="2nd Year">2nd Year Undergraduate</option>
                <option value="3rd Year">3rd Year Undergraduate</option>
                <option value="4th Year">4th Year Undergraduate / Final Year</option>
                <option value="Postgraduate">Postgraduate / Masters / PhD</option>
                <option value="Self-Learner">Self-Learner / Career Switcher</option>
              </select>
            </div>

            <div>
              <label className="text-slate-400 font-semibold block mb-1">Major / Branch</label>
              <input
                type="text"
                value={formData.branch}
                onChange={(e) => setFormData({ ...formData, branch: e.target.value })}
                placeholder="e.g. Computer Science & Engineering"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200 focus:outline-none focus:border-teal-500"
              />
            </div>
          </div>

          {/* Section 2: Current Skill Proficiencies */}
          <div className="pt-2 border-t border-slate-800/80">
            <label className="text-slate-300 font-bold block mb-2">Current Skill Competencies (%)</label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {Object.entries(formData.skills).map(([skill, val]) => (
                <div key={skill} className="bg-slate-950/70 p-2.5 rounded-xl border border-slate-800 space-y-1">
                  <div className="flex justify-between items-center text-[11px]">
                    <span className="text-slate-300 font-semibold">{skill}</span>
                    <span className="text-teal-400 font-bold">{val}%</span>
                  </div>
                  <input
                    type="range"
                    min="10"
                    max="100"
                    step="5"
                    value={val}
                    onChange={(e) => handleSkillChange(skill, e.target.value)}
                    className="w-full accent-teal-400 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Section 3: Priority Guidance & Weak Topics */}
          <div className="pt-2 border-t border-slate-800/80">
            <label className="text-slate-300 font-bold block mb-1">Topics You Need Immediate Guidance On (Weak Areas)</label>
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                value={weakInput}
                onChange={(e) => setWeakInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addWeakTopic())}
                placeholder="e.g. Probability, Deep Learning, System Design, Backpropagation..."
                className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200 focus:outline-none focus:border-teal-500"
              />
              <button
                type="button"
                onClick={addWeakTopic}
                className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-teal-400 rounded-xl font-bold transition"
              >
                + Add Topic
              </button>
            </div>

            <div className="flex flex-wrap gap-1.5">
              {formData.weak_topics.map((topic, idx) => (
                <span
                  key={idx}
                  className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300 text-[11px]"
                >
                  <span>{topic}</span>
                  <button
                    type="button"
                    onClick={() => removeWeakTopic(topic)}
                    className="hover:text-white"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          </div>

          {/* Section 4: Study Habits & Schedule */}
          <div className="pt-2 border-t border-slate-800/80 grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label className="text-slate-400 font-semibold block mb-1">Daily Study Commitment</label>
              <select
                value={formData.daily_hours}
                onChange={(e) => setFormData({ ...formData, daily_hours: parseFloat(e.target.value) })}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-2.5 py-2 text-slate-200 focus:outline-none focus:border-teal-500"
              >
                <option value={1.0}>1.0 Hour / Day</option>
                <option value={1.5}>1.5 Hours / Day</option>
                <option value={2.0}>2.0 Hours / Day (Recommended)</option>
                <option value={3.0}>3.0 Hours / Day (Intensive)</option>
                <option value={4.0}>4.0+ Hours / Day (Full-Time)</option>
              </select>
            </div>

            <div>
              <label className="text-slate-400 font-semibold block mb-1">Preferred Time of Day</label>
              <select
                value={formData.preferred_time}
                onChange={(e) => setFormData({ ...formData, preferred_time: e.target.value })}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-2.5 py-2 text-slate-200 focus:outline-none focus:border-teal-500"
              >
                <option value="Morning">Morning (6:00 AM - 10:00 AM)</option>
                <option value="Afternoon">Afternoon (1:00 PM - 5:00 PM)</option>
                <option value="Evening">Evening (6:00 PM - 10:00 PM)</option>
                <option value="Night">Late Night (10:00 PM - 2:00 AM)</option>
              </select>
            </div>

            <div>
              <label className="text-slate-400 font-semibold block mb-1">Learning Approach</label>
              <select
                value={formData.learning_style}
                onChange={(e) => setFormData({ ...formData, learning_style: e.target.value })}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-2.5 py-2 text-slate-200 focus:outline-none focus:border-teal-500"
              >
                <option value="Hands-on projects & Code examples">Hands-on Code & Projects</option>
                <option value="Structured step-by-step roadmap">Structured Step-by-Step</option>
                <option value="Math & conceptual derivations">Theory & Mathematical Derivations</option>
              </select>
            </div>
          </div>

          {/* Submit Button */}
          <div className="pt-3">
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-teal-500 to-emerald-400 hover:from-teal-600 hover:to-emerald-500 text-slate-950 font-bold py-2.5 px-4 rounded-xl shadow-lg shadow-teal-500/20 transition disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {loading ? (
                <span>Saving to Database Cluster...</span>
              ) : (
                <>
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Save Guidance Preferences & Calibrate Agent</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
