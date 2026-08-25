##
# File: testBinaryCifWriterSynthetic.py
#
# Small writer-level tests for centralized BinaryCIF type policy.
##

import os
import tempfile
import unittest

import msgpack

from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import DataContainer
from mmcif.io.BinaryCifReader import BinaryCifReader
from mmcif.io.BinaryCifWriter import BinaryCifWriter


class BinaryCifWriterSyntheticTests(unittest.TestCase):
    def _serialize_column(self, category_name, attribute_name, values):
        category = DataCategory(category_name)
        category.appendAttribute(attribute_name)
        for value in values:
            category.append([value])

        container = DataContainer("task1")
        container.append(category)

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = os.path.join(tmp_dir, "column.bcif")
            writer = BinaryCifWriter(dictionaryApi=None, useAutoDetect=True)
            self.assertTrue(writer.serialize(file_path, [container]))
            with open(file_path, "rb") as input_file:
                packed = msgpack.unpack(input_file, raw=False)
            decoded = BinaryCifReader(storeStringsAsBytes=False).deserialize(file_path)

        column = packed["dataBlocks"][0]["categories"][0]["columns"][0]
        decoded_category = decoded[0].getObj(category_name)
        attribute_index = decoded_category.getAttributeIndex(attribute_name)
        decoded_values = decoded_category.getColumn(attribute_index)
        return column, decoded_values

    def _encoding_kinds(self, column):
        return [encoding["kind"] for encoding in column["data"]["encoding"]]

    def assertFloatPath(self, category_name, attribute_name, values):
        column, decoded_values = self._serialize_column(category_name, attribute_name, values)
        self.assertIn("FixedPoint", self._encoding_kinds(column))
        self.assertEqual([float(value) for value in values], decoded_values)

    def testOneRowFloatConfiguredItemsReachFloatPath(self):
        cases = [
            ("atom_site_anisotrop", "U[1][1]", ["0.1234"]),
            ("ihm_sphere_obj_site", "object_radius", ["4.125"]),
            ("ihm_sphere_obj_site", "rmsf", ["0.25"]),
            ("ihm_starting_model_coord", "B_iso_or_equiv", ["12.5"]),
        ]
        for category_name, attribute_name, values in cases:
            with self.subTest(item="_%s.%s" % (category_name, attribute_name)):
                self.assertFloatPath(category_name, attribute_name, values)

    def testForcedStringAndIntegerItemsKeepTheirTypes(self):
        string_column, string_values = self._serialize_column(
            "audit_conform", "dict_version", ["5.281"]
        )
        integer_column, integer_values = self._serialize_column(
            "atom_site", "id", ["7"]
        )
        self.assertEqual(self._encoding_kinds(string_column), ["StringArray"])
        self.assertEqual(string_values, ["5.281"])
        self.assertNotIn("StringArray", self._encoding_kinds(integer_column))
        self.assertEqual(integer_values, [7])

    def testGeneralSmallDecimalColumnsReachFloatPath(self):
        self.assertFloatPath("task1_test", "one_row", ["1.25"])
        self.assertFloatPath("task1_test", "two_rows", ["1.25", "2.5"])

    def testSentinelsPreserveMaskAndRoundTrip(self):
        column, decoded_values = self._serialize_column(
            "task1_test", "masked_float", ["1.5", ".", "?", "2.5", "3.5"]
        )
        self.assertIsNotNone(column["mask"])
        self.assertEqual(decoded_values, [1.5, ".", "?", 2.5, 3.5])


if __name__ == "__main__":
    unittest.main()
