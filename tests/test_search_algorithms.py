"""
Test suite for Classical AI Search Algorithms (BFS, DFS, UCS, A*, Hill Climbing, Beam Search).
"""

import pytest
from backend.app.search.search_algorithms import (
    Graph,
    breadth_first_search,
    depth_first_search,
    uniform_cost_search,
    a_star_search,
    hill_climbing_search,
    beam_search
)
from backend.app.search.path_optimizer import path_optimizer


@pytest.fixture
def sample_graph():
    g = Graph()
    # Directed graph with known optimal path A -> B -> D (cost 3) vs A -> C -> D (cost 5)
    g.add_edge("A", "B", 1.0)
    g.add_edge("B", "D", 2.0)
    g.add_edge("A", "C", 2.0)
    g.add_edge("C", "D", 3.0)
    
    g.set_heuristic("A", 3.0)
    g.set_heuristic("B", 2.0)
    g.set_heuristic("C", 3.0)
    g.set_heuristic("D", 0.0)
    return g


def test_breadth_first_search(sample_graph):
    res = breadth_first_search(sample_graph, "A", "D")
    assert res.success is True
    assert res.path == ["A", "B", "D"] or res.path == ["A", "C", "D"]
    assert res.nodes_visited > 0
    assert res.execution_time_ms >= 0


def test_depth_first_search(sample_graph):
    res = depth_first_search(sample_graph, "A", "D")
    assert res.success is True
    assert res.path[0] == "A"
    assert res.path[-1] == "D"
    assert res.nodes_visited > 0


def test_uniform_cost_search(sample_graph):
    res = uniform_cost_search(sample_graph, "A", "D")
    assert res.success is True
    assert res.path == ["A", "B", "D"]
    assert res.total_cost == 3.0


def test_a_star_search(sample_graph):
    res = a_star_search(sample_graph, "A", "D")
    assert res.success is True
    assert res.path == ["A", "B", "D"]
    assert res.total_cost == 3.0


def test_hill_climbing_search(sample_graph):
    res = hill_climbing_search(sample_graph, "A", "D")
    assert res.success is True
    assert res.path == ["A", "B", "D"]


def test_beam_search(sample_graph):
    res = beam_search(sample_graph, "A", "D", beam_width=2)
    assert res.success is True
    assert res.path == ["A", "B", "D"]


def test_curriculum_path_optimizer():
    res = path_optimizer.find_optimal_path("Python Basics", "AI Engineer Mastery", "a_star")
    assert res["success"] is True
    assert "Python Basics" in res["path"]
    assert res["path"][-1] == "AI Engineer Mastery"
    assert res["total_cost"] > 0
