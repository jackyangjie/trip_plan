"""
MCP Client Configuration for amap-mcp-server
"""

from agentscope.mcp import StdIOStatefulClient
import os


def create_amap_mcp_client() -> StdIOStatefulClient:
    """
    Create Amap MCP client using uvx to run amap-mcp-server.

    Returns:
        StdIOStatefulClient connected to amap-mcp-server
    """
    return StdIOStatefulClient(
        name="amap-mcp-server",
        command="uvx",
        args=["amap-mcp-server"],
        env={
            "AMAP_MAPS_API_KEY": os.getenv("AMAP_API_KEY", ""),
            "UV_HTTP_TIMEOUT": "300",
        },
    )


# MCP server configuration mapping
MCP_SERVERS = {"amap": {"client_factory": create_amap_mcp_client, "enabled": True}}
