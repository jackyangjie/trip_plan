"""
AI Provider Configuration Module

Provides centralized configuration for different AI model providers.
"""

from typing import Optional
from config import settings


class AIProviderConfig:
    """Centralized AI provider configuration"""

    # OpenAI Configuration
    @staticmethod
    def get_openai_config() -> dict:
        """Get OpenAI provider configuration"""
        return {
            "api_key": settings.openai_api_key,
            "base_url": settings.openai_base_url,
            "model": settings.openai_model,
            "provider": "openai",
        }

    # Anthropic Configuration
    @staticmethod
    def get_anthropic_config() -> dict:
        """Get Anthropic (Claude) provider configuration"""
        return {
            "api_key": settings.anthropic_api_key,
            "base_url": settings.anthropic_base_url,
            "model": settings.anthropic_model,
            "provider": "anthropic",
        }

    # Tongyi Configuration
    @staticmethod
    def get_tongyi_config() -> dict:
        """Get Tongyi (Qwen) provider configuration"""
        return {
            "api_key": settings.tongyi_api_key,
            "base_url": settings.tongyi_base_url,
            "model": settings.tongyi_model,
            "provider": "tongyi",
        }

    @staticmethod
    def get_provider_config(provider_name: str) -> Optional[dict]:
        """
        Get configuration for a specific provider by name

        Args:
            provider_name: Name of the provider ('openai', 'anthropic', 'tongyi')

        Returns:
            Provider configuration dict or None if not found
        """
        configs = {
            "openai": AIProviderConfig.get_openai_config(),
            "anthropic": AIProviderConfig.get_anthropic_config(),
            "tongyi": AIProviderConfig.get_tongyi_config(),
        }
        return configs.get(provider_name.lower())

    @staticmethod
    def get_available_providers() -> list[str]:
        """Get list of available provider names"""
        return ["openai", "anthropic", "tongyi"]

    @staticmethod
    def get_default_provider() -> str:
        """Get the default provider to use"""
        if settings.openai_api_key:
            return "openai"
        elif settings.anthropic_api_key:
            return "anthropic"
        elif settings.tongyi_api_key:
            return "tongyi"
        return "openai"


def get_openai_config() -> dict:
    """Convenience function to get OpenAI config"""
    return AIProviderConfig.get_openai_config()


def get_anthropic_config() -> dict:
    """Convenience function to get Anthropic config"""
    return AIProviderConfig.get_anthropic_config()


def get_tongyi_config() -> dict:
    """Convenience function to get Tongyi config"""
    return AIProviderConfig.get_tongyi_config()


def get_provider_config(provider_name: str) -> Optional[dict]:
    """Convenience function to get any provider config"""
    return AIProviderConfig.get_provider_config(provider_name)
