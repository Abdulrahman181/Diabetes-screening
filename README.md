# Diabetes screening

A small Streamlit inference app for the Pima-style diabetes classifier in
`model.pkl`. The repository contains the application and an exploratory/training
notebook; it does **not** contain the source CSV dataset.

> This model is an educational screening aid, not a medical diagnosis. Do not
> use it for clinical decisions without appropriate validation and oversight.

## Run the app

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run diabetes.py
```

By default the app loads `model.pkl` from the repository directory. To use a
model stored elsewhere, set a portable path explicitly:

```bash
DIABETES_MODEL_PATH=/absolute/path/to/model.pkl streamlit run diabetes.py
```

The model must expose `predict()` and accept these columns in this exact order:

`Pregnancies`, `Glucose`, `BloodPressure`, `SkinThickness`, `Insulin`, `BMI`,
`DiabetesPedigreeFunction`, `Age`.

Pickle files can execute code while being loaded. Load only a trusted artifact.
The checked-in artifact was not retrained during this review because the source
dataset is absent and the sandbox did not have scikit-learn installed.

## Notebook and data

`diabetes.ipynb` is a cleaned, reproducible template. It expects the original
CSV at `data/diabetes.csv` (or a path supplied through `DIABETES_DATA_PATH`) and
requires a target column named `Outcome`. No dataset or new metrics are claimed
in this repository. If the file is missing, the notebook raises a clear error
instead of silently fabricating data.

The notebook splits data before fitting any preprocessing or balancing step,
uses a stratified fixed random seed, and reports accuracy, recall, F1, and ROC
AUC only after a held-out evaluation. Oversampling, if enabled, is performed
inside the training pipeline and never on the test set.

## Static checks

```bash
python -m pytest -q
ruff check diabetes.py tests
python -m json.tool diabetes.ipynb >/dev/null
```

These checks validate syntax and repository structure; they do not constitute a
full model evaluation. A full run additionally requires the CSV dataset and the
Python dependencies above.
