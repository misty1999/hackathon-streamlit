import os
import streamlit as st

# APIのベースURL（環境変数から取得）
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def init_session_state():
    """セッション状態の初期化"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'access_token' not in st.session_state:
        st.session_state.access_token = None

def get_auth_headers():
    """認証ヘッダーを取得"""
    return {"Authorization": f"Bearer {st.session_state.access_token}"}

def setup_page():
    """ページの基本設定"""
    st.set_page_config(
        page_title="マッチングアプリ",
        page_icon="💕",
        layout="wide"
    )
