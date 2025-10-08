# streamlit entry page
import streamlit as st
from dotenv import load_dotenv
import os
from page.favorites import favorites
from page.analyze_stock import analyze_stock
from page.ai_chat import ai_chat
from page.settings import settings
from page.help import help
from page.p01_about import about
from page.exit import exit

load_dotenv()
st.set_page_config(layout="wide", page_title="Stork")

# fetch language choice from .env
language_choice = os.getenv("LANGUAGE_CHOICE")

if language_choice == "1":
    st.title("Welcome to Stork")
else:
    st.title("Stork에 오신 것을 환영합니다")


# Show a sidebar of pages but not radio button, but instead show a list of pages, not dropdown, but buttons
with st.sidebar:
    st.button(
        "Home" if language_choice == "1" else "홈",
    )
    st.button(
        "Analyze Stock" if language_choice == "1" else "주식 분석",
        on_click=analyze_stock,
    )
    st.button("Favorites" if language_choice == "1" else "즐겨찾기", on_click=favorites)
    st.button("AI Chat" if language_choice == "1" else "AI 채팅", on_click=ai_chat)
    st.button("Settings" if language_choice == "1" else "설정", on_click=settings)
    st.button("Help" if language_choice == "1" else "도움말", on_click=help)
    st.button("About" if language_choice == "1" else "정보", on_click=about)
    st.button("Exit" if language_choice == "1" else "종료", on_click=exit)
