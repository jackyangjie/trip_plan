"""
Base Agent Factory Functions
"""

from agentscope.agent import ReActAgent
from agentscope.formatter import OpenAIChatFormatter
from agentscope.model import OpenAIChatModel, AnthropicChatModel, DashScopeChatModel
from agentscope.tool import Toolkit
from typing import Dict, Any, Optional
import os


def create_react_agent(
    name: str,
    sys_prompt: str,
    model_config: Dict[str, str],
    toolkit: Optional[Toolkit] = None,
    max_iters: int = 20,
) -> ReActAgent:
    """
    Create a ReActAgent with flexible model configuration.

    Args:
        name: Agent name
        sys_prompt: System prompt defining agent role
        model_config: {"base_url", "model", "api_key"}
        toolkit: Optional toolkit with MCP tools
        max_iters: Maximum reasoning iterations

    Returns:
        Configured ReActAgent instance
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
        model = OpenAIChatModel(
            model_name=model_name,
            api_key=api_key,
            base_http_api_url=base_url,
            client_kwargs={"base_url": base_url},
        )
        formatter = OpenAIChatFormatter()

    # Create ReActAgent with toolkit injection
    agent = ReActAgent(
        name=name,
        sys_prompt=sys_prompt,
        model=model,
        formatter=formatter,
        toolkit=toolkit,
        max_iters=max_iters,
    )

    return agent
