import json
import unittest
from pathlib import Path

from diabetes_inputs import FEATURES, validate_model_schema


ROOT = Path(__file__).resolve().parents[1]


class ModelSchemaTests(unittest.TestCase):
    def test_accepts_matching_feature_count_and_names(self):
        class Model:
            n_features_in_ = len(FEATURES)
            feature_names_in_ = FEATURES

        model = Model()
        self.assertIs(validate_model_schema(model), model)

    def test_rejects_feature_count_mismatch(self):
        class Model:
            n_features_in_ = len(FEATURES) - 1

        with self.assertRaisesRegex(ValueError, "feature count"):
            validate_model_schema(Model())

    def test_rejects_feature_order_mismatch(self):
        class Model:
            n_features_in_ = len(FEATURES)
            feature_names_in_ = tuple(reversed(FEATURES))

        with self.assertRaisesRegex(ValueError, "feature order"):
            validate_model_schema(Model())

    def test_rejects_artifact_without_feature_count(self):
        with self.assertRaisesRegex(ValueError, "feature count"):
            validate_model_schema(object())


class NotebookWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook = json.loads((ROOT / "diabetes.ipynb").read_text(encoding="utf-8"))
        cls.code = "\n".join(
            "".join(cell.get("source", []))
            for cell in cls.notebook.get("cells", [])
            if cell.get("cell_type") == "code"
        )

    def test_code_cells_are_syntactically_valid_and_have_no_saved_outputs(self):
        for index, cell in enumerate(self.notebook.get("cells", [])):
            if cell.get("cell_type") != "code":
                continue
            with self.subTest(cell=index):
                compile("".join(cell.get("source", [])), f"notebook-cell-{index}", "exec")
                self.assertIsNone(cell.get("execution_count"))
                self.assertFalse(cell.get("outputs"))

    def test_sampling_and_model_selection_do_not_use_the_test_set(self):
        self.assertEqual(self.code.count("train_test_split("), 2)
        self.assertIn("stratify=y", self.code)
        self.assertIn("stratify=y_train_val", self.code)
        self.assertIn('("sampler", RandomOverSampler(random_state=0))', self.code)
        self.assertIn("candidate_pipeline.fit(X_train, y_train)", self.code)
        self.assertIn("candidate_pipeline.predict(X_validation)", self.code)
        self.assertIn("final_model.predict(X_test)", self.code)
        self.assertNotIn("fit_resample", self.code)


if __name__ == "__main__":
    unittest.main()
