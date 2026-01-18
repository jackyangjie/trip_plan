"""Test AI Provider Configuration"""

import pytest
from app.ai_providers import AIProviderConfig, get_provider_config


class TestAIProviders:
    """Test AI Provider configuration module"""

    def test_get_openai_config(self):
        """Test OpenAI configuration includes model name"""
        config = AIProviderConfig.get_openai_config()

        assert config["provider"] == "openai"
        assert "api_key" in config
        assert "base_url" in config
        assert "model" in config
        assert config["model"] == "gpt-4"  # Default model

    def test_get_anthropic_config(self):
        """Test Anthropic configuration includes model name"""
        config = AIProviderConfig.get_anthropic_config()

        assert config["provider"] == "anthropic"
        assert "api_key" in config
        assert "base_url" in config
        assert "model" in config
        assert "claude" in config["model"].lower()

    def test_get_tongyi_config(self):
        """Test Tongyi configuration includes model name"""
        config = AIProviderConfig.get_tongyi_config()

        assert config["provider"] == "tongyi"
        assert "api_key" in config
        assert "base_url" in config
        assert "model" in config
        assert "qwen" in config["model"].lower()

    def test_get_provider_config_openai(self):
        """Test dynamic provider retrieval for OpenAI"""
        config = get_provider_config("openai")

        assert config is not None
        assert config["provider"] == "openai"
        assert config["model"] == "gpt-4"

    def test_get_provider_config_anthropic(self):
        """Test dynamic provider retrieval for Anthropic"""
        config = get_provider_config("anthropic")

        assert config is not None
        assert config["provider"] == "anthropic"
        assert "claude" in config["model"].lower()

    def test_get_provider_config_tongyi(self):
        """Test dynamic provider retrieval for Tongyi"""
        config = get_provider_config("tongyi")

        assert config is not None
        assert config["provider"] == "tongyi"
        assert "qwen" in config["model"].lower()

    def test_get_provider_config_invalid(self):
        """Test dynamic provider retrieval with invalid name"""
        config = get_provider_config("invalid")

        assert config is None

    def test_get_available_providers(self):
        """Test list of available providers"""
        providers = AIProviderConfig.get_available_providers()

        assert isinstance(providers, list)
        assert "openai" in providers
        assert "anthropic" in providers
        assert "tongyi" in providers
        assert len(providers) == 3

    def test_config_keys(self):
        """Test all required config keys are present"""
        for provider in ["openai", "anthropic", "tongyi"]:
            config = get_provider_config(provider)

            assert config is not None
            assert set(config.keys()) >= {"provider", "api_key", "base_url", "model"}
