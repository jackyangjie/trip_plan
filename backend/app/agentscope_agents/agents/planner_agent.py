"""
Planner Agent - Coordinates all agents and generates final itinerary
"""

from .base_agent import create_react_agent
from agentscope.agent import ReActAgent
from agentscope.tool import Toolkit
from typing import Dict, Any, Optional


PLANNER_PROMPT = """你是专业的旅行规划师，负责整合所有专业 agent 的建议并生成最终行程。

你的职责：
1. 接收来自交通、住宿、景点、美食、预算 agent 的推荐
2. 综合考虑时间、地点、预算、偏好
3. 生成详细的逐日行程安排
4. 确保行程合理、高效、符合预算

工作流程：
1. 收集所有专业 agent 的推荐结果
2. 根据地理距离和时间安排优化行程
3. 平衡预算和体验质量
4. 生成结构化的行程表

输入格式：
{
  "action": "generate_itinerary",
  "trip_data": {...},
  "transport_recommendations": {...},
  "accommodation_recommendations": {...},
  "attraction_recommendations": {...},
  "food_recommendations": {...},
  "budget_analysis": {...}
}

输出要求：
- 返回 JSON 格式
- 按天组织行程，每天包含时间段安排
- 每个活动包含：时间、地点、活动类型、费用、备注
- 提供总体预算汇总
- 包含交通衔接建议
"""


def create_planner_agent(
    model_config: Dict[str, str], toolkit: Optional[Toolkit] = None
) -> ReActAgent:
    """
    Create a Planner Agent specialized in itinerary generation.

    Args:
        model_config: {"base_url", "model", "api_key"}
        toolkit: Optional toolkit (not needed for planning)

    Returns:
        ReActAgent configured for itinerary planning
    """
    return create_react_agent(
        name="PlannerAgent",
        sys_prompt=PLANNER_PROMPT,
        model_config=model_config,
        toolkit=toolkit,
        max_iters=25,
    )
