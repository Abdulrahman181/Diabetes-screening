# Diabetes screening demo

A small Streamlit interface for the included, pre-trained `model.pkl` artifact. **This is an educational prototype, not a validated medical device. Do not use its output for diagnosis, treatment, or clinical decisions.** The model's performance has not been validated as part of this repository maintenance, and the training dataset is not included.

## Run the app

The notebook metadata records Python 3.9.13, and static inspection of the model's pickle metadata identifies scikit-learn 1.0.2. Use Python 3.9 with the direct dependency versions in `requirements.txt` for best compatibility with this legacy artifact:

```bash
python3.9 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run diabetes.py
```

The app reads `model.pkl` relative to `diabetes.py`; it no longer relies on a machine-specific Windows path. It accepts numeric feature values, rejects blank/non-numeric/non-finite inputs, and reports only the model's class label. Do not enter identifiable or real patient health information; this demo does not provide a secure clinical workflow.

## Model and reproducibility limitations

- `diabetes.csv` is not present. The notebook's training and analysis cells cannot be reproduced until the appropriate dataset is supplied locally; this repository does not provide or claim permission to redistribute it.
- The checked-in model is a Python pickle. Pickle deserialization can execute code, so load it only from a source you trust. Pickled scikit-learn models are version-sensitive; the dependency pin follows the artifact's recorded scikit-learn version, but runtime loading and predictions were not validated in this environment.
- Notebook outputs have been cleared to avoid presenting stale results as validated metrics. No model-performance claim is made.

## Credentials

Do not commit `kaggle.json`, `.env`, or other credentials. `.gitignore` excludes common local credential files, but ignore rules do not remove secrets already committed or invalidate them. **If a Kaggle API credential was exposed in any prior revision, fork, or other location, revoke/rotate it in Kaggle now; this repository change does not rotate credentials or erase protected branch history.** Keep any replacement credential outside version control.
