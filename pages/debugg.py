#Show faborites table in database
import os
import streamlit as st
from utils.ui import hide_sidebar, home_button
from utils.sqlite import query_db_and_close
from dotenv import load_dotenv
import pandas as pd

def debugg():
    load_dotenv()
    language_choice = os.getenv("LANGUAGE_CHOICE")
    hide_sidebar()
    st.title("Debug" if language_choice == "1" else "디버그")
    st.write("---")
    st.write("### Favorites table in database")
    #Show favorites table in database
    favorites = query_db_and_close("SELECT * FROM company_info")
    # If loading takes long or returns nothing, display a message
    if not favorites or len(favorites) == 0:
        st.warning("No data to display, or loading took too long." if language_choice == "1" else "표시할 데이터가 없거나, 불러오기에 시간이 너무 오래 걸립니다.")
    else:
        # Try to display with column information (as a DataFrame)
        df = pd.DataFrame(favorites)
        st.dataframe(df)
    st.write("---")
    home_button(language_choice)

debugg()