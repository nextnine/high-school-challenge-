AI Tutor 项目说明
本项目是一个基于 FastAPI + WebSocket 实现的 AI 聊天系统，具备以下功能：

用户注册、登录获取 Token

WebSocket 实时对话，向大语言模型提问并返回回答

SQLite 数据库存储用户与聊天记录

简易的问答引擎 (qa_engine)，可对接 HuggingFace 模型

健康检查接口

适用于 Windows 11 环境，使用 Python 3.13.1，在 VSCode 中通过虚拟环境（venv）运行。

目录结构

├─ .env                # 环境变量配置文件
├─ main.py             # FastAPI 应用入口
├─ text.html           # 测试 WebSocket 前端页面
├─ config
│   ├─ settings.py     # 项目设置（模型名、数据库URL、JWT等）
│   └─ security.py     # 加密、token 创建、WebSocket鉴权
├─ services
│   ├─ qa_engine.py    # 模型加载与回答生成逻辑
│   └─ validator.py    # 输入验证（敏感词、长度、字符过滤）
├─ database
│   ├─ models.py       # SQLAlchemy ORM 模型定义
│   ├─ session.py      # 数据库会话，异步引擎
│   └─ crud.py         # 增删查改操作封装
├─ routers
│   ├─ auth.py         # 用户注册、获取 token 等路由
│   ├─ chat.py         # WebSocket 聊天路由
│   └─ health.py       # 健康检查路由
├─ .venv               # (可选) 你的虚拟环境文件夹

注意：.venv 文件夹默认不会上传到 Git 仓库；此处仅说明你可能在该文件夹中创建虚拟环境。

准备环境
1. 安装 Python 3.13.1
可在 Python 官网 下载对应版本并安装。

安装时建议勾选“Add Python to PATH”。

2. 创建虚拟环境 (venv)
在项目根目录执行：


python -m venv .venv
然后激活虚拟环境 (Windows PowerShell)：


.\.venv\Scripts\activate
若使用 VSCode，通常会自动探测 .venv 并激活环境。

3. 安装依赖
确保你处于激活状态后，执行：


pip install fastapi uvicorn[standard] sqlalchemy aiosqlite passlib cryptography python-multipart 
pip install transformers accelerate 
# 以上包含大部分所需，若缺少再补充

配置环境变量
在项目根目录下有一个 .env 文件，包含例如：

env

# 模型配置
DEEPSEEK_API_KEY=xxx
MODEL_NAME=deepseek-ai/deepseek-math-7b-base
MODEL_PRECISION=float16

# 数据库配置
DATABASE_URL=sqlite+aiosqlite:///./tutor.db

# 安全配置
JWT_SECRET=your_jwt_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE=30

# 系统配置
DEBUG=True
MAX_GPU_MEMORY=0.8
可以根据需求修改。
如不需要访问特定模型，可将 MODEL_NAME 改成 "distilgpt2" 等小模型做快速测试。

运行项目
激活虚拟环境后，执行：


uvicorn main:app --reload
控制台会输出：

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
...
访问以下链接：

http://127.0.0.1:8000/docs
查看自动生成的 API 文档，可测试 /register_999、/token、/health 等接口。

http://127.0.0.1:8000/health
健康检查接口

功能说明
1. 用户注册 (/register_999)
URL: POST /register_999

说明: 注册新用户

请求体:


{
  "username": "test",
  "email": "test@example.com",
  "password": "mypassword"
}
返回: 用户的基本信息（不包含密码）

2. 用户登录获取 Token (/token)
URL: POST /token

说明: 登录并获得 JWT Token，用于后续 WebSocket 连接

请求形式: x-www-form-urlencoded


username=test
password=mypassword
返回:

{
  "access_token": "...",
  "token_type": "bearer"
}
3. WebSocket 聊天 (/chat/ws)
URL: ws://127.0.0.1:8000/chat/ws?token=xxx

说明: 建立 WebSocket 长连接，并发送文本消息与 AI 模型交互。

使用方式：

拿到登录后的 access_token，在前端或客户端里拼接到连接 URL 的 token 参数：


ws://127.0.0.1:8000/chat/ws?token=<你的JWT>
连接成功后，会返回一条 JSON 消息：


{
  "type": "system",
  "session_id": "<UUID>",
  "message": "连接已建立"
}
然后发送文本字符串（问题）给服务器，服务器会调用 AI 模型生成答案，返回：


{
  "type": "response",
  "session_id": "...",
  "content": "模型回答"
}
测试 WebSocket (text.html)
项目自带一个简单的 text.html，可在浏览器中打开：

有一个“Token”输入框，粘贴 /token 接口获取的 JWT

点击“连接 WebSocket”，若成功，会显示“已连接 WebSocket”

在下方输入你的问题，点击“发送”，可查看后端返回的回答。

数据持久化
数据库: 使用 SQLite，文件名默认是 tutor.db。

用户表: users

聊天记录表: chat_history

每次模型生成的回答，都会在 chat_history 保存一条记录，含 question, answer, user_id, timestamp 等。

常见问题
WebSocket 连接失败

确认安装了 uvicorn[standard] 或 websockets 库，不然会报 Unsupported upgrade request。

Token 无效

如果提示 401/403，看看登录的用户名密码是否正确，或者 Token 是否过期。

模型推理太慢

7B 模型初次推理耗时可能较高。如果 GPU 内存有限，建议换小模型。

在 .env 或 settings.py 里将 MODEL_NAME 改成 "distilgpt2" 做快速测试。

表结构变动

修改 models.py 后，最好删除或迁移旧的 tutor.db，再次运行会自动创建表。

版本信息
Python: 3.13.1

操作系统: Windows 11

编辑器: VSCode

依赖:

FastAPI

Uvicorn

SQLAlchemy / aiosqlite

passlib

transformers / accelerate

其余详见 requirements.txt

结语
完成以上步骤，就可以在本地运行 AI Tutor 服务，注册用户、获取 Token，并通过 WebSocket 实时与模型交互。若有需要进一步扩展，可以在 qa_engine.py 中替换或微调模型，或在前端引入更完善的界面交互。祝使用愉快！
