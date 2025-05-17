from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import models
from database import database
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI(title="マッチングアプリ API")

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# パスワードハッシュ化の設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydanticモデル
class UserBase(BaseModel):
    username: str
    email: str
    age: int
    gender: str
    bio: Optional[str] = None
    interests: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    profile_image_url: Optional[str] = None
    created_at: datetime
    is_active: bool

    class Config:
        orm_mode = True

class LikeCreate(BaseModel):
    to_user_id: int

# ユーザー関連のエンドポイント
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(database.get_db)):
    # ユーザー名とメールアドレスの重複チェック
    db_user = db.query(models.User).filter(
        (models.User.username == user.username) | 
        (models.User.email == user.email)
    ).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ユーザー名またはメールアドレスが既に使用されています"
        )
    
    # パスワードのハッシュ化
    hashed_password = pwd_context.hash(user.password)
    
    # ユーザーの作成
    db_user = models.User(
        **user.dict(exclude={'password'}),
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[User])
def get_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database.get_db)
):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    return user

# マッチング関連のエンドポイント
@app.post("/likes/")
def create_like(like: LikeCreate, from_user_id: int, db: Session = Depends(database.get_db)):
    # 既存のいいねをチェック
    existing_like = db.query(models.Like).filter(
        models.Like.from_user_id == from_user_id,
        models.Like.to_user_id == like.to_user_id
    ).first()
    
    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="既にいいねを送っています"
        )
    
    # 新しいいいねを作成
    db_like = models.Like(from_user_id=from_user_id, to_user_id=like.to_user_id)
    db.add(db_like)
    
    # マッチングのチェック
    mutual_like = db.query(models.Like).filter(
        models.Like.from_user_id == like.to_user_id,
        models.Like.to_user_id == from_user_id
    ).first()
    
    if mutual_like:
        # マッチングを作成
        db.execute(
            models.matches.insert().values(
                user_id_1=min(from_user_id, like.to_user_id),
                user_id_2=max(from_user_id, like.to_user_id),
                is_matched=True
            )
        )
    
    db.commit()
    return {"message": "いいねを送信しました"}

@app.get("/matches/{user_id}")
def get_matches(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    
    return {
        "matches": [
            {
                "user_id": match.id,
                "username": match.username,
                "profile_image_url": match.profile_image_url
            }
            for match in user.matches
        ]
    } 