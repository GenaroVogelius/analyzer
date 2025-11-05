"""
Main MCP tools registration module.
This module imports and registers all MCP tools from various modules.
"""

from fastmcp import FastMCP

from app.infrastructure.mcp.postgresql.tools.tools import (
    register_tools as register_postgresql_tools,
)


def register_tools(mcp: FastMCP) -> None:
    """
    Register all MCP tools with the FastMCP instance.
    This function aggregates tool registrations from all modules.
    """
    # Register PostgreSQL tools
    register_postgresql_tools(mcp)
