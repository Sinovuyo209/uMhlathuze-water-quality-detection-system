"""Compatibility shim for model utilities.

This file exists so `from utils.model_utils import ...` works when the
actual implementation is defined in the root `model_utils.py` module.
"""

from model_utils import load_models, make_prediction, get_feature_importance

__all__ = ["load_models", "make_prediction", "get_feature_importance"]
