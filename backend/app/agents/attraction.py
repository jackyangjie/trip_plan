from typing import Dict, Any
from app.agents.base import BaseAgent, AgentResult


class AttractionAgent(BaseAgent):
    name = "attraction"
    description = "Recommends attractions and activities"

    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        action = input_data.get("action", "recommend")
        destinations = input_data.get("destinations", [])
        preferences = input_data.get("preferences", {})
        attraction_types = preferences.get("attractionTypes", [])

        recommendations = []

        for dest in destinations:
            attractions = [
                {
                    "destination": dest,
                    "type": "scenic",
                    "title": f"{dest}自然风光",
                    "estimated_duration": "4-6小时",
                    "cost_estimate": 100,
                    "description": "欣赏自然美景",
                },
                {
                    "destination": dest,
                    "type": "cultural",
                    "title": f"{dest}历史古迹",
                    "estimated_duration": "3-4小时",
                    "cost_estimate": 50,
                    "description": "体验历史文化",
                },
            ]
            recommendations.extend(attractions)

        return AgentResult(
            success=True,
            data={"recommendations": recommendations, "count": len(recommendations)},
        )
