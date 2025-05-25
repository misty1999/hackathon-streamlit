import streamlit as st
import requests
from .utils import API_BASE_URL, get_auth_headers

def display_user_profile(user):
    """ユーザープロフィールの表示"""
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(
                user["profile_image_url"] or "https://pbs.twimg.com/profile_images/1916445120804864000/DeLpBkOR_400x400.jpg",
                width=150
            )
        with col2:
            st.subheader(user["username"])
            st.write(f"年齢: {user['age']}歳")
            st.write(f"性別: {user['gender']}")
            if user['bio']:
                st.write(f"自己紹介: {user['bio']}")
            if user['interests']:
                st.write(f"興味: {user['interests']}")
            
            if st.button(f"いいね！💕", key=f"like_{user['id']}"):
                send_like(user["id"])
        st.markdown("---")

def send_like(to_user_id):
    """いいねを送信"""
    try:
        like_response = requests.post(
            f"{API_BASE_URL}/likes/",
            params={"from_user_id": st.session_state.user_id},
            json={"to_user_id": to_user_id},
            headers=get_auth_headers()
        )
        if like_response.status_code == 200:
            st.success("いいねを送信しました！(◍•ᴗ•◍)✧*。")
        else:
            st.error(f"エラーが発生しました: {like_response.json()['detail']}")
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")

def get_recommended_users():
    """おすすめユーザーを取得"""
    try:
        response = requests.get(f"{API_BASE_URL}/users/", headers=get_auth_headers())
        if response.status_code == 200:
            users = response.json()
            return [user for user in users if user["id"] != st.session_state.user_id]
        else:
            st.error("ユーザー情報の取得に失敗しました")
            return []
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        return []
