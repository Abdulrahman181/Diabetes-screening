"""Streamlit demo for the repository's pre-trained diabetes model."""

import pickle
from pathlib import Path

import streamlit as st

from diabetes_inputs import FEATURES, make_input_frame, validate_model_schema

MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"


@st.cache_resource
def load_model():
    """Load the trusted repository artifact once per Streamlit process."""
    with MODEL_PATH.open("rb") as model_file:
        model = pickle.load(model_file)
    return validate_model_schema(model)


st.title("Diabetes screening model demo")
st.warning(
    "Educational prototype only. This model is not clinically validated and "
    "must not be used for diagnosis, treatment, or other clinical decisions."
)
st.caption(
    "Do not enter identifiable or real patient health information. "
    "The app does not provide a secure clinical workflow."
)

with st.form("screening_inputs"):
    st.subheader("Enter numeric feature values")
    raw_values = {
        feature: st.text_input(feature, key=f"input_{feature}")
        for feature in FEATURES
    }
    submitted = st.form_submit_button("Get model output")

if submitted:
    try:
        input_frame = make_input_frame(raw_values)
    except ValueError as error:
        st.error(str(error))
    else:
        try:
            model = load_model()
            predictions = model.predict(input_frame)
            if len(predictions) != 1:
                raise ValueError("The model returned an unexpected number of predictions.")
            prediction = predictions[0]
        except Exception:
            # Avoid displaying user inputs, model internals, or local paths.
            st.error(
                "The model could not be loaded or run. Check the documented "
                "Python/dependency versions and trusted model artifact."
            )
        else:
            if prediction == 0:
                st.info("Model output: class 0 (negative in the source target).")
            elif prediction == 1:
                st.warning("Model output: class 1 (positive in the source target).")
            else:
                st.error("The model returned an unexpected class label.")
