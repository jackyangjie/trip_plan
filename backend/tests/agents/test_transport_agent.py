import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from app.agentscope_agents.agents.transport_agent import create_transport_agent


def test_transport_agent_creation():
    """Test that transport agent can be created with valid config"""
    model_config = {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4",
        "api_key": "sk-test-key",
    }

    agent = create_transport_agent(model_config)

    assert agent.name == "TransportAgent"
    assert "交通" in agent.sys_prompt
    assert agent.max_iters == 20


@pytest.mark.asyncio
async def test_transport_agent_toolkit_injection():
    """Test that toolkit with MCP tools is injected correctly"""
    from agentscope.tool import Toolkit

    model_config = {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4",
        "api_key": "sk-test-key",
    }

    # Create mock toolkit with MCP tools
    mock_toolkit = Toolkit()
    mock_toolkit.tools = {
        "amap_geocode": MagicMock(),
        "amap_route_planning": MagicMock(),
    }

    agent = create_transport_agent(model_config, toolkit=mock_toolkit)

    # Verify toolkit was injected
    assert agent.toolkit is not None
    assert len(agent.toolkit.tools) > 0
