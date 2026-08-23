import streamlit as st
import pandas as pd
from config import FEATURE_NAMES, FEATURE_LABELS, FEATURE_UNITS, CLASS_INFO, explain_result, build_explainable_verdict
from utils.model_utils import make_prediction
from utils.nav import go_back, go_to
from styles import get_page_background_css


def _labelled_input(feature_key, current_value, max_value=None):
    unit = FEATURE_UNITS[feature_key]
    label_text = f"{FEATURE_LABELS[feature_key]}" + (f" ({unit})" if unit else "")
    kwargs = {"min_value": 0.0, "format": "%g", "value": current_value, "key": f"input_{feature_key}"}
    if max_value is not None:
        kwargs["max_value"] = max_value
    return st.number_input(label_text, **kwargs)


def _read_uploaded_file(uploaded_file):
    file_name = uploaded_file.name.lower()
    if file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif file_name.endswith((".xlsx", ".xls")):
        excel_file = pd.ExcelFile(uploaded_file)
        if "MHLATHUZE" in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name="MHLATHUZE")
        else:
            df = pd.read_excel(excel_file, sheet_name=excel_file.sheet_names[0])
    else:
        raise ValueError("Unsupported file type. Please upload a CSV or Excel file.")
    df.columns = df.columns.str.strip()
    return df


def _render_community_report(is_safe, headline, explanation_text, parameter_checks=None):
    dot = "🟢" if is_safe else "🔴"
    accent = "#27ae60" if is_safe else "#c0392b"

    evidence_block = ""
    if parameter_checks:
        rows = ""
        for name, status, detail in parameter_checks:
            row_color = "#c0392b" if status == "OUT OF RANGE" else "#27ae60"
            icon = "✗" if status == "OUT OF RANGE" else "✓"
            rows += f'<div style="color:{row_color}; font-weight:700; margin-bottom:8px; font-size:1.05rem;">{icon} {name}: <span style="color:#0a192f; font-weight:600;">{detail}</span></div>'
        evidence_block = (
            f'<div style="font-size:1.1rem; font-weight:900; color:#0a192f; margin:20px 0 10px 0;">Parameter Health Breakdown</div>'
            f'<div style="background:#f8f9fa; padding:20px; border-radius:12px; border:1px solid #d5dbdb;">{rows}</div>'
        )

    st.markdown(
        f'<div style="background-color:#ffffff; border-radius:16px; border:3px solid {accent}; '
        f'box-shadow:0 12px 35px rgba(0,0,0,0.25); padding:36px; margin:20px 0;">'
        f'<div style="display:flex; align-items:center; gap:18px; border-bottom:3px solid {accent}; '
        f'padding-bottom:18px; margin-bottom:22px;">'
        f'<span style="font-size:3rem;">{dot}</span>'
        f'<div style="font-size:1.55rem; font-weight:900; color:#0a192f; text-transform:uppercase;">{headline}</div>'
        f'</div>'
        f'<div style="font-size:1.12rem; line-height:1.75; color:#0a192f; font-weight:600;">{explanation_text}</div>'
        f'{evidence_block}'
        f'</div>',
        unsafe_allow_html=True
    )


