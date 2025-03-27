from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.settings import settings  # 添加settings导入
from database.session import engine, Base
from routers import auth, chat, health
from services.qa_engine import QaEngine
from utils.logger import setup_logging
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import traceback


@asynccontextmanager
async def lifespan(app: FastAPI):
    """替代原有的on_event启动逻辑"""
    # 初始化日志
    setup_logging()
    
    # 初始化数据库
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ 数据库表创建完成")

    '''
    if settings.PREWARM_MODEL:
        dummy_input = "预热模型"
        await app.state.qa_engine.generate_answer(dummy_input, 0, "prewarm")
    '''    
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

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("🔴 全局异常捕获:", exc)
    traceback.print_exc()   # 这会打印完整报错堆栈
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误，请查看控制台"},
    )
    
# 测试路由  

#@app.post("/test_hello")
#def test_hello():
#    print("🔥 进入 test_hello 路由")
#    return {"msg": "ok"}


# 注册路由
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(health.router)