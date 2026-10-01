"""
Student Knowledge Graph Representation.
Models entities (Student, Topic, Skill, Career, Resource) and directed relational triples
(e.g., Student -[KNOWS]-> Python, Student -[WEAK_IN]-> Statistics, Python -[PREREQUISITE_OF]-> Machine Learning).
"""

from typing import Dict, List, Any, Optional, Set, Tuple


class KnowledgeGraph:
    """Directed Property Graph representation of student academic and conceptual knowledge."""
    
    def __init__(self):
        # Nodes: id -> {"label": str, "type": str, "properties": dict}
        self.nodes: Dict[str, Dict[str, Any]] = {}
        # Edges: List of {"source": str, "relation": str, "target": str, "properties": dict}
        self.edges: List[Dict[str, Any]] = []
        self._build_curriculum_ontology()

    def add_node(self, node_id: str, node_type: str, label: str, properties: Optional[Dict[str, Any]] = None):
        self.nodes[node_id] = {
            "id": node_id,
            "type": node_type,  # Student, Topic, Skill, Career, Resource
            "label": label,
            "properties": properties or {}
        }

    def add_edge(self, source_id: str, relation: str, target_id: str, properties: Optional[Dict[str, Any]] = None):
        edge = {
            "source": source_id,
            "relation": relation,  # KNOWS, LEARNING, WEAK_IN, PREREQUISITE_OF, TARGETS, RECOMMENDS
            "target": target_id,
            "properties": properties or {}
        }
        # Avoid duplicate triples
        if not any(e["source"] == source_id and e["relation"] == relation and e["target"] == target_id for e in self.edges):
            self.edges.append(edge)

    def _build_curriculum_ontology(self):
        """Seed foundational domain entities and prerequisite relationships."""
        topics = [
            ("topic_python", "Python Programming", "Skill"),
            ("topic_sql", "SQL Databases", "Skill"),
            ("topic_dsa", "Data Structures & Algorithms", "Topic"),
            ("topic_stats", "Statistics & Probability", "Topic"),
            ("topic_ml", "Machine Learning", "Topic"),
            ("topic_dl", "Deep Learning & Neural Networks", "Topic"),
            ("topic_llm", "Generative AI & LLMs", "Topic"),
            ("topic_agents", "Multi-Agent AI Systems", "Topic"),
            ("topic_sys_design", "Distributed System Design", "Topic"),
            # Careers
            ("career_ai_eng", "AI Engineer", "Career"),
            ("career_ds", "Data Scientist", "Career"),
            ("career_swe", "Software Engineer", "Career"),
            ("career_mlops", "MLOps Engineer", "Career")
        ]
        for tid, label, ntype in topics:
            self.add_node(tid, ntype, label)

        prerequisites = [
            ("topic_python", "PREREQUISITE_OF", "topic_dsa"),
            ("topic_python", "PREREQUISITE_OF", "topic_ml"),
            ("topic_stats", "PREREQUISITE_OF", "topic_ml"),
            ("topic_ml", "PREREQUISITE_OF", "topic_dl"),
            ("topic_dl", "PREREQUISITE_OF", "topic_llm"),
            ("topic_llm", "PREREQUISITE_OF", "topic_agents"),
            ("topic_dsa", "PREREQUISITE_OF", "topic_sys_design"),
            # Career target requirements
            ("career_ai_eng", "REQUIRES", "topic_python"),
            ("career_ai_eng", "REQUIRES", "topic_ml"),
            ("career_ai_eng", "REQUIRES", "topic_dl"),
            ("career_ai_eng", "REQUIRES", "topic_agents"),
            ("career_ds", "REQUIRES", "topic_sql"),
            ("career_ds", "REQUIRES", "topic_stats"),
            ("career_ds", "REQUIRES", "topic_ml"),
            ("career_swe", "REQUIRES", "topic_python"),
            ("career_swe", "REQUIRES", "topic_dsa"),
            ("career_swe", "REQUIRES", "topic_sys_design")
        ]
        for src, rel, tgt in prerequisites:
            self.add_edge(src, rel, tgt)

    def sync_student_state(
        self,
        student_id: str,
        student_name: str,
        career_goal: str,
        skills: Dict[str, int],
        weak_topics: List[str],
        learning_progress: Dict[str, int]
    ):
        """Synchronize the live student profile into the knowledge graph structure."""
        # Add student node
        self.add_node(f"student_{student_id}", "Student", student_name, {"user_id": student_id})
        s_id = f"student_{student_id}"

        # Clean old student edges
        self.edges = [e for e in self.edges if e["source"] != s_id]

        # Target Career Goal
        c_node_id = f"career_{career_goal.lower().replace(' ', '_')}"
        if c_node_id in self.nodes:
            self.add_edge(s_id, "TARGETS", c_node_id)
        else:
            self.add_node(c_node_id, "Career", career_goal)
            self.add_edge(s_id, "TARGETS", c_node_id)

        # Known Skills
        for skill, score in skills.items():
            t_node_id = f"topic_{skill.lower().replace(' ', '_')}"
            if t_node_id not in self.nodes:
                self.add_node(t_node_id, "Skill", skill)
            self.add_edge(s_id, "KNOWS", t_node_id, {"proficiency": score})

        # Weak Topics
        for weak in weak_topics:
            w_node_id = f"topic_{weak.lower().replace(' ', '_')}"
            if w_node_id not in self.nodes:
                self.add_node(w_node_id, "Topic", weak)
            self.add_edge(s_id, "WEAK_IN", w_node_id)

        # Learning In-Progress
        for topic, progress in learning_progress.items():
            if progress > 0 and progress < 100:
                p_node_id = f"topic_{topic.lower().replace(' ', '_')}"
                if p_node_id not in self.nodes:
                    self.add_node(p_node_id, "Topic", topic)
                self.add_edge(s_id, "LEARNING", p_node_id, {"progress": progress})

    def get_subgraph_for_student(self, student_id: str) -> Dict[str, Any]:
        """Return nodes and links suitable for interactive D3 / SVG graph visualization."""
        s_id = f"student_{student_id}"
        related_node_ids = {s_id}
        
        student_edges = []
        for e in self.edges:
            if e["source"] == s_id or e["target"] == s_id:
                student_edges.append(e)
                related_node_ids.add(e["source"])
                related_node_ids.add(e["target"])

        # Also include prerequisite links between connected topics
        domain_edges = [
            e for e in self.edges
            if e["source"] in related_node_ids and e["target"] in related_node_ids and e["relation"] in ["PREREQUISITE_OF", "REQUIRES"]
        ]
        all_edges = student_edges + domain_edges

        nodes_data = [self.nodes[nid] for nid in related_node_ids if nid in self.nodes]
        return {
            "nodes": nodes_data,
            "edges": all_edges,
            "total_nodes": len(nodes_data),
            "total_edges": len(all_edges)
        }


# Global knowledge graph instance
knowledge_graph = KnowledgeGraph()
