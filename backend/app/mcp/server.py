"""
MCP (Model Context Protocol) Server for EduAgent.
Exposes JSON-RPC 2.0 endpoints for tool discovery ('tools/list') and execution ('tools/call').
"""

import logging
from typing import Dict, Any, Optional
from .schemas import MCPRequest, MCPResponse
from .tools import MCP_TOOL_DEFINITIONS, execute_mcp_tool

logger = logging.getLogger("edumind.mcp.server")


class MCPServer:
    """Model Context Protocol server implementation."""
    
    def __init__(self, name: str = "edumind-mcp-server", version: str = "1.0.0"):
        self.name = name
        self.version = version

    def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming MCP JSON-RPC 2.0 message."""
        req_id = request_data.get("id", "1")
        method = request_data.get("method", "")
        params = request_data.get("params", {}) or {}

        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": self.name, "version": self.version},
                        "capabilities": {"tools": {}}
                    }
                }

            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": MCP_TOOL_DEFINITIONS
                    }
                }

            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                if not tool_name:
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32602, "message": "Missing 'name' in tools/call parameters"}
                    }
                
                result = execute_mcp_tool(tool_name, arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": str(result)
                            }
                        ],
                        "data": result,
                        "isError": False
                    }
                }

            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }

        except Exception as e:
            logger.error(f"MCP server error processing {method}: {e}")
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32603, "message": str(e)}
            }


# Global MCP server instance
mcp_server = MCPServer()
