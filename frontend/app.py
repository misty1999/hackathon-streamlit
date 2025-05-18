import streamlit as st
import requests
import json
from datetime import datetime
import os

# APIのベースURL（開発環境用）
API_BASE_URL = "http://localhost:8000"  # ローカル環境用に変更

# セッション状態の初期化
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None

def login_page():
    st.title("マッチングアプリへようこそ！(｀・ω・´)")
    
    with st.form("login_form"):
        email = st.text_input("メールアドレス")
        password = st.text_input("パスワード", type="password")
        submitted = st.form_submit_button("ログイン")
        
        if submitted:
            # ここでログイン処理を実装
            st.info("ログイン機能は現在開発中です！(๑•̀ㅂ•́)و✧")

def signup_page():
    st.title("新規登録 (๑•̀ㅂ•́)و✧")
    
    with st.form("signup_form"):
        username = st.text_input("ユーザー名")
        email = st.text_input("メールアドレス")
        password = st.text_input("パスワード", type="password")
        age = st.number_input("年齢", min_value=18, max_value=100)
        gender = st.selectbox("性別", ["男性", "女性", "その他"])
        bio = st.text_area("自己紹介")
        interests = st.text_area("興味のあること（カンマ区切りで入力）")
        
        submitted = st.form_submit_button("登録")
        
        if submitted:
            try:
                response = requests.post(
                    f"{API_BASE_URL}/users/",
                    json={
                        "username": username,
                        "email": email,
                        "password": password,
                        "age": age,
                        "gender": gender,
                        "bio": bio,
                        "interests": interests
                    }
                )
                if response.status_code == 200:
                    st.success("登録が完了しました！(◍•ᴗ•◍)✧*。")
                    st.session_state.user_id = response.json()["id"]
                    st.session_state.username = username
                    st.experimental_rerun()
                else:
                    st.error(f"エラーが発生しました: {response.json()['detail']}")
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")

def main_page():
    st.title(f"ようこそ、{st.session_state.username}さん！(◍•ᴗ•◍)✧*。")
    
    # サイドバー
    with st.sidebar:
        st.header("メニュー")
        if st.button("ログアウト"):
            st.session_state.user_id = None
            st.session_state.username = None
            st.experimental_rerun()
        
        st.header("マッチング一覧")
        try:
            response = requests.get(f"{API_BASE_URL}/matches/{st.session_state.user_id}")
            if response.status_code == 200:
                matches = response.json()["matches"]
                for match in matches:
                    st.write(f"💕 {match['username']}")
            else:
                st.error("マッチング情報の取得に失敗しました")
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
    
    # メインコンテンツ
    st.header("おすすめユーザー")
    
    try:
        response = requests.get(f"{API_BASE_URL}/users/")
        if response.status_code == 200:
            users = response.json()
            for user in users:
                if user["id"] != st.session_state.user_id:
                    with st.container():
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.image(
                                user.get("profile_image_url", "https://via.placeholder.com/150"),
                                width=150
                            )
                        with col2:
                            st.subheader(user["username"])
                            st.write(f"年齢: {user['age']}歳")
                            st.write(f"性別: {user['gender']}")
                            st.write(f"自己紹介: {user['bio']}")
                            st.write(f"興味: {user['interests']}")
                            
                            if st.button(f"いいね！💕", key=f"like_{user['id']}"):
                                try:
                                    like_response = requests.post(
                                        f"{API_BASE_URL}/likes/",
                                        params={"from_user_id": st.session_state.user_id},
                                        json={"to_user_id": user["id"]}
                                    )
                                    if like_response.status_code == 200:
                                        st.success("いいねを送信しました！(◍•ᴗ•◍)✧*。")
                                    else:
                                        st.error(f"エラーが発生しました: {like_response.json()['detail']}")
                                except Exception as e:
                                    st.error(f"エラーが発生しました: {str(e)}")
                        st.markdown("---")
        else:
            st.error("ユーザー情報の取得に失敗しました")
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")

# メインアプリケーション
def main():
    st.set_page_config(
        page_title="マッチングアプリ",
        page_icon="💕",
        layout="wide"
    )
    
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