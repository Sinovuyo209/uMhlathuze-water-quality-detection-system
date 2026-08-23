import streamlit as st
from utils.nav import go_back, go_to


def render():
    st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">This tool follows a simple three-step process to '
        'turn your water sample readings into a classification result.</div>',
        unsafe_allow_html=True
    )

    step1, step2, step3 = st.columns(3)
    with step1:
        st.markdown(
            '<div class="step-card"><div class="step-number">Step 1</div>'
            '<div class="step-text">Enter the physicochemical measurements from your '
            'water sample using the labelled input fields on the Assessment page.</div></div>',
            unsafe_allow_html=True
        )
    with step2:
        st.markdown(
            '<div class="step-card"><div class="step-number">Step 2</div>'
            '<div class="step-text">Select which trained machine learning model to use '
            'and click Classify Water Quality.</div></div>',
            unsafe_allow_html=True
        )
    with step3:
        st.markdown(
            '<div class="step-card"><div class="step-number">Step 3</div>'
            '<div class="step-text">Review the predicted quality class, confidence '
            'score, and explanation of which parameters exceeded safe limits.</div></div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown('<div class="section-title">Frequently Asked Questions</div>', unsafe_allow_html=True)

    faqs = [
        ("Why does pH start empty like all other fields?",
         "All parameter fields, including pH, start empty so that a classification is only "
         "based on readings you have genuinely entered, avoiding accidental use of a default value."),
        ("How accurate is the classification?",
         "XGBoost achieved 96% accuracy, Random Forest 92%, and Decision Tree 82% on a "
         "held-out test set of 198 real uMhlathuze River samples."),
        ("What do the four water quality classes mean?",
         "Excellent and Good indicate safe parameters. Poor requires treatment. Very Poor "
         "indicates serious contamination and direct health risk."),
        ("Is my data stored or shared?",
         "No. Values entered are used only to generate an immediate prediction and are "
         "not saved or transmitted elsewhere."),
        ("Can this tool replace laboratory water testing?",
         "No. It supports rapid screening between laboratory intervals. Laboratory "
         "confirmation remains essential for Poor or Very Poor results."),
    ]

    for question, answer in faqs:
        st.markdown(f'<div class="faq-question">{question}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="faq-answer">{answer}</div>', unsafe_allow_html=True)

    st.markdown('<div class="nav-bottom-row"></div>', unsafe_allow_html=True)
    col_back, col_spacer, col_next = st.columns([1, 4, 1])
    with col_back:
        if st.button("Back", key="back_from_how_it_works", use_container_width=True):
            go_back()
    with col_next:
        if st.button("Next", key="next_from_how_it_works", use_container_width=True):
            go_to("Home")