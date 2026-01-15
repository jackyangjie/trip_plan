from typing import Dict, Any
from datetime import datetime, timedelta
from app.agents.base import BaseAgent, AgentResult


class PlannerAgent(BaseAgent):
    name = "planner"
    description = "Analyzes travel requests and generates comprehensive trip plans"

    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        action = input_data.get("action", "analyze")

        if action == "analyze":
            return await self._analyze_request(input_data.get("request", {}))
        elif action == "generate":
            return await self._generate_itinerary(input_data)

        return AgentResult(success=False, error=f"Unknown action: {action}")

    async def _analyze_request(self, request: Dict[str, Any]) -> AgentResult:
        analysis = {
            "destinations": request.get("destinations", []),
            "duration_days": self._calculate_duration(
                request.get("start_date", ""), request.get("end_date", "")
            ),
            "travelers": request.get("travelers", 1),
            "budget_range": self._categorize_budget(request.get("budget", {})),
            "preferences": request.get("preferences", {}),
        }
        return AgentResult(success=True, data=analysis)

    async def _generate_itinerary(self, input_data: Dict[str, Any]) -> AgentResult:
        days = input_data.get("duration_days", 1)
        itinerary = []

        for day in range(1, days + 1):
            daily_activities = []

            day_itinerary = {"day": day, "activities": daily_activities}
            itinerary.append(day_itinerary)

        result = {
            "itinerary": itinerary,
            "budget": input_data.get("budget_analysis", {}),
        }
        return AgentResult(success=True, data=result)

    def _calculate_duration(self, start_date: str, end_date: str) -> int:
        if not start_date or not end_date:
            return 1
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            return max(1, (end - start).days + 1)
        except:
            return 1

    def _categorize_budget(self, budget: Dict[str, int]) -> str:
        total = budget.get("total", 0)
        if total < 2000:
            return "budget"
        elif total < 8000:
            return "medium"
        return "luxury"
