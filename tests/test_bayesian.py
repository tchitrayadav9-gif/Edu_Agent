"""
Test suite for Bayesian Career Suitability network.
"""

from backend.app.uncertainty.bayesian_network import bayesian_career_network


def test_bayesian_career_probabilities_sum_to_100():
    skills = {"Python": 85, "Machine Learning": 75, "Deep Learning": 80, "Statistics": 70}
    res = bayesian_career_network.calculate_career_probabilities(student_skills=skills, career_interest="AI Engineer")
    
    total_pct = sum(r["confidence_percentage"] for r in res["recommendations"])
    assert 99.0 <= total_pct <= 101.0
    assert res["top_career"] in ["AI Engineer", "Machine Learning Engineer"]
    assert "disclaimer" in res


def test_bayesian_weakness_impact():
    skills = {"Python": 85, "SQL": 80, "Machine Learning": 40}
    res = bayesian_career_network.calculate_career_probabilities(
        student_skills=skills,
        weak_topics=["Machine Learning", "Deep Learning"],
        career_interest="Data Scientist"
    )
    # Data Scientist should have higher confidence than AI Engineer due to ML weakness
    roles = {r["career_role"]: r["confidence_percentage"] for r in res["recommendations"]}
    assert roles["Data Scientist"] >= roles["AI Engineer"]
