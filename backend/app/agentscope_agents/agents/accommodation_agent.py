"""
Accommodation Agent - Specializes in hotel/accommodation recommendations
"""

from .base_agent import create_react_agent
from agentscope.tool import Toolkit
from agentscope.agent import ReActAgent
from typing import Dict, Any, Optional


ACCOMMODATION_PROMPT = """你是专业的住宿推荐专家。

你的职责：
1. 根据目的地和预算推荐合适的住宿
2. 调用高德地图搜索周边酒店、民宿
3. 考虑位置便利性、价格、评分
4. 提供多种类型选择（酒店、民宿、青旅）

可用工具（会自动根据任务调用）：
- amap_geocode: 将地址转换为坐标
- amap_search_around: 搜索周边 POI（酒店、民宿）

输出要求：
- 返回 JSON 格式
- 包含至少 3 家住宿选项
- 每个住宿包含：类型、价格、评分、设施
"""


def create_accommodation_agent(
    model_config: Dict[str, str], toolkit: Optional[Toolkit] = None
):
    """
    Create an Accommodation Agent specialized in hotel recommendations.

    Args:
        model_config: {"base_url", "model", "api_key"}
        toolkit: Optional toolkit with registered MCP tools

    Returns:
        ReActAgent configured for accommodation recommendations
    """
    return create_react_agent(
        name="AccommodationAgent",
        sys_prompt=ACCOMMODATION_PROMPT,
        model_config=model_config,
        toolkit=toolkit,
        max_iters=20,
    )
