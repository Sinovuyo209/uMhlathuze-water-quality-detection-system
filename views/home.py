import streamlit as st
from styles import get_page_background_css
from utils.nav import go_to


def render():
    st.markdown(get_page_background_css("hero_river.jpg"), unsafe_allow_html=True)

    # Centered container wrapper with custom styling for white text and alignment
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; min-height: 70vh;">
            <div class="home-wrapper" style="width: 100%; max-width: 850px; margin: 0 auto; text-align: center;">
                <div class="home-panel" style="background: rgba(0, 0, 0, 0.55); backdrop-filter: blur(8px); padding: 40px; border-radius: 15px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);">
                    <div class="home-title" style="color: #ffffff; font-size: 2.3rem; font-weight: 700; margin-bottom: 15px; text-align: center;">
                        uMhlathuze River Water Quality Detection System
                    </div>
                    <div class="home-subtitle" style="color: #ffffff; font-size: 1.3rem; font-weight: 500; margin-bottom: 25px; text-align: center;">
                        uMhlathuze River Catchment, KwaZulu-Natal
                    </div>
                    <div class="home-description" style="color: #ffffff; font-size: 1.05rem; line-height: 1.6; text-align: center; margin-bottom: 30px;">
                        A supervised machine learning tool that classifies river water quality from physicochemical readings within seconds, developed as a BSc Honours research project at Walter Sisulu University to support communities relying on the uMhlathuze River, where laboratory testing can take up to a week. Trained on 198 real river samples across 18 physicochemical parameters, the XGBoost model achieved 96 percent classification accuracy.
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Start Assessment", key="home_start_btn", use_container_width=True):
            go_to("Assessment") 