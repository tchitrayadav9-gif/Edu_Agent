# 📚 Academic Course Syllabus Mapping

EduAgent demonstrates comprehensive coverage of academic Fundamentals of Artificial Intelligence (FAI) and Advanced Agentic AI curricula:

| Course Module | Theoretical Topic | Project Implementation Location |
| :--- | :--- | :--- |
| **Module I** | Python Foundations, LLM APIs, Prompting & Autonomous Agents | `backend/app/agents/main_agent.py`, `backend/app/llm/` |
| **Module II** | Uninformed Search (BFS, DFS, Uniform Cost Search) | `backend/app/search/search_algorithms.py` (`breadth_first_search`, `depth_first_search`, `uniform_cost_search`) |
| **Module III** | Informed Heuristic Search (A*, Hill Climbing, Beam Search) | `backend/app/search/search_algorithms.py` (`a_star_search`, `hill_climbing_search`, `beam_search`) |
| **Module IV** | Decision Making, Path Cost Minimization & Curriculum Graph Optimization | `backend/app/search/path_optimizer.py` |
| **Module V** | Propositional & First-Order Logic Inference (Forward & Backward Chaining) | `backend/app/reasoning/forward_chaining.py`, `backend/app/reasoning/backward_chaining.py` |
| **Module VI** | Knowledge Representation, Property Graphs & Ontologies | `backend/app/knowledge/knowledge_graph.py`, `backend/app/knowledge/ontology.py` |
| **Module VII** | Classical AI Planning (STRIPS Preconditions & Effects) | `backend/app/planning/planner.py`, `backend/app/planning/study_planner.py` |
| **Module VIII** | Probabilistic Reasoning & Bayesian Uncertainty | `backend/app/uncertainty/bayesian_network.py` |
| **Module IX** | Multi-Agent Systems, Agent Delegation & Adaptive Learning | `backend/app/agents/crew_manager.py`, `backend/app/agents/langgraph_workflow.py` |
| **Module X** | AI Applications in Personalized Education, Adaptive Mock Interviews & RAG | `backend/app/rag/`, `backend/app/agents/interview_agent.py` |

---

## LLM & Modern AI Architecture Mapping

| Modern AI Concept | Implementation in EduAgent |
| :--- | :--- |
| **Core AI Language** | Python 3.11+ / 3.14 with strict typing and Pydantic schemas |
| **Central Cognitive Agent** | EduMind Coordinator Agent |
| **Prompt Engineering** | Systematic multi-agent prompt hierarchy (`backend/app/llm/prompt_templates.py`) |
| **Function / Tool Calling** | Python callable tool registry (`backend/app/tools/agent_tools.py`) |
| **RAG (Document Grounding)** | PDF / DOCX / TXT vector chunking and citation Q&A (`backend/app/rag/`) |
| **Dynamic Context Engineering** | Synthesizer merging query, STM, LTM, profile, tools, and RAG (`backend/app/services/context_builder.py`) |
| **LangChain Integration** | Vector stores, embeddings, document loaders, retrievers |
| **LangGraph Orchestration** | State graph with conditional intent routing nodes (`backend/app/agents/langgraph_workflow.py`) |
| **CrewAI Collaboration** | Specialized autonomous agents with role/goal task delegation (`backend/app/agents/crew_manager.py`) |
| **Model Context Protocol (MCP)** | JSON-RPC 2.0 tool server (`backend/app/mcp/server.py`) |
| **Long-Term Memory** | Persistent MongoDB collection with automatic fact extraction & conflict resolution |
| **Evaluation Framework** | 50-Question Benchmark measuring accuracy, relevance, faithfulness, latency, and cost |
| **Local LLM Execution** | Ollama client supporting local private inference (`backend/app/llm/ollama_client.py`) |
| **Fine-Tuning Experiment** | Domain-alignment evaluation script on educational datasets (`experiments/`) |
