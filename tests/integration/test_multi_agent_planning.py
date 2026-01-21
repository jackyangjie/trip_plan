"""
Integration test for multi-agent planning workflow
"""
import pytest
from unittest.mock import MagicMock, AsyncMock, patch


@pytest.mark.asyncio
async def test_full_planning_workflow():
    """Test complete multi-agent planning workflow"""
    # Mock all dependencies
    with patch('app.main.create_amap_mcp_client') as mock_create_mcp:
        mock_mcp = AsyncMock()
        mock_create_mcp.return_value = mock_mcp
        
        # Test planning flow
        from app.agentscope_agents.coordinator import AgentCoordinator
        
        model_configs = {
            "transport": {"model": "gpt-4", "api_key": "sk-test"},
            "accommodation": {"model": "gpt-4", "api_key": "sk-test"},
            "attraction": {"model": "gpt-4", "api_key": "sk-test"},
            "food": {"model": "gpt-4", "api_key": "sk-test"},
            "budget": {"model": "gpt-4", "api_key": "sk-test"},
            "planner": {"model": "gpt-4", "api_key": "sk-test"},
        }
        
        # Initialize without real MCP
        await coordinator.initialize(mcp_clients=None)
        
        # Test trip planning
        trip_data = {
            "title": "Test Trip",
            "destinations": ["Tokyo"],
            "start_date": "2026-03-01",
            "end_date": "2026-03-07",
            "travelers": 2,
            "budget": {"total": 20000},
            "preferences": {}
        }
        
        result = await coordinator.plan_trip(trip_data)
        
        assert result["success"] == True
        assert "transport" in result
        assert "accommodation" in result
        assert "attractions" in result
        assert "food" in result
        assert "budget" in result
        assert "final_itinerary" in result
