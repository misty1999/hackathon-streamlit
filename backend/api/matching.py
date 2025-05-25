from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import database, models
from schemas.matching import LikeCreate, MatchList

router = APIRouter()

@router.post("/likes/")
def create_like(like: LikeCreate, from_user_id: int, db: Session = Depends(database.get_db)):
    """いいねを送信"""
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

@router.get("/matches/{user_id}", response_model=MatchList)
def get_matches(user_id: int, db: Session = Depends(database.get_db)):
    """マッチング一覧を取得"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    
    # マッチしたユーザーの情報を取得
    matches_query = (
        db.query(models.User)
        .join(models.matches, 
            ((models.matches.c.user_id_1 == user_id) & (models.matches.c.user_id_2 == models.User.id)) |
            ((models.matches.c.user_id_2 == user_id) & (models.matches.c.user_id_1 == models.User.id))
        )
        .filter(models.matches.c.is_matched == True)
        .all()
    )

    return {
        "matches": [
            {
                "user_id": match.id,
                "username": match.username,
                "profile_image_url": match.profile_image_url or ""
            }
            for match in matches_query
        ]
    }
