"""Model utility functions for water quality detection."""
import joblib
import pandas as pd
import numpy as np
import os

def load_models():
    """Load trained machine learning models."""
    # Add your model loading logic here or paths relative to root
    models = {}
    try:
        models['xgboost'] = joblib.load('xgboost_model.pkl') # Update path if needed
    except Exception:
        pass
    return models

def make_prediction(model, input_data):
    """Make a prediction using the provided model."""
    return model.predict(input_data)

def get_feature_importance(model):
    """Get feature importances."""
    if hasattr(model, 'feature_importances_'):
        return model.feature_importances_
    return None