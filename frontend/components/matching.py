import streamlit as st
import requests
from .utils import API_BASE_URL, get_auth_headers

def display_matches():
    """マッチング一覧を表示"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/matches/{st.session_state.user_id}",
            headers=get_auth_headers()
        )
        if response.status_code == 200:
            matches = response.json()["matches"]
            for match in matches:
                st.write(f"💕 {match['username']}")
        else:
            st.error("マッチング情報の取得に失敗しました")
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")

def display_matching_sidebar():
    """マッチング一覧をサイドバーに表示"""
    st.header("マッチング一覧")
    display_matches()
