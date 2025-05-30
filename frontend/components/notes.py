import streamlit as st
import requests
import markdown
from .utils import handle_error

def render_notes():
    # カスタムCSS
    st.markdown("""
        <style>
        .stApp {
            background-color: #FFF8F0;
        }
        .css-1d391kg {  /* サイドバーのスタイル */
            background-color: #FFE4E1;
        }
        .stButton>button {
            background-color: #FF7F50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #FF6B6B;
            transform: translateY(-2px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .stTextInput>div>div>input {
            background-color: white;
            border: 1px solid #FFB6C1;
            border-radius: 5px;
        }
        .stTextArea>div>div>textarea {
            background-color: white;
            border: 1px solid #FFB6C1;
            border-radius: 5px;
        }
        .css-10trblm {  /* タイトルのスタイル */
            color: #333333;
        }
        </style>
    """, unsafe_allow_html=True)

    if "user_id" not in st.session_state or not st.session_state.user_id:
        st.warning("ログインしてください。", icon="⚠️")
        return

    st.title("📝 メモ帳")

    # 左サイドバー: メモリスト
    with st.sidebar:
        st.subheader("メモ一覧")
        
        # 検索機能
        search_query = st.text_input("メモを検索", key="search_notes")
        if search_query:
            response = requests.get(
                f"http://localhost:8000/notes/search/?query={search_query}",
                headers={"Authorization": f"Bearer {st.session_state.access_token}"}
            )
            if response.status_code == 200:
                notes = response.json()
            else:
                handle_error("メモの検索に失敗しました", response)
                notes = []
        else:
            response = requests.get(
                "http://localhost:8000/notes/",
                headers={"Authorization": f"Bearer {st.session_state.access_token}"}
            )
            if response.status_code == 200:
                notes = response.json()
            else:
                handle_error("メモの取得に失敗しました", response)
                notes = []
        
        # メモリストの表示
        selected_note = None
        for note in notes:
            if st.button(note["title"], key=f"note_{note['id']}", use_container_width=True):
                selected_note = note

    # メインエリア
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.subheader("新規メモ作成")
        with st.form("create_note", clear_on_submit=True):
            title = st.text_input("タイトル")
            content = st.text_area("内容（マークダウン対応）", height=300)
            parent_id = None
            if notes:
                parent_options = ["なし"] + [note["title"] for note in notes]
                parent_idx = st.selectbox("親メモ", options=range(len(parent_options)), format_func=lambda x: parent_options[x])
                if parent_idx > 0:
                    parent_id = notes[parent_idx - 1]["id"]
            
            if st.form_submit_button("保存"):
                response = requests.post(
                    "http://localhost:8000/notes/",
                    headers={"Authorization": f"Bearer {st.session_state.access_token}"},
                    json={"title": title, "content": content, "parent_id": parent_id}
                )
                if response.status_code == 200:
                    st.success("メモを作成しました")
                    st.rerun()
                else:
                    handle_error("メモの作成に失敗しました", response)

    with col2:
        if selected_note:
            st.subheader("メモの編集")
            with st.form("edit_note"):
                new_title = st.text_input("タイトル", value=selected_note["title"])
                new_content = st.text_area("内容（マークダウン対応）", value=selected_note["content"], height=300)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("更新"):
                        response = requests.put(
                            f"http://localhost:8000/notes/{selected_note['id']}",
                            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
                            json={"title": new_title, "content": new_content, "parent_id": selected_note["parent_id"]}
                        )
                        if response.status_code == 200:
                            st.success("メモを更新しました")
                            st.rerun()
                        else:
                            handle_error("メモの更新に失敗しました", response)
                
                with col2:
                    if st.form_submit_button("削除", type="secondary"):
                        response = requests.delete(
                            f"http://localhost:8000/notes/{selected_note['id']}",
                            headers={"Authorization": f"Bearer {st.session_state.access_token}"}
                        )
                        if response.status_code == 200:
                            st.success("メモを削除しました")
                            st.rerun()
                        else:
                            handle_error("メモの削除に失敗しました", response)
            
            st.subheader("プレビュー")
            st.markdown(selected_note["content"])
            
            if selected_note.get("children"):
                st.subheader("子メモ")
                for child in selected_note["children"]:
                    st.text(f"- {child['title']}")
