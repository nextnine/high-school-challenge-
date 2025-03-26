from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime

    # Pydantic V2新配置方式
    model_config = ConfigDict(from_attributes=True)  # 替代原来的orm_mode