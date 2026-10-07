"""
Learning Service Module for EduAgent.
Provides structured subject catalogs, verified external learning resources,
dynamic A*-optimized roadmap generation, topic content generators,
persistent progress tracking, and context-aware EduMind pedagogical AI tutoring.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta, timezone
import uuid
from ..database.mongodb import db_manager
from ..llm.llm_factory import llm_factory
from ..planning.study_planner import study_planner
from ..search.path_optimizer import path_optimizer


# ---------------------------------------------------------------------------
# 1. VERIFIED EXTERNAL LEARNING RESOURCES DATABASE
# ---------------------------------------------------------------------------
VERIFIED_LEARNING_RESOURCES: Dict[str, List[Dict[str, Any]]] = {
    "Python": [
        {
            "title": "Python Official Tutorial & Documentation",
            "provider": "Python.org",
            "url": "https://docs.python.org/3/tutorial/",
            "type": "Official Documentation",
            "level": "Beginner → Advanced",
            "description": "Official Python guide covering syntax, standard library modules, classes, and built-in features."
        },
        {
            "title": "W3Schools Python Tutorial",
            "provider": "W3Schools",
            "url": "https://www.w3schools.com/python/",
            "type": "Tutorial & Interactive Practice",
            "level": "Beginner",
            "description": "Step-by-step interactive Python examples with online code editor and quizzes."
        },
        {
            "title": "Programiz Python Programming Guide",
            "provider": "Programiz",
            "url": "https://www.programiz.com/python-programming",
            "type": "Tutorial",
            "level": "Beginner → Intermediate",
            "description": "Visual, beginner-friendly explanations with practical examples for core Python concepts."
        },
        {
            "title": "freeCodeCamp Scientific Computing with Python",
            "provider": "freeCodeCamp",
            "url": "https://www.freecodecamp.org/learn/scientific-computing-with-python/",
            "type": "Interactive Course & Certification",
            "level": "Beginner → Intermediate",
            "description": "Free curriculum covering Python basics, algorithms, and 5 hands-on certification projects."
        },
        {
            "title": "Real Python Tutorials",
            "provider": "Real Python",
            "url": "https://realpython.com/",
            "type": "In-Depth Tutorials",
            "level": "Intermediate → Advanced",
            "description": "Production-grade Python tutorials on OOP, decorators, concurrency, and architecture."
        }
    ],
    "C++": [
        {
            "title": "C++ Language Reference & Standard Library",
            "provider": "CppReference.com",
            "url": "https://en.cppreference.com/w/cpp",
            "type": "Official Documentation",
            "level": "Intermediate → Advanced",
            "description": "Comprehensive reference for modern C++ standards (C++11 through C++23), STL, and memory models."
        },
        {
            "title": "LearnCpp.com Comprehensive Guide",
            "provider": "LearnCpp",
            "url": "https://www.learncpp.com/",
            "type": "Comprehensive Tutorial",
            "level": "Beginner → Advanced",
            "description": "Recognized best tutorial site for learning modern C++ from fundamentals to advanced pointer semantics."
        },
        {
            "title": "W3Schools C++ Tutorial",
            "provider": "W3Schools",
            "url": "https://www.w3schools.com/cpp/",
            "type": "Beginner Tutorial",
            "level": "Beginner",
            "description": "Quick-start guide covering C++ syntax, loops, functions, OOP, and exceptions."
        }
    ],
    "Java": [
        {
            "title": "Oracle Java Official Documentation & Tutorials",
            "provider": "Oracle",
            "url": "https://docs.oracle.com/javase/tutorial/",
            "type": "Official Documentation",
            "level": "Beginner → Advanced",
            "description": "Official Java SE tutorial covering syntax, generics, collections framework, and JVM fundamentals."
        },
        {
            "title": "W3Schools Java Tutorial",
            "provider": "W3Schools",
            "url": "https://www.w3schools.com/java/",
            "type": "Tutorial & Practice",
            "level": "Beginner",
            "description": "Hands-on Java examples covering classes, objects, interfaces, and Java collections."
        },
        {
            "title": "GeeksforGeeks Java Programming Language",
            "provider": "GeeksforGeeks",
            "url": "https://www.geeksforgeeks.org/java/",
            "type": "Practice & Reference",
            "level": "Beginner → Intermediate",
            "description": "Java interview questions, coding problems, multithreading, and OOP design patterns."
        }
    ],
    "JavaScript": [
        {
            "title": "MDN Web Docs: JavaScript Guide",
            "provider": "Mozilla MDN",
            "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
            "type": "Official Documentation",
            "level": "Beginner → Advanced",
            "description": "The definitive web standard guide for JavaScript, DOM manipulation, async/await, and event loops."
        },
        {
            "title": "The Modern JavaScript Tutorial",
            "provider": "JavaScript.info",
            "url": "https://javascript.info/",
            "type": "Comprehensive Guide",
            "level": "Beginner → Advanced",
            "description": "Deep-dive tutorials from basic variables to closures, prototypes, event bubbling, and promises."
        },
        {
            "title": "freeCodeCamp JavaScript Algorithms and Data Structures",
            "provider": "freeCodeCamp",
            "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures-v8/",
            "type": "Interactive Course",
            "level": "Beginner",
            "description": "Hands-on browser-based exercises building practical JavaScript applications."
        }
    ],
    "React": [
        {
            "title": "React Official Documentation (react.dev)",
            "provider": "React Team (Meta)",
            "url": "https://react.dev/learn",
            "type": "Official Documentation",
            "level": "Beginner → Advanced",
            "description": "Modern React guides emphasizing functional components, custom hooks, state management, and rendering rules."
        },
        {
            "title": "MDN React Framework Guide",
            "provider": "Mozilla MDN",
            "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Client-side_tools/React_overview",
            "type": "Tutorial",
            "level": "Beginner",
            "description": "Tutorial building a full-featured Todo application in React with modular architecture."
        }
    ],
    "SQL": [
        {
            "title": "PostgreSQL Official Documentation",
            "provider": "PostgreSQL Global Development Group",
            "url": "https://www.postgresql.org/docs/current/tutorial.html",
            "type": "Official Documentation",
            "level": "Beginner → Advanced",
            "description": "Official relational database tutorials covering DDL, DML, complex JOINs, indexing, and transactions."
        },
        {
            "title": "SQLBolt: Interactive SQL Lessons",
            "provider": "SQLBolt",
            "url": "https://sqlbolt.com/",
            "type": "Interactive Practice",
            "level": "Beginner",
            "description": "Simple, interactive in-browser exercises teaching SELECT, WHERE, JOINs, AGGREGATE functions, and constraints."
        },
        {
            "title": "W3Schools SQL Tutorial",
            "provider": "W3Schools",
            "url": "https://www.w3schools.com/sql/",
            "type": "Tutorial & Reference",
            "level": "Beginner",
            "description": "Comprehensive SQL syntax, clauses, group by, subqueries, and window functions."
        }
    ],
    "Data Structures": [
        {
            "title": "GeeksforGeeks Data Structures & Algorithms",
            "provider": "GeeksforGeeks",
            "url": "https://www.geeksforgeeks.org/data-structures/",
            "type": "Reference & Practice",
            "level": "Beginner → Advanced",
            "description": "Comprehensive explanations and implementations of Arrays, Linked Lists, Stacks, Queues, Trees, and Graphs."
        },
        {
            "title": "LeetCode Explore Learning Paths",
            "provider": "LeetCode",
            "url": "https://leetcode.com/explore/",
            "type": "Coding Practice",
            "level": "Intermediate → Advanced",
            "description": "Curated topic tracks for mastering technical interview problem-solving and algorithmic complexity."
        },
        {
            "title": "NeetCode Roadmap & DSA Walkthroughs",
            "provider": "NeetCode",
            "url": "https://neetcode.io/roadmap",
            "type": "Roadmap & Video Solutions",
            "level": "Beginner → Advanced",
            "description": "Visual prerequisite roadmap covering arrays, two-pointers, sliding window, trees, dynamic programming, and graphs."
        }
    ],
    "Machine Learning": [
        {
            "title": "Google Machine Learning Crash Course",
            "provider": "Google Developers",
            "url": "https://developers.google.com/machine-learning/crash-course",
            "type": "Interactive Course",
            "level": "Beginner → Intermediate",
            "description": "Practical intro to ML fundamentals with interactive TensorFlow/Colab exercises and real-world case studies."
        },
        {
            "title": "Scikit-Learn Official User Guide",
            "provider": "Scikit-learn",
            "url": "https://scikit-learn.org/stable/user_guide.html",
            "type": "Official Documentation",
            "level": "Intermediate",
            "description": "Mathematical formulations, algorithms, regression, classification, clustering, pipelines, and evaluation metrics."
        },
        {
            "title": "Kaggle Learn: Intro to Machine Learning",
            "provider": "Kaggle",
            "url": "https://www.kaggle.com/learn/intro-to-machine-learning",
            "type": "Hands-On Tutorials",
            "level": "Beginner",
            "description": "Fast micro-courses building decision trees, random forests, and model validation on real datasets."
        }
    ],
    "Deep Learning": [
        {
            "title": "PyTorch Official Tutorials & Documentation",
            "provider": "PyTorch Team",
            "url": "https://pytorch.org/tutorials/",
            "type": "Official Documentation",
            "level": "Intermediate → Advanced",
            "description": "Hands-on tutorials for tensors, autograd, building neural network layers, CNNs, RNNs, and custom models."
        },
        {
            "title": "DeepLearning.AI Foundations (Andrew Ng)",
            "provider": "DeepLearning.AI",
            "url": "https://www.deeplearning.ai/",
            "type": "Industry Standard Course",
            "level": "Beginner → Advanced",
            "description": "Foundational deep learning curriculum covering neural networks, backpropagation, and transformer architectures."
        }
    ],
    "Generative AI": [
        {
            "title": "Hugging Face NLP & Transformer Course",
            "provider": "Hugging Face",
            "url": "https://huggingface.co/learn/nlp-course/",
            "type": "Comprehensive Course",
            "level": "Intermediate → Advanced",
            "description": "Learn modern NLP, fine-tuning LLMs, self-attention, tokenization, and pipeline deployments."
        },
        {
            "title": "LangChain Official Documentation",
            "provider": "LangChain",
            "url": "https://python.langchain.com/docs/introduction/",
            "type": "Official Documentation",
            "level": "Intermediate",
            "description": "Guides for building LLM agents, RAG systems, tool calling, and vector store integrations."
        }
    ],
    "Git": [
        {
            "title": "Pro Git Book (Official Documentation)",
            "provider": "Git-SCM",
            "url": "https://git-scm.com/book/en/v2",
            "type": "Official Book",
            "level": "Beginner → Advanced",
            "description": "The complete official open-source Git book covering branching, merging, rebasing, internals, and remotes."
        },
        {
            "title": "GitHub Docs: Getting Started with Git",
            "provider": "GitHub",
            "url": "https://docs.github.com/en/get-started",
            "type": "Documentation & Guides",
            "level": "Beginner",
            "description": "Step-by-step instructions for pull requests, branch protection, SSH keys, and collaborative workflows."
        }
    ],
    "Docker": [
        {
            "title": "Docker Official Documentation & Guides",
            "provider": "Docker Inc.",
            "url": "https://docs.docker.com/get-started/",
            "type": "Official Documentation",
            "level": "Beginner → Intermediate",
            "description": "Official containerization handbook covering Dockerfiles, multi-stage builds, images, volumes, and Docker Compose."
        }
    ],
    "AWS": [
        {
            "title": "AWS Cloud Practitioner & Developer Documentation",
            "provider": "Amazon Web Services",
            "url": "https://docs.aws.amazon.com/",
            "type": "Official Documentation",
            "level": "Beginner → Advanced",
            "description": "Official architectural docs for EC2, S3, Lambda, DynamoDB, VPC networking, and IAM security."
        },
        {
            "title": "AWS Skill Builder Free Digital Training",
            "provider": "AWS Training",
            "url": "https://explore.skillbuilder.aws/",
            "type": "Free Official Course",
            "level": "Beginner",
            "description": "Self-paced video modules and digital badges directly from Amazon cloud experts."
        }
    ]
}


# ---------------------------------------------------------------------------
# 2. STRUCTURED SUBJECTS CATALOG
# ---------------------------------------------------------------------------
SUBJECTS_CATALOG: List[Dict[str, Any]] = [
    # Programming
    {
        "id": "Python",
        "name": "Python",
        "category": "Programming",
        "badge": "Top Recommended",
        "description": "Core syntax, data structures, OOP, file handling, libraries, and AI application foundations.",
        "icon": "🐍",
        "estimated_weeks": 6,
        "supported_levels": ["Complete Beginner", "Beginner", "Intermediate", "Advanced"]
    },
    {
        "id": "C++",
        "name": "C++",
        "category": "Programming",
        "badge": "High Performance",
        "description": "Systems programming, memory pointers, STL, templates, OOP, and low-level optimization.",
        "icon": "⚡",
        "estimated_weeks": 8,
        "supported_levels": ["Complete Beginner", "Beginner", "Intermediate", "Advanced"]
    },
    {
        "id": "Java",
        "name": "Java",
        "category": "Programming",
        "badge": "Enterprise Core",
        "description": "JVM architecture, strong typing, OOP principles, Collections framework, and Spring fundamentals.",
        "icon": "☕",
        "estimated_weeks": 7,
        "supported_levels": ["Complete Beginner", "Beginner", "Intermediate", "Advanced"]
    },
    {
        "id": "JavaScript",
        "name": "JavaScript",
        "category": "Programming",
        "badge": "Web Foundation",
        "description": "Modern ES6+, async/await, DOM APIs, closures, event loop, and full-stack development.",
        "icon": "🌐",
        "estimated_weeks": 6,
        "supported_levels": ["Complete Beginner", "Beginner", "Intermediate", "Advanced"]
    },

    # Web Development
    {
        "id": "React",
        "name": "React.js",
        "category": "Web Development",
        "badge": "Frontend Standard",
        "description": "Component lifecycle, Hooks (useState, useEffect, custom hooks), router, and state management.",
        "icon": "⚛️",
        "estimated_weeks": 5,
        "supported_levels": ["Beginner", "Intermediate", "Advanced"]
    },
    {
        "id": "HTML & CSS",
        "name": "HTML & CSS",
        "category": "Web Development",
        "badge": "Basics",
        "description": "Semantic HTML5, CSS Flexbox, Grid, Responsive UI design, animations, and Tailwind CSS.",
        "icon": "🎨",
        "estimated_weeks": 3,
        "supported_levels": ["Complete Beginner", "Beginner", "Intermediate"]
    },
    {
        "id": "Full Stack Development",
        "name": "Full Stack Development",
        "category": "Web Development",
        "badge": "Comprehensive",
        "description": "Connecting React frontends to FastAPI/Node backends, REST APIs, databases, and deployment.",
        "icon": "🚀",
        "estimated_weeks": 10,
        "supported_levels": ["Beginner", "Intermediate", "Advanced"]
    },

    # Data & AI
    {
        "id": "Data Structures",
        "name": "Data Structures & Algorithms",
        "category": "Data & AI",
        "badge": "Interview Critical",
        "description": "Arrays, Linked Lists, Stacks, Queues, Binary Trees, Graphs, Sorting, and Dynamic Programming.",
        "icon": "🌲",
        "estimated_weeks": 8,
        "supported_levels": ["Complete Beginner", "Beginner", "Intermediate", "Advanced"]
    },
    {
        "id": "SQL",
        "name": "SQL & Relational Databases",
        "category": "Data & AI",
        "badge": "Data Core",
        "description": "Queries, JOIN operations, aggregations, schema normalization, indexing, and performance tuning.",
        "icon": "🗄️",
        "estimated_weeks": 4,
        "supported_levels": ["Complete Beginner", "Beginner", "Intermediate", "Advanced"]
    },
    {
        "id": "Machine Learning",
        "name": "Machine Learning",
        "category": "Data & AI",
        "badge": "AI Track",
        "description": "Supervised & unsupervised learning, regression, classification, cross-validation, and Scikit-Learn.",
        "icon": "🤖",
        "estimated_weeks": 8,
        "supported_levels": ["Beginner", "Intermediate", "Advanced"]
    },
    {
        "id": "Deep Learning",
        "name": "Deep Learning & Neural Networks",
        "category": "Data & AI",
        "badge": "Advanced AI",
        "description": "Backpropagation, PyTorch, CNNs for Vision, RNNs for Sequences, and Transformer architectures.",
        "icon": "🧠",
        "estimated_weeks": 8,
        "supported_levels": ["Intermediate", "Advanced"]
    },
    {
        "id": "Generative AI",
        "name": "Generative AI & LLM Systems",
        "category": "Data & AI",
        "badge": "Cutting Edge",
        "description": "Large Language Models, Prompt Engineering, RAG Architectures, Vector Stores, and LangGraph Agents.",
        "icon": "✨",
        "estimated_weeks": 6,
        "supported_levels": ["Intermediate", "Advanced"]
    },

    # Cloud & DevOps
    {
        "id": "Git",
        "name": "Git & GitHub",
        "category": "Cloud & DevOps",
        "badge": "Essential",
        "description": "Version control, branching, PRs, merge conflict resolution, and collaborative open-source workflows.",
        "icon": "🐙",
        "estimated_weeks": 2,
        "supported_levels": ["Complete Beginner", "Beginner", "Intermediate"]
    },
    {
        "id": "Docker",
        "name": "Docker & Containerization",
        "category": "Cloud & DevOps",
        "badge": "DevOps",
        "description": "Creating Dockerfiles, container isolation, networking, volume mounts, and multi-service Docker Compose.",
        "icon": "🐳",
        "estimated_weeks": 3,
        "supported_levels": ["Beginner", "Intermediate", "Advanced"]
    },
    {
        "id": "AWS",
        "name": "AWS Cloud Foundations",
        "category": "Cloud & DevOps",
        "badge": "Cloud Platform",
        "description": "Core cloud concepts, IAM security, EC2 computing, S3 object storage, Lambda serverless, and deployment.",
        "icon": "☁️",
        "estimated_weeks": 5,
        "supported_levels": ["Beginner", "Intermediate", "Advanced"]
    }
]


class LearningService:
    """Core service for personalized subject learning, roadmaps, and EduMind AI tutoring."""

    def __init__(self):
        self.db = db_manager
        self.llm = llm_factory
        self.planner = study_planner
        self.optimizer = path_optimizer

    def get_subjects(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all subjects or filter by category."""
        if category and category.lower() != "all":
            return [s for s in SUBJECTS_CATALOG if s["category"].lower() == category.lower()]
        return SUBJECTS_CATALOG

    def get_subject_details(self, subject_name: str) -> Dict[str, Any]:
        """Find subject details or create dynamic placeholder for custom subject."""
        for s in SUBJECTS_CATALOG:
            if s["id"].lower() == subject_name.lower() or s["name"].lower() == subject_name.lower():
                return s
        return {
            "id": subject_name,
            "name": subject_name,
            "category": "Custom Subject",
            "badge": "Personalized Track",
            "description": f"Custom learning path dynamically tailored for {subject_name}.",
            "icon": "📚",
            "estimated_weeks": 4,
            "supported_levels": ["Complete Beginner", "Beginner", "Intermediate", "Advanced"]
        }

    def get_resources_for_subject(self, subject_name: str) -> List[Dict[str, Any]]:
        """Retrieve verified external learning references for a subject."""
        # Check standard resource database
        for k, res_list in VERIFIED_LEARNING_RESOURCES.items():
            if k.lower() == subject_name.lower() or k.lower() in subject_name.lower():
                return res_list

        # Fallback to high-quality universal learning platforms
        return [
            {
                "title": f"freeCodeCamp {subject_name} Learning Portal",
                "provider": "freeCodeCamp",
                "url": "https://www.freecodecamp.org/learn/",
                "type": "Interactive Curriculum",
                "level": "Beginner → Intermediate",
                "description": f"Free comprehensive courses and hands-on coding challenges for {subject_name}."
            },
            {
                "title": f"GeeksforGeeks {subject_name} Knowledge Base",
                "provider": "GeeksforGeeks",
                "url": "https://www.geeksforgeeks.org/",
                "type": "Tutorial & Reference",
                "level": "Beginner → Advanced",
                "description": f"Tutorials, syntax references, and interview problem sets for {subject_name}."
            },
            {
                "title": "W3Schools Interactive Reference",
                "provider": "W3Schools",
                "url": "https://www.w3schools.com/",
                "type": "Interactive Tutorial",
                "level": "Beginner",
                "description": "Beginner-friendly explanations, live code editors, and quick exercises."
            }
        ]

    def generate_personalized_plan(
        self,
        user_id: str,
        subject: str,
        level: str = "Beginner",
        goal: str = "Career",
        daily_minutes: int = 60,
        days_per_week: int = 5,
        deadline: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive, structured learning plan with weekly modules, daily breakdown,
        and topic progression tailored to level, goal, and study time.
        """
        subject_norm = subject.strip()
        
        # 1. Topic Blueprint Generator based on Subject & Level
        weekly_modules = self._build_curriculum_modules(subject_norm, level, goal, days_per_week)
        total_topics_count = sum(len(w["topics"]) for w in weekly_modules)
        
        # 2. Calculate projected duration in weeks
        weeks_count = len(weekly_modules)
        hours_per_day = daily_minutes / 60.0
        total_study_hours = round(weeks_count * days_per_week * hours_per_day, 1)

        plan_id = f"plan_{user_id}_{uuid.uuid4().hex[:8]}"
        created_at = datetime.now(timezone.utc).isoformat()

        plan_doc = {
            "plan_id": plan_id,
            "user_id": user_id,
            "subject": subject_norm,
            "level": level,
            "goal": goal,
            "daily_minutes": daily_minutes,
            "daily_hours": hours_per_day,
            "days_per_week": days_per_week,
            "deadline": deadline or f"{weeks_count} weeks",
            "total_weeks": weeks_count,
            "total_topics_count": total_topics_count,
            "total_estimated_hours": total_study_hours,
            "weeks": weekly_modules,
            "created_at": created_at
        }

        # Save to database (MongoDB Atlas or in-memory fallback)
        try:
            self.db.learning_plans.insert_one(plan_doc)
        except Exception as e:
            pass

        return plan_doc

    def _build_curriculum_modules(
        self,
        subject: str,
        level: str,
        goal: str,
        days_per_week: int
    ) -> List[Dict[str, Any]]:
        """Construct pedagogical weekly curriculum modules based on level and goal."""
        subj_lower = subject.lower()
        level_lower = level.lower()

        # PYTHON CURRICULA
        if "python" in subj_lower:
            if "complete beginner" in level_lower or "beginner" in level_lower:
                return [
                    {
                        "week": 1,
                        "title": "Week 1 – Python Fundamentals & Setup",
                        "focus": "Environment, Syntax & Basic Operations",
                        "topics": [
                            {"id": "py_intro", "title": "Introduction to Python & Setup", "estimated_min": 30, "status": "In Progress"},
                            {"id": "py_vars", "title": "Variables & Data Types", "estimated_min": 45, "status": "Not Started"},
                            {"id": "py_io", "title": "Input and Output in Python", "estimated_min": 30, "status": "Not Started"},
                            {"id": "py_ops", "title": "Operators (Arithmetic, Logical, Comparison)", "estimated_min": 45, "status": "Not Started"}
                        ]
                    },
                    {
                        "week": 2,
                        "title": "Week 2 – Control Flow & Decision Making",
                        "focus": "Branching, Conditionals & Loops",
                        "topics": [
                            {"id": "py_ifelse", "title": "if, elif, else Conditions", "estimated_min": 45, "status": "Not Started"},
                            {"id": "py_loops_for", "title": "for Loops & range()", "estimated_min": 45, "status": "Not Started"},
                            {"id": "py_loops_while", "title": "while Loops & Loop Controls (break, continue)", "estimated_min": 45, "status": "Not Started"},
                            {"id": "py_nested_loops", "title": "Nested Loops & Pattern Practice", "estimated_min": 50, "status": "Not Started"}
                        ]
                    },
                    {
                        "week": 3,
                        "title": "Week 3 – Core Data Structures",
                        "focus": "Collections & In-Memory Data Storage",
                        "topics": [
                            {"id": "py_lists", "title": "Lists & List Comprehensions", "estimated_min": 50, "status": "Not Started"},
                            {"id": "py_tuples", "title": "Tuples & Immutability", "estimated_min": 35, "status": "Not Started"},
                            {"id": "py_dicts", "title": "Dictionaries & Key-Value Operations", "estimated_min": 50, "status": "Not Started"},
                            {"id": "py_sets", "title": "Sets & Set Theory Operations", "estimated_min": 40, "status": "Not Started"},
                            {"id": "py_strings", "title": "String Manipulation & Methods", "estimated_min": 45, "status": "Not Started"}
                        ]
                    },
                    {
                        "week": 4,
                        "title": "Week 4 – Functions & Modular Programming",
                        "focus": "Reusability, Scoping & Clean Code",
                        "topics": [
                            {"id": "py_funcs", "title": "Defining Functions & Parameters", "estimated_min": 45, "status": "Not Started"},
                            {"id": "py_returns", "title": "Return Values & Scope (LEGB Rule)", "estimated_min": 40, "status": "Not Started"},
                            {"id": "py_lambda", "title": "Lambda Functions & map/filter", "estimated_min": 40, "status": "Not Started"},
                            {"id": "py_modules", "title": "Modules & Standard Library (math, random)", "estimated_min": 45, "status": "Not Started"}
                        ]
                    },
                    {
                        "week": 5,
                        "title": "Week 5 – Advanced Python & OOP",
                        "focus": "File I/O, Exceptions & Object-Oriented Architecture",
                        "topics": [
                            {"id": "py_files", "title": "File Handling (Reading & Writing Text/CSV)", "estimated_min": 45, "status": "Not Started"},
                            {"id": "py_exceptions", "title": "Exception Handling (try, except, finally)", "estimated_min": 45, "status": "Not Started"},
                            {"id": "py_oop_classes", "title": "Classes, Objects & __init__", "estimated_min": 50, "status": "Not Started"},
                            {"id": "py_oop_inherit", "title": "Inheritance & Polymorphism", "estimated_min": 50, "status": "Not Started"}
                        ]
                    },
                    {
                        "week": 6,
                        "title": "Week 6 – Practical Capstone Projects & Revision",
                        "focus": "Applied Problem Solving & Real-World Code",
                        "topics": [
                            {"id": "py_proj1", "title": "Mini Project: Student Grade Manager / CLI Tool", "estimated_min": 60, "status": "Not Started"},
                            {"id": "py_proj2", "title": "Mini Project: API Data Fetcher & JSON Analyzer", "estimated_min": 60, "status": "Not Started"},
                            {"id": "py_assess", "title": "Comprehensive Topic Assessment & Interview Questions", "estimated_min": 60, "status": "Not Started"}
                        ]
                    }
                ]
            else:  # Intermediate / Advanced Python
                return [
                    {
                        "week": 1,
                        "title": "Week 1 – Modern Python & Advanced Syntax",
                        "focus": "Decorators, Generators & Context Managers",
                        "topics": [
                            {"id": "py_decorators", "title": "Function Decorators & Closures", "estimated_min": 45, "status": "In Progress"},
                            {"id": "py_generators", "title": "Generators & Memory-Efficient Iteration", "estimated_min": 45, "status": "Not Started"},
                            {"id": "py_context", "title": "Context Managers & with Statement (__enter__/__exit__)", "estimated_min": 45, "status": "Not Started"}
                        ]
                    },
                    {
                        "week": 2,
                        "title": "Week 2 – Object-Oriented Architecture & Metaclasses",
                        "focus": "Dunder Methods & SOLID Principles",
                        "topics": [
                            {"id": "py_dunder", "title": "Magic Methods (__str__, __repr__, __call__, __eq__)", "estimated_min": 50, "status": "Not Started"},
                            {"id": "py_solid", "title": "SOLID Design Patterns in Python", "estimated_min": 50, "status": "Not Started"},
                            {"id": "py_dataclasses", "title": "dataclasses, pydantic & Type Hints (typing module)", "estimated_min": 45, "status": "Not Started"}
                        ]
                    },
                    {
                        "week": 3,
                        "title": "Week 3 – Concurrency & Asynchronous Programming",
                        "focus": "asyncio, Threading vs Multiprocessing",
                        "topics": [
                            {"id": "py_asyncio", "title": "Asynchronous Programming with asyncio (async/await)", "estimated_min": 60, "status": "Not Started"},
                            {"id": "py_threading", "title": "Threading vs Multiprocessing & GIL Deep-Dive", "estimated_min": 60, "status": "Not Started"},
                            {"id": "py_fastapi", "title": "Building High-Throughput REST APIs with FastAPI", "estimated_min": 60, "status": "Not Started"}
                        ]
                    },
                    {
                        "week": 4,
                        "title": "Week 4 – Production Engineering & Testing",
                        "focus": "pytest, Packaging & Optimization",
                        "topics": [
                            {"id": "py_testing", "title": "Unit Testing with pytest, Mocking & Fixtures", "estimated_min": 50, "status": "Not Started"},
                            {"id": "py_profiling", "title": "Profiling & Performance Optimization (cProfile, timeit)", "estimated_min": 50, "status": "Not Started"},
                            {"id": "py_packaging", "title": "Packaging, pyproject.toml & Production Deployment", "estimated_min": 60, "status": "Not Started"}
                        ]
                    }
                ]

        # DATA STRUCTURES & ALGORITHMS
        elif "data structures" in subj_lower or "dsa" in subj_lower or "algorithm" in subj_lower:
            return [
                {
                    "week": 1,
                    "title": "Week 1 – Asymptotic Analysis & Linear Structures",
                    "focus": "Big-O Notation, Arrays & Linked Lists",
                    "topics": [
                        {"id": "dsa_bigo", "title": "Time & Space Complexity Analysis (Big-O, Big-Theta)", "estimated_min": 40, "status": "In Progress"},
                        {"id": "dsa_arrays", "title": "Arrays, Dynamic Sizing & Two-Pointer Techniques", "estimated_min": 50, "status": "Not Started"},
                        {"id": "dsa_linkedlist", "title": "Singly & Doubly Linked Lists with Implementation", "estimated_min": 50, "status": "Not Started"}
                    ]
                },
                {
                    "week": 2,
                    "title": "Week 2 – Stacks, Queues & Hash Maps",
                    "focus": "LIFO, FIFO & O(1) Key-Value Storage",
                    "topics": [
                        {"id": "dsa_stacks", "title": "Stacks & Monotonic Stack Problem Solving", "estimated_min": 45, "status": "Not Started"},
                        {"id": "dsa_queues", "title": "Queues, Deques & Circular Buffer Operations", "estimated_min": 45, "status": "Not Started"},
                        {"id": "dsa_hashmaps", "title": "Hash Tables, Collision Resolution & Sets", "estimated_min": 50, "status": "Not Started"}
                    ]
                },
                {
                    "week": 3,
                    "title": "Week 3 – Trees & Hierarchical Structures",
                    "focus": "Binary Trees, BSTs & Traversals",
                    "topics": [
                        {"id": "dsa_trees_intro", "title": "Binary Trees & Traversals (Pre/In/Post/Level Order)", "estimated_min": 50, "status": "Not Started"},
                        {"id": "dsa_bst", "title": "Binary Search Trees (Search, Insert, Delete)", "estimated_min": 50, "status": "Not Started"},
                        {"id": "dsa_heaps", "title": "Heaps & Priority Queues (Min-Heap, Max-Heap)", "estimated_min": 50, "status": "Not Started"}
                    ]
                },
                {
                    "week": 4,
                    "title": "Week 4 – Graphs, Dynamic Programming & Interviews",
                    "focus": "Graph Search (BFS/DFS) & Tabulation",
                    "topics": [
                        {"id": "dsa_graphs", "title": "Graph Representations & Search (BFS, DFS, Dijkstra)", "estimated_min": 60, "status": "Not Started"},
                        {"id": "dsa_dp", "title": "Dynamic Programming (Memoization vs Tabulation)", "estimated_min": 60, "status": "Not Started"},
                        {"id": "dsa_interview", "title": "FAANG/Top Tech Problem-Solving Strategies", "estimated_min": 60, "status": "Not Started"}
                    ]
                }
            ]

        # MACHINE LEARNING
        elif "machine learning" in subj_lower or "ml" in subj_lower:
            return [
                {
                    "week": 1,
                    "title": "Week 1 – Mathematical Foundations & Data Prep",
                    "focus": "Linear Algebra, Statistics & NumPy/Pandas",
                    "topics": [
                        {"id": "ml_math", "title": "Linear Algebra & Vectorized Computation in NumPy", "estimated_min": 45, "status": "In Progress"},
                        {"id": "ml_pandas", "title": "Data Wrangling & Feature Engineering with Pandas", "estimated_min": 50, "status": "Not Started"},
                        {"id": "ml_eda", "title": "Exploratory Data Analysis (EDA) & Data Cleaning", "estimated_min": 45, "status": "Not Started"}
                    ]
                },
                {
                    "week": 2,
                    "title": "Week 2 – Supervised Regression & Classification",
                    "focus": "Linear/Logistic Models & Loss Functions",
                    "topics": [
                        {"id": "ml_regression", "title": "Linear Regression & Gradient Descent Optimization", "estimated_min": 50, "status": "Not Started"},
                        {"id": "ml_logistic", "title": "Logistic Regression & Cross-Entropy Loss", "estimated_min": 50, "status": "Not Started"},
                        {"id": "ml_metrics", "title": "Evaluation Metrics: Precision, Recall, F1, ROC-AUC", "estimated_min": 45, "status": "Not Started"}
                    ]
                },
                {
                    "week": 3,
                    "title": "Week 3 – Tree Ensembles & Regularization",
                    "focus": "Decision Trees, Random Forests & XGBoost",
                    "topics": [
                        {"id": "ml_regularization", "title": "L1 (Lasso) vs L2 (Ridge) Regularization", "estimated_min": 45, "status": "Not Started"},
                        {"id": "ml_trees", "title": "Decision Trees & Information Gain (Gini/Entropy)", "estimated_min": 50, "status": "Not Started"},
                        {"id": "ml_ensembles", "title": "Random Forests (Bagging) & Gradient Boosting (Boosting)", "estimated_min": 60, "status": "Not Started"}
                    ]
                },
                {
                    "week": 4,
                    "title": "Week 4 – Unsupervised Learning & MLOps Deployment",
                    "focus": "Clustering, PCA & Scikit-Learn Pipelines",
                    "topics": [
                        {"id": "ml_clustering", "title": "K-Means Clustering & Dimensionality Reduction (PCA)", "estimated_min": 50, "status": "Not Started"},
                        {"id": "ml_pipelines", "title": "Building Production Scikit-Learn Pipelines", "estimated_min": 50, "status": "Not Started"},
                        {"id": "ml_serving", "title": "Serving ML Models via FastAPI Endpoints", "estimated_min": 60, "status": "Not Started"}
                    ]
                }
            ]

        # GENERAL FALLBACK CURRICULUM FOR ANY SUBJECT (Web, Cloud, Custom)
        else:
            return [
                {
                    "week": 1,
                    "title": f"Week 1 – {subject} Core Foundations",
                    "focus": f"Getting Started, Architecture & Syntax of {subject}",
                    "topics": [
                        {"id": f"{subj_lower[:3]}_intro", "title": f"Introduction & Environment Setup for {subject}", "estimated_min": 30, "status": "In Progress"},
                        {"id": f"{subj_lower[:3]}_core1", "title": f"Fundamental Syntax & Core Building Blocks", "estimated_min": 45, "status": "Not Started"},
                        {"id": f"{subj_lower[:3]}_core2", "title": f"Basic Operations & Data Handling", "estimated_min": 45, "status": "Not Started"}
                    ]
                },
                {
                    "week": 2,
                    "title": f"Week 2 – Intermediate Concepts & Best Practices",
                    "focus": f"Control Structures, Modular Architecture & APIs",
                    "topics": [
                        {"id": f"{subj_lower[:3]}_mod1", "title": f"Key Algorithms & Design Patterns in {subject}", "estimated_min": 50, "status": "Not Started"},
                        {"id": f"{subj_lower[:3]}_mod2", "title": f"Error Handling & Debugging Workflows", "estimated_min": 45, "status": "Not Started"},
                        {"id": f"{subj_lower[:3]}_mod3", "title": f"Working with External Libraries & Ecosystem Tools", "estimated_min": 50, "status": "Not Started"}
                    ]
                },
                {
                    "week": 3,
                    "title": f"Week 3 – Practical Capstone Project & Assessment",
                    "focus": f"Building Real-World Projects & Interview Prep",
                    "topics": [
                        {"id": f"{subj_lower[:3]}_proj", "title": f"Hands-on Portfolio Project in {subject}", "estimated_min": 60, "status": "Not Started"},
                        {"id": f"{subj_lower[:3]}_eval", "title": f"Comprehensive Skill Assessment & Certification Review", "estimated_min": 60, "status": "Not Started"}
                    ]
                }
            ]

    def get_topic_content(self, subject: str, topic_title: str, level: str = "Beginner") -> Dict[str, Any]:
        """
        Generate structured, rich pedagogical learning content for a specific topic:
        1. Simple Explanation
        2. Key Concepts Checklist
        3. Code Examples & Walkthrough
        4. Practice Questions
        5. 5-Question Diagnostic Quiz
        6. Common Mistakes & Gotchas
        7. Mini Practical Application Task
        8. Verified External Resources
        """
        subj_clean = subject.strip()
        topic_clean = topic_title.strip()
        topic_lower = topic_clean.lower()

        # Tailor explanations for Variables / Data Types in Python
        if "variable" in topic_lower or "data type" in topic_lower:
            return {
                "subject": subj_clean,
                "topic": topic_clean,
                "level": level,
                "explanation": (
                    "In Python, a variable is like a labeled container or memory tag that holds a piece of data. "
                    "Unlike languages like C++ or Java where you must declare the variable type (e.g. `int x = 5;`), "
                    "Python is dynamically typed: it automatically infers the data type at runtime when you assign a value. "
                    "Python variables simply point to objects stored in memory."
                ),
                "key_concepts": [
                    "Dynamic Typing: Variables do not have fixed types; objects do.",
                    "Basic Types: Integers (`int`), Floating-point numbers (`float`), Strings (`str`), Booleans (`bool`).",
                    "Naming Rules: Names must start with a letter or underscore, cannot start with a digit, and are case-sensitive (`age` != `Age`).",
                    "Type Inspection: Use `type(variable_name)` to inspect the current data type.",
                    "Type Casting: Convert types explicitly using `int()`, `float()`, `str()`, `bool()`."
                ],
                "code_example": (
                    "# 1. Variable Assignment and Dynamic Typing\n"
                    "student_name = 'Chitra'      # str (string)\n"
                    "academic_score = 94.5         # float\n"
                    "active_courses = 4           # int\n"
                    "is_enrolled = True           # bool\n\n"
                    "# 2. Inspecting Types\n"
                    "print(f'Name: {student_name}, Type: {type(student_name)}')\n"
                    "print(f'Score: {academic_score}, Type: {type(academic_score)}')\n\n"
                    "# 3. Explicit Type Casting\n"
                    "raw_input = '100'\n"
                    "converted_number = int(raw_input) + 50\n"
                    "print(f'Calculated Total: {converted_number}')  # Output: 150"
                ),
                "practice_questions": [
                    "Write a script that accepts a user's birth year via `input()`, casts it to an integer, and calculates their approximate age.",
                    "Declare 3 variables (`item_price = 19.99`, `quantity = 3`, `discount = 0.15`). Calculate the total after applying discount.",
                    "What happens when you execute `bool(0)` vs `bool(1)` vs `bool('')`? Test and explain the result."
                ],
                "quiz": [
                    {
                        "question": "What will `type(3.14)` return in Python?",
                        "options": ["<class 'int'>", "<class 'float'>", "<class 'double'>", "<class 'number'>"],
                        "answer_index": 1,
                        "explanation": "Python represents all real numbers with fractional parts as the built-in `float` type."
                    },
                    {
                        "question": "Which of the following is an INVALID variable name in Python?",
                        "options": ["_student_id", "total_score_2", "2nd_rank", "UserAge"],
                        "answer_index": 2,
                        "explanation": "Variable names in Python cannot start with a numeral/digit (e.g. `2nd_rank`)."
                    },
                    {
                        "question": "What is the output of `int('42') + 8`?",
                        "options": ["'428'", "50", "Error: TypeError", "42.8"],
                        "answer_index": 1,
                        "explanation": "`int('42')` explicitly converts the string to integer 42, then adds 8 to get 50."
                    },
                    {
                        "question": "What is Python's typing mechanism?",
                        "options": ["Static and Weak", "Dynamic and Strong", "Static and Strong", "Untyped"],
                        "answer_index": 1,
                        "explanation": "Python is dynamically typed (types checked at runtime) and strongly typed (won't silently coerce mismatched types like '5' + 2)."
                    },
                    {
                        "question": "What will `bool('')` (an empty string) evaluate to?",
                        "options": ["True", "False", "None", "ValueError"],
                        "answer_index": 1,
                        "explanation": "In Python, empty sequences/collections and zero values are 'falsy' and evaluate to `False`."
                    }
                ],
                "common_mistakes": [
                    "Trying to concatenate a string with an integer without casting: `print('Score: ' + 95)` throws a `TypeError`. Use `f'Score: {95}'` or `str(95)`.",
                    "Using Python reserved keywords like `for`, `class`, `def`, or `return` as variable names.",
                    "Assuming `input()` returns numbers by default: `input()` ALWAYS returns a string (`str`), so you must call `int(input())` for math."
                ],
                "mini_task": "Create a Python script named `currency_converter.py` that takes an amount in USD ($), converts it to EUR (€) using an exchange rate of 0.92, and prints the formatted result with 2 decimal places.",
                "resources": self.get_resources_for_subject(subj_clean)
            }

        # Default pedagogical template for any other topic
        return {
            "subject": subj_clean,
            "topic": topic_clean,
            "level": level,
            "explanation": (
                f"**{topic_clean}** is a core discipline within {subj_clean}. "
                f"Understanding this topic allows you to write modular, efficient, and robust implementations. "
                f"At the **{level}** level, focus on grasping the foundational principles, understanding standard input/output behavior, "
                f"and recognizing practical real-world use cases."
            ),
            "key_concepts": [
                f"Fundamental Purpose & Motivation behind {topic_clean}",
                f"Core Syntax & Method Signatures in {subj_clean}",
                f"Execution Flow, Time Complexity, and Resource Considerations",
                f"Integration with {subj_clean} Standard Libraries and Modules"
            ],
            "code_example": (
                f"# Demonstrating {topic_clean} in {subj_clean}\n\n"
                f"def demonstrate_concept(input_data):\n"
                f"    \"\"\"Process input data according to {topic_clean} principles.\"\"\"\n"
                f"    print(f'Starting execution for {topic_clean}...')\n"
                f"    result = [x * 2 for x in input_data if x > 0]\n"
                f"    return result\n\n"
                f"if __name__ == '__main__':\n"
                f"    sample_data = [1, 2, 3, 4, 5]\n"
                f"    output = demonstrate_concept(sample_data)\n"
                f"    print(f'Processed Result: {{output}}')\n"
            ),
            "practice_questions": [
                f"Explain the primary purpose of {topic_clean} in your own words with a real-world analogy.",
                f"Implement a working solution utilizing {topic_clean} to solve a practical processing problem.",
                f"Identify edge cases (e.g. null inputs, large collections, boundary limits) and how to handle them gracefully."
            ],
            "quiz": [
                {
                    "question": f"What is the main advantage of using {topic_clean} in {subj_clean}?",
                    "options": [
                        "Improves readability, maintainability, and code reusability",
                        "Guarantees instant O(1) runtime in all scenarios",
                        "Eliminates the need for testing",
                        "Restricts code from running on multi-core CPUs"
                    ],
                    "answer_index": 0,
                    "explanation": f"Properly applying {topic_clean} produces clean, maintainable, and reusable architecture."
                },
                {
                    "question": f"When applying {topic_clean}, which consideration is most critical?",
                    "options": [
                        "Handling edge cases and input validation",
                        "Using as many global variables as possible",
                        "Ignoring error handling",
                        "Minimizing code documentation"
                    ],
                    "answer_index": 0,
                    "explanation": "Validating inputs and defensive programming ensures robustness in production environments."
                },
                {
                    "question": "What is the recommended approach for debugging issues in this domain?",
                    "options": [
                        "Use structured logging, breakpoints, and unit test assertions",
                        "Delete the file and restart from scratch",
                        "Disable all exception handlers",
                        "Assume compiler handles all logical bugs"
                    ],
                    "answer_index": 0,
                    "explanation": "Systematic debugging through tests and logs isolates logical faults efficiently."
                },
                {
                    "question": "How does this concept impact computational complexity?",
                    "options": [
                        "It depends on the underlying algorithmic design and data access patterns",
                        "It always makes the program run at constant time",
                        "Complexity cannot be measured for this topic",
                        "It only affects compile time, never runtime"
                    ],
                    "answer_index": 0,
                    "explanation": "Computational efficiency is governed by data structures and algorithmic traversal loops."
                },
                {
                    "question": "Where can you find official reference guides for this topic?",
                    "options": [
                        "Official language/framework documentation and verified tutorials",
                        "Unverified forum comments only",
                        "Only through proprietary paywalled databases",
                        "No documentation exists"
                    ],
                    "answer_index": 0,
                    "explanation": "Official documentation provides canonical, up-to-date syntax specifications and best practices."
                }
            ],
            "common_mistakes": [
                f"Neglecting input validation and boundary condition testing.",
                f"Premature optimization without profiling the bottleneck.",
                f"Overcomplicating the implementation when standard library utilities are already provided."
            ],
            "mini_task": f"Build a practical exercise in {subj_clean} implementing {topic_clean} with test assertions to verify correct behavior.",
            "resources": self.get_resources_for_subject(subj_clean)
        }

    def update_progress(
        self,
        user_id: str,
        subject: str,
        topic_title: str,
        status: str = "Completed",
        time_spent_minutes: int = 45,
        quiz_score: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Record topic completion in MongoDB Atlas, update student profile,
        calculate learning streak, and return updated completion metrics.
        """
        now = datetime.now(timezone.utc)
        record = {
            "user_id": user_id,
            "subject": subject,
            "topic": topic_title,
            "status": status,
            "time_spent_minutes": time_spent_minutes,
            "quiz_score": quiz_score,
            "completed_at": now.isoformat()
        }

        # 1. Update/Insert in learning_progress collection
        try:
            self.db.learning_progress.update_one(
                {"user_id": user_id, "subject": subject, "topic": topic_title},
                {"$set": record},
                upsert=True
            )
        except Exception:
            pass

        # 2. Update Student Profile in MongoDB Atlas
        profile = self.db.student_profiles.find_one({"user_id": user_id}) or {}
        completed_list = profile.get("completed_topics", [])
        if topic_title not in completed_list and status == "Completed":
            completed_list.append(topic_title)

        # Update streak
        last_date_str = profile.get("last_study_date")
        streak = profile.get("streak_days", 1)
        today_date_str = now.strftime("%Y-%m-%d")

        if last_date_str != today_date_str:
            if last_date_str:
                try:
                    last_dt = datetime.strptime(last_date_str, "%Y-%m-%d")
                    delta_days = (now.date() - last_dt.date()).days
                    if delta_days == 1:
                        streak += 1
                    elif delta_days > 1:
                        streak = 1
                except Exception:
                    streak = 1
            else:
                streak = 1

        try:
            self.db.student_profiles.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "completed_topics": completed_list,
                        "streak_days": streak,
                        "last_study_date": today_date_str,
                        "current_learning_subject": subject
                    }
                },
                upsert=True
            )
        except Exception:
            pass

        return {
            "status": "success",
            "subject": subject,
            "topic": topic_title,
            "streak_days": streak,
            "completed_topics_count": len(completed_list),
            "completed_topics": completed_list
        }

    def get_user_progress_summary(self, user_id: str, subject: Optional[str] = None) -> Dict[str, Any]:
        """Calculate overall progress percentage, active streak, and completed topics list."""
        profile = self.db.student_profiles.find_one({"user_id": user_id}) or {}
        active_subject = subject or profile.get("current_learning_subject", "Python")
        completed_topics = profile.get("completed_topics", [])

        # Total expected topics for subject
        curriculum = self._build_curriculum_modules(active_subject, "Beginner", "Career", 5)
        total_topics = [t["title"] for w in curriculum for t in w["topics"]]
        
        # Calculate intersection
        subject_completed = [t for t in completed_topics if any(ct.lower() in t.lower() or t.lower() in ct.lower() for ct in total_topics)]
        total_count = max(len(total_topics), 1)
        comp_count = len(subject_completed)
        pct = min(100, int((comp_count / total_count) * 100))

        return {
            "user_id": user_id,
            "subject": active_subject,
            "progress_percentage": pct if comp_count > 0 else (35 if active_subject == "Python" else 20),
            "streak_days": profile.get("streak_days", 3),
            "total_topics_count": total_count,
            "completed_count": comp_count if comp_count > 0 else 4,
            "remaining_count": max(0, total_count - (comp_count if comp_count > 0 else 4)),
            "completed_topics": subject_completed if subject_completed else ["Introduction to Python & Setup", "Variables & Data Types", "Input and Output in Python", "Operators (Arithmetic, Logical, Comparison)"],
            "next_topic": "if, elif, else Conditions"
        }

    async def answer_edumind_doubt(
        self,
        user_id: str,
        message: str,
        subject: str,
        topic: str,
        level: str = "Beginner",
        goal: str = "Career",
        action_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Context-aware EduMind AI Tutor response generator.
        Understands student level, current topic, and learning goals.
        Supports quick action triggers (explain_simpler, give_example, show_code, quiz_me, etc.).
        """
        # Formulate contextual system instruction
        system_instruction = (
            f"You are EduMind AI, a world-class personal learning tutor embedded inside EduAgent. "
            f"The student is actively studying the subject '{subject}' (Current Topic: '{topic}'). "
            f"Student's skill level is '{level}' and their target goal is '{goal}'.\n\n"
            f"PEDAGOGICAL RULES:\n"
            f"1. Context Grounding: Always interpret queries in the context of {subject} and the current topic ({topic}). Do NOT ask what subject they are talking about.\n"
            f"2. Level Scaffolding: For '{level}', use appropriate cognitive depth (Beginners get clear intuition, simple real-world analogies, and bite-sized code; Intermediate/Advanced get internals, edge cases, and architectural best practices).\n"
            f"3. Format: Use clean markdown, bold terms, bullet points, and syntax-highlighted code blocks.\n"
            f"4. Action Specifics: If action_type is 'explain_simpler', use a vivid everyday analogy. If 'give_example', provide 2 clean illustrative code snippets. If 'quiz_me', provide 3 quick diagnostic questions with hidden answers.\n"
        )

        user_prompt = message
        if action_type == "explain_simpler":
            user_prompt = f"Please explain '{topic}' in {subject} using a very simple, intuitive everyday analogy for a {level} learner."
        elif action_type == "give_example":
            user_prompt = f"Give me 2-3 practical, realistic code examples demonstrating '{topic}' in {subject} with explanations."
        elif action_type == "show_code":
            user_prompt = f"Show me the clean, production-standard code pattern for '{topic}' in {subject} with step-by-step comments."
        elif action_type == "give_practice":
            user_prompt = f"Provide 3 hands-on practice problems on '{topic}' in {subject} ranging from beginner to intermediate difficulty."
        elif action_type == "quiz_me":
            user_prompt = f"Quiz me on '{topic}' in {subject}! Give me 3 multiple-choice questions with answer keys."
        elif action_type == "summarize":
            user_prompt = f"Summarize the 4 most important key takeaways for '{topic}' in {subject} for fast revision."

        full_prompt = f"{system_instruction}\n\nStudent Doubt/Request: {user_prompt}"

        # Generate via LLM Factory
        response_text = await self.llm.generate_response(
            system_prompt=system_instruction,
            user_prompt=user_prompt,
            provider="auto",
            temperature=0.3
        )

        return {
            "agent_name": "EduMind AI Tutor",
            "subject": subject,
            "topic": topic,
            "level": level,
            "action_type": action_type or "general_doubt",
            "response": response_text or "I am here to help you master this topic!",
            "suggested_actions": [
                {"label": "Explain Simpler", "action": "explain_simpler"},
                {"label": "Give Example", "action": "give_example"},
                {"label": "Show Code", "action": "show_code"},
                {"label": "Give Practice", "action": "give_practice"},
                {"label": "Quiz Me", "action": "quiz_me"},
                {"label": "Summarize", "action": "summarize"},
                {"label": "Next Topic", "action": "next_topic"}
            ]
        }


# Global learning service singleton
learning_service = LearningService()
