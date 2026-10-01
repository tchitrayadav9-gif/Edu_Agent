"""
Classical AI Search Algorithms Module.
Pure Python implementations of:
1. Breadth-First Search (BFS)
2. Depth-First Search (DFS)
3. Uniform Cost Search (UCS)
4. A* Search (f(n) = g(n) + h(n))
5. Hill Climbing Search (Local Search)
6. Beam Search (Heuristic width-limited search)

All algorithms return path, visited nodes count, total path cost, and execution time.
"""

import time
import heapq
from typing import Dict, List, Tuple, Any, Optional, Set
from collections import deque


class Graph:
    """Weighted directed graph representation for state space search."""
    def __init__(self):
        self.adj: Dict[str, List[Tuple[str, float]]] = {}
        self.heuristics: Dict[str, float] = {}
        self.node_metadata: Dict[str, Dict[str, Any]] = {}

    def add_edge(self, u: str, v: str, cost: float = 1.0):
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        self.adj[u].append((v, float(cost)))

    def set_heuristic(self, node: str, h_val: float):
        self.heuristics[node] = float(h_val)

    def get_heuristic(self, node: str) -> float:
        return self.heuristics.get(node, 0.0)

    def get_neighbors(self, node: str) -> List[Tuple[str, float]]:
        return self.adj.get(node, [])


class SearchResult:
    def __init__(
        self,
        algorithm: str,
        path: List[str],
        total_cost: float,
        nodes_visited: int,
        nodes_explored: List[str],
        execution_time_ms: float,
        success: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.algorithm = algorithm
        self.path = path
        self.total_cost = total_cost
        self.nodes_visited = nodes_visited
        self.nodes_explored = nodes_explored
        self.execution_time_ms = execution_time_ms
        self.success = success
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "algorithm": self.algorithm,
            "path": self.path,
            "total_cost": round(self.total_cost, 2),
            "nodes_visited": self.nodes_visited,
            "nodes_explored": self.nodes_explored,
            "execution_time_ms": round(self.execution_time_ms, 3),
            "success": self.success,
            "metadata": self.metadata
        }


def breadth_first_search(graph: Graph, start: str, goal: str) -> SearchResult:
    """Breadth-First Search (BFS) - Explores shallowest nodes first."""
    start_time = time.perf_counter()
    queue = deque([(start, [start], 0.0)])
    visited: Set[str] = {start}
    explored_order: List[str] = []

    while queue:
        current, path, cost = queue.popleft()
        explored_order.append(current)

        if current == goal:
            elapsed = (time.perf_counter() - start_time) * 1000
            return SearchResult("BFS", path, cost, len(explored_order), explored_order, elapsed, True)

        for neighbor, edge_cost in graph.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor], cost + edge_cost))

    elapsed = (time.perf_counter() - start_time) * 1000
    return SearchResult("BFS", [], 0.0, len(explored_order), explored_order, elapsed, False)


def depth_first_search(graph: Graph, start: str, goal: str, max_depth: int = 50) -> SearchResult:
    """Depth-First Search (DFS) - Explores deepest nodes first using explicit stack."""
    start_time = time.perf_counter()
    stack = [(start, [start], 0.0)]
    visited: Set[str] = set()
    explored_order: List[str] = []

    while stack:
        current, path, cost = stack.pop()
        
        if current not in visited:
            visited.add(current)
            explored_order.append(current)

            if current == goal:
                elapsed = (time.perf_counter() - start_time) * 1000
                return SearchResult("DFS", path, cost, len(explored_order), explored_order, elapsed, True)

            if len(path) < max_depth:
                # Reverse neighbors to explore in predictable order
                for neighbor, edge_cost in reversed(graph.get_neighbors(current)):
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor], cost + edge_cost))

    elapsed = (time.perf_counter() - start_time) * 1000
    return SearchResult("DFS", [], 0.0, len(explored_order), explored_order, elapsed, False)


def uniform_cost_search(graph: Graph, start: str, goal: str) -> SearchResult:
    """Uniform Cost Search (Dijkstra) - Expands lowest path cost g(n)."""
    start_time = time.perf_counter()
    # (g_cost, current_node, path)
    pqueue = [(0.0, start, [start])]
    visited_cost: Dict[str, float] = {start: 0.0}
    explored_order: List[str] = []

    while pqueue:
        cost, current, path = heapq.heappop(pqueue)
        explored_order.append(current)

        if current == goal:
            elapsed = (time.perf_counter() - start_time) * 1000
            return SearchResult("Uniform Cost Search", path, cost, len(explored_order), explored_order, elapsed, True)

        for neighbor, edge_cost in graph.get_neighbors(current):
            new_cost = cost + edge_cost
            if neighbor not in visited_cost or new_cost < visited_cost[neighbor]:
                visited_cost[neighbor] = new_cost
                heapq.heappush(pqueue, (new_cost, neighbor, path + [neighbor]))

    elapsed = (time.perf_counter() - start_time) * 1000
    return SearchResult("Uniform Cost Search", [], 0.0, len(explored_order), explored_order, elapsed, False)


