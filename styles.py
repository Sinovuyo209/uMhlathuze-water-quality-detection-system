import base64
import os
import streamlit as st


CUSTOM_CSS = """
    <style>
    html, body, [class*="css"] { font-size: 18px; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    section[data-testid="stSidebar"] {display: none;}

    [data-testid="stAppViewContainer"] {
        background-color: #ffffff;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }

    [data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
    }

    .st-key-nav_bar {
        background: #062c43;
        padding: 1.6rem 2rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    .st-key-nav_bar [data-testid="stHorizontalBlock"] {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.6rem;
    }
    .st-key-nav_bar [data-testid="column"] {
        width: fit-content !important;
        flex: 0 0 auto !important;
    }
    .nav-brand {
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 800;
        white-space: nowrap;
        margin-right: 1.2rem;
    }
    .st-key-nav_bar button {
        background-color: #0a4d68 !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 0.5rem 1.2rem !important;
        white-space: nowrap;
    }
    .st-key-nav_bar button:hover {
        background-color: #087ea8 !important;
    }

    .st-key-home_wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: calc(100vh - 160px);
    }
    .st-key-home_panel {
        background: rgba(255, 255, 255, 0.55);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 2px solid rgba(6, 44, 67, 0.22);
        border-radius: 16px;
        padding: 3.4rem 4rem;
        max-width: 960px;
        margin: 0 auto;
        box-shadow: 0 16px 48px rgba(6, 44, 67, 0.28);
    }
    .home-title {
        color: #062c43;
        font-size: 2.7rem;
        font-weight: 800;
        line-height: 1.25;
        text-align: center;
        border-bottom: 2px solid rgba(6, 44, 67, 0.18);
        padding-bottom: 1rem;
        margin-bottom: 1.2rem;
    }
    .home-subtitle {
        color: #0a4d68;
        font-size: 1.35rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.2rem;
    }
    .home-description {
        color: #0d2233;
        font-size: 1.2rem;
        line-height: 1.8;
        text-align: left;
    }

    div.stButton > button {
        background-color: #0a4d68;
        color: #ffffff !important;
        font-size: 1.1rem;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 0.75rem 2.4rem;
    }
    div.stButton > button:hover {
        background-color: #087ea8;
        color: #ffffff !important;
    }

    .st-key-assessment_panel {
        background: rgba(255, 255, 255, 0.62);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 16px;
        padding: 2.4rem 2.8rem;
        max-width: 1200px;
        margin: 0 auto;
        box-shadow: 0 10px 34px rgba(6, 44, 67, 0.22);
    }

    .section-title {
        color: #062c43;
        font-size: 1.9rem;
        font-weight: 800;
        margin: 0 0 0.4rem 0;
    }
    .section-subtitle {
        color: #3d566b;
        font-size: 1.15rem;
        line-height: 1.65;
        margin-bottom: 1.1rem;
    }
    .step-card {
        background: #eef5fa;
        border-left: 4px solid #0a4d68;
        border-radius: 6px;
        padding: 1.1rem 1.3rem;
        height: 100%;
    }
    .step-number {
        color: #0a4d68;
        font-weight: 800;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .step-text {
        color: #2c4a5e;
        font-size: 1rem;
        margin-top: 0.3rem;
    }
    .faq-question {
        color: #062c43;
        font-size: 1.15rem;
        font-weight: 800;
        margin-top: 1.1rem;
        margin-bottom: 0.3rem;
    }
    .faq-answer {
        color: #3d566b;
        font-size: 1.02rem;
        line-height: 1.6;
    }

    div[data-testid="stNumberInput"] label {
        color: #062c43 !important;
        font-weight: 700 !important;
        font-size: 1.08rem !important;
    }
    div[data-testid="stNumberInput"] input {
        font-size: 1.15rem !important;
        padding: 0.6rem 0.8rem !important;
    }

    .st-key-assessment_tab_bar [data-testid="stHorizontalBlock"] {
        gap: 1rem !important;
    }
    .st-key-assessment_tab_bar button {
        background-color: #0a4d68 !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.9rem 1rem !important;
    }
    .st-key-assessment_tab_bar button:hover {
        background-color: #087ea8 !important;
        color: #ffffff !important;
    }

    .result-box { border-radius: 10px; padding: 2rem; margin-top: 1rem; }
    .result-excellent { background: #e8f4fa; border-left: 6px solid #0a4d68; }
    .result-good { background: #eef5fa; border-left: 6px solid #087ea8; }
    .result-poor { background: #d9ecf5; border-left: 6px solid #05374f; }
    .result-critical { background: #cfe6f2; border-left: 6px solid #062c43; }
    .result-label { color: #062c43; font-size: 1.7rem; font-weight: 800; margin-bottom: 0.5rem; }
    .result-description { color: #2c4a5e; font-size: 1.05rem; margin-bottom: 1rem; }
    .reason-item { color: #05374f; font-size: 1rem; padding: 0.45rem 0; border-bottom: 1px solid #d8e4ea; }

    .caption-text { color: #6d8194; font-size: 0.88rem; font-style: italic; margin-top: 0.35rem; }

    .nav-bottom-row {
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(6,44,67,0.12);
    }
    </style>
"""


@st.cache_data
def get_image_base64(image_filename):
    image_path = os.path.join("assets", image_filename)
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        ext = image_filename.split(".")[-1]
        return f"data:image/{ext};base64,{encoded}"
    return None


def get_page_background_css(image_filename):
    bg_data = get_image_base64(image_filename)
    if bg_data:
        bg_rule = f"background-image: url('{bg_data}');"
    else:
        bg_rule = "background: linear-gradient(120deg, #062c43, #0a4d68);"

    return f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            {bg_rule}
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
    """