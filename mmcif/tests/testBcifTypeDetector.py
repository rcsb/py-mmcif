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
            ("str", ["1", "2.5", "3"]),
            ("int", []),
            ("int", [" 1 ", " 2 ", " 3 "]),
            ("float", [" 1.5 ", " 2.5 ", " 3.5 "]),
        ]
        for expected, values in cases:
            with self.subTest(values=values):
                self.assertColumnType(expected, values)

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
