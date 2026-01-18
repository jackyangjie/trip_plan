"""
Food Agent - Specializes in restaurant and cuisine recommendations
"""

from .base_agent import create_react_agent
from agentscope.tool import Toolkit
from agentscope.agent import ReActAgent
from typing import Dict, Any, Optional


FOOD_PROMPT = """你是专业的美食推荐专家。

你的职责：
1. 根据目的地和用户偏好推荐餐厅
2. 调用高德地图搜索周边美食
3. 推荐当地特色菜和知名餐厅
4. 考虑口味、价格、地理位置、用户评价

可用工具（会自动根据任务调用）：
- amap_geocode: 将地址转换为坐标
- amap_search_around: 搜索周边 POI（餐厅、咖啡馆、小吃店）

输出要求：
- 返回 JSON 格式
- 包含至少 5 家餐厅推荐
- 每个餐厅包含：名称、菜系、人均消费、特色菜、用户评分
"""


def create_food_agent(
    model_config: Dict[str, str], toolkit: Optional[Toolkit] = None
) -> ReActAgent:
    """
    Create a Food Agent specialized in restaurant recommendations.

    Args:
        model_config: {"base_url", "model", "api_key"}
        toolkit: Optional toolkit with registered MCP tools

    Returns:
        ReActAgent configured for food recommendations
    """
    return create_react_agent(
        name="FoodAgent",
        sys_prompt=FOOD_PROMPT,
        model_config=model_config,
        toolkit=toolkit,
        max_iters=20,
    )
