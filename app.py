import streamlit as st
from styles import CUSTOM_CSS
from utils.model_utils import load_models
from utils.nav import go_to
from views import home, assessment, model_performance, research_context, how_it_works


def configure_page():
    st.set_page_config(
        page_title="uMhlathuze Water Quality Classification System",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_top_nav():
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if "page_history" not in st.session_state:
        st.session_state.page_history = []

    # Dropped down, thick full-width navy background bar covering title and buttons completely
    st.markdown("""
        <style>
        * {
            transition: none !important;
            animation: none !important;
        }
        /* Override Streamlit's default header clipping to drop our nav bar down */
        .block-container {
            padding-top: 1rem !important;
        }
        header {
            visibility: hidden;
            height: 0px;
        }
        .nav-container-box {
            background: linear-gradient(135deg, #0b1d28 0%, #15293a 100%) !important;
            border-bottom: 6px solid #2b7a9f !important;
            padding: 22px 30px !important;
            margin: -6rem -6rem 30px -6rem !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.9) !important;
            width: calc(100% + 12rem) !important;
            position: relative;
            z-index: 99999;
        }
        .top-nav-title {
            color: #ffffff !important;
            font-size: 1.25rem !important;
            font-weight: 900 !important;
            line-height: 2.6rem !important;
            letter-spacing: 0.5px !important;
            white-space: nowrap !important;
        }
        div.stButton > button {
            white-space: nowrap !important;
            font-size: 0.95rem !important;
            font-weight: 700 !important;
            padding: 0.45rem 0.6rem !important;
            background-color: #1b364d !important;
            color: #ffffff !important;
            border: 2px solid #2b7a9f !important;
            border-radius: 6px !important;
        }
        div.stButton > button:hover {
            background-color: #2b7a9f !important;
            border-color: #ffffff !important;
        }
        </style>
        <div class="nav-container-box">
    """, unsafe_allow_html=True)

    with st.container():
        nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(
            [2.4, 0.8, 1.1, 1.1, 0.9, 1.2]
        )
        with nav_col1:
            st.markdown('<div class="top-nav-title">uMhlathuze Water Quality Detection System</div>', unsafe_allow_html=True)
        with nav_col2:
            if st.button("Home", key="nav_home", use_container_width=True):
                go_to("Home")
        with nav_col3:
            if st.button("Assessment", key="nav_assessment", use_container_width=True):
                go_to("Assessment")
        with nav_col4:
            if st.button("Performance", key="nav_performance", use_container_width=True):
                go_to("Model Performance")
        with nav_col5:
            if st.button("Research", key="nav_research", use_container_width=True):
                go_to("Research Context")
        with nav_col6:
            if st.button("How It Works", key="nav_how", use_container_width=True):
                go_to("How It Works")

    st.markdown('</div>', unsafe_allow_html=True)


def main():
    configure_page()
    models = load_models()
    render_top_nav()

    page = st.session_state.page

    try:
        if page == "Home":
            home.render()
        elif page == "Assessment":
            assessment.render(models)
        elif page == "Model Performance":
            model_performance.render()
        elif page == "How It Works":
            how_it_works.render()
        else:
            research_context.render()
    except Exception as e:
        st.error(f"An error occurred while loading this page: {e}")
        st.exception(e)


if __name__ == "__main__":
    main()