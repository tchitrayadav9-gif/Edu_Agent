"""
CrewAI Multi-Agent Collaboration Manager.
Defines specialized autonomous agents, role definitions, goals, and collaborative crew execution.
"""

from typing import Dict, List, Any, Optional
import logging
from .career_agent import career_agent
from .study_agent import study_agent
from .interview_agent import interview_agent
from .research_agent import research_agent
from .rag_agent import rag_agent

logger = logging.getLogger("edumind.crew")


class CrewAgentDefinition:
    def __init__(self, role: str, goal: str, backstory: str):
        self.role = role
        self.goal = goal
        self.backstory = backstory


class CrewTaskDefinition:
    def __init__(self, description: str, expected_output: str, agent: CrewAgentDefinition):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent


class CrewManager:
    """Manages multi-agent crew collaboration and task delegation."""
    
    def __init__(self):
        self._init_crew_agents()

    def _init_crew_agents(self):
        self.manager_agent = CrewAgentDefinition(
            role="EduMind Coordinator",
            goal="Synthesize student goals, orchestrate sub-agents, and maintain long-term learning trajectory",
            backstory="Expert AI pedagogical advisor dedicated to student career success and skill acquisition."
        )
        self.career_agent = CrewAgentDefinition(
            role="Career Strategist",
            goal="Perform skill-gap analysis, calculate Bayesian career probabilities, and structure career roadmaps",
            backstory="Experienced tech recruiter and engineering career coach."
        )
        self.study_agent = CrewAgentDefinition(
            role="Curriculum & Study Planner",
            goal="Optimize topic prerequisite ordering using graph algorithms and construct daily study schedules",
            backstory="Academic curriculum architect specializing in cognitive learning efficiency."
        )
        self.interview_agent = CrewAgentDefinition(
            role="Adaptive Technical Interviewer",
            goal="Conduct mock technical rounds, grade answers rigorously, and track weaknesses in memory",
            backstory="Principal engineer conducting technical hiring loops."
        )
        self.research_agent = CrewAgentDefinition(
            role="Academic Researcher",
            goal="Provide deep conceptual explanations, mathematical formulations, and curated resources",
            backstory="Computer science researcher and educator."
        )

    def run_crew_pipeline(
        self,
        user_id: str,
        intent: str,
        user_message: str,
        profile: Dict[str, Any],
        memories: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Execute multi-agent crew workflow by delegating tasks to specialized agents based on intent.
        """
        agents_invoked = ["EduMind Coordinator"]
        agent_outputs = {}

        if intent in ["career_guidance", "skill_gap"]:
            agents_invoked.append("Career Strategist")
            career_out = career_agent.analyze_career_path(
                user_id=user_id,
                target_role=profile.get("career_goal", "AI Engineer"),
                current_skills=profile.get("skills", {}),
                weak_topics=profile.get("weak_topics", [])
            )
            agent_outputs["career_analysis"] = career_out

        if intent in ["study_plan", "learning_path"]:
            agents_invoked.append("Curriculum & Study Planner")
            study_out = study_agent.generate_plan_for_student(
                user_id=user_id,
                career_goal=profile.get("career_goal", "AI Engineer"),
                skills=profile.get("skills", {}),
                weak_topics=profile.get("weak_topics", []),
                daily_hours=profile.get("study_preferences", {}).get("daily_hours", 2.0),
                preferred_time=profile.get("study_preferences", {}).get("preferred_time", "Evening")
            )
            agent_outputs["study_plan"] = study_out

        if intent in ["interview_prep", "mock_interview"]:
            agents_invoked.append("Adaptive Technical Interviewer")
            interview_out = interview_agent.start_session(
                user_id=user_id,
                target_role=profile.get("career_goal", "AI Engineer"),
                topic="Machine Learning"
            )
            agent_outputs["interview_session"] = interview_out

        if intent in ["concept_research", "algorithm_query"]:
            agents_invoked.append("Academic Researcher")
            res_out = research_agent.explain_concept("A* Search Algorithm")
            agent_outputs["research_summary"] = res_out

        return {
            "crew_status": "completed",
            "agents_invoked": agents_invoked,
            "agent_outputs": agent_outputs,
            "delegation_summary": f"Orchestrated {len(agents_invoked)} specialized agents in crew loop."
        }


# Global crew manager instance
crew_manager = CrewManager()
