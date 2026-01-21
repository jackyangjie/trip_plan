"""
Budget Agent - Specializes in budget analysis and optimization
"""

from typing import Dict, Any, Optional
from agentscope.agent import ReActAgent
from agentscope.model import OpenAIChatModel, AnthropicChatModel, DashScopeChatModel
from agentscope.formatter import OpenAIChatFormatter
import os

BUDGET_PROMPT = """你是专业的预算分析专家。

你的职责：
1. 分析旅行预算分配的合理性
2. 根据推荐内容优化预算
3. 识别可能的节省机会
4. 提供预算调整建议

工作流程：
1. 接收交通、住宿、景点、美食等推荐内容
2. 分析各项费用
3. 评估预算分配的平衡性
4. 提供优化建议

可用工具：
- 无需调用外部工具
- 基于其他agent的推荐进行分析

输出要求：
- 返回 JSON 格式
- 包含预算分析报告
- 提供优化建议
"""


def create_budget_agent(model_config: Dict[str, str], toolkit: Any = None):
    """
    Create a Budget Agent specialized in budget analysis.

    Args:
        model_config: {"base_url", "model", "api_key"}
        toolkit: Optional toolkit (Budget agent may not need MCP tools)

    Returns:
        ReActAgent configured for budget analysis
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
        name="BudgetAgent",
        sys_prompt=BUDGET_PROMPT,
        model=model,
        formatter=formatter,
        toolkit=toolkit,
        max_iters=20,
    )

    return agent
