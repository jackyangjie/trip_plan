"""
Transport Agent - Specializes in transportation recommendations
"""

from .base_agent import create_react_agent
from agentscope.tool import Toolkit
from agentscope.agent import ReActAgent
from typing import Dict, Any, Optional


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
- amap_geocode: 将地址转换为地理坐标
- amap_route_planning: 规划出行路线，支持多种交通方式

输出要求：
- 提供至少 2-3 种交通方案
- 每个方案包含：类型、费用、时间、优缺点
- 优先考虑预算和时间效率的平衡

请根据用户需求，调用适当的工具并给出专业建议。
"""


def create_transport_agent(
    model_config: Dict[str, str], toolkit: Optional[Toolkit] = None
) -> ReActAgent:
    """
    Create a Transport Agent specialized in transportation recommendations.

    The agent automatically calls MCP tools through ReAct reasoning.

    Args:
        model_config: {"base_url", "model", "api_key"}
        toolkit: Optional toolkit with registered MCP tools

    Returns:
        ReActAgent configured for transport recommendations
    """
    return create_react_agent(
        name="TransportAgent",
        sys_prompt=TRANSPORT_PROMPT,
        model_config=model_config,
        toolkit=toolkit,
        max_iters=20,
    )
