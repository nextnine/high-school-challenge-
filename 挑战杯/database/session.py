# database/session.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# 创建一个基础类，用于模型继承
Base = declarative_base()

# 创建异步数据库引擎
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 创建异步 session
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 创建数据库会话的依赖
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

