import streamlit as st
from config import RESEARCH_INFO
from utils.nav import go_back, go_to


def render():
    st.markdown('<div class="section-title">Research Context</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="section-subtitle">
    <strong style="font-size:1.4rem; color:#062c43;">Research Title</strong><br>
    <span style="font-size:1.1rem;">{RESEARCH_INFO['title']}</span><br><br>

    <strong style="font-size:1.4rem; color:#062c43;">Problem Statement</strong><br>
    <span style="font-size:1.1rem;">Rural communities around the uMhlathuze River in KwaZulu-Natal depend on river water for
    domestic use, yet access to regular water quality monitoring remains limited. Laboratory
    testing is costly and typically takes three to seven days, delaying the detection of
    contamination events and increasing the risk of waterborne disease.</span><br><br>

    <strong style="font-size:1.4rem; color:#062c43;">Research Objectives</strong><br>
    <span style="font-size:1.1rem;">
    1. Identify the key variables that most significantly influence water quality in South African rivers.<br>
    2. Develop and evaluate machine learning models for detecting water quality.<br>
    3. Design and develop a web-based prototype integrating a machine learning model for water quality detection.
    </span><br><br>

    <strong style="font-size:1.4rem; color:#062c43;">Methodology</strong><br>
    <span style="font-size:1.1rem;">This study follows the Design Science Research Methodology (DSRM) integrated with
    the Cross-Industry Standard Process for Data Mining (CRISP-DM), covering data
    understanding, data preparation, modelling, evaluation, and deployment phases.</span><br><br>

    <strong style="font-size:1.4rem; color:#062c43;">Dataset</strong><br>
    <span style="font-size:1.1rem;">The uMhlathuze water quality dataset comprises 198 real river water samples measured
    across 18 physicochemical parameters, sourced from the uMhlathuze catchment in
    KwaZulu-Natal, South Africa. Class imbalance in the dataset was addressed using the
    Synthetic Minority Over-sampling Technique (SMOTE).</span><br><br>

    <strong style="font-size:1.4rem; color:#062c43;">Key Findings</strong><br>
    <span style="font-size:1.1rem;">XGBoost achieved the highest classification accuracy at 96%, outperforming Random Forest
    (92%) and Decision Tree (82%). Aluminium, Cobalt, and Copper were identified as the most
    influential predictors of water quality deterioration in the uMhlathuze catchment.</span><br><br>

    <strong style="font-size:1.4rem; color:#062c43;">Significance</strong><br>
    <span style="font-size:1.1rem;">This tool provides a proof-of-concept for rapid, low-cost water quality screening that can
    support the Department of Water and Sanitation in identifying unsafe water conditions
    between formal laboratory testing intervals.</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-bottom-row"></div>', unsafe_allow_html=True)
    col_back, col_spacer, col_next = st.columns([1, 4, 1])
    with col_back:
        if st.button("Back", key="back_from_research", use_container_width=True):
            go_back()
    with col_next:
        if st.button("Next", key="next_from_research", use_container_width=True):
            go_to("How It Works")