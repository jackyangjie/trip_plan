# Multi-Agent Travel Planning System - Implementation Guide

## Architecture Overview

The multi-agent travel planning system uses the AgentScope framework to coordinate 6 specialized AI agents for intelligent trip planning.

### Components

- **AgentScope Framework**: Core AI agent framework
- **ReActAgent**: Agents that use reasoning to decide when/how to call tools
- **MsgHub**: Message hub for inter-agent communication
- **MCP Integration**: Model Context Protocol for tool integration
- **Toolkit**: Manages MCP tool connections

### Specialized Agents

1. **TransportAgent** - Transportation recommendations
   - Recommends flights, trains, car rentals
   - Uses Amap MCP tools for geocoding and route planning

2. **AccommodationAgent** - Hotel/accommodation search
   - Searches hotels, hostels, vacation rentals
   - Uses Amap search tools

3. **AttractionAgent** - Attraction and activity recommendations
   - Recommends scenic spots, museums, parks
   - Uses Amap search tools

4. **FoodAgent** - Restaurant and cuisine recommendations
   - Recommends local restaurants, street food
   - Uses Amap search tools

5. **BudgetAgent** - Budget analysis and optimization
   - Analyzes cost distribution
   - Identifies saving opportunities
   - No MCP tools needed

6. **PlannerAgent** - Itinerary generation
   - Integrates all agent recommendations
   - Creates day-by-day schedules
   - No MCP tools needed

### Workflow

1. **Initialization**: AgentCoordinator creates all 6 agents with optional MCP tools
2. **Task Broadcast**: Coordinator sends planning request to all agents via MsgHub
3. **Parallel Execution**: Each agent calls relevant MCP tools autonomously
4. **Result Collection**: Coordinator gathers all agent outputs
5. **Integration**: PlannerAgent combines everything into final itinerary

### File Structure

```
backend/app/agentscope_agents/
├── __init__.py              # Package initialization
├── mcp_config.py             # MCP client configuration
├── coordinator.py             # Multi-agent coordinator
└── agents/
    ├── __init__.py          # Agent factory functions
    ├── base_agent.py         # ReActAgent factory
    ├── transport_agent.py    # Transportation specialist
    ├── accommodation_agent.py  # Accommodation specialist
    ├── attraction_agent.py   # Attraction specialist
    ├── food_agent.py       # Food specialist
    ├── budget_agent.py      # Budget analyst
    └── planner_agent.py      # Itinerary planner
```

## Configuration

### Environment Variables

```bash
# AI Models
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-4

ANTHROPIC_API_KEY=your-anthropic-key
ANTHROPIC_MODEL=claude-3-opus

TONGYI_API_KEY=your-tongyi-key
TONGYI_MODEL=qwen-max

# MCP Server
AMAP_API_KEY=your-amap-key
```

### API Endpoints

- `POST /trips/ai-plan` - Main AI planning endpoint with SSE streaming
  - Returns real-time progress updates
  - Streams steps as agents complete their tasks

## Usage Example

```python
from app.agentscope_agents import AgentCoordinator
from fastapi import BackgroundTasks

async def plan_trip(trip_data: dict, db: Session):
    coordinator = AgentCoordinator({
        "transport": {"model": "gpt-4", "agent": "transport", "api_key": "sk-xxx"},
        # ... other agents
    })
    
    await coordinator.initialize()
    result = await coordinator.plan_trip(trip_data)
    
    return result
```

## Agent Responsibilities

### TransportAgent
- Analyzes travel needs (origin, destination, dates, budget)
- Recommends optimal transportation (flights, trains, car rental)
- Uses Amap MCP tools:
  - `amap_geocode`: Convert addresses to coordinates
  - `amap_route_planning`: Plan routes with multiple transport modes
- Provides 2-3 options with pros/cons
- Considers budget and time efficiency tradeoffs

### AccommodationAgent
- Recommends hotels and accommodations
- Considers location, price, rating, facilities
- Uses Amap MCP tools:
  - `amap_geocode`: Convert addresses to coordinates
  - `amap_search_around`: Search nearby hotels
- Returns 3+ options with details

### AttractionAgent
- Recommends scenic spots, museums, parks
- Considers weather, season, local culture
- Uses Amap MCP tools:
  - `amap_geocode`: Convert addresses to coordinates
  - `amap_search_around`: Search nearby attractions
- Returns 5+ recommendations

### FoodAgent
- Recommends local restaurants and street food
- Considers cuisine preferences (spicy, light, vegetarian)
- Uses Amap MCP tools:
  - `amap_geocode`: Convert addresses to coordinates
  - `amap_search_around`: Search nearby restaurants
- Returns 5+ restaurant options

### BudgetAgent
- Analyzes cost distribution
- Identifies saving opportunities
- No MCP tools needed (works with other agent results)
- Provides optimization suggestions

### PlannerAgent
- Integrates all agent recommendations
- Creates day-by-day schedule
- Optimizes time allocation
- Generates complete JSON itinerary
- No MCP tools needed (works with other agents' results)

## Agent Communication Pattern

The coordinator broadcasts tasks via MsgHub:

```python
task_msg = Msg(
    name="Coordinator",
    content=json.dumps({"action": "recommend", "trip_data": ...}),
    role="coordinator"
)

hub.broadcast(task_msg)
```

Agents respond with recommendations:

```python
response = await agent(msg)
result = json.loads(response.content)
```

## System Features

### MCP Tool Integration
- Automatic tool discovery and registration
- Runtime tool execution via ReAct reasoning
- Support for StdIOStatefulClient (amap-mcp-server)

### Multi-Agent Coordination
- MsgHub for inter-agent messaging
- Parallel task execution with asyncio.gather
- Result aggregation and integration

### Real-Time Progress
- SSE streaming for live updates
- Step-by-step progress tracking
- Agent status monitoring

## Testing

Run integration tests:

```bash
pytest backend/tests/integration/test_multi_agent_planning.py -v
```

Run unit tests:

```bash
pytest backend/tests/agents/test_transport_agent.py -v
pytest backend/tests/agents/test_specialized_agents.py -v
```

## Development Notes

### Common Issues

**Toolkit Type Annotation**
- Use `toolkit: Any = None` instead of `toolkit: Optional[Toolkit] = None`
- This resolves SQLAlchemy type checker issues

**Import Dependencies**
- Always import from `agentscope.agent` not `agentscope.models`
- Models must be imported separately if needed

### Debugging

To debug agent behavior:

```python
from app.agentscope_agents import AgentCoordinator

coordinator = AgentCoordinator({...})
await coordinator.initialize()

# Check agent initialization
print(coordinator._agents.keys())

# Verify MCP client registration
if coordinator._agents["transport"].toolkit:
    print("Transport agent has toolkit")
```

## Performance Considerations

- Agents run in parallel for efficiency
- MCP tools are called lazily via ReAct reasoning
- SSE streaming provides user feedback
- Connection pooling for MCP servers
