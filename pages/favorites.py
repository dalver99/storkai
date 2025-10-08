import streamlit as st
from utils.ui import hide_sidebar
from utils.check import check_essential_env_vars


def favorites():
    st.title("Favorites")
    st.write("This is the favorites page")

    # Show list of favorites, add or remove
    if check_essential_env_vars():
        st.write("Favorites")
    else:
        st.write("No favorites found")


favorites()
