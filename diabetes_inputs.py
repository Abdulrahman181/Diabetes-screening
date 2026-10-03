"""Input validation shared by the Streamlit UI and unit tests."""

import math
from collections.abc import Mapping

import pandas as pd

FEATURES = (
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
)


def make_input_frame(raw_values: Mapping[str, object]) -> pd.DataFrame:
    """Return one ordered model input row, or raise ValueError for invalid input."""
    converted: dict[str, float] = {}
    invalid = []
    for feature in FEATURES:
        try:
            value = float(raw_values[feature])
        except (KeyError, TypeError, ValueError):
            invalid.append(feature)
            continue
        if not math.isfinite(value):
            invalid.append(feature)
            continue
        converted[feature] = value

    if invalid:
        raise ValueError("Enter a finite numeric value for: " + ", ".join(invalid))

    return pd.DataFrame(
        [[converted[feature] for feature in FEATURES]],
        columns=FEATURES,
    )


def validate_model_schema(model: object) -> object:
    """Reject an artifact that cannot accept this app's ordered feature schema."""
    feature_count = getattr(model, "n_features_in_", None)
    if feature_count != len(FEATURES):
        raise ValueError("The model feature count does not match the app schema.")

    feature_names = getattr(model, "feature_names_in_", None)
    if feature_names is not None and tuple(feature_names) != FEATURES:
        raise ValueError("The model feature order does not match the app schema.")

    return model
