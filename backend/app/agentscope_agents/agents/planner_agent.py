"""
Planner Agent - Specializes in integrating all recommendations into itinerary
"""

from typing import Dict, Any, Optional
from agentscope.agent import ReActAgent
from agentscope.model import OpenAIChatModel, AnthropicChatModel, DashScopeChatModel
from agentscope.formatter import OpenAIChatFormatter
import os

PLANNER_PROMPT = """你是专业的行程规划专家。

你的职责：
1. 整合交通、住宿、景点、美食、天气等推荐
2. 生成每日详细行程安排
3. 确保行程的可行性和合理性
4. 优化时间安排，避免行程过紧
5. 根据天气建议调整户外活动

工作流程：
1. 接收所有agent的推荐结果
2. 根据旅行天数规划每日行程
3. 合理分配活动时间
4. 考虑景点之间的交通便利性
5. 根据天气信息调整行程安排
6. 生成完整的JSON格式行程

输入数据格式：
- transport_recommendations: 交通推荐
- accommodation_recommendations: 住宿推荐
- attraction_recommendations: 景点推荐
- food_recommendations: 美食推荐
- weather_recommendations: 天气信息
- budget_analysis: 预算分析

输出要求：
- 返回 JSON 格式的完整行程
- 包含 days 字段（按天组织的行程）
- 每天包含：日期、天气、景点、交通、住宿、美食、详细行程
- 每个活动包含时间、地点、活动类型、费用估算
- 根据天气情况调整户外活动时间
"""


def create_planner_agent(model_config: Dict[str, str], toolkit: Any = None):
    """
    Create a Planner Agent specialized in itinerary generation.

    Args:
        model_config: {"base_url", "model", "api_key"}
        toolkit: Optional toolkit (Planner agent works with other agents' results)

    Returns:
        ReActAgent configured for itinerary planning
    """
    base_url = model_config.get("base_url", "https://api.openai.com/v1")
    model_name = model_config.get("model", "gpt-4")
    api_key = model_config.get("api_key") or os.getenv("OPENAI_API_KEY")

    if "anthropic" in base_url.lower():
        model = AnthropicChatModel(model_name=model_name, api_key=api_key)
        formatter = None
    elif "tongyi" in base_url.lower() or "qwen" in model_name.lower():
        model = DashScopeChatModel(model_name=model_name, api_key=api_key)
        formatter = None
    else:
        client_kwargs = {}
        if base_url != "https://api.openai.com/v1":
            client_kwargs["base_url"] = base_url

        model = OpenAIChatModel(
            model_name=model_name, api_key=api_key, client_kwargs=client_kwargs
        )
        formatter = OpenAIChatFormatter()

    agent = ReActAgent(
        name="PlannerAgent",
        sys_prompt=PLANNER_PROMPT,
        model=model,
        formatter=formatter,
        toolkit=toolkit,
        max_iters=20,
    )

    return agent
