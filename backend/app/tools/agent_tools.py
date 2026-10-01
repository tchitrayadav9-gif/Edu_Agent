"""
Function Calling & Agent Tools Module for EduAgent.
Exposes callable Python tools for profile querying, document searching, study planning,
interview questions, learning path search, logical inference, Bayesian analysis, and memory persistence.
"""

from typing import Dict, List, Any, Optional
import json
import logging
from ..database.mongodb import db_manager
from ..memory.long_term_memory import long_term_memory
from ..memory.short_term_memory import short_term_memory
from ..rag.rag_pipeline import rag_pipeline
from ..planning.study_planner import study_planner
from ..search.path_optimizer import path_optimizer
from ..reasoning.forward_chaining import forward_chaining_engine
from ..uncertainty.bayesian_network import bayesian_career_network

logger = logging.getLogger("edumind.tools")


def get_student_profile(user_id: str) -> Dict[str, Any]:
    """Retrieve full student profile including skills, branch, academic year, and goals."""
    profile = db_manager.student_profiles.find_one({"user_id": user_id})
    if not profile:
        profile = {
            "user_id": user_id,
            "name": "Chitra",
            "academic_year": "2nd Year",
            "branch": "Computer Science and Engineering",
            "career_goal": "AI Engineer",
            "skills": {"Python": 85, "SQL": 70, "Machine Learning": 40, "Data Structures": 75, "Statistics": 45},
            "weak_topics": ["Statistics", "Deep Learning"],
            "completed_topics": ["Python Basics", "Object Oriented Programming"],
            "learning_progress": {"Python": 85, "Machine Learning": 40},
            "study_preferences": {"preferred_time": "Evening", "daily_hours": 2.0},
            "interview_scores": {"Python": 8.0, "Machine Learning": 4.5}
        }
        db_manager.student_profiles.insert_one(profile)
    return profile


def get_student_skills(user_id: str) -> Dict[str, int]:
    """Get dictionary of current student skills and numerical mastery levels."""
    profile = get_student_profile(user_id)
    return profile.get("skills", {})


def get_learning_progress(user_id: str) -> Dict[str, int]:
    """Get topic completion progress percentages for the student."""
    profile = get_student_profile(user_id)
    return profile.get("learning_progress", {})


def get_career_goal(user_id: str) -> str:
    """Retrieve current declared career goal of student."""
    # Check long-term memory first for newest update
    memories = long_term_memory.get_memories_by_type(user_id, "career_goal")
    if memories:
        meta_goal = memories[-1].get("metadata", {}).get("career_goal")
        if meta_goal:
            return meta_goal
    profile = get_student_profile(user_id)
    return profile.get("career_goal", "AI Engineer")


