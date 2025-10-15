# Check if .env has its API Keys Required
import os
import streamlit as st
from dotenv import load_dotenv
from utils.sqlite import query_db_and_close

def check_essential_env_vars():
    load_dotenv()
    required_env_vars = [
        "DART_API_KEY",
        "OPENAI_API_KEY",
        "DATABASE_NAME",
        "DATABASE_TYPE",
        "LANGUAGE_CHOICE",
        "AI_CHOICE",
    ]
    all_good = False

    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            st.error(f"{var} is not set")
            missing_vars.append(var)

    if not missing_vars:
        all_good = True

    else:
        st.error(
            "Some of the required variables are not set. Please run 'python install.py' to set the required variables"
        )
        # in Koreran too
        st.error(
            "일부 필수 변수가 설정되지 않았습니다 'python install.py'를 실행하여 필수 변수를 설정해주세요"
        )

    return all_good

def check_if_favorite_stock_exists():
    load_dotenv()
    language_choice = os.getenv("LANGUAGE_CHOICE")
    favorite_stocks = query_db_and_close("SELECT * FROM favorite_stocks")
    if len(favorite_stocks) == 0:
        # st.error("No favorite stocks found" if language_choice == "1" else "관심 종목이 없습니다.")
        return False
    return True