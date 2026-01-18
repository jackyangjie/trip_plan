"""
AgentCoordinator - Manages multi-agent collaboration using MsgHub
"""

from agentscope.pipeline import MsgHub
from agentscope.message import Msg
from agentscope.agent import ReActAgent
from agentscope.tool import Toolkit
from typing import Dict, Any, List, Optional
import asyncio
import json
import logging

from .agents import (
    create_transport_agent,
    create_accommodation_agent,
    create_attraction_agent,
    create_food_agent,
    create_budget_agent,
    create_planner_agent,
)

logger = logging.getLogger(__name__)


class AgentCoordinator:
    """
    Coordinates multiple specialized agents for travel planning.

    Uses MsgHub for inter-agent communication and Toolkit for MCP integration.
    """

    def __init__(self, model_configs: Dict[str, Dict[str, str]]):
        """
        Initialize coordinator with model configurations for each agent.

        Args:
            model_configs: Dictionary mapping agent names to model configs
                {
                    "transport": {"base_url", "model", "api_key"},
                    "accommodation": {...},
                    "attraction": {...},
                    "food": {...},
                    "budget": {...},
                    "planner": {...}
                }
        """
        self.model_configs = model_configs
        self._agents = {}
        self._is_initialized = False

    async def initialize(self, mcp_clients: Dict[str, Any] = None):
        """
        Initialize all specialized agents with optional MCP tools.

        Args:
            mcp_clients: Dictionary of MCP clients to inject
                {"amap": amap_client}
        """
        if self._is_initialized:
            return

        logger.info("Initializing multi-agent system...")

        # Create Toolkit with MCP tools if provided
        amap_toolkit = None
        if mcp_clients and "amap" in mcp_clients:
            amap_toolkit = Toolkit()
            await amap_toolkit.register_mcp_client(mcp_clients["amap"])
            logger.info("Injected Amap MCP tools into specialized agents")

        # Create all specialized agents with toolkit injection
        self._agents["transport"] = create_transport_agent(
            self.model_configs.get("transport", {}), toolkit=amap_toolkit
        )
        self._agents["accommodation"] = create_accommodation_agent(
            self.model_configs.get("accommodation", {}), toolkit=amap_toolkit
        )
        self._agents["attraction"] = create_attraction_agent(
            self.model_configs.get("attraction", {}), toolkit=amap_toolkit
        )
        self._agents["food"] = create_food_agent(
            self.model_configs.get("food", {}), toolkit=amap_toolkit
        )
        self._agents["budget"] = create_budget_agent(
            self.model_configs.get("budget", {}), toolkit=None
        )
        self._agents["planner"] = create_planner_agent(
            self.model_configs.get("planner", {}), toolkit=None
        )

        self._is_initialized = True
        logger.info("All specialized agents initialized with MCP tools")

    async def plan_trip(self, trip_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute multi-agent collaborative trip planning.

        Workflow:
        1. Broadcast task to all agents via MsgHub
        2. Agents automatically call MCP tools via ReAct reasoning
        3. Collect results from all agents
        4. Send to PlannerAgent for final itinerary generation

        Args:
            trip_data: Trip information including destinations, dates, budget, etc.

        Returns:
            Complete planning result with all agent recommendations
        """
        if not self._is_initialized:
            await self.initialize()

        logger.info(f"Starting multi-agent planning: {trip_data.get('title')}")

        try:
            # Create MsgHub for agent communication
            participants = list(self._agents.values())

            async with MsgHub(participants=participants) as hub:
                # Broadcast task to all agents
                task_msg = Msg(
                    name="Coordinator",
                    content=json.dumps(
                        {"action": "recommend", "trip_data": trip_data},
                        ensure_ascii=False,
                    ),
                    role="coordinator",
                )

                hub.broadcast(task_msg)
                logger.info("Task broadcasted to all agents")

                # Collect results from all agents
                transport_agent = self._agents["transport"]
                accommodation_agent = self._agents["accommodation"]
                attraction_agent = self._agents["attraction"]
                food_agent = self._agents["food"]
                budget_agent = self._agents["budget"]
                planner_agent = self._agents["planner"]

                # Parallel execution - agents call MCP tools automatically
                results = await asyncio.gather(
                    self._execute_agent(transport_agent, trip_data, "transport"),
                    self._execute_agent(
                        accommodation_agent, trip_data, "accommodation"
                    ),
                    self._execute_agent(attraction_agent, trip_data, "attraction"),
                    self._execute_agent(food_agent, trip_data, "food"),
                    self._execute_agent(budget_agent, trip_data, "budget"),
                    return_exceptions=True,
                )

                transport_result = results[0]
                accommodation_result = results[1]
                attraction_result = results[2]
                food_result = results[3]
                budget_result = results[4]

                logger.info("All specialized agents completed recommendations")

                # Send to PlannerAgent for integration
                planner_content = {
                    "action": "generate_itinerary",
                    "trip_data": trip_data,
                    "transport_recommendations": transport_result,
                    "accommodation_recommendations": accommodation_result,
                    "attraction_recommendations": attraction_result,
                    "food_recommendations": food_result,
                    "budget_analysis": budget_result,
                }

                final_result = await self._execute_agent(
                    planner_agent, planner_content, "planner"
                )

                logger.info("PlannerAgent generated final itinerary")

                return {
                    "success": True,
                    "transport": transport_result,
                    "accommodation": accommodation_result,
                    "attractions": attraction_result,
                    "food": food_result,
                    "budget": budget_result,
                    "final_itinerary": final_result,
                }

        except Exception as e:
            logger.error(f"Multi-agent planning failed: {e}")
            return {"success": False, "error": str(e)}

    async def _execute_agent(
        self, agent: ReActAgent, task_data: Dict[str, Any], task_name: str
    ) -> Dict[str, Any]:
        """
        Execute a single agent's task.

        The agent automatically calls MCP tools via ReAct reasoning.

        Args:
            agent: ReActAgent instance
            task_data: Task information
            task_name: Name for logging

        Returns:
            Agent's response as dictionary
        """
        try:
            msg = Msg(
                name="Coordinator",
                content=json.dumps(task_data, ensure_ascii=False, default=str),
                role="coordinator",
            )

            # Agent automatically calls tools and returns result
            response = await agent(msg)

            try:
                result = json.loads(response.content)
                logger.info(f"{task_name} completed successfully")
                return result
            except json.JSONDecodeError:
                return {"content": response.content}

        except Exception as e:
            logger.error(f"{task_name} failed: {e}")
            return {"error": str(e)}
