# Multi-Agent Travel Planning System Guide

## Overview

This is a multi-agent travel planning system built with AgentScope framework. It uses 6 specialized agents that collaborate to generate comprehensive travel itineraries.

## Architecture

### Components

- **AgentScope Framework**: Core framework for building AI agents
- **ReActAgent**: Reasoning agents that can call tools automatically
- **Toolkit**: Manages MCP (Model Context Protocol) tool integration
- **MsgHub**: Coordinates multi-agent communication
- **amap-mcp-server**: Provides real-time map services via MCP

### Specialized Agents

1. **TransportAgent**: Recommends transportation options (flights, trains, etc.)
2. **AccommodationAgent**: Suggests hotels and accommodations
3. **AttractionAgent**: Recommends attractions and activities
4. **FoodAgent**: Suggests restaurants and local cuisine
5. **BudgetAgent**: Analyzes and optimizes trip budget
6. **PlannerAgent**: Coordinates all recommendations into final itinerary

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# AI Models (choose one or multiple)
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4
OPENAI_API_KEY=sk-your-openai-key

# Amap Maps API (required for map services)
AMAP_API_KEY=your-amap-maps-api-key

# Optional: Anthropic
ANTHROPIC_BASE_URL=https://api.anthropic.com/v1
ANTHROPIC_MODEL=claude-3-sonnet-20240229
ANTHROPIC_API_KEY=your-anthropic-key

# Optional: Tongyi (Alibaba Qwen)
TONGYI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
TONGYI_MODEL=qwen-max
TONGYI_API_KEY=your-tongyi-key
```

### MCP Server Setup

The system uses `amap-mcp-server` via stdio for map services:

```bash
# The MCP client is automatically created by create_amap_mcp_client()
# Make sure AMAP_API_KEY is set in environment
```

## Usage

### Backend API

Start the FastAPI server:

```bash
cd backend
python -m uvicorn main:app --reload
```

### AI Trip Planning Endpoint

POST `/trips/ai-plan`

Sends SSE (Server-Sent Events) stream with planning progress:

```json
{
  "title": "Tokyo Trip",
  "destinations": ["Tokyo"],
  "start_date": "2026-03-01",
  "end_date": "2026-03-07",
  "travelers": 2,
  "budget": {"total": 20000},
  "preferences": {}
}
```

**Response Stream:**

1. Initialization step (5% progress)
2. Trip creation (10% progress)
3. Agent initialization (15% progress)
4. Transport recommendations (30-40% progress)
5. Accommodation recommendations (50-60% progress)
6. Attraction recommendations (70-80% progress)
7. Food recommendations (85-90% progress)
8. Budget analysis (95-98% progress)
9. Itinerary generation (99% progress)
10. Complete (100% progress) - Returns full trip object

### Agent-Only Usage

You can use agents directly in Python:

```python
from app.agentscope_agents import AgentCoordinator
from app.ai_providers import get_provider_config

# Get model configuration
ai_config = get_provider_config("openai")

# Create coordinator
model_configs = {
    "transport": ai_config,
    "accommodation": ai_config,
    "attraction": ai_config,
    "food": ai_config,
    "budget": ai_config,
    "planner": ai_config,
}

coordinator = AgentCoordinator(model_configs)
await coordinator.initialize(mcp_clients={"amap": mcp_client})

# Plan a trip
trip_data = {
    "title": "My Trip",
    "destinations": ["Paris"],
    "start_date": "2026-06-01",
    "end_date": "2026-06-07",
    "travelers": 2,
    "budget": {"total": 5000},
    "preferences": {"interests": ["art", "food"]}
}

result = await coordinator.plan_trip(trip_data)

print(result["success"])  # True
print(result["final_itinerary"])  # Complete itinerary
```

## Agent Workflow

1. **Initialize**: Coordinator creates all 6 agents with ReAct reasoning
2. **Inject MCP Tools**: Agents receive map tools (geocode, search, routing)
3. **Broadcast Task**: MsgHub sends planning task to all agents
4. **Parallel Execution**: Each agent processes their specialty:
   - TransportAgent queries route planning
   - AccommodationAgent searches hotels
   - AttractionAgent finds attractions
   - FoodAgent recommends restaurants
   - BudgetAgent analyzes costs
5. **Consolidate**: PlannerAgent combines all recommendations
6. **Generate**: Final itinerary with daily schedule
7. **Return**: Complete trip with all recommendations

## MCP Tool Integration

Agents automatically call these tools via ReAct reasoning:

- `amap_geocode`: Convert addresses to coordinates
- `amap_route_planning`: Plan routes between locations
- `amap_search_around`: Find POIs around a location (hotels, restaurants, attractions)

The toolkit is injected into agents during initialization:

```python
# In coordinator.py
amap_toolkit = Toolkit()
await amap_toolkit.register_mcp_client(mcp_client)

# Inject into agents
create_transport_agent(model_config, toolkit=amap_toolkit)
```

## Testing

Run all tests:

```bash
cd backend
pytest tests/ -v
```

Run specific test suites:

```bash
# Agent tests
pytest tests/agents/ -v

# Integration tests
pytest tests/integration/ -v

# Specific test
pytest tests/agents/test_transport_agent.py::test_transport_agent_creation -v
```

## Troubleshooting

### AgentScope Import Errors

If you see `ModuleNotFoundError: No module named 'agentscope'`:

```bash
pip install agentscope[full]
```

### MCP Client Connection Issues

Check that `AMAP_API_KEY` is set and valid:

```bash
echo $AMAP_API_KEY
```

### Agent Not Calling Tools

Verify toolkit injection in coordinator initialization:

```python
await coordinator.initialize(mcp_clients={"amap": mcp_client})
```

### API Model Configuration Issues

Check model config format:

```python
{
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4",
    "api_key": "sk-..."
}
```

## Project Structure

```
backend/
├── app/
│   ├── agentscope_agents/          # Multi-agent system
│   │   ├── coordinator.py        # Agent coordination
│   │   ├── mcp_config.py        # MCP client config
│   │   ├── agents/              # Specialized agents
│   │   │   ├── base_agent.py   # ReActAgent factory
│   │   │   ├── transport_agent.py
│   │   │   ├── accommodation_agent.py
│   │   │   ├── attraction_agent.py
│   │   │   ├── food_agent.py
│   │   │   ├── budget_agent.py
│   │   │   └── planner_agent.py
│   │   └── __init__.py
│   │   └── __init__.py
│   ├── api_models.py             # Pydantic models
│   ├── ai_providers.py           # AI provider config
│   └── main.py                 # FastAPI app
├── tests/
│   ├── agents/                   # Agent unit tests
│   └── integration/             # End-to-end tests
└── requirements.txt              # Dependencies
```

## License

MIT
