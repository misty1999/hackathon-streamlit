import streamlit as st
import requests
from .utils import API_BASE_URL, get_auth_headers

def login_page():
    """ログインページの表示と処理"""
    st.title("メモアプリへようこそ！(｀・ω・´)")
    
    with st.form("login_form"):
        email = st.text_input("メールアドレス")
        password = st.text_input("パスワード", type="password")
        submitted = st.form_submit_button("ログイン")
        
        if submitted:
            try:
                response = requests.post(
                    f"{API_BASE_URL}/token",
                    data={
                        "username": email,
                        "password": password
                    }
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    st.session_state.access_token = token_data["access_token"]
                    
                    # ユーザー情報を取得
                    user_response = requests.get(f"{API_BASE_URL}/users/me", headers=get_auth_headers())
                    
                    if user_response.status_code == 200:
                        user_data = user_response.json()
                        st.session_state.user_id = user_data["id"]
                        st.session_state.username = user_data["username"]
                        st.success("ログインしました！(◍•ᴗ•◍)✧*。")
                        st.rerun()
                else:
                    st.error(response.json()["detail"])
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")

def signup_page():
    """サインアップページの表示と処理"""
    st.title("新規登録 (๑•̀ㅂ•́)و✧")
    
    with st.form("signup_form"):
        username = st.text_input("ユーザー名")
        email = st.text_input("メールアドレス")
        password = st.text_input("パスワード", type="password")
        
        submitted = st.form_submit_button("登録")
        
        if submitted:
            try:
                response = requests.post(
                    f"{API_BASE_URL}/users/",
                    json={
                        "username": username,
                        "email": email,
                        "password": password,
                        "age": 0,
                        "gender": "その他",
                        "bio": "",
                        "interests": ""
                    }
                )
                if response.status_code == 200:
                    st.success("登録が完了しました！(◍•ᴗ•◍)✧*。")
                    user_data = response.json()
                    
                    # ログイントークンを取得
                    login_response = requests.post(
                        f"{API_BASE_URL}/token",
                        data={
                            "username": email,
                            "password": password
                        }
                    )
                    
                    if login_response.status_code == 200:
                        token_data = login_response.json()
                        st.session_state.access_token = token_data["access_token"]
                        st.session_state.user_id = user_data["id"]
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("ログインに失敗しました")
                else:
                    st.error(f"エラーが発生しました: {response.json()['detail']}")
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")

def logout():
    """ログアウト処理"""
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.access_token = None
    st.rerun()
