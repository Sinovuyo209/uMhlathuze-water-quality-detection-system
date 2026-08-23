# uMhlathuze Water Quality Detection System

An advanced machine learning web application developed to classify, evaluate, and monitor water quality metrics and river health within the uMhlathuze catchment in South Africa.

## Overview
This platform is designed to support community health and environmental assessment by providing instant physicochemical analysis. It evaluates key water parameters (such as pH, Electrical Conductivity, Total Dissolved Solids, and heavy metals) using trained machine learning classifiers to determine whether water sources are safe for human consumption and daily domestic use.

## Key Features
* **Instant Single Sample Assessment:** Input general chemistry and metal parameters manually for real-time classification.
* **Batch Catchment CSV Upload:** Upload large environmental datasets to analyze entire catchments simultaneously with summary metrics and downloadable CSV reports.
* **Explainable AI (XAI):** Parameter-by-parameter evidence breakdown that translates complex machine learning outputs into clear, community-friendly safety verdicts.
* **Model Performance Comparison:** Evaluate the accuracy and metrics of underlying machine learning models (XGBoost, Random Forest, Decision Tree).

## Built With
* **Python** & **Streamlit** (Interactive Web Framework)
* **Scikit-Learn**, **XGBoost** (Machine Learning Classifiers)
* **Pandas** & **NumPy** (Data Processing)
