"""
Student Service module.
Manages student profiles, career targets, skill proficiency mappings, and statistics.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from ..database.mongodb import db_manager
from ..database.models import StudentProfile
from ..knowledge.knowledge_graph import knowledge_graph


class StudentService:
    """Business logic for student profiles and progress."""
    
    def __init__(self):
        self.db = db_manager

    def get_or_create_profile(self, user_id: str, default_name: str = "Chitra") -> Dict[str, Any]:
        """Fetch profile from DB or initialize default educational profile."""
        profile = self.db.student_profiles.find_one({"user_id": user_id})
        if not profile:
            profile = {
                "user_id": user_id,
                "name": default_name,
                "academic_year": "2nd Year",
                "branch": "Computer Science and Engineering",
                "career_goal": "AI Engineer",
                "target_role": "Artificial Intelligence Engineer",
                "skills": {
                    "Python": 85,
                    "SQL": 70,
                    "Machine Learning": 40,
                    "Data Structures": 75,
                    "Statistics": 45
                },
                "weak_topics": ["Statistics", "Deep Learning", "System Design"],
                "completed_topics": ["Python Basics", "Object Oriented Programming", "SQL Fundamentals"],
                "learning_progress": {
                    "Python": 85,
                    "Machine Learning": 40,
                    "Data Science": 55,
                    "Algorithms": 65
                },
                "study_preferences": {
                    "preferred_time": "Evening",
                    "daily_hours": 2.0,
                    "learning_style": "Hands-on projects & Code examples"
                },
                "interview_scores": {
                    "Python": 8.0,
                    "Machine Learning": 4.5,
                    "AI Fundamentals": 6.0
                },
                "updated_at": datetime.utcnow().isoformat()
            }
            self.db.student_profiles.insert_one(profile)

        # Sync with Knowledge Graph
        knowledge_graph.sync_student_state(
            student_id=user_id,
            student_name=profile.get("name", "Student"),
            career_goal=profile.get("career_goal", "AI Engineer"),
            skills=profile.get("skills", {}),
            weak_topics=profile.get("weak_topics", []),
            learning_progress=profile.get("learning_progress", {})
        )

        return profile

    def update_profile(self, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update student profile fields."""
        update_data["updated_at"] = datetime.utcnow().isoformat()
        self.db.student_profiles.update_one(
            {"user_id": user_id},
            {"$set": update_data},
            upsert=True
        )
        return self.get_or_create_profile(user_id)

    def get_dashboard_data(self, user_id: str) -> Dict[str, Any]:
        """Compile unified dashboard summary data."""
        profile = self.get_or_create_profile(user_id)
        memories = self.db.memory.find({"user_id": user_id})
        documents = self.db.documents.find({"user_id": user_id})
        study_plans = self.db.study_plans.find({"user_id": user_id})
        recent_chats = self.db.chat_history.find({"user_id": user_id})

        # Calculate overall skill average
        skills = profile.get("skills", {})
        avg_skill = sum(skills.values()) / max(1, len(skills)) if skills else 0.0

        # Calculate average interview score
        interview_scores = profile.get("interview_scores", {})
        avg_interview = sum(interview_scores.values()) / max(1, len(interview_scores)) if interview_scores else 0.0

        return {
            "student_name": profile.get("name", "Student"),
            "academic_year": profile.get("academic_year", "2nd Year"),
            "branch": profile.get("branch", "CSE"),
            "career_goal": profile.get("career_goal", "AI Engineer"),
            "skills": skills,
            "average_skill_score": round(avg_skill, 1),
            "average_interview_score": round(avg_interview, 1),
            "interview_scores": interview_scores,
            "weak_skills": profile.get("weak_topics", []),
            "completed_topics": profile.get("completed_topics", []),
            "learning_progress": profile.get("learning_progress", {}),
            "recommended_next_skill": profile.get("weak_topics", ["Machine Learning"])[0] if profile.get("weak_topics") else "Deep Learning",
            "memory_count": len(memories),
            "document_count": len(documents),
            "study_plan_active": len(study_plans) > 0,
            "recent_conversations_count": len(recent_chats),
            "study_preferences": profile.get("study_preferences", {})
        }


# Global student service instance
student_service = StudentService()
