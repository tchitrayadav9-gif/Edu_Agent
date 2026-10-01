"""
MCP API Router.
Endpoints for Model Context Protocol interactions and Ollama status check.
"""

from fastapi import APIRouter, Body
from typing import Dict, Any
from ..mcp.server import mcp_server
from ..mcp.tools import MCP_TOOL_DEFINITIONS
from ..llm.ollama_client import ollama_client

router = APIRouter(prefix="/api/mcp", tags=["Model Context Protocol"])


@router.post("/rpc")
def handle_mcp_rpc(request_data: Dict[str, Any] = Body(...)):
    """Handle standard JSON-RPC 2.0 MCP requests."""
    return mcp_server.handle_request(request_data)


@router.get("/tools")
def get_mcp_tools():
    """List available MCP tools."""
    return {"tools": MCP_TOOL_DEFINITIONS}


@router.get("/ollama/status")
async def get_ollama_status():
    """Check if local Ollama daemon is active and return models."""
    return await ollama_client.check_health()
