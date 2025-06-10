"""MCP server configuration and initialization."""

from typing import Any

from fastmcp import FastMCP

from gemini_claude_code_mcp.tools.summarize_project_tool import register_summarize_project_tool

mcp = FastMCP[Any]('Gemini claude code MCP')

# Register available tools
register_summarize_project_tool(mcp)

__all__ = ['mcp']
