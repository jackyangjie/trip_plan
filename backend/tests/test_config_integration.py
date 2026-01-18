"""Integration test for AI Provider Configuration with .env file

This test verifies that the configuration from .env file is correctly loaded
and can be used to initialize AI clients.
"""

import os
import pytest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.ai_providers import AIProviderConfig, get_provider_config


class TestAIProviderIntegration:
    """Integration tests for AI provider configuration"""

    def test_env_file_exists(self):
        """Verify .env file exists"""
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        assert os.path.exists(env_path), f".env file not found at {env_path}"

    def test_openai_config_from_env(self):
        """Test OpenAI configuration is loaded from environment"""
        config = AIProviderConfig.get_openai_config()

        print(f"\nOpenAI Config:")
        print(
            f"  API Key: {config['api_key'][:20]}..."
            if config["api_key"]
            else "  API Key: (not set)"
        )
        print(f"  Base URL: {config['base_url']}")
        print(f"  Model: {config['model']}")

        assert "api_key" in config
        assert "base_url" in config
        assert "model" in config
        assert "provider" in config
        assert config["provider"] == "openai"

        # Verify model is from environment
        if "OPENAI_MODEL" in os.environ:
            assert config["model"] == os.environ["OPENAI_MODEL"]
            print(f"  ✓ Model loaded from env: {config['model']}")

    def test_anthropic_config_from_env(self):
        """Test Anthropic configuration is loaded from environment"""
        config = AIProviderConfig.get_anthropic_config()

        print(f"\nAnthropic Config:")
        print(
            f"  API Key: {config['api_key'][:20]}..."
            if config["api_key"]
            else "  API Key: (not set)"
        )
        print(f"  Base URL: {config['base_url']}")
        print(f"  Model: {config['model']}")

        assert "api_key" in config
        assert "base_url" in config
        assert "model" in config
        assert "provider" in config
        assert config["provider"] == "anthropic"

        # Verify model is from environment
        if "ANTHROPIC_MODEL" in os.environ:
            assert config["model"] == os.environ["ANTHROPIC_MODEL"]
            print(f"  ✓ Model loaded from env: {config['model']}")

    def test_tongyi_config_from_env(self):
        """Test Tongyi configuration is loaded from environment"""
        config = AIProviderConfig.get_tongyi_config()

        print(f"\nTongyi Config:")
        print(
            f"  API Key: {config['api_key'][:20]}..."
            if config["api_key"]
            else "  API Key: (not set)"
        )
        print(f"  Base URL: {config['base_url']}")
        print(f"  Model: {config['model']}")

        assert "api_key" in config
        assert "base_url" in config
        assert "model" in config
        assert "provider" in config
        assert config["provider"] == "tongyi"

        # Verify model is from environment
        if "TONGYI_MODEL" in os.environ:
            assert config["model"] == os.environ["TONGYI_MODEL"]
            print(f"  ✓ Model loaded from env: {config['model']}")

    def test_dynamic_provider_selection_openai(self):
        """Test dynamic OpenAI provider selection"""
        config = get_provider_config("openai")

        assert config is not None
        assert config["provider"] == "openai"
        assert "model" in config

        print(f"\nDynamic OpenAI Selection:")
        print(f"  Provider: {config['provider']}")
        print(f"  Model: {config['model']}")
        print(f"  Base URL: {config['base_url']}")

    def test_dynamic_provider_selection_anthropic(self):
        """Test dynamic Anthropic provider selection"""
        config = get_provider_config("anthropic")

        assert config is not None
        assert config["provider"] == "anthropic"
        assert "model" in config

        print(f"\nDynamic Anthropic Selection:")
        print(f"  Provider: {config['provider']}")
        print(f"  Model: {config['model']}")
        print(f"  Base URL: {config['base_url']}")

    def test_dynamic_provider_selection_tongyi(self):
        """Test dynamic Tongyi provider selection"""
        config = get_provider_config("tongyi")

        assert config is not None
        assert config["provider"] == "tongyi"
        assert "model" in config

        print(f"\nDynamic Tongyi Selection:")
        print(f"  Provider: {config['provider']}")
        print(f"  Model: {config['model']}")
        print(f"  Base URL: {config['base_url']}")

    def test_default_provider_selection(self):
        """Test automatic default provider selection"""
        default_provider = AIProviderConfig.get_default_provider()

        print(f"\nDefault Provider Selection:")
        print(f"  Default Provider: {default_provider}")

        assert default_provider in ["openai", "anthropic", "tongyi"]

    def test_available_providers_list(self):
        """Test list of available providers"""
        providers = AIProviderConfig.get_available_providers()

        print(f"\nAvailable Providers:")
        for provider in providers:
            print(f"  - {provider}")

        assert len(providers) == 3
        assert "openai" in providers
        assert "anthropic" in providers
        assert "tongyi" in providers

    def test_configuration_integration(self):
        """Comprehensive integration test for all configurations"""
        print("\n" + "=" * 60)
        print("AI PROVIDER CONFIGURATION INTEGRATION TEST")
        print("=" * 60)

        # Load all configurations
        openai_config = AIProviderConfig.get_openai_config()
        anthropic_config = AIProviderConfig.get_anthropic_config()
        tongyi_config = AIProviderConfig.get_tongyi_config()

        # Verify all configurations are loaded
        assert all([openai_config, anthropic_config, tongyi_config])

        # Print summary
        print("\nConfiguration Summary:")
        print(f"  OpenAI: {openai_config['model']} @ {openai_config['base_url']}")
        print(
            f"  Anthropic: {anthropic_config['model']} @ {anthropic_config['base_url']}"
        )
        print(f"  Tongyi: {tongyi_config['model']} @ {tongyi_config['base_url']}")

        print("\n" + "=" * 60)
        print("INTEGRATION TEST PASSED")
        print("=" * 60)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
