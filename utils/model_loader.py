"""
Model loading utilities with caching for performance.
"""

import streamlit as st
import joblib
import os


@st.cache_resource
def load_models():
    """
    Load all trained machine learning models from the models folder.
    Uses Streamlit caching to load only once per session.
    
    Returns:
    dict: Dictionary containing all models
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_path = os.path.join(base_dir, "models")
    
    models = {
        "random_forest": joblib.load(os.path.join(models_path, "random_forest_model.pkl")),
        "decision_tree": joblib.load(os.path.join(models_path, "decision_tree_model.pkl")),
        "xgboost": joblib.load(os.path.join(models_path, "xgboost_model.pkl"))
    }
    
    return models


@st.cache_resource
def load_scaler():
    """
    Load the fitted MinMaxScaler used for preprocessing.
    
    Returns:
    MinMaxScaler: Fitted scaler object
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_path = os.path.join(base_dir, "models")
    return joblib.load(os.path.join(models_path, "scaler.pkl"))