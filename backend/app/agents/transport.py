from typing import Dict, Any
from app.agents.base import BaseAgent, AgentResult


class TransportAgent(BaseAgent):
    name = "transport"
    description = "Recommends transportation options"

    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        action = input_data.get("action", "recommend")
        destinations = input_data.get("destinations", [])
        start_date = input_data.get("start_date", "")
        end_date = input_data.get("end_date", "")
        travelers = input_data.get("travelers", 1)

        recommendations = [
            {
                "type": "high_speed_rail",
                "title": "高铁",
                "cost_estimate": travelers * 500,
                "duration": "快速便捷",
            },
            {
                "type": "flight",
                "title": "航班",
                "cost_estimate": travelers * 800,
                "duration": "最快捷",
            },
        ]

        return AgentResult(
            success=True,
            data={"recommendations": recommendations, "count": len(recommendations)},
        )