def a_star_search(graph: Graph, start: str, goal: str) -> SearchResult:
    """A* Search - Uses f(n) = g(n) + h(n) with admissible heuristic."""
    start_time = time.perf_counter()
    # (f_cost, g_cost, current_node, path)
    start_h = graph.get_heuristic(start)
    pqueue = [(start_h, 0.0, start, [start])]
    visited_g: Dict[str, float] = {start: 0.0}
    explored_order: List[str] = []

    while pqueue:
        f, g, current, path = heapq.heappop(pqueue)
        explored_order.append(current)

        if current == goal:
            elapsed = (time.perf_counter() - start_time) * 1000
            return SearchResult("A* Search", path, g, len(explored_order), explored_order, elapsed, True, {
                "final_f_cost": round(f, 2),
                "heuristic_at_start": round(start_h, 2)
            })

        for neighbor, edge_cost in graph.get_neighbors(current):
            tentative_g = g + edge_cost
            if neighbor not in visited_g or tentative_g < visited_g[neighbor]:
                visited_g[neighbor] = tentative_g
                h = graph.get_heuristic(neighbor)
                f_cost = tentative_g + h
                heapq.heappush(pqueue, (f_cost, tentative_g, neighbor, path + [neighbor]))

    elapsed = (time.perf_counter() - start_time) * 1000
    return SearchResult("A* Search", [], 0.0, len(explored_order), explored_order, elapsed, False)


def hill_climbing_search(graph: Graph, start: str, goal: str, max_iterations: int = 50) -> SearchResult:
    """Hill Climbing (Greedy Local Search) - Greedily moves to neighbor with lowest heuristic value."""
    start_time = time.perf_counter()
    current = start
    path = [current]
    total_cost = 0.0
    explored_order = [current]

    for _ in range(max_iterations):
        if current == goal:
            elapsed = (time.perf_counter() - start_time) * 1000
            return SearchResult("Hill Climbing", path, total_cost, len(explored_order), explored_order, elapsed, True)

        neighbors = graph.get_neighbors(current)
        if not neighbors:
            break

        # Pick neighbor with strictly lowest heuristic h(n)
        best_neighbor = None
        best_h = graph.get_heuristic(current)
        best_edge_cost = 0.0

        for neighbor, edge_cost in neighbors:
            if neighbor not in path:  # Avoid direct loop
                h_val = graph.get_heuristic(neighbor)
                if h_val < best_h:
                    best_h = h_val
                    best_neighbor = neighbor
                    best_edge_cost = edge_cost

        if best_neighbor is None:
            # Local extrema reached
            break

        current = best_neighbor
        path.append(current)
        total_cost += best_edge_cost
        explored_order.append(current)

    elapsed = (time.perf_counter() - start_time) * 1000
    success = (current == goal)
    return SearchResult("Hill Climbing", path if success else [], total_cost, len(explored_order), explored_order, elapsed, success)


def beam_search(graph: Graph, start: str, goal: str, beam_width: int = 2) -> SearchResult:
    """Beam Search - Heuristic search keeping top-k best candidate partial paths at each depth."""
    start_time = time.perf_counter()
    # List of (h_cost, g_cost, current_node, path)
    beam = [(graph.get_heuristic(start), 0.0, start, [start])]
    explored_order: List[str] = []

    while beam:
        next_candidates = []
        for h, g, current, path in beam:
            explored_order.append(current)
            if current == goal:
                elapsed = (time.perf_counter() - start_time) * 1000
                return SearchResult("Beam Search", path, g, len(explored_order), explored_order, elapsed, True, {"beam_width": beam_width})

            for neighbor, edge_cost in graph.get_neighbors(current):
                if neighbor not in path:
                    new_g = g + edge_cost
                    new_h = graph.get_heuristic(neighbor)
                    next_candidates.append((new_h, new_g, neighbor, path + [neighbor]))

        if not next_candidates:
            break

        # Sort by heuristic and take beam_width
        next_candidates.sort(key=lambda x: x[0])
        beam = next_candidates[:beam_width]

    elapsed = (time.perf_counter() - start_time) * 1000
    return SearchResult("Beam Search", [], 0.0, len(explored_order), explored_order, elapsed, False, {"beam_width": beam_width})
