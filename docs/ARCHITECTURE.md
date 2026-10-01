# 🏛️ EduAgent Architecture & System Design

EduAgent is a production-style, Python-powered memory-enabled multi-agent RAG platform designed for personalized academic guidance, career roadmap planning, and adaptive mock interview preparation.

---

## 1. High-Level System Architecture

```mermaid
flowchart TD
    User([Student / User]) --> Frontend[React + Tailwind Dashboard & Chat UI]
    Frontend --> FastAPIServer[FastAPI Backend Gateway :8000]
    
    FastAPIServer --> Auth[JWT Authentication & Session Manager]
    FastAPIServer --> CentralAgent[EduMind Main Agent Coordinator]
    
    CentralAgent --> MemoryManager[Memory Manager Engine]
    MemoryManager --> STM[Short-Term Session Buffer]
    MemoryManager --> LTM[(Long-Term Memory Collection)]
    
    CentralAgent --> LangGraphWF[LangGraph State Workflow]
    
    LangGraphWF --> RAG[RAG Document Pipeline]
    RAG --> VectorStore[(Vector Store Index)]
    
    LangGraphWF --> CrewAI[CrewAI Multi-Agent Collaboration]
    CrewAI --> CareerAgent[Career Guidance Agent]
    CrewAI --> StudyAgent[Study Planning Agent]
    CrewAI --> InterviewAgent[Adaptive Interview Agent]
    CrewAI --> ResearchAgent[Research Agent]
    
    LangGraphWF --> ClassicalAI[Classical AI Suite]
    ClassicalAI --> SearchAlg[BFS / DFS / UCS / A* / Hill Climbing / Beam]
    ClassicalAI --> LogicEngine[Forward & Backward Chaining]
    ClassicalAI --> BayesEngine[Bayesian Uncertainty Inference]
    ClassicalAI --> StripsPlan[STRIPS Action Planner]
    
    LangGraphWF --> MCP[Model Context Protocol Server]
    LangGraphWF --> LLMFactory[LLM Factory: OpenAI / Local Ollama / Cognitive Engine]
```

---

## 2. Multi-Agent Collaboration Flow (CrewAI & LangGraph)

```mermaid
sequenceDiagram
    autonumber
    actor User as Student
    participant Coord as EduMind Coordinator
    participant Mem as Memory Retriever & Store
    participant RAG as RAG Document Pipeline
    participant Crew as Specialized Sub-Agents
    participant LLM as LLM Inference Engine

    User->>Coord: "What should I learn next for AI Engineering?"
    Coord->>Mem: Retrieve Long-Term Memories (Target Role, Weaknesses, Skills)
    Mem-->>Coord: Career: AI Eng, Python: 85%, Weak: Statistics & ML (40%)
    Coord->>Coord: Intent Classification -> Study Planning & Career Gap
    Coord->>Crew: Delegate to Study Agent & Career Agent
    Crew->>Crew: Run A* Curriculum Path Optimizer & Bayesian Suitability
    Crew-->>Coord: Optimal Next Topic: Probability & Machine Learning Core
    Coord->>LLM: Synthesize Context (Profile + Memory + Tool Output)
    LLM-->>Coord: Formatted Pedagogical Advice & Milestone Steps
    Coord->>Mem: Persist Interaction & Extract Facts
    Coord-->>User: Structured Personalized Learning Guidance
```

---

## 3. Dynamic Prompt Context Engineering

The system dynamically constructs the LLM context prior to every inference step:

$$\text{Context} = \text{Query} + \text{STM}_{\text{recent}} + \text{LTM}_{\text{retrieved}} + \text{Profile} + \text{RAG}_{\text{citations}} + \text{Tools}_{\text{output}}$$

---

## 4. Search & Optimization Algorithms

1. **Breadth-First Search (BFS)**: Unweighted state expansion using FIFO queue.
2. **Depth-First Search (DFS)**: Deep path exploration with LIFO stack.
3. **Uniform Cost Search (UCS)**: Dijkstra lowest path cost $g(n)$ expansion.
4. **A\* Search**: Optimal heuristic search using $f(n) = g(n) + h(n)$ with admissible heuristic $h(n) \le h^*(n)$.
5. **Hill Climbing**: Greedy local search moving strictly to lower heuristic states.
6. **Beam Search**: Heuristic search maintaining top-$k$ paths at each depth horizon.
