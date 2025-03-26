from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from database.crud import get_user_by_username, create_user  # 确保正确导入
from config.security import (
    verify_password,
    create_access_token,
    get_password_hash
)
from schemas.user import UserCreate, UserRead
from database.session import get_db

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate):
    async for session in get_db():
        # 检查用户是否存在
        existing_user = await get_user_by_username(session, user.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 创建新用户
        hashed_password = get_password_hash(user.password)
        db_user = await create_user(
            session,
            {
                "username": user.username,
                "email": user.email,
                "hashed_password": hashed_password
            }
        )
        return db_user

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    async for session in get_db():
        user = await get_user_by_username(session, form_data.username)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效凭证",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {
            "access_token": create_access_token({"sub": user.username}),
            "token_type": "bearer"
        }