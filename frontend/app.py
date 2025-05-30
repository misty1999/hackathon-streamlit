import streamlit as st
from components.utils import init_session_state, setup_page
from components.auth import login_page, signup_page, logout
from components.notes import render_notes

def main_page():
    """メインページの表示"""
    # サイドバー
    with st.sidebar:
        st.header("メニュー")
        if st.button("ログアウト"):
            logout()
    
    st.title(f"ようこそ、{st.session_state.username}さん！(◍•ᴗ•◍)✧*。")
    render_notes()

def main():
    """メインアプリケーション"""
    setup_page()
    init_session_state()
    
    if st.session_state.user_id is None:
        tab1, tab2 = st.tabs(["ログイン", "新規登録"])
        with tab1:
            login_page()
        with tab2:
            signup_page()
    else:
        main_page()

if __name__ == "__main__":
    main()
