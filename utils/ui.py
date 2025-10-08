import streamlit as st


def hide_sidebar():
    st.markdown(
        """
    <style>
    .stSidebar {
        display: none;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
