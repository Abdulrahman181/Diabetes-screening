import unittest

from diabetes_inputs import FEATURES, make_input_frame


class MakeInputFrameTests(unittest.TestCase):
    def test_preserves_model_feature_order_and_converts_to_numeric(self):
        frame = make_input_frame({feature: str(index + 0.5) for index, feature in enumerate(FEATURES)})

        self.assertEqual(tuple(frame.columns), FEATURES)
        self.assertEqual(frame.shape, (1, len(FEATURES)))
        self.assertEqual(frame.iloc[0, 0], 0.5)
        self.assertEqual(frame.iloc[0, -1], 7.5)

    def test_rejects_missing_or_non_numeric_values(self):
        values = {feature: "1" for feature in FEATURES}
        values["Glucose"] = ""

        with self.assertRaisesRegex(ValueError, "Glucose"):
            make_input_frame(values)

    def test_rejects_non_finite_values(self):
        for value in ("nan", "inf", "-inf"):
            with self.subTest(value=value):
                values = {feature: "1" for feature in FEATURES}
                values["BMI"] = value
                with self.assertRaisesRegex(ValueError, "BMI"):
                    make_input_frame(values)


if __name__ == "__main__":
    unittest.main()
