"""
Example usage of AI Provider Configuration

This module demonstrates how to use the AI provider configuration
to initialize AI clients from different providers.
"""

from app.ai_providers import AIProviderConfig, get_provider_config
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic


def initialize_openai_client():
    """Initialize OpenAI client with configured API key and model"""
    config = AIProviderConfig.get_openai_config()

    client = AsyncOpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"],
    )

    model_name = config["model"]  # gpt-4, gpt-3.5-turbo, etc.

    return client, model_name


def initialize_anthropic_client():
    """Initialize Anthropic client with configured API key and model"""
    config = AIProviderConfig.get_anthropic_config()

    client = AsyncAnthropic(
        api_key=config["api_key"],
        base_url=config["base_url"],
    )

    model_name = config["model"]  # claude-3-sonnet-20240229, claude-2, etc.

    return client, model_name


def get_client_for_provider(provider_name: str):
    """
    Dynamically get client configuration for a given provider

    Args:
        provider_name: Name of the provider ('openai', 'anthropic', 'tongyi')

    Returns:
        Tuple of (client_config, model_name) or (None, None)
    """
    config = get_provider_config(provider_name)

    if config is None:
        return None, None

    return config, config["model"]


def usage_example():
    """Example of using the AI provider configuration"""

    # Method 1: Direct provider methods
    openai_config = AIProviderConfig.get_openai_config()
    print(f"Using OpenAI with model: {openai_config['model']}")

    # Method 2: Dynamic provider selection
    provider_name = "openai"  # Could come from user settings or environment
    config, model = get_client_for_provider(provider_name)

    if config:
        print(f"Initializing {config['provider']} client...")
        print(f"Model: {model}")
        print(f"Base URL: {config['base_url']}")
        # Here you would create the actual client instance
        # client = AsyncOpenAI(api_key=config['api_key'], ...)
    else:
        print(f"Unknown provider: {provider_name}")

    # Method 3: Check available providers
    available = AIProviderConfig.get_available_providers()
    print(f"Available providers: {', '.join(available)}")

    # Method 4: Get default provider
    default = AIProviderConfig.get_default_provider()
    print(f"Default provider: {default}")


if __name__ == "__main__":
    usage_example()
