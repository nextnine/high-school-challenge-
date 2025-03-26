from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User, ChatHistory  # 确保导入User模型

async def get_user_by_username(session: AsyncSession, username: str):
    """根据用户名获取用户"""
    result = await session.execute(
        select(User)
        .where(User.username == username)
    )
    return result.scalars().first()

async def create_user(session: AsyncSession, user_data: dict):
    """创建新用户"""
    db_user = User(**user_data)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

async def get_chat_history(session: AsyncSession, user_id: int, limit: int = 5):
    """获取用户聊天历史"""
    result = await session.execute(
        select(ChatHistory)
        .where(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.timestamp.desc())
        .limit(limit)
    )
    return result.scalars().all()

async def save_chat_record(
    session: AsyncSession,
    user_id: int,
    question: str,
    answer: str,
    session_id: str
):
    """保存聊天记录"""
    new_record = ChatHistory(
        user_id=user_id,
        question=question,
        answer=answer,
        session_id=session_id
    )
    session.add(new_record)
    await session.commit()
    return new_record