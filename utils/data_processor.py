"""
Data processing utilities for preparing user input for prediction.
"""

import numpy as np


def prepare_input(values):
    """
    Prepare user input data for machine learning prediction.
    
    Parameters:
    values (dict): Dictionary containing parameter name-value pairs
    
    Returns:
    numpy.ndarray: 2D array ready for prediction
    """
    feature_order = [
        'EC', 'TDS', 'pH', 'HCO3', 'Cl', 'SO4', 'Ca', 'K', 
        'Mg', 'Na', 'NO3', 'Al', 'Co', 'Cu', 'Fe', 'Mn', 'Ni', 'Zn'
    ]
    
    input_array = np.zeros(len(feature_order))
    
    for i, feature in enumerate(feature_order):
        if feature in values:
            input_array[i] = values[feature]
    
    return input_array.reshape(1, -1)


def get_feature_names():
    """
    Get the list of feature names in the correct order.
    
    Returns:
    list: Feature names in order expected by the model
    """
    return [
        'EC', 'TDS', 'pH', 'HCO3', 'Cl', 'SO4', 'Ca', 'K', 
        'Mg', 'Na', 'NO3', 'Al', 'Co', 'Cu', 'Fe', 'Mn', 'Ni', 'Zn'
    ]