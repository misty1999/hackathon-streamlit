from . import models
from . import database

def init_tables():
    try:
        # テーブルを作成
        models.Base.metadata.create_all(bind=database.engine)
        print("テーブルの作成が完了しました！(◍•ᴗ•◍)")
    except Exception as e:
        print(f"テーブル作成中にエラーが発生しました: {str(e)}")
        raise

if __name__ == "__main__":
    init_tables()
