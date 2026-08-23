import streamlit as st
import os
from styles import get_page_background_css
from utils.nav import go_back, go_to


def render():
    st.markdown(get_page_background_css("hero_river.jpg"), unsafe_allow_html=True)

    # Page Title & Description with white text styling
    st.markdown('<div class="section-title" style="text-align: center; color: #ffffff; font-size: 2.2rem; font-weight: 700; margin-bottom: 10px;">Model Performance & Evaluation</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle" style="text-align: center; color: #ffffff; font-size: 1.1rem; margin-bottom: 30px;">'
        'Comprehensive evaluation of trained machine learning models for uMhlathuze River water quality classification, '
        'incorporating multi-line trend metrics and feature importance analysis.</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # 1. Multi-Line Performance Comparison
    st.markdown('<div class="section-title" style="color: #ffffff; font-size: 1.5rem; font-weight: bold; margin-bottom: 5px;">Multi-Line Performance Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #ffffff; margin-bottom: 15px;">Comparing accuracy, precision, recall, and F1-score trends across XGBoost, Random Forest, and Decision Tree classifiers.</div>', unsafe_allow_html=True)
    
    if os.path.exists("model_performance_line_graph.png"):
        st.image("model_performance_line_graph.png", use_container_width=True)
    else:
        st.warning("Multi-line performance graph image ('model_performance_line_graph.png') not found in your project folder.")

    st.markdown("---")

    # 2. Feature Importance Analysis
    st.markdown('<div class="section-title" style="color: #ffffff; font-size: 1.5rem; font-weight: bold; margin-bottom: 5px;">Feature Importance Analysis (Aluminium & Cobalt Focus)</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #ffffff; margin-bottom: 15px;">Evaluating the relative contribution of physicochemical parameters, highlighting key indicators such as Aluminium and Cobalt.</div>', unsafe_allow_html=True)
    
    if os.path.exists("all_models_feature_importance.png"):
        st.image("all_models_feature_importance.png", use_container_width=True)
    else:
        st.warning("Feature importance image ('all_models_feature_importance.png') not found in your project folder.")

    st.markdown("---")

    # 3. Confusion Matrices
    st.markdown('<div class="section-title" style="color: #ffffff; font-size: 1.5rem; font-weight: bold; margin-bottom: 5px;">Confusion Matrices</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #ffffff; margin-bottom: 15px;">Visualizing class-wise prediction accuracy across the models.</div>', unsafe_allow_html=True)
    
    if os.path.exists("confusion_matrices.png"):
        st.image("confusion_matrices.png", use_container_width=True)
    else:
        st.warning("Confusion matrices image ('confusion_matrices.png') not found in your project folder.")

    st.markdown("---")

    # 4. Correlation Heatmap
    st.markdown('<div class="section-title" style="color: #ffffff; font-size: 1.5rem; font-weight: bold; margin-bottom: 5px;">Correlation Heatmap</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #ffffff; margin-bottom: 15px;">Examining relationships between physicochemical parameters in the uMhlathuze River dataset.</div>', unsafe_allow_html=True)
    
    if os.path.exists("correlation_heatmap.png"):
        st.image("correlation_heatmap.png", use_container_width=True)
    else:
        st.warning("Correlation heatmap image ('correlation_heatmap.png') not found in your project folder.")

    st.markdown('<div class="nav-bottom-row"></div>', unsafe_allow_html=True)
    col_back, col_spacer, col_next = st.columns([1, 4, 1])
    with col_back:
        if st.button("Back", key="back_from_perf", use_container_width=True):
            go_back()
    with col_next:
        if st.button("Next", key="next_from_perf", use_container_width=True):
            go_to("Home")