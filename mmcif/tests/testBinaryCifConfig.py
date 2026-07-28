##
# File: testBinaryCifConfig.py
#
# Invariants for centralized BinaryCIF policy and reusable encoding chains.
##

import unittest

from mmcif.io.config import (
    DEFAULT_FIXED_POINT_INTEGER_CHAIN,
    DEFAULT_INTEGER_CHAIN,
    FIXED_POINT_CANDIDATE_INTEGER_CHAINS,
    FLOAT_BYTE_ARRAY_FALLBACK_CHAIN,
    FORCED_FLOAT_ITEMS,
    FORCED_INTEGER_ITEMS,
    FORCED_STRING_ITEMS,
    MASK_ENCODING_CHAIN,
    MISSING_VALUE_TOKENS,
    SUPPORTED_ENCODERS,
    TYPE_DETECTION_CONFIG,
    get_forced_type,
    validate_binary_cif_config,
)


class BinaryCifConfigTests(unittest.TestCase):
    def testItemPoliciesDoNotConflict(self):
        self.assertFalse(FORCED_STRING_ITEMS & FORCED_INTEGER_ITEMS)
        self.assertFalse(FORCED_STRING_ITEMS & set(FORCED_FLOAT_ITEMS))
        self.assertFalse(FORCED_INTEGER_ITEMS & set(FORCED_FLOAT_ITEMS))

    def testEveryFloatConfigForcesFloatType(self):
        for item_name in FORCED_FLOAT_ITEMS:
            with self.subTest(item_name=item_name):
                self.assertEqual(get_forced_type(item_name), "float")

    def testEncoderNamesAndFactorsAreValid(self):
        chains = list(FIXED_POINT_CANDIDATE_INTEGER_CHAINS) + [
            DEFAULT_FIXED_POINT_INTEGER_CHAIN,
            DEFAULT_INTEGER_CHAIN,
            FLOAT_BYTE_ARRAY_FALLBACK_CHAIN,
            MASK_ENCODING_CHAIN,
        ]
        for chain in chains:
            self.assertIsInstance(chain, tuple)
            self.assertTrue(set(chain) <= SUPPORTED_ENCODERS)

        for item_name, item_config in FORCED_FLOAT_ITEMS.items():
            with self.subTest(item_name=item_name):
                self.assertIsInstance(item_config.integer_chain, tuple)
                self.assertTrue(set(item_config.integer_chain) <= SUPPORTED_ENCODERS)
                if item_config.factor is not None:
                    self.assertIsInstance(item_config.factor, int)
                    self.assertGreater(item_config.factor, 0)

    def testReusableConfigurationIsImmutable(self):
        self.assertIsInstance(MISSING_VALUE_TOKENS, frozenset)
        self.assertIsInstance(FORCED_STRING_ITEMS, frozenset)
        self.assertIsInstance(FORCED_INTEGER_ITEMS, frozenset)
        self.assertIsInstance(FIXED_POINT_CANDIDATE_INTEGER_CHAINS, tuple)
        with self.assertRaises(TypeError):
            FORCED_FLOAT_ITEMS["_test.value"] = object()

    def testForcedTypeLookup(self):
        self.assertEqual(get_forced_type("_audit_conform.dict_version"), "string")
        self.assertEqual(get_forced_type("_atom_site.id"), "integer")
        self.assertIsNone(get_forced_type("_task1_test.unconfigured"))

    def testDefaultTypeDetectionPolicy(self):
        self.assertFalse(TYPE_DETECTION_CONFIG.force_small_float_as_string)
        self.assertEqual(TYPE_DETECTION_CONFIG.min_rows_to_classify_as_float, 3)

    def testValidationHelperAcceptsDefaultConfiguration(self):
        self.assertTrue(validate_binary_cif_config())


if __name__ == "__main__":
    unittest.main()
