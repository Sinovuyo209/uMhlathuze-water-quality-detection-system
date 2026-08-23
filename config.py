FEATURE_NAMES = ['EC', 'TDS', 'pH', 'HCO3', 'Cl', 'SO4', 'Ca', 'K', 'Mg',
                 'Na', 'NO3', 'Al', 'Co', 'Cu', 'Fe', 'Mn', 'Ni', 'Zn']

FEATURE_LABELS = {
    'EC': 'Electrical Conductivity',
    'TDS': 'Total Dissolved Solids',
    'pH': 'pH Level',
    'HCO3': 'Bicarbonate',
    'Cl': 'Chloride',
    'SO4': 'Sulphate',
    'Ca': 'Calcium',
    'K': 'Potassium',
    'Mg': 'Magnesium',
    'Na': 'Sodium',
    'NO3': 'Nitrate',
    'Al': 'Aluminium',
    'Co': 'Cobalt',
    'Cu': 'Copper',
    'Fe': 'Iron',
    'Mn': 'Manganese',
    'Ni': 'Nickel',
    'Zn': 'Zinc'
}

FEATURE_UNITS = {
    'EC': 'uS/cm', 'TDS': 'mg/L', 'pH': '', 'HCO3': 'mg/L', 'Cl': 'mg/L',
    'SO4': 'mg/L', 'Ca': 'mg/L', 'K': 'mg/L', 'Mg': 'mg/L', 'Na': 'mg/L',
    'NO3': 'mg/L', 'Al': 'mg/L', 'Co': 'mg/L', 'Cu': 'mg/L', 'Fe': 'mg/L',
    'Mn': 'mg/L', 'Ni': 'mg/L', 'Zn': 'mg/L'
}

DEFAULT_VALUES = {name: 0.0 for name in FEATURE_NAMES}
DEFAULT_VALUES['pH'] = 7.0

SAFE_LIMITS = {
    'EC': 750, 'TDS': 500, 'pH_low': 6.5, 'pH_high': 8.5, 'HCO3': 300,
    'Cl': 250, 'SO4': 250, 'NO3': 45, 'Al': 0.3, 'Co': 0.1,
    'Cu': 1.0, 'Fe': 0.3, 'Mn': 0.4, 'Ni': 0.07, 'Zn': 5.0
}

CLASS_INFO = {
    0: {"label": "EXCELLENT", "css_class": "result-excellent",
        "description": "All measured parameters fall within safe limits for human consumption."},
    1: {"label": "GOOD", "css_class": "result-good",
        "description": "Parameters are within generally acceptable ranges. Routine monitoring is recommended."},
    2: {"label": "POOR", "css_class": "result-poor",
        "description": "One or more parameters exceed safe limits. Treatment is required before use."},
    3: {"label": "VERY POOR", "css_class": "result-critical",
        "description": "Multiple parameters indicate serious contamination. This water poses health risks."}
}

MODEL_PERFORMANCE = {
    'Model': ['Random Forest', 'Decision Tree', 'XGBoost'],
    'Accuracy': [0.92, 0.82, 0.96],
    'F1 Score': [0.92, 0.82, 0.96],
    'Precision': [0.93, 0.85, 0.96],
    'Recall': [0.92, 0.82, 0.96]
}

RESEARCH_INFO = {
    'title': 'Supervised Machine Learning-Based Tool for Detecting Water Quality in South African Rivers',
    'student': 'Sinovuyo Fusa',
    'student_number': '231170637',
    'programme': 'BSc Honours in Computer Science',
    'institution': 'Walter Sisulu University',
    'supervisor': 'Dr Paulina Phoobane'
}


def explain_result(input_values, predicted_class):
    """
    Returns a list of (parameter, status, detail) tuples showing every
    checked parameter's compliance status, used to build an explainable-AI
    style breakdown that is reconciled with the model's actual prediction.
    """
    checks = []

    def check(name, value, low=None, high=None, unit=""):
        if low is not None and value < low:
            checks.append((name, "OUT OF RANGE", f"{value}{unit} is below the safe minimum of {low}{unit}"))
        elif high is not None and value > high:
            checks.append((name, "OUT OF RANGE", f"{value}{unit} exceeds the safe maximum of {high}{unit}"))
        else:
            checks.append((name, "WITHIN RANGE", f"{value}{unit} is within the safe range"))

    check("pH", input_values.get("pH", 7), low=SAFE_LIMITS['pH_low'], high=SAFE_LIMITS['pH_high'])
    check("Electrical Conductivity", input_values.get("EC", 0), high=SAFE_LIMITS['EC'], unit=" uS/cm")
    check("Total Dissolved Solids", input_values.get("TDS", 0), high=SAFE_LIMITS['TDS'], unit=" mg/L")
    check("Aluminium", input_values.get("Al", 0), high=SAFE_LIMITS['Al'], unit=" mg/L")
    check("Cobalt", input_values.get("Co", 0), high=SAFE_LIMITS['Co'], unit=" mg/L")
    check("Copper", input_values.get("Cu", 0), high=SAFE_LIMITS['Cu'], unit=" mg/L")
    check("Iron", input_values.get("Fe", 0), high=SAFE_LIMITS['Fe'], unit=" mg/L")
    check("Manganese", input_values.get("Mn", 0), high=SAFE_LIMITS['Mn'], unit=" mg/L")
    check("Nickel", input_values.get("Ni", 0), high=SAFE_LIMITS['Ni'], unit=" mg/L")
    check("Zinc", input_values.get("Zn", 0), high=SAFE_LIMITS['Zn'], unit=" mg/L")
    check("Nitrate", input_values.get("NO3", 0), high=SAFE_LIMITS['NO3'], unit=" mg/L")

    return checks


def build_explainable_verdict(predicted_class, class_label, confidence, parameter_checks):
    """
    Produces a single, reconciled explainable-AI verdict combining the
    model's prediction with the actual rule-based parameter checks, so
    the displayed conclusion never contradicts the listed evidence.
    """
    failed_checks = [c for c in parameter_checks if c[1] == "OUT OF RANGE"]
    passed_checks = [c for c in parameter_checks if c[1] == "WITHIN RANGE"]

    if failed_checks:
        overall_verdict = "UNSAFE — TREATMENT REQUIRED"
        verdict_class = "result-poor" if len(failed_checks) <= 2 else "result-critical"
        reasoning = (
            f"The classification model assigned this sample to the '{class_label}' category "
            f"with {confidence:.1f}% confidence based on the overall pattern across all 18 "
            f"measured parameters. However, {len(failed_checks)} individual parameter(s) exceed "
            f"regulatory safe limits, which is why this sample is flagged as requiring further "
            f"attention despite the model's category label."
        )
    else:
        overall_verdict = "SAFE TO DRINK"
        verdict_class = "result-excellent" if predicted_class == 0 else "result-good"
        reasoning = (
            f"The classification model assigned this sample to the '{class_label}' category "
            f"with {confidence:.1f}% confidence, and all {len(passed_checks)} individually checked "
            f"parameters fall within safe regulatory limits. This confirms the model's assessment."
        )

    return {
        "overall_verdict": overall_verdict,
        "verdict_class": verdict_class,
        "reasoning": reasoning,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
    }