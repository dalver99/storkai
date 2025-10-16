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

def home_button(language_choice):
    if st.button("Home" if language_choice == "1" else "홈", key="home_button"):
        st.switch_page("app.py")