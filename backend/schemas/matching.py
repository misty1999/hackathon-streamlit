from pydantic import BaseModel
from typing import List

class LikeCreate(BaseModel):
    """いいね作成時のスキーマ"""
    to_user_id: int

class MatchUser(BaseModel):
    """マッチしたユーザーの情報"""
    user_id: int
    username: str
    profile_image_url: str

class MatchList(BaseModel):
    """マッチング一覧のスキーマ"""
    matches: List[MatchUser]
