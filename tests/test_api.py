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
    import uuid
    # 1. Register a new custom user with dynamic unique handle
    unique_suffix = uuid.uuid4().hex[:6]
    unique_username = f"teststudent_{unique_suffix}"
    unique_email = f"alex_{unique_suffix}@university.edu"
    r_reg = client.post("/api/auth/register", json={
        "username": unique_username,
        "name": "Alex Smith",
        "email": unique_email,
        "password": "Password123!",
        "academic_year": "3rd Year",
        "branch": "Computer Science and Engineering",
        "career_goal": "Data Scientist"
    })
    assert r_reg.status_code == 200
    reg_data = r_reg.json()
    assert reg_data["user"]["username"] == unique_username
    assert reg_data["user"]["name"] == "Alex Smith"
    token = reg_data["access_token"]
    assert token is not None

    # 2. Prevent duplicate username registration
    r_dup = client.post("/api/auth/register", json={
        "username": unique_username,
        "name": "Alex Duplicate",
        "email": "another@university.edu",
        "password": "Password123!"
    })
    assert r_dup.status_code == 400
    assert "already taken" in r_dup.json()["detail"]

    # 3. Login with email
    r_login = client.post("/api/auth/login", json={"username": unique_email, "password": "Password123!"})
    assert r_login.status_code == 200
    assert r_login.json()["user"]["username"] == unique_username

    # 4. Verify /api/auth/me
    headers = {"Authorization": f"Bearer {token}", "X-User-Id": reg_data["user"]["id"]}
    r_me = client.get("/api/auth/me", headers=headers)
    assert r_me.status_code == 200
    assert r_me.json()["username"] == unique_username

    # 5. Get student profile for registered user
    r_prof = client.get("/api/student/profile", headers=headers)
    assert r_prof.status_code == 200
    data = r_prof.json()
    assert data["name"] == "Alex Smith"
    assert data["career_goal"] == "Data Scientist"



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
