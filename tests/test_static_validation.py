"""Dependency-light checks for the repository's portable entry points."""

from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_python_sources_parse() -> None:
    for path in ROOT.rglob("*.py"):
        if ".git" not in path.parts:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_streamlit_entrypoint_has_no_machine_specific_path() -> None:
    source = (ROOT / "diabetes.py").read_text(encoding="utf-8")
    assert "C:\\\\Users" not in source
    assert "DIABETES_MODEL_PATH" in source
    assert "FEATURES" in source


def test_notebook_is_valid_json_and_has_no_stale_outputs() -> None:
    notebook = json.loads((ROOT / "diabetes.ipynb").read_text(encoding="utf-8"))
    assert notebook["nbformat"] >= 4
    code_cells = [cell for cell in notebook["cells"] if cell.get("cell_type") == "code"]
    assert code_cells
    assert all(not cell.get("outputs") and cell.get("execution_count") is None for cell in code_cells)
