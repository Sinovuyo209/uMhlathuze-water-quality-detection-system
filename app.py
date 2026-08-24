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

    # Instant navigation + Unified navy header background wrapping title & nav buttons across all pages
    st.markdown("""
        <style>
        * {
            transition: none !important;
            animation: none !important;
        }
        .nav-container-box {
            background: linear-gradient(135deg, #0b1d28 0%, #15293a 100%);
            border-bottom: 5px solid #2b7a9f;
            padding: 16px 20px;
            margin: -60px -60px 25px -60px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.85);
            width: calc(100% + 120px);
        }
        .top-nav-title {
            color: #ffffff;
            font-size: 1.05rem;
            font-weight: 900;
            line-height: 2.4rem;
            letter-spacing: 0.3px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        /* Force buttons to never wrap their text awkwardly */
        div.stButton > button {
            white-space: nowrap !important;
            font-size: 0.9rem !important;
            padding: 0.35rem 0.5rem !important;
        }
        .block-container {
            padding-top: 1.5rem !important;
        }
        </style>
        <div class="nav-container-box">
    """, unsafe_allow_html=True)

    with st.container():
        # Adjusted column widths to give buttons enough breathing room so text doesn't break
        nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(
            [2.2, 1.0, 1.1, 1.1, 1.0, 1.3]
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