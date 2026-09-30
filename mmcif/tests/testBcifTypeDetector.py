##
# File: testBcifTypeDetector.py
#
# Characterization tests for schema-less BinaryCIF column classification.
##

import unittest

from mmcif.io.bcif_type_detector import classify_column
from mmcif.io.config import TypeDetectionConfig


class BcifTypeDetectorTests(unittest.TestCase):
    def assertColumnType(self, expected, values, config=None):
        profile = classify_column(values, type_detection_config=config)
        self.assertEqual(profile.col_type, expected)

    def testNumericAndStringCharacterization(self):
        cases = [
            ("int", ["1", "2", "3"]),
            ("int", [1, 2, 3]),
            ("float", ["1.25", "2.50", "3.75"]),
            ("float", [1.25, 2.5, 3.75]),
            ("int", ["-3", "-2", "-1"]),
            ("float", ["-3.5", "-2.5", "-1.5"]),
            ("str", ["0004"]),
            ("str", ["1e-3", "2e-3", "3e-3"]),
            ("str", [True, False]),
            ("int", [".", "?", None]),
            ("int", [".", "1", "?", "2"]),
            ("float", [".", "1.5", "?", "2.5", "3.5"]),
            ("str", [".", "alpha", "?", "beta"]),
            ("int", []),
            ("int", [" 1 ", " 2 ", " 3 "]),
            ("float", [" 1.5 ", " 2.5 ", " 3.5 "]),
            # A lone "0" is still an integer; only multi-digit values with a leading zero are strings
            ("int", ["0", "1", "2", "3"]),
            ("float", [0.5, 1.0, 2.5, 3.5]),
            ("float", ["0.5", "1.0", "2.5", "3.5"]),
            ("float", ["0.0", "1.0", "2.5", "3.5"]),
            ("float", [0.0]),
        ]
        for expected, values in cases:
            with self.subTest(values=values):
                self.assertColumnType(expected, values)

    def testMixedTypesClassifyAsString(self):
        """A column mixing value types is classified as "str".

        Mixed int and float values are not promoted to float; any combination
        of int, float and non-numeric values falls back to "str".
        """
        cases = [
            [0.5, 1, 2.5, 3.5],  # mix of native float and int
            ["1", "2.5", "3"],  # mix of int and float strings
            ["A", "B", "1.0"],  # mix of non-numeric and float strings
            ["1", "2", "B"],  # mix of int and non-numeric strings
        ]
        for values in cases:
            with self.subTest(values=values):
                self.assertColumnType("str", values)

    def testSmallFloatOverrideDisabled(self):
        config = TypeDetectionConfig(
            force_small_float_as_string=False,
            min_rows_to_classify_as_float=3,
        )
        for values in (["1.5"], ["1.5", "2.5"], ["1.5", "2.5", "3.5"]):
            with self.subTest(values=values):
                self.assertColumnType("float", values, config)

    def testSmallFloatOverrideEnabled(self):
        config = TypeDetectionConfig(
            force_small_float_as_string=True,
            min_rows_to_classify_as_float=3,
        )
        self.assertColumnType("str", ["1.5"], config)
        self.assertColumnType("str", ["1.5", "2.5"], config)
        self.assertColumnType("float", ["1.5", "2.5", "3.5"], config)

    def testSentinelsDoNotCountTowardSmallFloatThreshold(self):
        config = TypeDetectionConfig(
            force_small_float_as_string=True,
            min_rows_to_classify_as_float=3,
        )
        self.assertColumnType("str", [".", "1.5", "?", "2.5", None], config)
        self.assertColumnType("float", [".", "1.5", "?", "2.5", "3.5"], config)

    def testConfiguredThresholdOnlyAffectsEnabledOverride(self):
        enabled = TypeDetectionConfig(
            force_small_float_as_string=True,
            min_rows_to_classify_as_float=2,
        )
        disabled = TypeDetectionConfig(
            force_small_float_as_string=False,
            min_rows_to_classify_as_float=99,
        )
        self.assertColumnType("str", ["1.5"], enabled)
        self.assertColumnType("float", ["1.5", "2.5"], enabled)
        self.assertColumnType("float", ["1.5"], disabled)


if __name__ == "__main__":
    unittest.main()
