"""
Test suite for Learning Service, Subject Catalog, Resources, Plan Generator,
Topic Content, Progress Tracking, and EduMind AI Tutor.
"""

import pytest
from backend.app.services.learning_service import learning_service


def test_get_subjects_and_filtering():
    all_subjects = learning_service.get_subjects()
    assert len(all_subjects) >= 10
    
    prog_subjects = learning_service.get_subjects("Programming")
    assert len(prog_subjects) >= 3
    assert any(s["name"] == "Python" for s in prog_subjects)


def test_verified_resources_database():
    py_res = learning_service.get_resources_for_subject("Python")
    assert len(py_res) >= 3
    assert any("docs.python.org" in r["url"] for r in py_res)
    assert any("w3schools.com" in r["url"] for r in py_res)

    cpp_res = learning_service.get_resources_for_subject("C++")
    assert len(cpp_res) >= 2
    assert any("learncpp.com" in r["url"] for r in cpp_res)


def test_generate_personalized_plan():
    plan = learning_service.generate_personalized_plan(
        user_id="test_student_learning",
        subject="Python",
        level="Beginner",
        goal="Job Preparation",
        daily_minutes=60,
        days_per_week=5
    )
    assert plan["subject"] == "Python"
    assert len(plan["weeks"]) >= 4
    assert plan["total_topics_count"] >= 10
    assert plan["total_estimated_hours"] > 0


def test_get_topic_content():
    content = learning_service.get_topic_content("Python", "Variables & Data Types", "Beginner")
    assert content["subject"] == "Python"
    assert len(content["explanation"]) > 50
    assert len(content["key_concepts"]) >= 3
    assert "code_example" in content
    assert len(content["quiz"]) == 5
    assert len(content["resources"]) >= 2


def test_progress_tracking_and_streak():
    prog = learning_service.update_progress(
        user_id="test_student_learning",
        subject="Python",
        topic_title="Variables & Data Types",
        status="Completed",
        time_spent_minutes=45,
        quiz_score=5
    )
    assert prog["status"] == "success"
    assert prog["streak_days"] >= 1

    summary = learning_service.get_user_progress_summary("test_student_learning", "Python")
    assert summary["progress_percentage"] >= 0
    assert summary["streak_days"] >= 1


@pytest.mark.asyncio
async def test_edumind_doubt_answering():
    resp = await learning_service.answer_edumind_doubt(
        user_id="test_student_learning",
        message="I don't understand how variables point to objects in Python memory.",
        subject="Python",
        topic="Variables & Data Types",
        level="Beginner",
        goal="Career",
        action_type="explain_simpler"
    )
    assert resp["agent_name"] == "EduMind AI Tutor"
    assert len(resp["response"]) > 30
    assert len(resp["suggested_actions"]) >= 5
