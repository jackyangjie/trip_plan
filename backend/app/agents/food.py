from typing import Dict, Any
from app.agents.base import BaseAgent, AgentResult


class FoodAgent(BaseAgent):
    name = "food"
    description = "Recommends restaurants and local cuisine"

    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        action = input_data.get("action", "recommend")
        destinations = input_data.get("destinations", [])
        preferences = input_data.get("preferences", {})
        food_types = preferences.get("foodTypes", [])

        recommendations = []

        for dest in destinations:
            restaurants = [
                {
                    "destination": dest,
                    "type": "local_specialty",
                    "title": f"{dest}特色菜",
                    "estimated_cost": 80,
                    "description": "品尝当地特色美食",
                },
                {
                    "destination": dest,
                    "type": "street_food",
                    "title": f"{dest}小吃街",
                    "estimated_cost": 40,
                    "description": "体验街头美食文化",
                },
            ]
            recommendations.extend(restaurants)

        return AgentResult(
            success=True,
            data={"recommendations": recommendations, "count": len(recommendations)},
        )
