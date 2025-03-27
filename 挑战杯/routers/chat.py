import uuid
from fastapi import APIRouter, WebSocket, HTTPException, status, Request
from config.security import get_current_user_ws
from services.validator import validator
from utils.logger import APILogger
from schemas.chat import ChatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])
logger = APILogger("ChatRouter")

@router.websocket("/ws")
async def websocket_chat(
    websocket: WebSocket,
    #request: Request
):
    await websocket.accept()
    # 直接从 scope 中拿 app
    the_app = websocket.scope.get("app")  # dict取值
    # 如果你的是新版 Starlette 也可以尝试 websocket.app (但某些版本无此属性)
    qa_engine = the_app.state.qa_engine  # 读取你的自定义 state

    token = websocket.query_params.get("token")
    
    try:
        # 用户认证
        #token = websocket.query_params.get("token")
        user = await get_current_user_ws(token)
        session_id = str(uuid.uuid4())
        
        # 获取问答引擎实例
        #qa_engine = request.app.state.qa_engine
        
        # 发送连接确认
        await websocket.send_json({
            "type": "system",
            "session_id": session_id,
            "message": "连接已建立"
        })
        
        while True:
            # 接收用户消息
            message = await websocket.receive_text()
            
            # 输入验证
            try:
                validator.validate_question(message)
            except HTTPException as e:
                await websocket.send_json({
                    "type": "error",
                    "code": e.status_code,
                    "detail": e.detail
                })
                continue
            
            # 生成回答
            print("📨 接收到用户消息：", message)

            # 在发送前打印
            print("🔄 开始生成回答...")
            try:
                async for response in qa_engine.generate_answer(
                    question=message,
                    user_id=user.id,
                    session_id=session_id
                ):
                    print("📤 向客户端发送内容：", response)
                    await websocket.send_json({
                        "type": "response",
                        "session_id": session_id,
                        "content": response
                    })
                    
            except Exception as e:
                print("❗ WebSocket 内部异常：", str(e))
                logger.error(f"处理失败: {str(e)}")
                await websocket.send_json({
                    "type": "error",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "detail": "内部服务器错误"
                })
                
    except HTTPException as e:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    except Exception as e:
        logger.error(f"连接异常: {str(e)}")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)