"""
Food Agent - Specializes in restaurant and cuisine recommendations
"""

from typing import Dict, Any, Optional
from agentscope.agent import ReActAgent
from agentscope.model import OpenAIChatModel, AnthropicChatModel, DashScopeChatModel
from agentscope.formatter import OpenAIChatFormatter
import os
import logging

logger = logging.getLogger(__name__)

FOOD_PROMPT = """你是专业的美食推荐专家。

你的职责：
1. 根据目的地推荐当地特色餐厅和美食
2. 考虑用户饮食偏好（辣、清淡、素食等）
3. 提供不同价位的选择
4. 推荐当地特色菜品和美食体验

可用工具（会自动根据任务调用）：
- maps_geo: 将地址转换为地理坐标
- maps_around_search: 搜索周边餐厅、小吃店、咖啡馆
- maps_search_detail: 获取POI详细信息
- maps_text_search: 全局搜索餐厅

输出要求：
- 返回 JSON 格式
- 推荐至少 5 家餐厅
- 每家餐厅包含：菜系类型、人均消费、推荐菜品、特色
"""


def create_food_agent(model_config: Dict[str, str], toolkit: Any = None):
    """
    Create a Food Agent specialized in restaurant recommendations.

    Args:
        model_config: {"base_url", "model", "api_key"}
        toolkit: Optional toolkit with registered MCP tools

    Returns:
        ReActAgent configured for food recommendations
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
        name="FoodAgent",
        sys_prompt=FOOD_PROMPT,
        model=model,
        formatter=formatter,
        toolkit=toolkit,
        max_iters=20,
    )

    return agent
