import streamlit as st
import os
from utils.ui import hide_sidebar
from dotenv import load_dotenv

hide_sidebar()

load_dotenv(override=True)
language_choice = os.getenv("LANGUAGE_CHOICE")
st.title("Settings" if language_choice == "1" else "설정")


def change_language():
    # Toggle text based on current language
    if language_choice == "1":
        new_lang = "2"
        button_label = "한국어 / Korean"
    else:
        new_lang = "1"
        button_label = "영어 / English"

    # Single toggle button
    if st.button(button_label):
        # Rewrite .env file with the new language
        with open(".env", "r") as f:
            lines = f.readlines()
        lines = [line for line in lines if not line.startswith("LANGUAGE_CHOICE=")]
        lines.append(f"LANGUAGE_CHOICE={new_lang}\n")
        with open(".env", "w") as f:
            f.writelines(lines)

        # Reload environment
        load_dotenv(override=True)
        st.rerun()


change_language()

# Navigate button back to home
if st.button("Back to Home" if language_choice == "1" else "홈으로 돌아가기"):
    st.switch_page("app.py")
