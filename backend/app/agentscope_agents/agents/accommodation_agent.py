"""
Accommodation Agent - Specializes in hotel/accommodation recommendations
"""

from typing import Dict, Any, Optional
from agentscope.agent import ReActAgent
from agentscope.model import OpenAIChatModel, AnthropicChatModel, DashScopeChatModel
from agentscope.formatter import OpenAIChatFormatter
import os
import logging

logger = logging.getLogger(__name__)

ACCOMMODATION_PROMPT = """你是专业的住宿推荐专家。

你的职责：
1. 根据目的地和预算推荐合适的住宿
2. 调用高德地图搜索周边酒店、民宿
3. 考虑位置便利性、价格、评分
4. 提供多种类型选择（酒店、民宿、青旅）

可用工具（会自动根据任务调用）：
- maps_geo: 将地址转换为地理坐标
- maps_around_search: 搜索周边 POI（酒店、民宿）
- maps_search_detail: 获取POI详细信息

输出要求：
- 返回 JSON 格式
- 包含至少 3 家住宿选项
- 每个住宿包含：类型、价格、评分、设施
"""


def create_accommodation_agent(model_config: Dict[str, str], toolkit: Any = None):
    """
    Create an Accommodation Agent specialized in hotel recommendations.

    Args:
        model_config: {"base_url", "model", "api_key"}
        toolkit: Optional toolkit with registered MCP tools

    Returns:
        ReActAgent configured for accommodation recommendations
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
        name="AccommodationAgent",
        sys_prompt=ACCOMMODATION_PROMPT,
        model=model,
        formatter=formatter,
        toolkit=toolkit,
        max_iters=20,
    )

    return agent
