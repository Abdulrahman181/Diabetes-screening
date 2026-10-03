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
- To run the notebook, start Jupyter from the repository root and place an authorized `diabetes.csv` there, or edit the notebook's `DATA_PATH` to the local authorized copy. The notebook checks for the required columns and finite numeric values before analysis.
- The notebook splits data into training, validation, and held-out test sets before fitting a sampler. Random oversampling occurs only inside an imbalanced-learn pipeline fitted on training data; validation is used for candidate selection, and the test set is reserved for a single final evaluation. These code paths have not been run here because the dataset is absent.
- Running the notebook writes a separate `model_trained.pkl` in the current working directory; it does not overwrite the checked-in `model.pkl` used by the app. Review any locally generated artifact and its provenance before replacing the app artifact.
- The checked-in model is a Python pickle. Pickle deserialization can execute code, so load it only from a source you trust. The app checks the artifact's feature count and, when available, exact feature names/order before inference. Pickled scikit-learn models are version-sensitive; the dependency pin follows the artifact's recorded scikit-learn version, but runtime loading and predictions were not validated in this environment.
- Notebook outputs have been cleared to avoid presenting stale results as validated metrics. No model-performance claim is made.

## Automated checks

GitHub Actions installs the pinned dependencies under Python 3.9, runs unit and notebook-structure tests, checks Python syntax, and verifies dependency consistency. These checks do not load or evaluate `model.pkl` and do not constitute clinical or external validation.

## Credentials

Do not commit `kaggle.json`, `.env`, or other credentials. `.gitignore` excludes common local credential files, but ignore rules do not remove secrets already committed or invalidate them. **If a Kaggle API credential was exposed in any prior revision, fork, or other location, revoke/rotate it in Kaggle now; this repository change does not rotate credentials or erase protected branch history.** Keep any replacement credential outside version control.
