"""
Rule Engine and Logic Representation for Classical AI Reasoning.
Defines Fact representations, Production Rules, LHS Conditions, and RHS Consequences.
"""

from typing import Dict, List, Any, Optional, Set, Callable


class Fact:
    """Represents a propositional or relational fact in the knowledge base."""
    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Fact):
            return self.key == other.key and self.value == other.value
        return False

    def __hash__(self):
        return hash((self.key, str(self.value)))

    def __repr__(self):
        return f"Fact({self.key} = {self.value})"

    def to_dict(self) -> Dict[str, Any]:
        return {"key": self.key, "value": self.value}


class Rule:
    """
    Represents an IF-THEN production rule.
    IF (antecedents/conditions) THEN (consequent/action)
    """
    def __init__(
        self,
        name: str,
        conditions: Dict[str, Any],  # key -> required value (or callable)
        consequence: Fact,
        explanation: str = ""
    ):
        self.name = name
        self.conditions = conditions
        self.consequence = consequence
        self.explanation = explanation

    def is_triggered(self, facts: Dict[str, Any]) -> bool:
        """Check if all conditions in antecedent match given fact base."""
        for key, expected in self.conditions.items():
            if key not in facts:
                return False
            actual = facts[key]
            if callable(expected):
                if not expected(actual):
                    return False
            elif actual != expected:
                return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        cond_repr = {}
        for k, v in self.conditions.items():
            cond_repr[k] = "satisfies_predicate" if callable(v) else v
        return {
            "name": self.name,
            "conditions": cond_repr,
            "consequence": self.consequence.to_dict(),
            "explanation": self.explanation
        }


def get_default_career_rules() -> List[Rule]:
    """Production rule base for Career Guidance and Skill Gap reasoning."""
    rules = [
        Rule(
            name="R1_AI_Engineer_Candidate",
            conditions={"Python": "Strong", "Machine Learning": "Strong", "Statistics": "Strong"},
            consequence=Fact("Career_Recommendation", "AI Engineer"),
            explanation="Strong foundation in Python, ML, and Statistics qualifies for AI Engineering."
        ),
        Rule(
            name="R2_Data_Scientist_Candidate",
            conditions={"Python": "Strong", "SQL": "Strong", "Statistics": "Strong"},
            consequence=Fact("Career_Recommendation", "Data Scientist"),
            explanation="SQL and Statistics proficiency paired with Python forms the core Data Scientist profile."
        ),
        Rule(
            name="R3_MLOps_Engineer_Candidate",
            conditions={"Python": "Strong", "System Design": "Strong", "Machine Learning": "Strong"},
            consequence=Fact("Career_Recommendation", "MLOps Engineer"),
            explanation="Proficiency in ML combined with System Design and Python enables MLOps and Model Pipeline engineering."
        ),
        Rule(
            name="R4_Software_Engineer_Candidate",
            conditions={"Python": "Strong", "Data Structures": "Strong", "SQL": "Strong"},
            consequence=Fact("Career_Recommendation", "Backend Software Engineer"),
            explanation="Data Structures, SQL, and Python qualify for Core Backend Engineering."
        ),
        Rule(
            name="R5_Skill_Gap_AI_Engineer",
            conditions={"Target_Career": "AI Engineer", "Machine Learning": "Weak"},
            consequence=Fact("Recommended_Action", "Focus on Machine Learning Fundamentals & Deep Learning"),
            explanation="Targeting AI Engineering while weak in Machine Learning necessitates immediate ML core study."
        ),
        Rule(
            name="R6_Skill_Gap_Statistics",
            conditions={"Target_Career": "AI Engineer", "Statistics": "Weak"},
            consequence=Fact("Recommended_Action", "Review Probability & Statistical Inference"),
            explanation="Statistical intuition is mandatory for loss function optimization and model evaluation."
        ),
        Rule(
            name="R7_Interview_Readiness",
            conditions={"Python": "Strong", "Data Structures": "Strong", "Interview_Score": "High"},
            consequence=Fact("Interview_Readiness", "Ready for Tier-1 Technical Rounds"),
            explanation="High mock interview scores with solid algorithmic foundation indicate interview readiness."
        )
    ]
    return rules
