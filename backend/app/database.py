"""
PostgreSQL/Supabase 数据库配置和会话管理
使用来自 docker-compose.supabase.yml 的配置
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# PostgreSQL 数据库连接 URL
# 格式: postgresql+psycopg2://user:password@host:port/database
DATABASE_URL = settings.database_url

# 创建引擎
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 使用连接前进行健康检查
    pool_recycle=3600,  # 1小时后回收连接
    echo=settings.debug,  # 调试模式下打印 SQL
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()


# 依赖项：获取数据库会话
def get_db():
    """
    依赖注入函数，用于 FastAPI 端点
    每个请求都会获得一个独立的会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 初始化数据库（创建所有表）
def init_db():
    """初始化数据库，创建所有表"""
    from app.db_models import Base  # 导入模型后才能创建

    Base.metadata.create_all(bind=engine)
