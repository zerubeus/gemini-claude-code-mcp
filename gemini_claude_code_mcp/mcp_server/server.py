"""MCP server configuration and initialization."""

from typing import Any

from fastmcp import FastMCP

from gemini_claude_code_mcp.tools.code_explain_tool import register_code_explain_tools

mcp = FastMCP[Any]('Gemini claude code MCP')

register_code_explain_tools(mcp)

__all__ = ['mcp']
