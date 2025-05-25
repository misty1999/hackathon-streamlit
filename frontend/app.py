import streamlit as st
from components.utils import init_session_state, setup_page
from components.auth import login_page, signup_page, logout
from components.user import display_user_profile, get_recommended_users
from components.matching import display_matching_sidebar

def main_page():
    """メインページの表示"""
    st.title(f"ようこそ、{st.session_state.username}さん！(◍•ᴗ•◍)✧*。")
    
    # サイドバー
    with st.sidebar:
        st.header("メニュー")
        if st.button("ログアウト"):
            logout()
        display_matching_sidebar()
    
    # メインコンテンツ
    st.header("おすすめユーザー")
    recommended_users = get_recommended_users()
    for user in recommended_users:
        display_user_profile(user)

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
