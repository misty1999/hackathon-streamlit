from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    """ユーザーの基本情報"""
    username: str
    email: str
    age: int
    gender: str
    bio: Optional[str] = None
    interests: Optional[str] = None

class UserCreate(UserBase):
    """ユーザー作成時のスキーマ"""
    password: str

class User(UserBase):
    """ユーザー情報のスキーマ"""
    id: int
    profile_image_url: Optional[str] = None
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    """トークンのスキーマ"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """トークンデータのスキーマ"""
    email: Optional[str] = None
