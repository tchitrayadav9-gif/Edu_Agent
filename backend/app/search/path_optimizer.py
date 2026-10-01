"""
Learning Path Optimizer module.
Builds educational prerequisite graphs and runs graph search algorithms (BFS, DFS, UCS, A*, Hill Climbing, Beam Search)
to compute optimal, cost-efficient learning sequences for students.
"""

from typing import Dict, List, Any, Optional
from .search_algorithms import (
    Graph,
    SearchResult,
    breadth_first_search,
    depth_first_search,
    uniform_cost_search,
    a_star_search,
    hill_climbing_search,
    beam_search
)


class LearningPathOptimizer:
    """Optimizes curriculum learning paths for AI, Data Science, and Software Engineering careers."""
    
    def __init__(self):
        self.graph = self._build_default_curriculum_graph()

    def _build_default_curriculum_graph(self) -> Graph:
        g = Graph()
        # Define curriculum edges (u, v, study_hours_cost)
        edges = [
            ("Python Basics", "NumPy & Pandas", 10.0),
            ("Python Basics", "Object Oriented Programming", 8.0),
            ("NumPy & Pandas", "Statistics & Probability", 15.0),
            ("NumPy & Pandas", "Data Visualization", 6.0),
            ("Object Oriented Programming", "Data Structures & Algorithms", 25.0),
            ("Statistics & Probability", "Machine Learning Fundamentals", 20.0),
            ("Data Structures & Algorithms", "System Design", 30.0),
            ("Data Visualization", "Exploratory Data Analysis", 8.0),
            ("Exploratory Data Analysis", "Machine Learning Fundamentals", 12.0),
            ("Machine Learning Fundamentals", "Deep Learning", 30.0),
            ("Machine Learning Fundamentals", "MLOps & Model Deployment", 18.0),
            ("Deep Learning", "Natural Language Processing", 25.0),
            ("Deep Learning", "Computer Vision", 25.0),
            ("Natural Language Processing", "Generative AI & LLMs", 20.0),
            ("Computer Vision", "Generative AI & LLMs", 22.0),
            ("Generative AI & LLMs", "AI Agent Systems", 15.0),
            ("MLOps & Model Deployment", "AI Agent Systems", 16.0),
            ("System Design", "AI Agent Systems", 20.0),
            # Full Career Milestones
            ("AI Agent Systems", "AI Engineer Mastery", 10.0),
            ("Machine Learning Fundamentals", "Data Scientist Mastery", 25.0),
            ("System Design", "Software Architect Mastery", 35.0)
        ]
        for u, v, cost in edges:
            g.add_edge(u, v, cost)

        # Admissible Heuristics: Estimated minimum remaining hours to "AI Engineer Mastery"
        heuristics_to_ai_engineer = {
            "Python Basics": 80.0,
            "NumPy & Pandas": 70.0,
            "Object Oriented Programming": 75.0,
            "Statistics & Probability": 55.0,
            "Data Visualization": 65.0,
            "Data Structures & Algorithms": 60.0,
            "System Design": 30.0,
            "Exploratory Data Analysis": 60.0,
            "Machine Learning Fundamentals": 45.0,
            "MLOps & Model Deployment": 25.0,
            "Deep Learning": 30.0,
            "Natural Language Processing": 20.0,
            "Computer Vision": 22.0,
            "Generative AI & LLMs": 10.0,
            "AI Agent Systems": 5.0,
            "AI Engineer Mastery": 0.0,
            "Data Scientist Mastery": 15.0,
            "Software Architect Mastery": 20.0
        }
        for node, h in heuristics_to_ai_engineer.items():
            g.set_heuristic(node, h)

        return g

    def run_all_algorithms(self, start_topic: str = "Python Basics", goal_topic: str = "AI Engineer Mastery") -> Dict[str, Any]:
        """Execute all 6 classical search algorithms and return comparative benchmarking."""
        results = {
            "start_topic": start_topic,
            "goal_topic": goal_topic,
            "algorithms": {
                "bfs": breadth_first_search(self.graph, start_topic, goal_topic).to_dict(),
                "dfs": depth_first_search(self.graph, start_topic, goal_topic).to_dict(),
                "ucs": uniform_cost_search(self.graph, start_topic, goal_topic).to_dict(),
                "a_star": a_star_search(self.graph, start_topic, goal_topic).to_dict(),
                "hill_climbing": hill_climbing_search(self.graph, start_topic, goal_topic).to_dict(),
                "beam_search": beam_search(self.graph, start_topic, goal_topic, beam_width=2).to_dict()
            }
        }
        return results

    def find_optimal_path(self, start_topic: str, goal_topic: str, algorithm: str = "a_star") -> Dict[str, Any]:
        """Run a specific search algorithm on the curriculum graph."""
        alg = algorithm.lower().replace(" ", "_")
        if alg in ["a_star", "astar", "a*"]:
            res = a_star_search(self.graph, start_topic, goal_topic)
        elif alg in ["ucs", "uniform_cost", "dijkstra"]:
            res = uniform_cost_search(self.graph, start_topic, goal_topic)
        elif alg in ["bfs", "breadth_first"]:
            res = breadth_first_search(self.graph, start_topic, goal_topic)
        elif alg in ["dfs", "depth_first"]:
            res = depth_first_search(self.graph, start_topic, goal_topic)
        elif alg in ["hill_climbing", "greedy"]:
            res = hill_climbing_search(self.graph, start_topic, goal_topic)
        elif alg in ["beam", "beam_search"]:
            res = beam_search(self.graph, start_topic, goal_topic, beam_width=2)
        else:
            res = a_star_search(self.graph, start_topic, goal_topic)
        
        return res.to_dict()

    def get_curriculum_nodes(self) -> List[str]:
        return list(self.graph.adj.keys())


# Global path optimizer instance
path_optimizer = LearningPathOptimizer()
