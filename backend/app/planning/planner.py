"""
Classical AI Action Planning (STRIPS-style State-Space Planner).
Represents operators with Preconditions and Effects (Add/Delete lists).
Solves goal state reachability for academic skill acquisition.
"""

from typing import Dict, List, Set, Any, Optional
import copy


class Action:
    """Represents a discrete planning operator."""
    def __init__(
        self,
        name: str,
        preconditions: Set[str],
        add_effects: Set[str],
        del_effects: Set[str],
        duration_days: int = 7,
        study_hours: int = 14
    ):
        self.name = name
        self.preconditions = preconditions
        self.add_effects = add_effects
        self.del_effects = del_effects
        self.duration_days = duration_days
        self.study_hours = study_hours

    def is_applicable(self, current_state: Set[str]) -> bool:
        return self.preconditions.issubset(current_state)

    def apply(self, current_state: Set[str]) -> Set[str]:
        new_state = (current_state - self.del_effects).union(self.add_effects)
        return new_state


class StripsPlanner:
    """Forward state-space search planner."""
    
    def __init__(self):
        self.actions = self._build_academic_actions()

    def _build_academic_actions(self) -> List[Action]:
        return [
            Action(
                name="Complete_Python_Fundamentals",
                preconditions=set(),
                add_effects={"knows_python_basics", "can_code_python"},
                del_effects=set(),
                duration_days=5,
                study_hours=10
            ),
            Action(
                name="Learn_Object_Oriented_Design",
                preconditions={"knows_python_basics"},
                add_effects={"knows_oop"},
                del_effects=set(),
                duration_days=4,
                study_hours=8
            ),
            Action(
                name="Master_Data_Structures_Algorithms",
                preconditions={"knows_oop"},
                add_effects={"knows_dsa", "interview_ready_dsa"},
                del_effects={"weak_in_dsa"},
                duration_days=10,
                study_hours=20
            ),
            Action(
                name="Study_Probability_Statistics",
                preconditions=set(),
                add_effects={"knows_statistics"},
                del_effects={"weak_in_statistics"},
                duration_days=7,
                study_hours=14
            ),
            Action(
                name="Learn_Machine_Learning_Core",
                preconditions={"knows_python_basics", "knows_statistics"},
                add_effects={"knows_ml", "can_train_models"},
                del_effects={"weak_in_ml"},
                duration_days=10,
                study_hours=20
            ),
            Action(
                name="Learn_Deep_Learning_PyTorch",
                preconditions={"knows_ml"},
                add_effects={"knows_deep_learning", "can_build_neural_nets"},
                del_effects={"weak_in_dl"},
                duration_days=10,
                study_hours=20
            ),
            Action(
                name="Build_Multi_Agent_RAG_Systems",
                preconditions={"knows_deep_learning", "can_code_python"},
                add_effects={"knows_ai_agents", "can_build_rag", "ai_engineer_certified"},
                del_effects=set(),
                duration_days=8,
                study_hours=16
            ),
            Action(
                name="Practice_Mock_Technical_Interviews",
                preconditions={"knows_python_basics"},
                add_effects={"mock_interview_passed"},
                del_effects=set(),
                duration_days=3,
                study_hours=6
            )
        ]

    def generate_plan(self, initial_state: Set[str], goal_state: Set[str], max_steps: int = 10) -> Dict[str, Any]:
        """
        Search for an ordered plan of actions that transforms initial_state -> goal_state.
        """
        # Breadth-first forward state search
        from collections import deque
        queue = deque([(initial_state, [], 0, 0)])
        visited = set()

        while queue:
            state, plan, total_days, total_hours = queue.popleft()
            state_key = frozenset(state)

            if goal_state.issubset(state):
                return {
                    "success": True,
                    "plan_steps": [
                        {
                            "step": i + 1,
                            "action": act.name.replace("_", " "),
                            "duration_days": act.duration_days,
                            "study_hours": act.study_hours,
                            "effects": list(act.add_effects)
                        }
                        for i, act in enumerate(plan)
                    ],
                    "total_days": total_days,
                    "total_hours": total_hours,
                    "final_state": list(state)
                }

            if state_key in visited:
                continue
            visited.add(state_key)

            if len(plan) >= max_steps:
                continue

            for action in self.actions:
                if action.is_applicable(state):
                    next_state = action.apply(state)
                    queue.append((
                        next_state,
                        plan + [action],
                        total_days + action.duration_days,
                        total_hours + action.study_hours
                    ))

        return {
            "success": False,
            "plan_steps": [],
            "message": "Could not find valid action sequence to satisfy all goals within horizon."
        }


# Global planner instance
strips_planner = StripsPlanner()
