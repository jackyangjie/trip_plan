"""
Budget Agent - Specializes in budget analysis and optimization
"""

from .base_agent import create_react_agent
from agentscope.agent import ReActAgent
from agentscope.tool import Toolkit
from typing import Dict, Any, Optional


BUDGET_PROMPT = """你是专业的预算分析专家。

你的职责：
1. 分析旅行总预算的合理分配
2. 评估各单项花费（交通、住宿、餐饮、景点、购物）
3. 提供预算优化建议
4. 识别可能的节省成本的机会

工作流程：
1. 理解用户的总预算和旅行天数
2. 分析各个专业 agent 的推荐费用
3. 评估预算分配的合理性
4. 提供优化建议和成本控制方案

输出要求：
- 返回 JSON 格式
- 包含预算分配表（交通、住宿、餐饮、景点、其他）
- 提供预算优化建议
- 识别潜在超支项目并给出解决方案
"""


def create_budget_agent(
    model_config: Dict[str, str], toolkit: Optional[Toolkit] = None
) -> ReActAgent:
    """
    Create a Budget Agent specialized in budget analysis.

    Args:
        model_config: {"base_url", "model", "api_key"}
        toolkit: Optional toolkit (not needed for budget analysis)

    Returns:
        ReActAgent configured for budget analysis
    """
    return create_react_agent(
        name="BudgetAgent",
        sys_prompt=BUDGET_PROMPT,
        model_config=model_config,
        toolkit=toolkit,
        max_iters=20,
    )
