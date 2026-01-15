from typing import Dict, Any, Optional
from app.agents.base import BaseAgent, AgentResult


class BudgetAgent(BaseAgent):
    name = "budget"
    description = "Analyzes and optimizes trip budget"

    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        action = input_data.get("action", "analyze")

        if action == "analyze":
            return await self._analyze_budget(input_data)
        elif action == "optimize":
            return await self._optimize_budget(input_data)

        return AgentResult(success=False, error=f"Unknown action: {action}")

    async def _analyze_budget(self, input_data: Dict[str, Any]) -> AgentResult:
        total_budget = input_data.get("budget", {}).get("total", 0)
        transport_cost = (
            input_data.get("transport", {}).get("data", [{}])[0].get("cost_estimate", 0)
        )
        accommodation_cost = (
            input_data.get("accommodation", {})
            .get("data", [{}])[0]
            .get("total_cost", 0)
        )

        analysis = {
            "total_budget": total_budget,
            "transport_estimate": transport_cost,
            "accommodation_estimate": accommodation_cost,
            "food_estimate": int(total_budget * 0.2),
            "activities_estimate": int(total_budget * 0.15),
            "remaining": total_budget
            - (
                transport_cost
                + accommodation_cost
                + int(total_budget * 0.2)
                + int(total_budget * 0.15)
            ),
        }

        if analysis["remaining"] < 0:
            analysis["warning"] = "预算可能超支"
        else:
            analysis["warning"] = None

        return AgentResult(success=True, data=analysis)

    async def _optimize_budget(self, input_data: Dict[str, Any]) -> AgentResult:
        current_budget = input_data.get("budget", {})
        total = current_budget.get("total", 0)

        optimized = {
            "total": total,
            "transport": int(total * 0.3),
            "accommodation": int(total * 0.35),
            "food": int(total * 0.2),
            "activities": int(total * 0.15),
        }

        return AgentResult(success=True, data=optimized)