def _process_batch_file(models, uploaded_file, model_key):
    try:
        df = _read_uploaded_file(uploaded_file)
    except Exception as e:
        st.error(f"Could not read uploaded file: {e}")
        return

    missing_columns = [col for col in FEATURE_NAMES if col not in df.columns]
    if missing_columns:
        st.error(f"Missing required columns in uploaded file: {', '.join(missing_columns)}")
        return

    input_array = df[FEATURE_NAMES].astype(float).values
    scaled_array = models['scaler'].transform(input_array)
    selected_model = models[model_key]

    predictions = selected_model.predict(scaled_array)
    probabilities = selected_model.predict_proba(scaled_array)

    class_label_map = {
        0: 'Excellent Water Quality (Safe)',
        1: 'Good Water Quality (Acceptable)',
        2: 'Poor Water Quality (Treatment Needed)',
        3: 'Very Poor / Contaminated'
    }

    predicted_labels, confidences, safety_verdicts = [], [], []

    for i in range(len(df)):
        row_values = {name: float(df.iloc[i][name]) for name in FEATURE_NAMES}
        pred = int(predictions[i])
        conf = float(probabilities[i][pred]) * 100
        class_label = class_label_map.get(pred, 'Unknown')
        parameter_checks = explain_result(row_values, pred)
        verdict = build_explainable_verdict(pred, class_label, conf, parameter_checks)
        predicted_labels.append(class_label)
        confidences.append(round(conf, 1))
        safety_verdicts.append(verdict['overall_verdict'])

    results_df = df.copy()
    results_df['Predicted Class'] = predicted_labels
    results_df['Confidence (%)'] = confidences
    results_df['Safety Verdict'] = safety_verdicts

    total = len(predicted_labels)
    safe_count = safety_verdicts.count('SAFE TO DRINK')
    safe_percentage = (safe_count / total) * 100 if total > 0 else 0
    is_overall_safe = safe_percentage >= 50

    excellent_count = sum(1 for l in predicted_labels if 'Excellent' in l)
    good_count = sum(1 for l in predicted_labels if 'Good' in l)
    poor_count = sum(1 for l in predicted_labels if 'Poor' in l and 'Very' not in l)
    very_poor_count = sum(1 for l in predicted_labels if 'Very Poor' in l)

    if is_overall_safe:
        headline = "WATER QUALITY IS SAFE FOR CONSUMPTION"
        explanation = (
            f"Out of {total} samples tested from this catchment, {safe_percentage:.1f}% "
            f"({safe_count} of {total}) met safe drinking water standards. This indicates the water "
            f"source is generally suitable for community use, though individual samples flagged as "
            f"poor or very poor below should still be treated with caution."
        )
    else:
        headline = "WATER QUALITY REQUIRES TREATMENT BEFORE USE"
        explanation = (
            f"Out of {total} samples tested from this catchment, {100 - safe_percentage:.1f}% "
            f"({total - safe_count} of {total}) showed contamination or parameters outside safe limits. "
            f"Communities relying on this water source should treat or boil water before drinking, and "
            f"prioritise the samples flagged below for further laboratory testing."
        )

    _render_community_report(is_overall_safe, headline, explanation)

    st.markdown(
        '<div style="background-color:#ffffff; color:#0a192f; padding:16px 22px; border-radius:10px; '
        'font-size:1.3rem; font-weight:900; margin:18px 0 16px 0; border-left:6px solid #1b4f72;">'
        'Batch Classification Summary</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    metrics_data = [
        ("Total Samples", total, "#0a192f"),
        ("Excellent", excellent_count, "#27ae60"),
        ("Good", good_count, "#2980b9"),
        ("Poor", poor_count, "#e67e22"),
        ("Very Poor", very_poor_count, "#c0392b")
    ]
    for col, (label, val, col_hex) in zip([col1, col2, col3, col4, col5], metrics_data):
        with col:
            st.markdown(
                f'<div style="background:#ffffff; padding:18px; border-radius:10px; text-align:center; '
                f'border:2px solid #1b4f72;">'
                f'<div style="font-size:0.85rem; font-weight:800; color:#34495e; text-transform:uppercase;">{label}</div>'
                f'<div style="font-size:2rem; font-weight:900; color:{col_hex}; margin-top:4px;">{val}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown(
        '<div style="color:#0a192f; font-size:1.25rem; font-weight:900; margin:28px 0 12px 0;">Detailed Results Table</div>',
        unsafe_allow_html=True
    )
    st.dataframe(results_df, use_container_width=True, height=350)
    st.download_button(
        "Download Full Results as CSV",
        data=results_df.to_csv(index=False).encode("utf-8"),
        file_name="water_quality_batch_results.csv",
        mime="text/csv",
        key="download_batch"
    )

    st.markdown(
        '<div style="color:#0a192f; font-size:1.25rem; font-weight:900; margin:28px 0 12px 0;">Inspect an Individual Sample</div>',
        unsafe_allow_html=True
    )
    sample_choice = st.selectbox(
        "Select a sample to view its detailed breakdown",
        options=list(range(len(df))),
        format_func=lambda i: f"Sample {i+1} — {predicted_labels[i]} ({confidences[i]}% confidence)",
        key="batch_inspector"
    )
    row_vals = {name: float(df.iloc[sample_choice][name]) for name in FEATURE_NAMES}
    pred_val = int(predictions[sample_choice])
    conf_val = float(probabilities[sample_choice][pred_val]) * 100
    lbl_val = class_label_map.get(pred_val, 'Unknown')
    checks_val = explain_result(row_vals, pred_val)
    sample_is_safe = "SAFE" in safety_verdicts[sample_choice].upper()

    if sample_is_safe:
        sample_headline = "EXCELLENT WATER QUALITY — SAFE FOR CONSUMPTION"
        failed = []
    else:
        sample_headline = "POOR WATER QUALITY — TREATMENT RECOMMENDED"
        failed = [c[0] for c in checks_val if c[1] == "OUT OF RANGE"]

    if sample_is_safe:
        sample_explanation = (
            f"This sample is classified as <strong>{lbl_val}</strong> with {conf_val:.1f}% confidence. "
            f"All measured parameters fall within safe limits, meaning this water can be used for daily "
            f"domestic and drinking purposes without concern."
        )
    else:
        names = ", ".join(failed) if failed else "certain parameters"
        sample_explanation = (
            f"This sample is classified as <strong>{lbl_val}</strong> with {conf_val:.1f}% confidence. "
            f"The water is flagged as unsafe because <strong>{names}</strong> exceeded safe limits. "
            f"Drinking this water without treatment may pose health risks, so it should be boiled or "
            f"treated before use."
        )

    _render_community_report(sample_is_safe, sample_headline, sample_explanation, checks_val)


