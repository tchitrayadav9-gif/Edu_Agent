"""
MCP (Model Context Protocol) JSON-RPC Schemas and Definitions.
Defines standard MCP Tool, Resource, and Prompt descriptor structures.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class MCPToolParameter(BaseModel):
    type: str = "string"
    description: Optional[str] = None
    required: bool = False
    default: Optional[Any] = None


class MCPToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Optional[Dict[str, Any]] = None
    id: Optional[str] = "1"


class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[str] = "1"
