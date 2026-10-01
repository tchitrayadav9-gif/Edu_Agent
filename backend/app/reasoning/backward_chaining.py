"""
Backward Chaining Inference Engine.
Goal-driven deduction algorithm that starts with a hypothesized goal (e.g., 'Career_Recommendation = AI Engineer')
and recursively proves sub-goals by verifying whether required antecedents are satisfied by known facts.
"""

from typing import Dict, List, Any, Optional, Tuple
from .rule_engine import Fact, Rule, get_default_career_rules


class BackwardChainingEngine:
    """Backward Chaining reasoning engine for goal verification and missing prerequisite diagnosis."""
    
    def __init__(self, rules: Optional[List[Rule]] = None):
        self.rules = rules or get_default_career_rules()

    def evaluate_goal(
        self,
        goal_key: str,
        goal_value: Any,
        known_facts: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prove or disprove a specific goal given known student facts.
        Returns:
            - is_proved: Boolean whether the goal holds
            - proof_tree: Tree of rule evaluations and condition checks
            - missing_facts: Antecedents that were missing or had incorrect values
        """
        proof_trace = []
        missing_facts = []

        # 1. Check if directly in known facts
        if goal_key in known_facts:
            if known_facts[goal_key] == goal_value:
                return {
                    "goal": f"{goal_key} = {goal_value}",
                    "is_proved": True,
                    "proof_trace": [{"step": 1, "note": f"Goal directly exists in known facts ({goal_key} = {goal_value})"}],
                    "missing_facts": []
                }

        # 2. Find rules that have this goal as consequent
        candidate_rules = [r for r in self.rules if r.consequence.key == goal_key and r.consequence.value == goal_value]
        
        if not candidate_rules:
            return {
                "goal": f"{goal_key} = {goal_value}",
                "is_proved": False,
                "proof_trace": [{"step": 1, "note": f"No rule concludes {goal_key} = {goal_value}"}],
                "missing_facts": [f"{goal_key} = {goal_value}"]
            }

        goal_proved = False
        for rule in candidate_rules:
            rule_satisfied = True
            sub_trace = {
                "rule_name": rule.name,
                "conditions_checked": [],
                "explanation": rule.explanation
            }

            for cond_key, cond_val in rule.conditions.items():
                actual_val = known_facts.get(cond_key)
                if actual_val is None:
                    rule_satisfied = False
                    sub_trace["conditions_checked"].append({
                        "condition": f"{cond_key} == {cond_val}",
                        "status": "MISSING",
                        "actual": None
                    })
                    missing_facts.append(f"Requires {cond_key} to be '{cond_val}', but not recorded.")
                elif actual_val != cond_val:
                    rule_satisfied = False
                    sub_trace["conditions_checked"].append({
                        "condition": f"{cond_key} == {cond_val}",
                        "status": "UNSATISFIED",
                        "actual": actual_val
                    })
                    missing_facts.append(f"Requires {cond_key} to be '{cond_val}', but currently '{actual_val}'.")
                else:
                    sub_trace["conditions_checked"].append({
                        "condition": f"{cond_key} == {cond_val}",
                        "status": "SATISFIED",
                        "actual": actual_val
                    })

            proof_trace.append(sub_trace)
            if rule_satisfied:
                goal_proved = True
                break

        return {
            "goal": f"{goal_key} = {goal_value}",
            "is_proved": goal_proved,
            "proof_trace": proof_trace,
            "missing_facts": missing_facts,
            "recommendation": "Prerequisites fully met!" if goal_proved else f"Need to fulfill: {', '.join(missing_facts)}"
        }


# Global backward chaining engine
backward_chaining_engine = BackwardChainingEngine()