def _display_results(models, input_values, selected_model_key):
    prediction, probabilities = make_prediction(models, input_values, selected_model_key)
    confidence = probabilities[prediction] * 100
    class_label_map = {
        0: 'Excellent Water Quality (Safe for Consumption)',
        1: 'Good Water Quality (Acceptable Standards)',
        2: 'Poor Water Quality (Treatment Recommended)',
        3: 'Very Poor / Contaminated (Unsafe)'
    }
    class_label = class_label_map.get(prediction, 'Unknown')
    parameter_checks = explain_result(input_values, prediction)
    is_safe = prediction in (0, 1)

    if is_safe:
        headline = "EXCELLENT WATER QUALITY — SAFE FOR CONSUMPTION"
        explanation = (
            f"This sample is classified as <strong>{class_label}</strong> with {confidence:.1f}% confidence. "
            f"All measured parameters fall within safe limits recognised for drinking water. There is no "
            f"chemical or contamination concern detected, and this water can be used for daily domestic "
            f"and drinking purposes."
        )
    else:
        failed = [c[0] for c in parameter_checks if c[1] == "OUT OF RANGE"]
        names = ", ".join(failed) if failed else "one or more parameters"
        headline = "POOR WATER QUALITY — TREATMENT RECOMMENDED BEFORE USE"
        explanation = (
            f"This sample is classified as <strong>{class_label}</strong> with {confidence:.1f}% confidence. "
            f"The water is flagged as unsafe because <strong>{names}</strong> exceeded the safe range for "
            f"human consumption. Drinking this water without treatment can cause health problems, so it "
            f"is recommended that this water be boiled or treated before use, and that it undergoes "
            f"further laboratory testing."
        )

    _render_community_report(is_safe, headline, explanation, parameter_checks)

    class_labels = ['Excellent', 'Good', 'Poor', 'Very Poor']
    bars = ""
    for i, prob in enumerate(probabilities):
        bars += (
            f'<div style="margin-bottom:10px;">'
            f'<div style="display:flex; justify-content:space-between; font-size:0.95rem; font-weight:700; color:#0a192f; margin-bottom:4px;">'
            f'<span>{class_labels[i]}</span><span>{prob*100:.1f}%</span></div>'
            f'<div style="background:#eaeded; border-radius:6px; height:10px; overflow:hidden;">'
            f'<div style="background:#1b4f72; height:100%; width:{prob*100:.1f}%;"></div></div></div>'
        )
    st.markdown(
        f'<div style="background:#ffffff; border-radius:14px; border:1px solid #d5dbdb; '
        f'box-shadow:0 4px 18px rgba(0,0,0,0.08); padding:26px 30px; margin-top:20px;">'
        f'<div style="font-size:1.15rem; font-weight:900; color:#0a192f; margin-bottom:16px;">'
        f'Model Confidence Across All Classes</div>{bars}</div>',
        unsafe_allow_html=True
    )


