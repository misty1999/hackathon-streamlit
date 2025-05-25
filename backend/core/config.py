import os
import logging
from datetime import timedelta

# JWT設定
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")  # 本番環境では環境変数から取得
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# データベース設定
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./matching_app.db"  # PostgreSQLからSQLiteに変更
)

# CORS設定
CORS_ORIGINS = ["*"]  # 本番環境では適切に制限してください
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# ロギング設定
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()
