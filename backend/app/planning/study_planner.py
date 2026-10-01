"""
Study Planner Module.
Creates tailored 30-day and multi-week curriculum schedules integrating student daily hours,
weak topics, target career goal, and prerequisite mastery order.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid


class StudyPlanGenerator:
    """Generates granular personalized study roadmaps and schedule calendars."""
    
    def generate_30_day_plan(
        self,
        user_id: str,
        career_goal: str = "AI Engineer",
        skills: Optional[Dict[str, int]] = None,
        weak_topics: Optional[List[str]] = None,
        daily_hours: float = 2.0,
        preferred_time: str = "Evening"
    ) -> Dict[str, Any]:
        skills = skills or {"Python": 85, "SQL": 70, "Machine Learning": 40}
        weak_topics = weak_topics or ["Statistics", "Deep Learning"]

        plan_id = str(uuid.uuid4())
        total_days = 30
        
        # Define module blocks based on career and weak areas
        modules = []
        
        # Priority 1: Address Weak Areas if in AI Engineer track
        if any("stat" in w.lower() for w in weak_topics):
            modules.append({
                "module_name": "Mathematics & Probability Foundation",
                "days": 5,
                "focus": "Probability distributions, Bayes Theorem, Linear Algebra for ML, Matrix operations",
                "milestone": "Solve 15 probability problems & implement Bayes Theorem in Python",
                "is_weakness_remediation": True
            })

        if skills.get("Machine Learning", 0) < 60 or any("machine" in w.lower() or "ml" in w.lower() for w in weak_topics):
            modules.append({
                "module_name": "Machine Learning Core & Scikit-Learn",
                "days": 8,
                "focus": "Supervised/Unsupervised algorithms, Loss functions, Cross-validation, Hyperparameter tuning",
                "milestone": "Build end-to-end ML prediction pipeline with evaluation metrics",
                "is_weakness_remediation": True
            })

        if any("deep" in w.lower() or "dl" in w.lower() for w in weak_topics) or career_goal.lower().find("ai") != -1:
            modules.append({
                "module_name": "Deep Learning & PyTorch Architectures",
                "days": 8,
                "focus": "CNNs, RNNs, Transformers, Backpropagation, Attention mechanisms",
                "milestone": "Train PyTorch vision & text classification models",
                "is_weakness_remediation": "Deep Learning" in weak_topics
            })

        modules.append({
            "module_name": "Generative AI, LLMs & Agent Systems",
            "days": 6,
            "focus": "Prompt Engineering, RAG architectures, Vector embeddings, CrewAI & LangGraph multi-agent orchestration",
            "milestone": "Deploy a complete multi-agent RAG workflow with tool calling",
            "is_weakness_remediation": False
        })

        modules.append({
            "module_name": "Mock Interviews & System Design Capstone",
            "days": 3,
            "focus": "Technical interview problem solving, System design for AI systems, Resume project defense",
            "milestone": "Pass 2 full mock technical interviews with score >= 8.0/10",
            "is_weakness_remediation": False
        })

        # Generate day-by-day schedule
        schedule = []
        current_day = 1
        start_date = datetime.utcnow()

        for mod in modules:
            mod_name = mod["module_name"]
            mod_days = mod["days"]
            for d in range(mod_days):
                if current_day > total_days:
                    break
                
                day_date = start_date + timedelta(days=current_day - 1)
                schedule.append({
                    "day": current_day,
                    "date": day_date.strftime("%Y-%m-%d"),
                    "module": mod_name,
                    "focus_topic": f"{mod_name} - Part {d + 1}",
                    "allocated_hours": daily_hours,
                    "time_slot": f"{preferred_time} ({daily_hours} hrs)",
                    "action_item": f"Study {mod['focus'].split(',')[d % len(mod['focus'].split(','))].strip()}",
                    "status": "pending"
                })
                current_day += 1

        return {
            "plan_id": plan_id,
            "user_id": user_id,
            "career_goal": career_goal,
            "duration_days": total_days,
            "daily_commitment_hours": daily_hours,
            "preferred_time": preferred_time,
            "total_estimated_study_hours": total_days * daily_hours,
            "modules": modules,
            "schedule": schedule,
            "weak_topics_addressed": [m["module_name"] for m in modules if m.get("is_weakness_remediation")],
            "created_at": datetime.utcnow().isoformat()
        }


# Global study plan generator
study_planner = StudyPlanGenerator()
