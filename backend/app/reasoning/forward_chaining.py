"""
Forward Chaining Inference Engine.
Data-driven reasoning algorithm that starts with known initial facts and iteratively fires
production rules to deduce new derived facts and recommendations.
"""

from typing import Dict, List, Any, Optional
from .rule_engine import Fact, Rule, get_default_career_rules


class ForwardChainingEngine:
    """Forward Chaining reasoning engine with step-by-step audit trace."""
    
    def __init__(self, rules: Optional[List[Rule]] = None):
        self.rules = rules or get_default_career_rules()

    def infer(self, initial_facts: Dict[str, Any], max_iterations: int = 20) -> Dict[str, Any]:
        """
        Execute forward chaining on given known facts.
        Returns:
            - derived_facts: Dictionary of all facts (initial + inferred)
            - reasoning_trace: Detailed list of rules fired, conditions satisfied, and new conclusions
            - recommendations: Filtered list of actionable recommendations
        """
        current_facts = dict(initial_facts)
        reasoning_trace = []
        fired_rules = set()

        iteration = 0
        new_fact_added = True

        while new_fact_added and iteration < max_iterations:
            iteration += 1
            new_fact_added = False

            for rule in self.rules:
                if rule.name in fired_rules:
                    continue

                if rule.is_triggered(current_facts):
                    # Check if consequence already known with same value
                    conseq = rule.consequence
                    if current_facts.get(conseq.key) != conseq.value:
                        current_facts[conseq.key] = conseq.value
                        new_fact_added = True
                        fired_rules.add(rule.name)

                        trace_entry = {
                            "step": len(reasoning_trace) + 1,
                            "iteration": iteration,
                            "rule_name": rule.name,
                            "conditions_matched": {k: current_facts.get(k) for k in rule.conditions.keys()},
                            "derived_fact": f"{conseq.key} = {conseq.value}",
                            "explanation": rule.explanation
                        }
                        reasoning_trace.append(trace_entry)

        # Extract recommendations
        recommendations = []
        for k, v in current_facts.items():
            if k in ["Career_Recommendation", "Recommended_Action", "Interview_Readiness"]:
                recommendations.append({"type": k, "value": v})

        return {
            "initial_facts": initial_facts,
            "derived_facts": current_facts,
            "reasoning_trace": reasoning_trace,
            "rules_fired_count": len(fired_rules),
            "recommendations": recommendations,
            "success": len(reasoning_trace) > 0
        }


# Global forward chaining engine
forward_chaining_engine = ForwardChainingEngine()