def render(models):
    st.markdown(get_page_background_css("field_sampling.jpg"), unsafe_allow_html=True)

    # Force parameter labels/text above inputs to be bright white and larger
    st.markdown("""
        <style>
        .stNumberInput label p, .stSelectbox label p, .stFileUploader label p, div[data-baseweb="select"] span {
            color: #ffffff !important;
            font-weight: 800 !important;
            font-size: 1.15rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    input_container = st.empty()

    with input_container.container():
        st.markdown('<div style="text-align:center; color:#ffffff; font-size: 2.2rem; font-weight: 900; margin-top: 10px; margin-bottom: 5px; text-shadow: 0 2px 6px rgba(0,0,0,0.8);">Water Quality Assessment System</div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="text-align:center; color:#f1f2f6; font-size: 1.05rem; font-weight: 600; margin-bottom: 20px; max-width: 900px; margin-left: auto; margin-right: auto; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">'
            'Input physicochemical readings below for instant machine learning classification, or upload a batch dataset for comprehensive catchment analysis.</div>',
            unsafe_allow_html=True
        )

        if "assessment_tab" not in st.session_state:
            st.session_state.assessment_tab = "General Chemistry"

        tab_col1, tab_col2, tab_col3, tab_col4 = st.columns(4)
        with tab_col1:
            if st.button("General Chemistry", key="tab_btn_general", use_container_width=True):
                st.session_state.assessment_tab = "General Chemistry"
        with tab_col2:
            if st.button("Metals", key="tab_btn_metals", use_container_width=True):
                st.session_state.assessment_tab = "Metals"
        with tab_col3:
            if st.button("Model Selection", key="tab_btn_model", use_container_width=True):
                st.session_state.assessment_tab = "Model"
        with tab_col4:
            if st.button("Batch CSV Upload", key="tab_btn_batch", use_container_width=True):
                st.session_state.assessment_tab = "Batch CSV Upload"

        active_tab = st.session_state.assessment_tab
        button_states = {"General Chemistry": "tab_btn_general", "Metals": "tab_btn_metals", "Model": "tab_btn_model", "Batch CSV Upload": "tab_btn_batch"}

        st.markdown(f"""
            <style>
            .st-key-{button_states[active_tab]} button {{
                background-color: #1b4f72 !important;
                color: #ffffff !important;
                border: 2px solid #5499c7 !important;
                font-weight: 900 !important;
            }}
            </style>
        """, unsafe_allow_html=True)

        model_key_map = {
            "XGBoost - 96% Accuracy (Recommended)": "xgboost",
            "Random Forest - 92% Accuracy": "random_forest",
            "Decision Tree - 82% Accuracy": "decision_tree"
        }
        model_options = list(model_key_map.keys())

        if "input_values_store" not in st.session_state:
            st.session_state.input_values_store = {name: None for name in FEATURE_NAMES}
        if "single_model_select" not in st.session_state:
            st.session_state.single_model_select = model_options[0]
        if "batch_model_select" not in st.session_state:
            st.session_state.batch_model_select = model_options[0]
        if "batch_uploaded_file" not in st.session_state:
            st.session_state.batch_uploaded_file = None

        st.markdown("<br>", unsafe_allow_html=True)

        if active_tab == "General Chemistry":
            r1 = st.columns(3)
            with r1[0]: st.session_state.input_values_store['EC'] = _labelled_input('EC', st.session_state.input_values_store['EC'])
            with r1[1]: st.session_state.input_values_store['TDS'] = _labelled_input('TDS', st.session_state.input_values_store['TDS'])
            with r1[2]: st.session_state.input_values_store['pH'] = _labelled_input('pH', st.session_state.input_values_store['pH'], max_value=14.0)

            r2 = st.columns(3)
            with r2[0]: st.session_state.input_values_store['HCO3'] = _labelled_input('HCO3', st.session_state.input_values_store['HCO3'])
            with r2[1]: st.session_state.input_values_store['Cl'] = _labelled_input('Cl', st.session_state.input_values_store['Cl'])
            with r2[2]: st.session_state.input_values_store['SO4'] = _labelled_input('SO4', st.session_state.input_values_store['SO4'])

            r3 = st.columns(3)
            with r3[0]: st.session_state.input_values_store['Ca'] = _labelled_input('Ca', st.session_state.input_values_store['Ca'])
            with r3[1]: st.session_state.input_values_store['K'] = _labelled_input('K', st.session_state.input_values_store['K'])
            with r3[2]: st.session_state.input_values_store['Mg'] = _labelled_input('Mg', st.session_state.input_values_store['Mg'])

        elif active_tab == "Metals":
            r1 = st.columns(3)
            with r1[0]: st.session_state.input_values_store['Na'] = _labelled_input('Na', st.session_state.input_values_store['Na'])
            with r1[1]: st.session_state.input_values_store['NO3'] = _labelled_input('NO3', st.session_state.input_values_store['NO3'])
            with r1[2]: st.session_state.input_values_store['Al'] = _labelled_input('Al', st.session_state.input_values_store['Al'])

            r2 = st.columns(3)
            with r2[0]: st.session_state.input_values_store['Co'] = _labelled_input('Co', st.session_state.input_values_store['Co'])
            with r2[1]: st.session_state.input_values_store['Cu'] = _labelled_input('Cu', st.session_state.input_values_store['Cu'])
            with r2[2]: st.session_state.input_values_store['Fe'] = _labelled_input('Fe', st.session_state.input_values_store['Fe'])

            r3 = st.columns(3)
            with r3[0]: st.session_state.input_values_store['Mn'] = _labelled_input('Mn', st.session_state.input_values_store['Mn'])
            with r3[1]: st.session_state.input_values_store['Ni'] = _labelled_input('Ni', st.session_state.input_values_store['Ni'])
            with r3[2]: st.session_state.input_values_store['Zn'] = _labelled_input('Zn', st.session_state.input_values_store['Zn'])

        elif active_tab == "Model":
            st.session_state.single_model_select = st.selectbox("Select classifier model", model_options, key="single_model_select_box", index=model_options.index(st.session_state.single_model_select))

        elif active_tab == "Batch CSV Upload":
            st.markdown(f'<div style="color:#ffffff; font-weight: 700; font-size: 1.05rem; margin-bottom: 8px;">Upload a CSV or Excel file containing the 18 required parameters: <b>{", ".join(FEATURE_NAMES)}</b></div>', unsafe_allow_html=True)
            st.session_state.batch_model_select = st.selectbox("Select model for batch classification", model_options, key="batch_model_select_box", index=model_options.index(st.session_state.batch_model_select))
            uploaded_file = st.file_uploader("Upload dataset file", type=["csv", "xlsx", "xls"], key="batch_csv_uploader")
            if uploaded_file is not None:
                st.session_state.batch_uploaded_file = uploaded_file
                st.success(f"File '{uploaded_file.name}' loaded successfully.")

        st.markdown("<br>", unsafe_allow_html=True)
        c_btn1, c_btn2, c_btn3 = st.columns([1, 2, 1])
        with c_btn2:
            classify_clicked = st.button("Classify Water Quality", key="classify_btn", use_container_width=True)

    if classify_clicked:
        if active_tab == "Batch CSV Upload":
            if st.session_state.batch_uploaded_file is None:
                st.warning("Please upload a file first.")
            else:
                input_container.empty()
                _process_batch_file(models, st.session_state.batch_uploaded_file, model_key_map[st.session_state.batch_model_select])
        else:
            filled_values = {k: (v if v is not None else 0.0) for k, v in st.session_state.input_values_store.items()}
            if all(v == 0.0 for v in filled_values.values()):
                st.warning("Please provide input parameter readings before classifying.")
            else:
                input_container.empty()
                _display_results(models, filled_values, model_key_map[st.session_state.single_model_select])

    # Dropped down vertical spacing before bottom navigation buttons
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col_back, col_next = st.columns([5, 1])
    with col_back:
        if st.button("← Back", key="back_from_assessment"):
            go_back()
    with col_next:
        if st.button("Next Page →", key="next_from_assessment"):
            go_to("Model Performance")