def get_chat_history(user_id: str, conversation_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve previous conversation logs for the user."""
    query = {"user_id": user_id}
    if conversation_id:
        query["conversation_id"] = conversation_id
    return db_manager.chat_history.find(query)


def search_documents(query: str, user_id: Optional[str] = None, top_k: int = 3) -> Dict[str, Any]:
    """Query uploaded student notes and textbooks via RAG pipeline."""
    return rag_pipeline.retrieve_context(query=query, user_id=user_id, top_k=top_k)


def generate_study_plan(user_id: str, career_goal: Optional[str] = None, daily_hours: float = 2.0, preferred_time: str = "Evening") -> Dict[str, Any]:
    """Generate and store an optimized 30-day curriculum study plan."""
    profile = get_student_profile(user_id)
    goal = career_goal or profile.get("career_goal", "AI Engineer")
    plan = study_planner.generate_30_day_plan(
        user_id=user_id,
        career_goal=goal,
        skills=profile.get("skills"),
        weak_topics=profile.get("weak_topics"),
        daily_hours=daily_hours,
        preferred_time=preferred_time
    )
    db_manager.study_plans.insert_one(plan)
    return plan


def get_interview_questions(topic: str = "Machine Learning", difficulty: str = "Medium") -> List[Dict[str, Any]]:
    """Fetch high-yield adaptive mock interview questions for a given topic."""
    sample_pool = [
        {
            "question_id": "q101",
            "topic": "Machine Learning",
            "difficulty": "Medium",
            "question": "Explain the difference between L1 (Lasso) and L2 (Ridge) Regularization and why L1 drives coefficients to zero.",
            "expected_keywords": ["Lasso", "Ridge", "sparsity", "diamond constraint", "L1 norm", "feature selection"],
            "sample_answer": "L1 uses the absolute value penalty leading to diamond corner intersections at zero, producing sparse models."
        },
        {
            "question_id": "q102",
            "topic": "Python",
            "difficulty": "Medium",
            "question": "How do Python generators differ from regular functions, and what is the internal role of the yield keyword?",
            "expected_keywords": ["yield", "iterator", "lazy evaluation", "memory efficiency", "__next__"],
            "sample_answer": "Generators maintain their execution state between yield calls, producing values lazily without loading the entire sequence into RAM."
        },
        {
            "question_id": "q103",
            "topic": "AI Fundamentals",
            "difficulty": "Hard",
            "question": "What is the mathematical condition for a heuristic to be admissible and consistent in A* search?",
            "expected_keywords": ["admissible", "consistent", "triangle inequality", "h(n) <= h*(n)", "monotonic"],
            "sample_answer": "Admissibility requires h(n) <= h*(n) (never overestimating). Consistency requires h(n) <= c(n,a,n') + h(n') (satisfying the triangle inequality)."
        }
    ]
    matched = [q for q in sample_pool if topic.lower() in q["topic"].lower() or topic.lower() == "all"]
    return matched if matched else sample_pool


def update_learning_progress(user_id: str, topic: str, progress: int) -> Dict[str, Any]:
    """Update student learning progress percentage for a topic."""
    profile = get_student_profile(user_id)
    lp = profile.get("learning_progress", {})
    lp[topic] = max(0, min(100, int(progress)))
    db_manager.student_profiles.update_one(
        {"user_id": user_id},
        {"$set": {"learning_progress": lp}}
    )
    return {"user_id": user_id, "topic": topic, "updated_progress": lp[topic]}


def save_memory(user_id: str, memory_type: str, content: str, importance: float = 0.8) -> Dict[str, Any]:
    """Explicitly save a persistent long-term memory fact."""
    return long_term_memory.save_memory(
        user_id=user_id,
        memory_type=memory_type,
        content=content,
        importance=importance,
        source="explicit_agent_tool"
    )


def run_classical_search(start_topic: str, goal_topic: str, algorithm: str = "a_star") -> Dict[str, Any]:
    """Run classical AI graph search to find optimal curriculum path."""
    return path_optimizer.find_optimal_path(start_topic=start_topic, goal_topic=goal_topic, algorithm=algorithm)


def run_bayesian_career_analysis(user_id: str) -> Dict[str, Any]:
    """Compute Bayesian career suitability probability rankings for student."""
    profile = get_student_profile(user_id)
    return bayesian_career_network.calculate_career_probabilities(
        student_skills=profile.get("skills", {}),
        weak_topics=profile.get("weak_topics", []),
        career_interest=profile.get("career_goal")
    )


def run_logical_inference(facts: Dict[str, Any]) -> Dict[str, Any]:
    """Execute forward chaining logical inference over student facts."""
    return forward_chaining_engine.infer(initial_facts=facts)


# Registry of available agent tools
TOOL_REGISTRY = {
    "get_student_profile": get_student_profile,
    "get_student_skills": get_student_skills,
    "get_learning_progress": get_learning_progress,
    "get_career_goal": get_career_goal,
    "get_chat_history": get_chat_history,
    "search_documents": search_documents,
    "generate_study_plan": generate_study_plan,
    "get_interview_questions": get_interview_questions,
    "update_learning_progress": update_learning_progress,
    "save_memory": save_memory,
    "run_classical_search": run_classical_search,
    "run_bayesian_career_analysis": run_bayesian_career_analysis,
    "run_logical_inference": run_logical_inference
}
