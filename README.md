# Streamlit + FastAPI + SQLAlchemy プロジェクト

このプロジェクトは、Streamlitを使用したフロントエンド、FastAPIを使用したバックエンドAPI、そしてSQLAlchemyを使用したデータベース操作を組み合わせたアプリケーションです。

## プロジェクト構成

```
hackathon/
├── backend/          # バックエンド関連のコード
│   ├── api/         # FastAPIエンドポイント
│   └── database/    # データベースモデルと設定
└── frontend/        # Streamlitアプリケーション
```

## セットアップ方法

### バックエンドのセットアップ

```bash
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload
```

### フロントエンドのセットアップ

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

## 使用技術

- フロントエンド: Streamlit
- バックエンド: FastAPI
- データベース: SQLAlchemy
- データベースエンジン: SQLite (開発環境)

## 開発者

あなたの名前をここに書いてください！ 

# バックエンド設定
DATABASE_URL=mysql://root:password@localhost/matching_app
SECRET_KEY=your-secret-key-here  # 本番環境では必ず変更してください！

# フロントエンド設定
API_BASE_URL=http://localhost:8000 