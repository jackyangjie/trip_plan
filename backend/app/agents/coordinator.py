from typing import Dict, Any
from app.agents.base import BaseAgent, AgentResult
from app.agents.planner import PlannerAgent
from app.agents.transport import TransportAgent
from app.agents.accommodation import AccommodationAgent
from app.agents.attraction import AttractionAgent
from app.agents.food import FoodAgent
from app.agents.budget import BudgetAgent


class AgentCoordinator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.transport = TransportAgent()
        self.accommodation = AccommodationAgent()
        self.attraction = AttractionAgent()
        self.food = FoodAgent()
        self.budget = BudgetAgent()

    async def plan_trip(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Step 1: Planning phase
        plan = await self.planner.process({"action": "analyze", "request": request})

        # Step 2: Parallel execution of specialized agents
        transport_result = await self.transport.process(
            {"action": "recommend", **request}
        )
        accommodation_result = await self.accommodation.process(
            {"action": "recommend", **request}
        )
        attraction_result = await self.attraction.process(
            {"action": "recommend", **request}
        )
        food_result = await self.food.process({"action": "recommend", **request})

        # Step 3: Budget analysis
        budget_result = await self.budget.process(
            {
                "action": "analyze",
                "transport": transport_result.data
                if transport_result.success
                else None,
                "accommodation": accommodation_result.data
                if accommodation_result.success
                else None,
                "attractions": attraction_result.data
                if attraction_result.success
                else None,
                "food": food_result.data if food_result.success else None,
                "budget": request.get("budget", {}),
            }
        )

        # Step 4: Generate final itinerary
        final_plan = await self.planner.process(
            {
                "action": "generate",
                "request": request,
                "transport": transport_result.data if transport_result.success else {},
                "accommodation": accommodation_result.data
                if accommodation_result.success
                else {},
                "attractions": attraction_result.data
                if attraction_result.success
                else {},
                "food": food_result.data if food_result.success else {},
                "budget_analysis": budget_result.data if budget_result.success else {},
            }
        )

        return {
            "success": final_plan.get("success", False),
            "itinerary": final_plan.get("itinerary", []),
            "budget": final_plan.get("budget", {}),
            "recommendations": {
                "transport": transport_result.data
                if transport_result.success
                else None,
                "accommodation": accommodation_result.data
                if accommodation_result.success
                else None,
                "attractions": attraction_result.data
                if attraction_result.success
                else None,
                "food": food_result.data if food_result.success else None,
            },
            "budget_analysis": budget_result.data if budget_result.success else None,
        }
