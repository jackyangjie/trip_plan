"""
AgentCoordinator - Manages multi-agent collaboration
"""
from agentscope.pipeline import MsgHub
from agentscope.message import Msg
from agentscope.agent import ReActAgent
from agentscope.tool import Toolkit
from typing import Dict, Any
import asyncio
import json
import logging

# Import agent factory functions directly
from app.agentscope_agents.agents.transport_agent import create_transport_agent
from app.agentscope_agents.agents.accommodation_agent import create_accommodation_agent
from app.agentscope_agents.agents.attraction_agent import create_attraction_agent
from app.agentscope_agents.agents.food_agent import create_food_agent
from app.agentscope_agents.agents.budget_agent import create_budget_agent
from app.agentscope_agents.agents.planner_agent import create_planner_agent

logger = logging.getLogger(__name__)


class AgentCoordinator:
    
    def __init__(self, model_configs: Dict[str, Dict[str, str]]):
        self.model_configs = model_configs
        self._agents = {}
        self._is_initialized = False
    
    async def initialize(self, mcp_clients: Dict[str, Any] = None):
        if self._is_initialized:
            return
        
        logger.info("Initializing multi-agent system...")
        
        amap_toolkit = None
        if mcp_clients and "amap" in mcp_clients:
            amap_toolkit = Toolkit()
            try:
                await amap_toolkit.register_mcp_client(mcp_clients["amap"])
                logger.info("Injected Amap MCP tools")
            except Exception as e:
                logger.warning(f"Failed to register MCP client: {e}")
        
        self._agents["transport"] = create_transport_agent(
            self.model_configs.get("transport", {}),
            toolkit=amap_toolkit
        )
        self._agents["accommodation"] = create_accommodation_agent(
            self.model_configs.get("accommodation", {}),
            toolkit=amap_toolkit
        )
        self._agents["attraction"] = create_attraction_agent(
            self.model_configs.get("attraction", {}),
            toolkit=amap_toolkit
        )
        self._agents["food"] = create_food_agent(
            self.model_configs.get("food", {}),
            toolkit=amap_toolkit
        )
        self._agents["budget"] = create_budget_agent(
            self.model_configs.get("budget", {}),
            toolkit=None
        )
        self._agents["planner"] = create_planner_agent(
            self.model_configs.get("planner", {}),
            toolkit=None
        )
        
        self._is_initialized = True
        logger.info("All specialized agents initialized")
    
    async def plan_trip(self, trip_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self._is_initialized:
            await self.initialize()
        
        logger.info(f"Starting multi-agent planning: {trip_data.get('title')}")
        
        try:
            participants = list(self._agents.values())
            
            async with MsgHub(participants=participants) as hub:
                task_msg = Msg(
                    name="Coordinator",
                    content=json.dumps({
                        "action": "recommend",
                        "trip_data": trip_data
                    }, ensure_ascii=False),
                    role="coordinator"
                )
                
                hub.broadcast(task_msg)
                logger.info("Task broadcasted")
                
                transport_agent = self._agents["transport"]
                accommodation_agent = self._agents["accommodation"]
                attraction_agent = self._agents["attraction"]
                food_agent = self._agents["food"]
                budget_agent = self._agents["budget"]
                planner_agent = self._agents["planner"]
                
                results = await asyncio.gather(
                    self._execute_agent(transport_agent, trip_data, "transport"),
                    self._execute_agent(accommodation_agent, trip_data, "accommodation"),
                    self._execute_agent(attraction_agent, trip_data, "attraction"),
                    self._execute_agent(food_agent, trip_data, "food"),
                    self._execute_agent(budget_agent, trip_data, "budget"),
                    return_exceptions=True
                )
                
                transport_result = results[0]
                accommodation_result = results[1]
                attraction_result = results[2]
                food_result = results[3]
                budget_result = results[4]
                
                logger.info("All specialized agents completed")
                
                planner_content = {
                    "action": "generate_itinerary",
                    "trip_data": trip_data,
                    "transport_recommendations": transport_result,
                    "accommodation_recommendations": accommodation_result,
                    "attraction_recommendations": attraction_result,
                    "food_recommendations": food_result,
                    "budget_analysis": budget_result
                }
                
                final_result = await self._execute_agent(
                    planner_agent,
                    planner_content,
                    "planner"
                )
                
                logger.info("PlannerAgent generated final itinerary")
                
                return {
                    "success": True,
                    "transport": transport_result,
                    "accommodation": accommodation_result,
                    "attractions": attraction_result,
                    "food": food_result,
                    "budget": budget_result,
                    "final_itinerary": final_result
                }
                
        except Exception as e:
            logger.error(f"Multi-agent planning failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _execute_agent(self, agent: ReActAgent, task_data: Dict[str, Any], task_name: str) -> Dict[str, Any]:
        try:
            msg = Msg(
                name="Coordinator",
                content=json.dumps(task_data, ensure_ascii=False, default=str),
                role="coordinator"
            )
            
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
