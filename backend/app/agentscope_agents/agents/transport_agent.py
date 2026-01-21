
"""
Transport Agent - Specializes in transportation recommendations
"""

from typing import Dict, Any, Optional
from agentscope.agent import ReActAgent
from agentscope.model import OpenAIChatModel, AnthropicChatModel, DashScopeChatModel
from agentscope.formatter import OpenAIChatFormatter
import os
import logging

logger = logging.getLogger(__name__)

TRANSPORT_PROMPT = """你是专业的交通规划专家。

你的职责：
1. 分析用户的出行需求（起点、终点、时间、预算）
2. 推荐最优交通方式（高铁、航班、自驾、大巴等）
3. 提供详细的费用估算和时间预估

工作流程：
1. 理解用户的交通需求
2. 调用高德地图工具查询路线和交通方式
3. 基于工具返回的数据，推荐最佳方案
4. 提供多种选择及其优缺点

可用工具（会自动根据任务调用）：
- maps_geo: 将地址转换为地理坐标
- maps_direction_driving_by_address: 驾车路线规划
- maps_direction_transit_integrated_by_address: 公共交通路线规划
- maps_distance: 计算两地距离
- maps_direction_walking_by_address: 步行路线规划

输出要求：
- 提供至少 2-3 种交通方案
- 每个方案包含：类型、费用、时间、优缺点
- 优先考虑预算和时间效率的平衡

请根据用户需求，调用适当的工具并给出专业建议。

⚠️ 重要输出格式要求：
- 必须返回**纯JSON格式**（不要使用markdown代码块）
- 不要添加任何解释性文字
- 不要使用 ```json 或其他标记
- 直接输出JSON对象

正确的输出示例：
{"transport": "高铁", "cost": 300, "duration": "1小时", "options": ["高铁", "动车", "航班"]}
"""


def create_transport_agent(
    model_config: Dict[str, str], toolkit: Any = None, max_iters: int = 20
) -> ReActAgent:
    """
    Create a Transport Agent specialized in transportation recommendations.

    The agent automatically calls MCP tools through ReAct reasoning.

    Args:
        model_config: {"base_url", "model", "api_key"}
        toolkit: Optional toolkit with registered MCP tools
        max_iters: Maximum reasoning iterations

    Returns:
        ReActAgent configured for transport recommendations
    """
    # Extract configuration
    base_url = model_config.get("base_url", "https://api.openai.com/v1")
    model_name = model_config.get("model", "gpt-4")
    api_key = model_config.get("api_key") or os.getenv("OPENAI_API_KEY")

    # Select appropriate model based on base_url
    if "anthropic" in base_url.lower():
        model = AnthropicChatModel(model_name=model_name, api_key=api_key)
        formatter = None
    elif "tongyi" in base_url.lower() or "qwen" in model_name.lower():
        model = DashScopeChatModel(model_name=model_name, api_key=api_key)
        formatter = None
    else:
        # Default to OpenAI-compatible
        client_kwargs = {}
        if base_url != "https://api.openai.com/v1":
            client_kwargs["base_url"] = base_url

        model = OpenAIChatModel(
            model_name=model_name, api_key=api_key, client_kwargs=client_kwargs
        )
        formatter = OpenAIChatFormatter()

    # Create ReActAgent
    agent = ReActAgent(
        name="TransportAgent",
        sys_prompt=TRANSPORT_PROMPT,
        model=model,
        formatter=formatter,
        toolkit=toolkit,
        max_iters=max_iters,
    )

    return agent
