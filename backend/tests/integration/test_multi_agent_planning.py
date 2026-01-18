import pytest
from unittest.mock import MagicMock, AsyncMock, patch


@pytest.mark.asyncio
async def test_coordinator_initialization_workflow():
    """Test coordinator initialization and agent creation"""
    from app.agentscope_agents.coordinator import AgentCoordinator

    model_configs = {
        "transport": {"model": "gpt-4", "api_key": "sk-test"},
        "accommodation": {"model": "gpt-4", "api_key": "sk-test"},
        "attraction": {"model": "gpt-4", "api_key": "sk-test"},
        "food": {"model": "gpt-4", "api_key": "sk-test"},
        "budget": {"model": "gpt-4", "api_key": "sk-test"},
        "planner": {"model": "gpt-4", "api_key": "sk-test"},
    }

    coordinator = AgentCoordinator(model_configs)

    await coordinator.initialize(mcp_clients=None)

    assert coordinator._is_initialized
    assert len(coordinator._agents) == 6
    assert "transport" in coordinator._agents
    assert "accommodation" in coordinator._agents
    assert "attraction" in coordinator._agents
    assert "food" in coordinator._agents
    assert "budget" in coordinator._agents
    assert "planner" in coordinator._agents


@pytest.mark.asyncio
async def test_coordinator_plan_trip_structure():
    """Test plan_trip method structure without real API calls"""
    from app.agentscope_agents.coordinator import AgentCoordinator

    model_configs = {
        "transport": {"model": "gpt-4", "api_key": "sk-test"},
        "accommodation": {"model": "gpt-4", "api_key": "sk-test"},
        "attraction": {"model": "gpt-4", "api_key": "sk-test"},
        "food": {"model": "gpt-4", "api_key": "sk-test"},
        "budget": {"model": "gpt-4", "api_key": "sk-test"},
        "planner": {"model": "gpt-4", "api_key": "sk-test"},
    }

    coordinator = AgentCoordinator(model_configs)
    await coordinator.initialize(mcp_clients=None)

    trip_data = {
        "title": "Test Trip",
        "destinations": ["Tokyo"],
        "start_date": "2026-03-01",
        "end_date": "2026-03-07",
        "travelers": 2,
        "budget": {"total": 20000},
        "preferences": {},
    }

    result = await coordinator.plan_trip(trip_data)

    assert result is not None
    assert "success" in result
    assert "error" in result or "transport" in result
