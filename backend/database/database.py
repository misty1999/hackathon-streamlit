from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# データベースURLの設定
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./matching_app.db")
if DATABASE_URL.startswith("sqlite"):
    # Render環境では/tmpディレクトリを使用
    DATABASE_URL = "sqlite:////tmp/matching_app.db"

# エンジンの作成（SQLite用）
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite用の設定
)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# データベースセッションの依存性
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ベースクラスの作成
Base = declarative_base()
