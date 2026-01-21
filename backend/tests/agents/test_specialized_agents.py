import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


import pytest
from app.agentscope_agents.agents import (
    create_transport_agent,
    create_accommodation_agent,
    create_attraction_agent,
    create_food_agent,
    create_budget_agent,
    create_planner_agent,
)


def test_all_agents_creation():
    """Test that all specialized agents can be created"""
    model_config = {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4",
        "api_key": "sk-test-key",
    }

    agents = [
        create_transport_agent(model_config),
        create_accommodation_agent(model_config),
        create_attraction_agent(model_config),
        create_food_agent(model_config),
        create_budget_agent(model_config),
        create_planner_agent(model_config),
    ]

    assert len(agents) == 6
    assert all(agent.name.endswith("Agent") for agent in agents)

    expected_names = [
        "TransportAgent",
        "AccommodationAgent",
        "AttractionAgent",
        "FoodAgent",
        "BudgetAgent",
        "PlannerAgent",
    ]

    actual_names = [agent.name for agent in agents]
    assert actual_names == expected_names


def test_all_agents_have_unique_prompts():
    """Test that each agent has a specialized system prompt"""
    model_config = {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4",
        "api_key": "sk-test-key",
    }

    agents = [
        create_transport_agent(model_config),
        create_accommodation_agent(model_config),
        create_attraction_agent(model_config),
        create_food_agent(model_config),
        create_budget_agent(model_config),
        create_planner_agent(model_config),
    ]

    prompts = [agent.sys_prompt for agent in agents]

    # All prompts should be unique
    assert len(set(prompts)) == len(prompts)

    # Each prompt should mention its specialty
    assert "交通" in prompts[0]
    assert "住宿" in prompts[1]
    assert "景点" in prompts[2]
    assert "美食" in prompts[3]
    assert "预算" in prompts[4]
    assert "整合" in prompts[5] or "协调" in prompts[5]
