from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy_utils import database_exists, create_database

from core.config import (
    SQLALCHEMY_DATABASE_URL,
    CORS_ORIGINS,
    CORS_CREDENTIALS,
    CORS_METHODS,
    CORS_HEADERS,
    logger
)
from database import database
from api.middleware import log_requests
from api.auth import router as auth_router
from api.users import router as users_router
from api.matching import router as matching_router

app = FastAPI(title="マッチングアプリ API")

# ミドルウェアの設定
app.middleware("http")(log_requests)

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

# ルーターの登録
app.include_router(auth_router, tags=["認証"])
app.include_router(users_router, prefix="/users", tags=["ユーザー"])
app.include_router(matching_router, tags=["マッチング"])

def init_db():
    """データベースの初期化"""
    try:
        engine = database.engine
        connection = engine.connect()
        
        try:
            # データベースの存在確認と作成
            if not database_exists(SQLALCHEMY_DATABASE_URL):
                create_database(SQLALCHEMY_DATABASE_URL)
                logger.info("データベースを作成しました")
            else:
                logger.info("データベースは既に存在します")
            
            logger.info("データベースの初期化が完了しました")
            
        except Exception as e:
            logger.error(f"データベース初期化中にエラーが発生: {str(e)}")
            raise
        finally:
            connection.close()
            
    except Exception as e:
        logger.error(f"データベース接続エラー: {str(e)}")
        raise

# アプリケーション起動時にデータベースを初期化
@app.on_event("startup")
async def startup_event():
    init_db()
