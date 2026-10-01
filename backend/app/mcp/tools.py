"""
MCP Tool handlers and metadata descriptors.
Provides handlers for standard MCP server endpoints.
"""

from typing import Dict, List, Any
from ..tools.agent_tools import (
    get_student_profile,
    get_student_skills,
    get_learning_progress,
    get_career_goal,
    search_documents,
    generate_study_plan,
    get_interview_questions,
    update_learning_progress
)

MCP_TOOL_DEFINITIONS = [
    {
        "name": "get_student_profile",
        "description": "Get student academic year, branch, career goal, and profile overview.",
        "inputSchema": {
            "type": "object",
            "properties": {"user_id": {"type": "string", "description": "Student User ID"}},
            "required": ["user_id"]
        }
    },
    {
        "name": "get_student_skills",
        "description": "Fetch current evaluated skill proficiency levels.",
        "inputSchema": {
            "type": "object",
            "properties": {"user_id": {"type": "string", "description": "Student User ID"}},
            "required": ["user_id"]
        }
    },
    {
        "name": "get_learning_progress",
        "description": "Retrieve curriculum module completion percentages.",
        "inputSchema": {
            "type": "object",
            "properties": {"user_id": {"type": "string", "description": "Student User ID"}},
            "required": ["user_id"]
        }
    },
    {
        "name": "get_career_goal",
        "description": "Get active target career goal for student.",
        "inputSchema": {
            "type": "object",
            "properties": {"user_id": {"type": "string", "description": "Student User ID"}},
            "required": ["user_id"]
        }
    },
    {
        "name": "search_resources",
        "description": "Search student notes, course PDFs, and textbook chunks using semantic RAG.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query or concept"},
                "user_id": {"type": "string", "description": "Student User ID"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_interview_questions",
        "description": "Retrieve adaptive mock technical interview questions by topic.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "Technical topic (e.g. ML, Python, AI)"},
                "difficulty": {"type": "string", "description": "Difficulty (Easy, Medium, Hard)"}
            }
        }
    },
    {
        "name": "create_study_plan",
        "description": "Generate an optimized 30-day personalized study schedule.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "Student User ID"},
                "career_goal": {"type": "string", "description": "Target Career Goal"},
                "daily_hours": {"type": "number", "description": "Daily study hours (e.g. 2.0)"}
            },
            "required": ["user_id"]
        }
    },
    {
        "name": "update_progress",
        "description": "Update learning completion progress for a specific topic.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "Student User ID"},
                "topic": {"type": "string", "description": "Topic Name"},
                "progress": {"type": "integer", "description": "Progress percent (0-100)"}
            },
            "required": ["user_id", "topic", "progress"]
        }
    }
]


def execute_mcp_tool(name: str, arguments: Dict[str, Any]) -> Any:
    """Dispatch execution of an MCP tool."""
    if name == "get_student_profile":
        return get_student_profile(arguments.get("user_id", "default_user"))
    elif name == "get_student_skills":
        return get_student_skills(arguments.get("user_id", "default_user"))
    elif name == "get_learning_progress":
        return get_learning_progress(arguments.get("user_id", "default_user"))
    elif name == "get_career_goal":
        return get_career_goal(arguments.get("user_id", "default_user"))
    elif name == "search_resources":
        return search_documents(arguments.get("query", ""), arguments.get("user_id"))
    elif name == "get_interview_questions":
        return get_interview_questions(arguments.get("topic", "Machine Learning"), arguments.get("difficulty", "Medium"))
    elif name == "create_study_plan":
        return generate_study_plan(arguments.get("user_id", "default_user"), arguments.get("career_goal"), arguments.get("daily_hours", 2.0))
    elif name == "update_progress":
        return update_learning_progress(arguments.get("user_id", "default_user"), arguments.get("topic", "Python"), arguments.get("progress", 50))
    else:
        raise ValueError(f"Unknown MCP Tool: {name}")
