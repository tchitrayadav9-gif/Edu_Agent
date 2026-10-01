"""
Career Agent Module.
Specialized agent for career recommendations, skill-gap analysis, Bayesian suitability, and career roadmaps.
"""

from typing import Dict, List, Any, Optional
from ..uncertainty.bayesian_network import bayesian_career_network
from ..reasoning.forward_chaining import forward_chaining_engine
from ..llm.llm_factory import llm_factory
from ..llm.prompt_templates import CAREER_AGENT_PROMPT


class CareerAgent:
    """Specialized agent analyzing career trajectories and required competencies."""
    
    def __init__(self):
        self.bayesian = bayesian_career_network
        self.reasoner = forward_chaining_engine
        self.llm = llm_factory

    def analyze_career_path(
        self,
        user_id: str,
        target_role: str,
        current_skills: Dict[str, int],
        weak_topics: List[str]
    ) -> Dict[str, Any]:
        """Perform comprehensive skill gap analysis and Bayesian suitability ranking."""
        # 1. Bayesian suitability calculation
        bayesian_results = self.bayesian.calculate_career_probabilities(
            student_skills=current_skills,
            weak_topics=weak_topics,
            career_interest=target_role
        )

        # 2. Forward Chaining Logical Inference
        facts = {
            "Target_Career": target_role,
            "Python": "Strong" if current_skills.get("Python", 0) >= 75 else "Developing",
            "Machine Learning": "Weak" if any("ml" in w.lower() or "machine" in w.lower() for w in weak_topics) or current_skills.get("Machine Learning", 0) < 50 else "Strong",
            "Statistics": "Weak" if any("stat" in w.lower() for w in weak_topics) or current_skills.get("Statistics", 0) < 50 else "Strong",
            "Data Structures": "Strong" if current_skills.get("Data Structures", 0) >= 70 else "Developing"
        }
        logical_inference = self.reasoner.infer(facts)

        # 3. Identify specific skill gaps
        standard_role_requirements = {
            "AI Engineer": {"Python": 85, "Machine Learning": 80, "Deep Learning": 75, "Statistics": 70, "Data Structures": 70},
            "Data Scientist": {"Python": 80, "SQL": 85, "Statistics": 85, "Machine Learning": 75, "Data Visualization": 75},
            "Machine Learning Engineer": {"Python": 85, "Machine Learning": 85, "Deep Learning": 80, "System Design": 75},
            "Software Engineer": {"Python": 85, "Data Structures": 85, "System Design": 80, "SQL": 75}
        }
        reqs = standard_role_requirements.get(target_role, standard_role_requirements["AI Engineer"])
        
        gaps = []
        for req_skill, target_score in reqs.items():
            curr_score = current_skills.get(req_skill, 0)
            if curr_score < target_score:
                gaps.append({
                    "skill": req_skill,
                    "current_level": curr_score,
                    "target_level": target_score,
                    "gap_delta": target_score - curr_score,
                    "is_weak_topic": any(req_skill.lower() in w.lower() for w in weak_topics)
                })

        # Sort gaps by gap_delta descending
        gaps.sort(key=lambda x: x["gap_delta"], reverse=True)

        return {
            "agent_name": "Career Agent",
            "target_role": target_role,
            "bayesian_suitability": bayesian_results,
            "skill_gaps": gaps,
            "logical_reasoning": logical_inference,
            "recommended_focus": gaps[0]["skill"] if gaps else "Interview Prep"
        }


# Global career agent instance
career_agent = CareerAgent()
