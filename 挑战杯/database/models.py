from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(300), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatHistory(Base):
    """聊天记录表"""
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)       # 关联用户ID
    session_id = Column(String(36), nullable=False) # 会话唯一标识
    question = Column(Text, nullable=False)         # 用户问题
    answer = Column(Text, nullable=False)           # 系统回答
    timestamp = Column(DateTime, default=datetime.utcnow)  # 记录时间
    
