"""
Test suite for Specialized Agents, Crew Manager, LangGraph Workflow, and EduMind Main Agent.
"""

import pytest
from backend.app.agents.career_agent import career_agent
from backend.app.agents.study_agent import study_agent
from backend.app.agents.interview_agent import interview_agent
from backend.app.agents.research_agent import research_agent
from backend.app.agents.crew_manager import crew_manager
from backend.app.agents.langgraph_workflow import workflow_engine
from backend.app.agents.main_agent import main_agent
from backend.app.database.models import ChatRequest


def test_career_agent_analysis():
    skills = {"Python": 85, "SQL": 70, "Machine Learning": 40}
    res = career_agent.analyze_career_path("test_user_agent", "AI Engineer", skills, ["Statistics"])
    assert res["agent_name"] == "Career Agent"
    assert "bayesian_suitability" in res
    assert len(res["skill_gaps"]) > 0


def test_study_agent_schedule_generation():
    skills = {"Python": 85, "SQL": 70, "Machine Learning": 40}
    res = study_agent.generate_plan_for_student("test_user_agent", "AI Engineer", skills, ["Statistics"], 2.0, "Evening")
    assert res["agent_name"] == "Study Agent"
    assert "study_plan" in res
    assert len(res["study_plan"]["schedule"]) > 0


def test_interview_agent_adaptive_evaluation():
    session = interview_agent.start_session("test_user_agent", "AI Engineer", "Machine Learning")
    assert "session_id" in session
    assert "question" in session

    eval_res = interview_agent.evaluate_answer(
        session_id=session["session_id"],
        user_id="test_user_agent",
        student_answer="L1 uses absolute penalty leading to sparsity, while L2 squares weights."
    )
    assert eval_res["agent_name"] == "Interview Agent"
    assert eval_res["score"] >= 5.0
    assert "feedback" in eval_res


def test_crew_manager_orchestration():
    profile = {"career_goal": "AI Engineer", "skills": {"Python": 85}, "weak_topics": []}
    res = crew_manager.run_crew_pipeline("test_user_agent", "career_guidance", "Analyze my career", profile, [])
    assert res["crew_status"] == "completed"
    assert len(res["agents_invoked"]) >= 2


@pytest.mark.asyncio
async def test_main_edumind_agent_chat_response():
    req = ChatRequest(message="What should I learn next to become an AI Engineer?")
    resp = await main_agent.process_message("test_user_agent", req)
    assert resp.agent_name == "EduMind Agent"
    assert resp.execution_time_ms > 0
    assert len(resp.activities) > 0
    assert len(resp.response) > 50
