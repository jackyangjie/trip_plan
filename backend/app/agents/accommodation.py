from typing import Dict, Any
from app.agents.base import BaseAgent, AgentResult


class AccommodationAgent(BaseAgent):
    name = "accommodation"
    description = "Finds suitable accommodations"

    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        action = input_data.get("action", "recommend")
        destinations = input_data.get("destinations", [])
        start_date = input_data.get("start_date", "")
        end_date = input_data.get("end_date", "")
        travelers = input_data.get("travelers", 1)
        budget = input_data.get("budget", {}).get("accommodation", 0)

        recommendations = []

        for dest in destinations:
            accommodations = [
                {
                    "destination": dest,
                    "type": "hotel",
                    "title": f"{dest}市中心酒店",
                    "cost_per_night": 400,
                    "total_cost": 400 * 3,
                    "rating": "4星",
                },
                {
                    "destination": dest,
                    "type": "apartment",
                    "title": f"{dest}民宿",
                    "cost_per_night": 300,
                    "total_cost": 300 * 3,
                    "rating": "经济实惠",
                },
            ]
            recommendations.extend(accommodations)

        return AgentResult(
            success=True,
            data={"recommendations": recommendations, "count": len(recommendations)},
        )
