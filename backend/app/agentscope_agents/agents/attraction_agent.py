"""
Attraction Agent - Specializes in attraction and activity recommendations
"""

from .base_agent import create_react_agent
from agentscope.tool import Toolkit
from agentscope.agent import ReActAgent
from typing import Dict, Any, Optional


ATTRACTION_PROMPT = """你是专业的景点和活动推荐专家。

你的职责：
1. 根据目的地和用户偏好推荐景点
2. 调用高德地图搜索周边景点、博物馆、公园等
3. 提供多种类型景点选择（自然风光、历史文化、娱乐设施）
4. 考虑景点距离、开放时间、票价

可用工具（会自动根据任务调用）：
- amap_geocode: 将地址转换为坐标
- amap_search_around: 搜索周边 POI（景点、公园、博物馆）

输出要求：
- 返回 JSON 格式
- 包含至少 5 个景点推荐
- 每个景点包含：名称、类型、描述、距离、预计游玩时间、门票价格
"""


def create_attraction_agent(
    model_config: Dict[str, str], toolkit: Optional[Toolkit] = None
) -> ReActAgent:
    """
    Create an Attraction Agent specialized in attraction recommendations.

    Args:
        model_config: {"base_url", "model", "api_key"}
        toolkit: Optional toolkit with registered MCP tools

    Returns:
        ReActAgent configured for attraction recommendations
    """
    return create_react_agent(
        name="AttractionAgent",
        sys_prompt=ATTRACTION_PROMPT,
        model_config=model_config,
        toolkit=toolkit,
        max_iters=20,
    )
