"""
Weather Agent - Specializes in weather information and forecasting
"""

from typing import Dict, Any, Optional
from agentscope.agent import ReActAgent
from agentscope.model import OpenAIChatModel, AnthropicChatModel, DashScopeChatModel
from agentscope.formatter import OpenAIChatFormatter
import os
import logging

logger = logging.getLogger(__name__)

WEATHER_PROMPT = """你是专业的天气查询专家。

你的职责：
1. 根据目的地和日期查询天气信息
2. 提供准确的天气预报
3. 给出穿衣、出行建议
4. 考虑季节和气候特点

可用工具（会自动根据任务调用）：
- maps_geo: 将地址转换为地理坐标
- maps_text_search: 搜索地点信息

输出要求：
- 返回 JSON 格式
- 包含每日天气信息
- 提供温度、天气状况、湿度、风速
- 给出实用的穿衣和出行建议
"""


def create_weather_agent(model_config: Dict[str, str], toolkit: Any = None):
    """
    Create a Weather Agent specialized in weather information.

    Args:
        model_config: {"base_url", "model", "api_key"}
        toolkit: Optional toolkit with registered MCP tools

    Returns:
        ReActAgent configured for weather information
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
        name="WeatherAgent",
        sys_prompt=WEATHER_PROMPT,
        model=model,
        formatter=formatter,
        toolkit=toolkit,
        max_iters=10,
    )

    return agent

