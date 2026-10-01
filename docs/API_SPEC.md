# 🔌 EduAgent API Reference Specification

EduAgent provides comprehensive REST endpoints and Model Context Protocol (MCP) JSON-RPC 2.0 endpoints on `http://localhost:8000`.

---

## 1. Central Agent Chat API

### `POST /api/chat`
Submit a message to the EduMind Central Agent.

**Request Body**:
```json
{
  "message": "What should I learn next to become an AI Engineer?",
  "conversation_id": "conv_demo_101",
  "provider": "auto"
}
```

**Response**:
```json
{
  "response": "### 🎯 Personalized Learning Recommendation\n...",
  "conversation_id": "conv_demo_101",
  "agent_name": "EduMind Agent",
  "intent": "study_planning",
  "activities": [
    "✓ Loaded student profile and target career goal",
    "✓ Retrieved 2 relevant long-term memories",
    "✓ Intent classified: Study Planning",
    "✓ Delegated to Study Agent (Running A* curriculum path optimization)",
    "✓ Generated grounded, personalized pedagogical response",
    "✓ Extracted and persisted 2 new facts into long-term memory"
  ],
  "memories_retrieved": [...],
  "documents_retrieved": [...],
  "tools_executed": [...],
  "agents_invoked": ["EduMind Coordinator", "Study Agent"],
  "memory_saved": {...},
  "execution_time_ms": 42.5
}
```

---

## 2. Memory System APIs

- `GET /api/memory`: Retrieve all long-term memories for student.
- `POST /api/memory`: Explicitly save a memory fact.
- `DELETE /api/memory/{id}`: Delete a memory record.
- `GET /api/memory/stats`: Return category breakdown.

---

## 3. Classical AI & Path Search APIs

### `POST /api/search/compare`
Run BFS, DFS, UCS, A*, Hill Climbing, and Beam Search side-by-side.

**Request Body**:
```json
{
  "start_topic": "Python Basics",
  "goal_topic": "AI Engineer Mastery"
}
```

**Response**:
```json
{
  "start_topic": "Python Basics",
  "goal_topic": "AI Engineer Mastery",
  "algorithms": {
    "a_star": {
      "algorithm": "A* Search",
      "path": ["Python Basics", "NumPy & Pandas", "Statistics & Probability", "Machine Learning Fundamentals", "Deep Learning", "Generative AI & LLMs", "AI Agent Systems", "AI Engineer Mastery"],
      "total_cost": 108.0,
      "nodes_visited": 8,
      "execution_time_ms": 0.42
    },
    "bfs": {...},
    "dfs": {...},
    "ucs": {...},
    "hill_climbing": {...},
    "beam_search": {...}
  }
}
```

---

## 4. Reasoning & Logic APIs

- `POST /api/reasoning/forward`: Forward chaining inference over student facts.
- `POST /api/reasoning/backward`: Backward chaining goal-driven verification.
- `GET /api/reasoning/rules`: View production rule base.

---

## 5. RAG Document APIs

- `POST /api/documents/upload`: Multipart upload for PDF, DOCX, TXT.
- `POST /api/documents/query`: Semantic query against vector indexed chunks.
- `GET /api/documents`: List uploaded files.

---

## 6. Adaptive Mock Interview APIs

- `POST /api/interview/start`: Start adaptive interview on chosen topic.
- `POST /api/interview/answer`: Submit answer, receive 0-10 score, feedback, and adaptive next question.

---

## 7. Model Context Protocol (MCP)

### `POST /api/mcp/rpc`
JSON-RPC 2.0 endpoint handling `initialize`, `tools/list`, and `tools/call`.
