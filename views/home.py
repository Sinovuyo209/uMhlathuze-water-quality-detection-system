import streamlit as st
from styles import get_page_background_css
from utils.nav import go_to


def render():
    st.markdown(get_page_background_css("hero_river.jpg"), unsafe_allow_html=True)

    # Centered container wrapper with custom styling for white text and alignment
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; min-height: 70vh;">
            <div class="home-wrapper" style="width: 100%; max-width: 950px; margin: 0 auto; text-align: center;">
                <div class="home-panel" style="background: rgba(0, 0, 0, 0.65); backdrop-filter: blur(10px); padding: 50px 60px; border-radius: 18px; box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5); border: 1px solid rgba(43, 122, 159, 0.4);">
                    <div class="home-title" style="color: #ffffff; font-size: 2.6rem; font-weight: 800; margin-bottom: 18px; text-align: center; letter-spacing: 0.5px;">
                        uMhlathuze River Water Quality Detection System
                    </div>
                    <div class="home-subtitle" style="color: #76c7c0; font-size: 1.4rem; font-weight: 600; margin-bottom: 28px; text-align: center; letter-spacing: 0.3px;">
                        uMhlathuze River Catchment, KwaZulu-Natal
                    </div>
                    <div class="home-description" style="color: #f0f0f0; font-size: 1.15rem; line-height: 1.7; text-align: center; margin-bottom: 10px;">
                        A supervised machine learning tool that classifies river water quality from physicochemical readings within seconds, developed as a BSc Honours research project at Walter Sisulu University to support communities relying on the uMhlathuze River, where laboratory testing can take up to a week. Trained on 198 real river samples across 18 physicochemical parameters, the XGBoost model achieved 96 percent classification accuracy.
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("Start Assessment", key="home_start_btn", use_container_width=True):
            go_to("Assessment")