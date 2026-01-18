from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow", env_file=".env")

    # PostgreSQL/Supabase 数据库配置
    # Supabase 配置 (来自 docker-compose.supabase.yml)
    database_host: str = "localhost"
    database_port: int = 55432
    database_user: str = "postgres"
    database_password: str = "your-super-secret-password"
    database_name: str = "postgres"

    # 兼容旧配置（用于迁移）
    # mysql_host: str = "localhost"
    # mysql_port: int = 3306
    # mysql_user: str = "root"
    # mysql_password: str = "password"
    # mysql_database: str = "travel_planner"

    # JWT
    jwt_secret: str = "change-this-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    # AI Providers
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4"
    anthropic_api_key: str = ""
    anthropic_base_url: str = "https://api.anthropic.com"
    anthropic_model: str = "claude-3-sonnet-20240229"
    tongyi_api_key: str = ""
    tongyi_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    tongyi_model: str = "qwen-max"

    # Amap
    amap_api_key: str = ""
    amap_web_api_key: str = ""

    # App
    app_name: str = "Travel Planner"
    app_version: str = "1.0.0"
    debug: bool = True

    # 便捷方法：获取数据库连接 URL
    @property
    def database_url(self) -> str:
        """返回 PostgreSQL 数据库连接 URL"""
        return f"postgresql+psycopg2://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
