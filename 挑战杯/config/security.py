from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status, WebSocket
from passlib.context import CryptContext
from config.settings import settings
from database.crud import get_user_by_username
from database.session import get_db
from schemas.user import UserRead

# 密码加密配置
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    """创建JWT令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

async def get_current_user_ws(token: str) -> UserRead:
    """WebSocket专用用户认证"""
    if not token:
        raise HTTPException(
            status_code=status.WS_1008_POLICY_VIOLATION,
            detail="缺少认证令牌"
        )
    
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.WS_1008_POLICY_VIOLATION,
                detail="无效凭证"
            )
    except JWTError as e:
        raise HTTPException(
            status_code=status.WS_1008_POLICY_VIOLATION,
            detail="凭证验证失败"
        )
    
    async for session in get_db():
        user = await get_user_by_username(session, username)
        if not user:
            raise HTTPException(
                status_code=status.WS_1008_POLICY_VIOLATION,
                detail="用户不存在"
            )
        return UserRead.from_orm(user)  # 注意这里使用from_attributes