import pytest
from app.agents.planner import PlannerAgent
from app.agents.transport import TransportAgent
from app.agents.budget import BudgetAgent


@pytest.mark.asyncio
async def test_planner_analyze():
    agent = PlannerAgent()
    request = {
        "destinations": ["北京"],
        "start_date": "2024-03-01",
        "end_date": "2024-03-05",
        "travelers": 2,
        "budget": {"total": 5000},
    }

    result = await agent.process({"action": "analyze", "request": request})

    assert result.success == True
    assert result.data["destinations"] == ["北京"]
    assert result.data["duration_days"] == 5
    assert result.data["budget_range"] == "medium"


@pytest.mark.asyncio
async def test_planner_generate():
    agent = PlannerAgent()
    request = {
        "destinations": ["北京"],
        "start_date": "2024-03-01",
        "end_date": "2024-03-05",
        "travelers": 2,
        "budget": {"total": 5000},
    }

    result = await agent.process(
        {"action": "generate", "duration_days": 5, "request": request}
    )

    assert result.success == True
    assert "itinerary" in result.data


@pytest.mark.asyncio
async def test_transport_recommend():
    agent = TransportAgent()
    request = {
        "destinations": ["北京", "上海"],
        "start_date": "2024-03-01",
        "end_date": "2024-03-05",
        "travelers": 2,
    }

    result = await agent.process({"action": "recommend", **request})

    assert result.success == True
    assert "recommendations" in result.data
    assert len(result.data["recommendations"]) > 0


@pytest.mark.asyncio
async def test_budget_analyze():
    agent = BudgetAgent()
    request = {
        "budget": {
            "total": 5000,
            "transport": 1500,
            "accommodation": 1750,
            "food": 1000,
            "activities": 750,
        }
    }

    result = await agent.process({"action": "analyze", "budget": request["budget"]})

    assert result.success == True
    assert "total_budget" in result.data
    assert result.data["total_budget"] == 5000
