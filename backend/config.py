from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Supabase
    supabase_url: str = "http://localhost:54321"
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""

    # JWT
    secret_key: str = "change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    # AI Providers
    openai_api_key: str = ""
    tongyi_api_key: str = ""
    claude_api_key: str = ""

    # Amap
    amap_api_key: str = ""
    amap_web_api_key: str = ""

    # App
    app_name: str = "Travel Planner"
    app_version: str = "0.1.0"
    debug: bool = True

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
