from contextlib import asynccontextmanager
from fastapi import FastAPI
from utils.logger import setup_logging
from database.session import engine, Base
from routers import auth, chat, health
from services.qa_engine import QaEngine

@asynccontextmanager
async def lifespan(app: FastAPI):
    """替代原有的on_event启动逻辑"""
    # 初始化日志
    setup_logging()
    
    # 初始化数据库
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 加载模型
    qa_engine = QaEngine()
    await qa_engine.initialize()
    app.state.qa_engine = qa_engine  # 存储到app状态
    
    yield  # 应用运行期间保持
    
    # 关闭逻辑（可选）
    await engine.dispose()

app = FastAPI(
    title="AI Tutor",
    lifespan=lifespan,  # 注册生命周期处理器
    version="1.0.0"
)

# 注册路由
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(health.router)