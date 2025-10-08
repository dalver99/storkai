# streamlit entry page
import os
import streamlit as st
from dotenv import load_dotenv
from utils.check import check_essential_env_vars
from utils.ui import hide_sidebar

load_dotenv()
st.set_page_config(layout="wide", page_title="Stork")

# Hide the default sidebar
hide_sidebar()

# fetch language choice from .env
language_choice = os.getenv("LANGUAGE_CHOICE")

if language_choice == "1":
    st.title("Welcome to Stork!")
else:
    st.title("Stork에 오신 것을 환영합니다!")

st.write("---")


if check_essential_env_vars():
    st.toast(
        (
            "All required variables are set"
            if language_choice == "1"
            else "모든 필수 변수가 설정되었습니다"
        ),
        icon="🎉",
    )

    # Show page navigation buttons at the top of the main page instead of the sidebar
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📈 Analyze Stock" if language_choice == "1" else "📈 주식 분석"):
            st.switch_page("pages/analyze_stock.py")
    with col2:
        if st.button("🌟 Favorites" if language_choice == "1" else "🌟 관심 종목"):
            st.switch_page("pages/favorites.py")
    with col3:
        if st.button("💬 AI Chat" if language_choice == "1" else "💬 AI 채팅"):
            st.switch_page("pages/ai_chat.py")

    st.write("---")
    # footer

    col4, col5 = st.columns(2)
    with col4:
        if st.button("🛠️ Settings" if language_choice == "1" else "🛠️ 설정"):
            st.switch_page("pages/settings.py")
    with col5:
        if st.button("💡 About" if language_choice == "1" else "💡 정보"):
            st.switch_page("pages/about.py")
