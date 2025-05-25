from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import database, models
from core.security import get_current_user, get_password_hash
from schemas.user import User, UserCreate

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(database.get_db)):
    """新規ユーザーを作成"""
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
    hashed_password = get_password_hash(user.password)
    
    # ユーザーの作成
    db_user = models.User(
        **user.dict(exclude={'password'}),
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    """現在のユーザー情報を取得"""
    return current_user

@router.get("/", response_model=List[User])
def get_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database.get_db)
):
    """ユーザー一覧を取得"""
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    """特定のユーザー情報を取得"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    return user
