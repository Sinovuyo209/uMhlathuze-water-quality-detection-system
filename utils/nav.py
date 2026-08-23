import streamlit as st


def go_to(page_name):
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if "page_history" not in st.session_state:
        st.session_state.page_history = []
    if st.session_state.page != page_name:
        st.session_state.page_history.append(st.session_state.page)
    st.session_state.page = page_name
    st.rerun()


def go_back():
    if "page_history" not in st.session_state:
        st.session_state.page_history = []
    if st.session_state.page_history:
        st.session_state.page = st.session_state.page_history.pop()
    else:
        st.session_state.page = "Home"
    st.rerun()