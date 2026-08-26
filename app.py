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

    # Styled nav container with larger button sizes and padding
    st.markdown("""
        <style>
        * {
            transition: none !important;
            animation: none !important;
            font-family: Arial, sans-serif !important;
        }
        .block-container {
            padding-top: 1rem !important;
        }
        header {
            visibility: hidden;
            height: 0px;
        }
        /* Streamlit's own thin accent bar (stDecoration) sits above the header,
           independent of it — hide it or it keeps floating above the nav bar. */
        div[data-testid="stDecoration"] {
            display: none !important;
            height: 0 !important;
        }

        /* Kill every source of a top gap and stop the vertical scrollbar from
           throwing off the 100vw full-bleed math below (that's what was
           leaving the sliver of space on the right edge). */
        html, body {
            margin: 0 !important;
            padding: 0 !important;
            overflow-x: hidden !important;
        }
        div[data-testid="stAppViewContainer"],
        section.main,
        div[data-testid="stMain"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
            overflow-x: hidden !important;
        }
        .block-container {
            padding-top: 0 !important;
        }

        /* IMPORTANT: this targets a real Streamlit container (via st.container(key=...))
           that the title and buttons are placed INSIDE of, not a raw <div> opened in one
           st.markdown call and closed in another. Streamlit doesn't let a hand-written
           <div> wrap around widgets rendered in later calls — each call becomes its own
           sibling block — so painting the background here is the only way to get one
           solid box that truly contains the title and every button. */
        div.st-key-nav_container {
            background: linear-gradient(135deg, #0b1d28 0%, #15293a 100%) !important;
            border-bottom: none !important;
            padding: 28px 30px 34px 30px !important;
            margin: 0 0 20px 0 !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.9) !important;
            position: relative !important;
            top: 0 !important;
            left: 50% !important;
            right: 50% !important;
            margin-left: -50vw !important;
            margin-right: -50vw !important;
            width: 100vw !important;
            z-index: 99999;
            box-sizing: border-box !important;
        }
        .top-nav-title {
            color: #ffffff !important;
            font-family: Arial, sans-serif !important;
            font-size: 1.25rem !important;
            font-weight: 900 !important;
            line-height: 2.8rem !important;
            letter-spacing: 0.5px !important;
            white-space: nowrap !important;
        }

        /* Navigation buttons: force solid navy fill on every Streamlit-generated
           button element/state so nothing renders transparent or untinted */
        div.st-key-nav_container div.stButton > button,
        div.st-key-nav_container div[data-testid="stButton"] > button,
        div.st-key-nav_container button[kind="secondary"],
        div.st-key-nav_container button[kind="primary"] {
            white-space: nowrap !important;
            font-family: Arial, sans-serif !important;
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            padding: 0.6rem 0.9rem !important;
            background-color: #1b364d !important;
            background: #1b364d !important;
            color: #ffffff !important;
            border: 2px solid #2b7a9f !important;
            border-radius: 8px !important;
            min-height: 45px !important;
            box-shadow: none !important;
        }
        div.st-key-nav_container div.stButton > button:hover,
        div.st-key-nav_container div[data-testid="stButton"] > button:hover,
        div.st-key-nav_container button[kind="secondary"]:hover,
        div.st-key-nav_container button[kind="primary"]:hover {
            background-color: #2b7a9f !important;
            background: #2b7a9f !important;
            border-color: #ffffff !important;
            color: #ffffff !important;
        }
        div.st-key-nav_container div.stButton > button:focus,
        div.st-key-nav_container div.stButton > button:active,
        div.st-key-nav_container div.stButton > button:focus:not(:active),
        div.st-key-nav_container div[data-testid="stButton"] > button:focus,
        div.st-key-nav_container div[data-testid="stButton"] > button:active {
            background-color: #1b364d !important;
            background: #1b364d !important;
            color: #ffffff !important;
            border: 2px solid #2b7a9f !important;
            box-shadow: none !important;
            outline: none !important;
        }
        /* Streamlit wraps the button label in a <p> / <div> — force it transparent
           so the button's own navy background always shows through */
        div.st-key-nav_container div.stButton > button p,
        div.st-key-nav_container div.stButton > button div,
        div.st-key-nav_container div.stButton > button span {
            font-family: Arial, sans-serif !important;
            color: #ffffff !important;
            background: transparent !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Everything below is rendered INSIDE this one real container, so the CSS
    # background above genuinely wraps around the title and every button.
    with st.container(key="nav_container"):
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