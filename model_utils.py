"""
Model utility functions.
Handles loading trained models and running predictions, searching
the project root, a models/ subfolder, or a utils/ subfolder so this
works regardless of where the .pkl files were saved.
"""

import os
import joblib
import numpy as np
import streamlit as st
from config import FEATURE_NAMES


def _find_file(filename):
    search_locations = [
        filename,
        os.path.join("models", filename),
        os.path.join("utils", filename),
    ]
    for path in search_locations:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        f"Could not find '{filename}'. Checked: {search_locations}. "
        f"Make sure your .pkl files are saved in the project root."
    )


@st.cache_resource
def load_models():
    xgb_model = joblib.load(_find_file('xgboost_model.pkl'))
    rf_model = joblib.load(_find_file('random_forest_model.pkl'))
    dt_model = joblib.load(_find_file('decision_tree_model.pkl'))
    scaler = joblib.load(_find_file('scaler.pkl'))

    return {
        'xgboost': xgb_model,
        'random_forest': rf_model,
        'decision_tree': dt_model,
        'scaler': scaler
    }


def make_prediction(models, input_values, model_key='xgboost'):
    input_array = np.array([[input_values[f] for f in FEATURE_NAMES]])
    input_scaled = models['scaler'].transform(input_array)

    selected_model = models[model_key]
    prediction = selected_model.predict(input_scaled)[0]
    probabilities = selected_model.predict_proba(input_scaled)[0]

    return prediction, probabilities


def get_feature_importance(models, model_key='random_forest'):
    return models[model_key].feature_importances_