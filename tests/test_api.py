"""
Test suite for FastAPI endpoints via TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root_and_health_endpoints():
    r_root = client.get("/")
    assert r_root.status_code == 200
    assert r_root.json()["status"] == "online"

    r_health = client.get("/health")
    assert r_health.status_code == 200
    assert r_health.json()["status"] == "healthy"


def test_auth_and_profile_flow():
    # Login as demo student
    r_login = client.post("/api/auth/login", json={"username": "chitra", "password": "securepassword"})
    assert r_login.status_code == 200
    token = r_login.json()["access_token"]
    assert token is not None

    # Get student profile
    headers = {"Authorization": f"Bearer {token}", "X-User-Id": "user_chitra"}
    r_prof = client.get("/api/student/profile", headers=headers)
    assert r_prof.status_code == 200
    data = r_prof.json()
    assert data["name"] == "Chitra"


def test_chat_api_endpoint():
    headers = {"X-User-Id": "user_chitra"}
    payload = {
        "message": "What should I learn next for AI Engineering?",
        "provider": "auto"
    }
    r = client.post("/api/chat", json=payload, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["agent_name"] == "EduMind Agent"
    assert len(data["activities"]) > 0
    assert len(data["response"]) > 20


def test_search_and_reasoning_endpoints():
    # Classical Search
    r_search = client.post("/api/search/run", json={"algorithm": "a_star", "start_topic": "Python Basics", "goal_topic": "AI Engineer Mastery"})
    assert r_search.status_code == 200
    assert r_search.json()["success"] is True

    # Forward Reasoning
    facts = {"Python": "Strong", "Machine Learning": "Strong", "Statistics": "Strong"}
    r_reason = client.post("/api/reasoning/forward", json={"facts": facts})
    assert r_reason.status_code == 200
    assert r_reason.json()["derived_facts"]["Career_Recommendation"] == "AI Engineer"


def test_dashboard_endpoint():
    headers = {"X-User-Id": "user_chitra"}
    r = client.get("/api/dashboard", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert "average_skill_score" in data
    assert "career_goal" in data
