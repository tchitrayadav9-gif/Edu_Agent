"""
Test suite for Forward and Backward Chaining Logical Reasoning engines.
"""

from backend.app.reasoning.forward_chaining import forward_chaining_engine
from backend.app.reasoning.backward_chaining import backward_chaining_engine
from backend.app.reasoning.rule_engine import Rule, Fact


def test_forward_chaining_career_deduction():
    known_facts = {
        "Python": "Strong",
        "Machine Learning": "Strong",
        "Statistics": "Strong"
    }
    res = forward_chaining_engine.infer(known_facts)
    assert res["success"] is True
    assert res["derived_facts"].get("Career_Recommendation") == "AI Engineer"
    assert len(res["reasoning_trace"]) > 0


def test_forward_chaining_skill_gap_deduction():
    known_facts = {
        "Target_Career": "AI Engineer",
        "Machine Learning": "Weak"
    }
    res = forward_chaining_engine.infer(known_facts)
    assert res["success"] is True
    assert "Recommended_Action" in res["derived_facts"]


def test_backward_chaining_proved_goal():
    facts = {
        "Python": "Strong",
        "SQL": "Strong",
        "Statistics": "Strong"
    }
    res = backward_chaining_engine.evaluate_goal("Career_Recommendation", "Data Scientist", facts)
    assert res["is_proved"] is True
    assert len(res["missing_facts"]) == 0


def test_backward_chaining_unproved_missing_prereq():
    facts = {
        "Python": "Strong",
        "SQL": "Weak",
        "Statistics": "Strong"
    }
    res = backward_chaining_engine.evaluate_goal("Career_Recommendation", "Data Scientist", facts)
    assert res["is_proved"] is False
    assert len(res["missing_facts"]) > 0
