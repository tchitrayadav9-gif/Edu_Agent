"""
Comprehensive 50-Question Benchmark Dataset for EduAgent Evaluation.
Covers:
- RAG & Document Grounding (10 questions)
- Career Guidance & Skill-Gap Analysis (8 questions)
- Study Planning & Optimization (8 questions)
- Mock Technical & HR Interviews (8 questions)
- Classical AI Search Algorithms (8 questions)
- Logical Reasoning & Forward/Backward Chaining (4 questions)
- Memory Persistence & Context Recall (4 questions)
"""

from typing import List, Dict, Any

EVALUATION_DATASET_50: List[Dict[str, Any]] = [
    # Category 1: RAG & Document Grounding (1-10)
    {
        "id": 1,
        "category": "RAG",
        "question": "What is the evaluation function of A* search according to my notes?",
        "expected_keywords": ["f(n)", "g(n)", "h(n)", "heuristic", "path cost"],
        "expected_intent": "rag_query"
    },
    {
        "id": 2,
        "category": "RAG",
        "question": "Explain heuristic admissibility from the uploaded AI lecture notes.",
        "expected_keywords": ["admissible", "never overestimates", "h*(n)", "optimal"],
        "expected_intent": "rag_query"
    },
    {
        "id": 3,
        "category": "RAG",
        "question": "What does my DBMS notes say about ACID properties in relational transactions?",
        "expected_keywords": ["Atomicity", "Consistency", "Isolation", "Durability", "transaction"],
        "expected_intent": "rag_query"
    },
    {
        "id": 4,
        "category": "RAG",
        "question": "Summarize the BFS algorithm properties mentioned in my uploaded notes.",
        "expected_keywords": ["FIFO", "queue", "shortest path", "complete", "O(b^d)"],
        "expected_intent": "rag_query"
    },
    {
        "id": 5,
        "category": "RAG",
        "question": "What is the time complexity of Uniform Cost Search according to the course PDF?",
        "expected_keywords": ["O(b^(1 + floor(C*/eps)))", "cost", "priority queue"],
        "expected_intent": "rag_query"
    },
    {
        "id": 6,
        "category": "RAG",
        "question": "What does my resume say about my current projects and skills?",
        "expected_keywords": ["projects", "Python", "experience", "education"],
        "expected_intent": "rag_query"
    },
    {
        "id": 7,
        "category": "RAG",
        "question": "Explain the difference between informed and uninformed search from my notes.",
        "expected_keywords": ["heuristic", "informed", "uninformed", "domain knowledge"],
        "expected_intent": "rag_query"
    },
    {
        "id": 8,
        "category": "RAG",
        "question": "What is the definition of consistent heuristic in graph search?",
        "expected_keywords": ["triangle inequality", "h(n) <= c(n,a,n') + h(n')", "monotonic"],
        "expected_intent": "rag_query"
    },
    {
        "id": 9,
        "category": "RAG",
        "question": "How does beam search restrict memory usage in large state spaces according to notes?",
        "expected_keywords": ["beam width", "top k", "pruning", "memory bounded"],
        "expected_intent": "rag_query"
    },
    {
        "id": 10,
        "category": "RAG",
        "question": "What are the limitations of Hill Climbing search mentioned in the notes?",
        "expected_keywords": ["local maxima", "plateau", "ridge", "greedy"],
        "expected_intent": "rag_query"
    },

    # Category 2: Career Guidance & Skill-Gap Analysis (11-18)
    {
        "id": 11,
        "category": "Career",
        "question": "What skills do I need to become an AI Engineer?",
        "expected_keywords": ["Python", "Machine Learning", "Deep Learning", "Mathematics", "Statistics", "PyTorch"],
        "expected_intent": "career_guidance"
    },
    {
        "id": 12,
        "category": "Career",
        "question": "Compare the roles of Data Scientist vs Machine Learning Engineer.",
        "expected_keywords": ["Data Scientist", "ML Engineer", "SQL", "MLOps", "deployment", "statistics"],
        "expected_intent": "career_guidance"
    },
    {
        "id": 13,
        "category": "Career",
        "question": "Analyze my skill gap for becoming a Backend Software Engineer.",
        "expected_keywords": ["Data Structures", "System Design", "SQL", "Databases", "APIs"],
        "expected_intent": "career_guidance"
    },
    {
        "id": 14,
        "category": "Career",
        "question": "What is my Bayesian suitability score for AI Engineering?",
        "expected_keywords": ["Bayesian", "suitability", "confidence", "percentage", "probability"],
        "expected_intent": "career_guidance"
    },
    {
        "id": 15,
        "category": "Career",
        "question": "Which career track fits best with strong Python and SQL skills?",
        "expected_keywords": ["Data Scientist", "Data Analyst", "Backend Engineer"],
        "expected_intent": "career_guidance"
    },
    {
        "id": 16,
        "category": "Career",
        "question": "What are the industry requirements for MLOps Engineer in 2026?",
        "expected_keywords": ["Docker", "Kubernetes", "CI/CD", "Model Registry", "Monitoring"],
        "expected_intent": "career_guidance"
    },
    {
        "id": 17,
        "category": "Career",
        "question": "How should a 2nd-year B.Tech student prepare for AI product internships?",
        "expected_keywords": ["portfolio", "GitHub", "DSA", "projects", "Kaggle"],
        "expected_intent": "career_guidance"
    },
    {
        "id": 18,
        "category": "Career",
        "question": "What math topics are strictly essential for Machine Learning?",
        "expected_keywords": ["Linear Algebra", "Multivariate Calculus", "Probability", "Optimization"],
        "expected_intent": "career_guidance"
    },

    # Category 3: Study Planning & Optimization (19-26)
    {
        "id": 19,
        "category": "Study Planning",
        "question": "Create a 30-day study plan for AI Engineering.",
        "expected_keywords": ["Week", "Day", "Machine Learning", "Deep Learning", "hours", "schedule"],
        "expected_intent": "study_planning"
    },
    {
        "id": 20,
        "category": "Study Planning",
        "question": "What should I learn next based on my current weak areas?",
        "expected_keywords": ["Statistics", "Machine Learning", "foundation", "focus"],
        "expected_intent": "study_planning"
    },
    {
        "id": 21,
        "category": "Study Planning",
        "question": "How should I allocate 2 hours every evening for deep learning?",
        "expected_keywords": ["Evening", "2 hours", "PyTorch", "theory", "coding practice"],
        "expected_intent": "study_planning"
    },
    {
        "id": 22,
        "category": "Study Planning",
        "question": "Show the optimized prerequisite learning order from Python to GenAI.",
        "expected_keywords": ["Python", "NumPy", "Statistics", "ML", "Deep Learning", "LLMs"],
        "expected_intent": "study_planning"
    },
    {
        "id": 23,
        "category": "Study Planning",
        "question": "Create a weekly roadmap to master Data Structures and Algorithms.",
        "expected_keywords": ["Arrays", "Linked Lists", "Trees", "Graphs", "Dynamic Programming"],
        "expected_intent": "study_planning"
    },
    {
        "id": 24,
        "category": "Study Planning",
        "question": "How can I balance semester exams with AI project development?",
        "expected_keywords": ["time management", "prioritization", "schedule", "consistency"],
        "expected_intent": "study_planning"
    },
    {
        "id": 25,
        "category": "Study Planning",
        "question": "What is the recommended sequence to learn PyTorch for computer vision?",
        "expected_keywords": ["Tensors", "Autograd", "nn.Module", "CNNs", "DataLoader"],
        "expected_intent": "study_planning"
    },
    {
        "id": 26,
        "category": "Study Planning",
        "question": "Generate a revision plan for my weak topic: Statistics.",
        "expected_keywords": ["Probability", "Distributions", "Hypothesis Testing", "Bayes Rule"],
        "expected_intent": "study_planning"
    },

    # Category 4: Mock Technical & HR Interviews (27-34)
    {
        "id": 27,
        "category": "Interview",
        "question": "Test me for an AI Engineer mock interview.",
        "expected_keywords": ["Question", "Explain", "Machine Learning", "answer"],
        "expected_intent": "interview_prep"
    },
    {
        "id": 28,
        "category": "Interview",
        "question": "Explain the difference between L1 and L2 regularization in machine learning.",
        "expected_keywords": ["Lasso", "Ridge", "sparsity", "penalty", "weights"],
        "expected_intent": "interview_prep"
    },
    {
        "id": 29,
        "category": "Interview",
        "question": "What is overfitting and how do you prevent it in deep neural networks?",
        "expected_keywords": ["Dropout", "Regularization", "Early Stopping", "Data Augmentation"],
        "expected_intent": "interview_prep"
    },
    {
        "id": 30,
        "category": "Interview",
        "question": "How does the Attention mechanism work in Transformer models?",
        "expected_keywords": ["Query", "Key", "Value", "Softmax", "scaled dot-product"],
        "expected_intent": "interview_prep"
    },
    {
        "id": 31,
        "category": "Interview",
        "question": "Explain how gradient descent optimizes neural network loss.",
        "expected_keywords": ["learning rate", "derivative", "gradient", "backpropagation", "loss"],
        "expected_intent": "interview_prep"
    },
    {
        "id": 32,
        "category": "Interview",
        "question": "What are the key differences between SQL and NoSQL database architectures?",
        "expected_keywords": ["schema", "relational", "ACID", "BASE", "document", "horizontal scaling"],
        "expected_intent": "interview_prep"
    },
    {
        "id": 33,
        "category": "Interview",
        "question": "How do you handle class imbalance in classification datasets?",
        "expected_keywords": ["SMOTE", "oversampling", "undersampling", "class weights", "F1 score"],
        "expected_intent": "interview_prep"
    },
    {
        "id": 34,
        "category": "Interview",
        "question": "What should I improve based on my previous interview score?",
        "expected_keywords": ["Machine Learning", "Score", "Improvement", "Practice"],
        "expected_intent": "interview_prep"
    },

    # Category 5: Classical AI Search Algorithms (35-42)
    {
        "id": 35,
        "category": "Classical AI Search",
        "question": "How does BFS guarantee finding the shortest path in unweighted graphs?",
        "expected_keywords": ["level by level", "queue", "unweighted", "optimality"],
        "expected_intent": "concept_research"
    },
    {
        "id": 36,
        "category": "Classical AI Search",
        "question": "Explain the time and space complexity of Depth-First Search.",
        "expected_keywords": ["O(b*m)", "O(b^m)", "linear space", "branching factor"],
        "expected_intent": "concept_research"
    },
    {
        "id": 37,
        "category": "Classical AI Search",
        "question": "How does Uniform Cost Search select the next node to expand?",
        "expected_keywords": ["priority queue", "lowest path cost", "g(n)", "Dijkstra"],
        "expected_intent": "concept_research"
    },
    {
        "id": 38,
        "category": "Classical AI Search",
        "question": "Why is A* search optimal when using an admissible heuristic?",
        "expected_keywords": ["f(n) = g(n) + h(n)", "never overestimates", "optimal", "admissible"],
        "expected_intent": "concept_research"
    },
    {
        "id": 39,
        "category": "Classical AI Search",
        "question": "What causes Hill Climbing to get stuck on plateaus and local maxima?",
        "expected_keywords": ["local maxima", "zero gradient", "greedy", "random restart"],
        "expected_intent": "concept_research"
    },
    {
        "id": 40,
        "category": "Classical AI Search",
        "question": "How does Beam Search balance search quality with memory constraints?",
        "expected_keywords": ["beam width k", "pruning", "memory bounded", "heuristic"],
        "expected_intent": "concept_research"
    },
    {
        "id": 41,
        "category": "Classical AI Search",
        "question": "Compare A* search with Dijkstra algorithm in terms of node expansions.",
        "expected_keywords": ["heuristic guidance", "goal directed", "fewer node expansions"],
        "expected_intent": "concept_research"
    },
    {
        "id": 42,
        "category": "Classical AI Search",
        "question": "Give a concrete example of an admissible heuristic for pathfinding.",
        "expected_keywords": ["Euclidean distance", "Manhattan distance", "straight line"],
        "expected_intent": "concept_research"
    },

    # Category 6: Logical Reasoning & Forward/Backward Chaining (43-46)
    {
        "id": 43,
        "category": "Logical Reasoning",
        "question": "Explain forward chaining with an example of career rule inference.",
        "expected_keywords": ["data-driven", "antecedents", "facts", "rules", "conclusions"],
        "expected_intent": "concept_research"
    },
    {
        "id": 44,
        "category": "Logical Reasoning",
        "question": "How does backward chaining prove whether a student meets AI Engineer criteria?",
        "expected_keywords": ["goal-driven", "sub-goals", "prerequisites", "hypothesized goal"],
        "expected_intent": "concept_research"
    },
    {
        "id": 45,
        "category": "Logical Reasoning",
        "question": "What is the difference between monotonic and non-monotonic logic in AI?",
        "expected_keywords": ["new facts", "invalidating conclusions", "default reasoning"],
        "expected_intent": "concept_research"
    },
    {
        "id": 46,
        "category": "Logical Reasoning",
        "question": "How can production rules represent academic curriculum constraints?",
        "expected_keywords": ["IF-THEN", "conditions", "prerequisites", "actions"],
        "expected_intent": "concept_research"
    },

    # Category 7: Memory Persistence & Context Recall (47-50)
    {
        "id": 47,
        "category": "Memory",
        "question": "My name is Chitra. I want to become an AI Engineer. I know Python but weak in ML.",
        "expected_keywords": ["Chitra", "AI Engineer", "Python", "Machine Learning", "memory"],
        "expected_intent": "general_tutoring"
    },
    {
        "id": 48,
        "category": "Memory",
        "question": "What is my declared career goal and my top weak topic?",
        "expected_keywords": ["AI Engineer", "Machine Learning", "Statistics"],
        "expected_intent": "general_tutoring"
    },
    {
        "id": 49,
        "category": "Memory",
        "question": "I prefer studying in the evening for 2 hours daily.",
        "expected_keywords": ["Evening", "2 hours", "preference", "stored"],
        "expected_intent": "general_tutoring"
    },
    {
        "id": 50,
        "category": "Memory",
        "question": "What should I focus on next based on everything you remember about me?",
        "expected_keywords": ["AI Engineer", "Machine Learning", "Statistics", "Python"],
        "expected_intent": "study_planning"
    }
]
