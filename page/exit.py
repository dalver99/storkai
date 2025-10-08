import streamlit as st


def exit():
    st.title("Exit")
    st.write("Are you sure you want to exit?")
    if st.button("Yes"):
        st.stop()
    else:
        st.stop()
