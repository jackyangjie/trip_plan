import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from app.agentscope_agents.coordinator import AgentCoordinator


def test_coordinator_initialization():
    """Test that coordinator can be initialized"""
    model_configs = {
        "transport": {"model": "gpt-4", "api_key": "sk-test"},
        "accommodation": {"model": "gpt-4", "api_key": "sk-test"},
        "attraction": {"model": "gpt-4", "api_key": "sk-test"},
        "food": {"model": "gpt-4", "api_key": "sk-test"},
        "budget": {"model": "gpt-4", "api_key": "sk-test"},
        "planner": {"model": "gpt-4", "api_key": "sk-test"},
    }

    coordinator = AgentCoordinator(model_configs)

    assert coordinator.model_configs == model_configs
    assert not coordinator._is_initialized


@pytest.mark.asyncio
async def test_coordinator_with_mcp_initialization():
    """Test coordinator initialization with MCP clients"""
    from agentscope.mcp import StdIOStatefulClient

    model_configs = {
        "transport": {"model": "gpt-4", "api_key": "sk-test"},
        "accommodation": {"model": "gpt-4", "api_key": "sk-test"},
        "attraction": {"model": "gpt-4", "api_key": "sk-test"},
        "food": {"model": "gpt-4", "api_key": "sk-test"},
        "budget": {"model": "gpt-4", "api_key": "sk-test"},
        "planner": {"model": "gpt-4", "api_key": "sk-test"},
    }

    coordinator = AgentCoordinator(model_configs)

    # Mock MCP client with is_connected attribute
    mock_mcp_client = MagicMock(spec=StdIOStatefulClient)
    mock_mcp_client.is_connected = True

    # Initialize with MCP
    await coordinator.initialize(mcp_clients={"amap": mock_mcp_client})

    assert coordinator._is_initialized
