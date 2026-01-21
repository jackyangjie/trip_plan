import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


import pytest
from unittest.mock import MagicMock
from app.agentscope_agents.agents.accommodation_agent import create_accommodation_agent


def test_accommodation_agent_creation():
    """Test that accommodation agent can be created"""
    model_config = {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4",
        "api_key": "sk-test-key",
    }

    agent = create_accommodation_agent(model_config)

    assert agent.name == "AccommodationAgent"
    assert "住宿" in agent.sys_prompt


@pytest.mark.asyncio
async def test_accommodation_agent_mcp_tools():
    """Test that MCP tools are available to the agent"""
    from agentscope.tool import Toolkit

    model_config = {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4",
        "api_key": "sk-test-key",
    }

    mock_toolkit = Toolkit()
    mock_toolkit.tools = {
        "amap_search_around": MagicMock(),
        "amap_geocode": MagicMock(),
    }

    agent = create_accommodation_agent(model_config, toolkit=mock_toolkit)

    assert "amap_search_around" in agent.toolkit.tools
    assert "amap_geocode" in agent.toolkit.tools
