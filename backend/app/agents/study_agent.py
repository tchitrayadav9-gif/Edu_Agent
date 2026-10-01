"""
Study Agent Module.
Specialized agent for generating curriculum schedules, optimizing learning paths via A* Search,
and adapting progress for weak topic remediation.
"""

from typing import Dict, List, Any, Optional
from ..planning.study_planner import study_planner
from ..search.path_optimizer import path_optimizer
from ..database.mongodb import db_manager


class StudyAgent:
    """Specialized agent managing study planning and curriculum optimization."""
    
    def __init__(self):
        self.planner = study_planner
        self.optimizer = path_optimizer
        self.db = db_manager

    def generate_plan_for_student(
        self,
        user_id: str,
        career_goal: str,
        skills: Dict[str, int],
        weak_topics: List[str],
        daily_hours: float = 2.0,
        preferred_time: str = "Evening"
    ) -> Dict[str, Any]:
        """Generate tailored study plan and compute optimal curriculum search path."""
        # 1. Run A* search to determine optimal prerequisite curriculum path
        curriculum_search = self.optimizer.find_optimal_path(
            start_topic="Python Basics",
            goal_topic="AI Engineer Mastery",
            algorithm="a_star"
        )

        # 2. Generate detailed 30-day schedule
        plan = self.planner.generate_30_day_plan(
            user_id=user_id,
            career_goal=career_goal,
            skills=skills,
            weak_topics=weak_topics,
            daily_hours=daily_hours,
            preferred_time=preferred_time
        )
        plan["optimal_curriculum_path"] = curriculum_search

        # Persist to database
        self.db.study_plans.insert_one(plan)

        return {
            "agent_name": "Study Agent",
            "study_plan": plan,
            "curriculum_path": curriculum_search.get("path", []),
            "total_estimated_study_hours": plan.get("total_estimated_study_hours", 60.0)
        }


# Global study agent instance
study_agent = StudyAgent()
