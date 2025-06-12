##
# -*- coding: utf-8 -*-
#
# File:    DataCategoryTests.py
# Author:  J. Westbrook
# Date:    06-Aug-2017
# Version: 0.001
#
# Updates:
#
##
"""
Test cases for data category container classes.

"""

import logging
import os
import sys
import time
import unittest
from itertools import chain, islice, repeat

from mmcif.api.DataCategory import DataCategory
from mmcif.api.DataCategoryBase import DataCategoryBase

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

try:
    from mmcif import __version__
except ImportError:
    sys.path.insert(0, TOPDIR)
    from mmcif import __version__


__docformat__ = "google en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def window(seq, size=2, fill=0, fillLeft=False, fillRight=False):
    """Returns a sliding window (of width n) over data from the iterable:
    s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
    """
    ssize = size - 1
    it = chain(repeat(fill, ssize * fillLeft), iter(seq), repeat(fill, ssize * fillRight))
    result = tuple(islice(it, size))
    if len(result) == size:  # `<=` if okay to return seq if len(seq) < size
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


class DataCategoryTests(unittest.TestCase):
    def setUp(self):
        self.__lfh = sys.stdout
        self.__verbose = True
        #
        self.__attributeList = ["colOrd", "colA", "colB", "colC", "colD"]
        self.__rowListAsciiA = []
        self.__testRowAsciiA = ["someData", 100222, 1.00056, "furtherdata"]
        for i in range(1, 10):
            tr = [i] + self.__testRowAsciiA
            self.__rowListAsciiA.append(tr)
        #
        self.__rowListAsciiB = []
        testRowAsciiB = ["someData", 100223, 1.00057, "furtherdata"]
        for i in range(1, 9):
            tr = [i] + self.__testRowAsciiA
            self.__rowListAsciiB.append(tr)
        for i in range(9, 10):
            tr = [i] + testRowAsciiB
            self.__rowListAsciiB.append(tr)
        #
        self.__rowListUnicode = []
        self.__testRowUnicode = [u"someData", 100222, 1.00056, u"abcdĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨxyz"]
        for i in range(1, 10):
            tr = [i] + self.__testRowUnicode
            self.__rowListUnicode.append(tr)
        #
        self.__rowListUnicodeMiss = []
        self.__attributeListMiss = ["colOrd", "colA", "colB", "colNone", "colM1", "colM2", "colC", "colD"]
        self.__testRowUnicodeMiss = [u"someData", 100222, None, "?", ".", u"abcdĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨxyz", 234.2345]
        for i in range(1, 10):
            tr = [i] + self.__testRowUnicodeMiss
            self.__rowListUnicodeMiss.append(tr)
        #
        self.__startTime = time.time()
        logger.debug("Running tests on version %s", __version__)
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testBaseBasicAscii(self):
        """Test case - base class instantiation with ascii data"""
        try:
            dcbA = DataCategoryBase("A", self.__attributeList, self.__rowListAsciiA)
            dcbB = DataCategoryBase("A", self.__attributeList, self.__rowListAsciiA)
            self.assertEqual(dcbA, dcbA)
            self.assertEqual(dcbB, dcbB)
            self.assertEqual(dcbA, dcbB)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testBaseMethodsAscii(self):
        """Test case -  base class methods"""
        try:
            name = "A"
            dcbA = DataCategoryBase(name, self.__attributeList, self.__rowListAsciiA)
            self.assertEqual(name, dcbA.getName())
            self.assertEqual(self.__attributeList, dcbA.getAttributeList())
            self.assertEqual(self.__rowListAsciiA, dcbA.getRowList())
            self.assertEqual(len(self.__rowListAsciiA), dcbA.getRowCount())
            ii = 0
            dcbA.setMapping("DATA")
            for row in dcbA:
                ii += 1
                self.assertEqual(self.__testRowAsciiA, row[1:])
            self.assertEqual(ii, dcbA.getRowCount())
            dcbA.setMapping("ATTRIBUTE")
            ii = 0
            na = len(dcbA.getAttributeList())
            for row in dcbA:
                ii += 1
                # logger.info("ii %d row %r " % (ii, row))
                self.assertEqual(ii, row["colOrd"])
                self.assertEqual(self.__testRowAsciiA[na - 2], row["colD"])
                #
            self.assertEqual(ii, dcbA.getRowCount())
            dcbA.setMapping("ITEM")
            ii = 0
            for row in dcbA:
                ii += 1
                self.assertEqual(ii, row["_" + name + "." + "colOrd"])
            self.assertEqual(ii, dcbA.getRowCount())
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testBaseMethodsUnicode(self):
        """Test case -  base class methods"""
        try:
            name = "A"
            dcbA = DataCategoryBase(name, self.__attributeList, self.__rowListUnicode)
            self.assertEqual(name, dcbA.getName())
            self.assertEqual(self.__attributeList, dcbA.getAttributeList())
            self.assertEqual(self.__rowListUnicode, dcbA.getRowList())
            self.assertEqual(len(self.__rowListUnicode), dcbA.getRowCount())
            ii = 0
            dcbA.setMapping("DATA")
            for row in dcbA:
                ii += 1
                self.assertEqual(self.__testRowUnicode, row[1:])
            self.assertEqual(ii, dcbA.getRowCount())
            dcbA.setMapping("ATTRIBUTE")
            ii = 0
            na = len(dcbA.getAttributeList())
            for row in dcbA:
                ii += 1
                # logger.info("ii %d row %r " % (ii, row))
                self.assertEqual(ii, row["colOrd"])
                self.assertEqual(self.__testRowUnicode[na - 2], row["colD"])
                #
            self.assertEqual(ii, dcbA.getRowCount())
            dcbA.setMapping("ITEM")
            ii = 0
            for row in dcbA:
                ii += 1
                self.assertEqual(ii, row["_" + name + "." + "colOrd"])
                self.assertEqual(self.__testRowUnicode[3], row["_" + name + "." + "colD"])
            self.assertEqual(ii, dcbA.getRowCount())
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testBaseBasicAsciiDiff(self):
        """Test case -  __eq__ and __ne__ methods"""
        try:
            dcbA = DataCategoryBase("A", self.__attributeList, self.__rowListAsciiA)
            dcbB = DataCategoryBase("A", self.__attributeList, self.__rowListAsciiB)
            self.assertEqual(dcbA, dcbA)
            self.assertIs(dcbA, dcbA)
            self.assertEqual(dcbB, dcbB)
            self.assertNotEqual(dcbA, dcbB)
            self.assertIsNot(dcbA, dcbB)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testBaseBasicUnicode(self):
        """Test case - base class instantiation including non-ascii"""
        try:
            dcbA = DataCategoryBase("A", self.__attributeList, self.__rowListUnicode)
            dcbB = DataCategoryBase("A", self.__attributeList, self.__rowListUnicode)
            self.assertEqual(dcbA, dcbA)
            self.assertEqual(dcbB, dcbB)
            self.assertEqual(dcbA, dcbB)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testBasicAscii(self):
        """Test case - subcclass instantiation with ascii data"""
        try:
            dcA = DataCategory("A", self.__attributeList, self.__rowListAsciiA)
            dcB = DataCategory("A", self.__attributeList, self.__rowListAsciiA)
            self.assertEqual(dcA, dcA)
            self.assertEqual(dcB, dcB)
            self.assertEqual(dcA, dcB)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testBasicAsciiDiff(self):
        """Test case -  __eq__ and __ne__ methods"""
        try:
            dcA = DataCategory("A", self.__attributeList, self.__rowListAsciiA)
            dcB = DataCategory("A", self.__attributeList, self.__rowListAsciiB)
            self.assertEqual(dcA, dcA)
            self.assertIs(dcA, dcA)
            self.assertEqual(dcB, dcB)
            self.assertNotEqual(dcA, dcB)
            self.assertIsNot(dcA, dcB)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testBasicUnicode(self):
        """Test case -   __eq__ and __ne__ methods w/ unicode"""
        try:
            dcA = DataCategory("A", self.__attributeList, self.__rowListUnicode)
            dcB = DataCategory("A", self.__attributeList, self.__rowListUnicode)
            self.assertEqual(dcA, dcA)
            self.assertEqual(dcB, dcB)
            self.assertEqual(dcA, dcB)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    #

    def testEditRemoveRow(self):
        """Test case -  remove rows"""
        try:
            dcA = DataCategory("A", self.__attributeList, self.__rowListUnicode, raiseExceptions=True)
            for _ in range(0, dcA.getRowCount()):
                ii = dcA.getRowCount()
                dcA.removeRow(0)
                self.assertEqual(ii - 1, dcA.getRowCount())
            #
            self.assertEqual(0, dcA.getRowCount())

        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testEditRowAccessors(self):
        """Test case -  row accessors"""
        try:
            #
            dcA = DataCategory("A", self.__attributeList, self.__rowListAsciiA)
            self.assertRaises(IndexError, dcA.getRow, dcA.getRowCount() + 1)
            self.assertRaises(IndexError, dcA.getRowAttributeDict, dcA.getRowCount() + 1)
            self.assertRaises(IndexError, dcA.getRowItemDict, dcA.getRowCount() + 1)
            #
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testEditAttributes(self):
        """Test case -  get and extend atttribute names"""
        try:
            #
            dcA = DataCategory("A", self.__attributeList, self.__rowListAsciiA)
            self.assertEqual(0, dcA.getRowIndex())
            self.assertEqual(None, dcA.getCurrentAttribute())
            #
            na = len(dcA.getAttributeList())
            tL = dcA.getAttributeListWithOrder()
            self.assertEqual(len(tL), na)

            na = len(dcA.getAttributeList())
            self.assertEqual(dcA.appendAttribute("ColNew"), na + 1)
            row = dcA.getFullRow(0)
            self.assertEqual(row[na], "?")
            #
            row = dcA.getFullRow(dcA.getRowCount() + 1)
            for cV in row:
                self.assertEqual(cV, "?")
            #
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testEditExtend(self):
        """Test case -  category extension methods"""
        try:
            dcA = DataCategory("A", self.__attributeList, self.__rowListAsciiA)
            na = len(dcA.getAttributeList())
            self.assertEqual(dcA.appendAttributeExtendRows("colNew"), na + 1)
            row = dcA.getRow(dcA.getRowCount() - 1)
            self.assertEqual(row[na], "?")
            #
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testGetValues(self):
        """Test case -  value getters"""
        try:
            dcU = DataCategory("A", self.__attributeList, self.__rowListUnicode)
            aL = dcU.getAttributeList()
            logger.debug("Row length %r", dcU.getRowCount())
            for ii, v in enumerate(self.__testRowUnicode):
                at = aL[ii + 1]
                for j in range(0, dcU.getRowCount()):
                    logger.debug("ii %d j %d at %s val %r ", ii, j, at, v)
                    self.assertEqual(dcU.getValue(at, j), v)
                    self.assertEqual(dcU.getValueOrDefault(at, j, "mydefault"), v)
            #
            # negative indices are interpreted in the python manner
            self.assertEqual(dcU.getValueOrDefault("colOrd", -1, "default"), 9)

            self.assertRaises(IndexError, dcU.getValue, "colOrd", dcU.getRowCount() + 1)
            self.assertRaises(ValueError, dcU.getValue, "badAtt", 0)
            #
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testGetSelectValues(self):
        """Test case -  value selectors"""
        try:
            dcU = DataCategory("A", self.__attributeListMiss, self.__rowListUnicodeMiss)
            #
            self.assertEqual(dcU.getFirstValueOrDefault(["colNone", "colM1", "colM2", "colC"], rowIndex=0, defaultValue="default"), u"abcdĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨxyz")
            self.assertEqual(dcU.getFirstValueOrDefault(["colNone", "colM1", "colM2"], rowIndex=0, defaultValue="default"), "default")
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testSetValues(self):
        """Test case -  value setters"""
        try:
            dcU = DataCategory("A", self.__attributeListMiss, self.__rowListUnicodeMiss)
            for i in range(0, dcU.getRowCount()):
                dcU.setValue("newValue", attributeName="colM1", rowIndex=i)

            self.assertTrue(dcU.setValue("newValue", attributeName="colM1", rowIndex=dcU.getRowCount() + 5))
            self.assertRaises(ValueError, dcU.setValue, "newValue", "colX", 0)

        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testReplaceValues(self):
        """Test case -  replace values"""
        try:
            dcU = DataCategory("A", self.__attributeListMiss, self.__rowListUnicodeMiss)
            at = self.__attributeListMiss[3]
            curV = self.__testRowUnicodeMiss[2]
            self.assertEqual(dcU.replaceValue(curV, "newVal", at), dcU.getRowCount())
            at = self.__attributeListMiss[4]
            curV = self.__testRowUnicodeMiss[3]
            self.assertEqual(dcU.replaceValue(curV, "newVal", at), dcU.getRowCount())
            at = self.__attributeListMiss[5]
            curV = self.__testRowUnicodeMiss[4]
            self.assertEqual(dcU.replaceValue(curV, "newVal", at), dcU.getRowCount())

            at = self.__attributeListMiss[6]
            curV = self.__testRowUnicodeMiss[5]
            self.assertEqual(dcU.replaceValue(curV, "newVal", at), dcU.getRowCount())

            for ii in range(3, 7):
                at = self.__attributeListMiss[ii]
                self.assertEqual(dcU.replaceSubstring("newVal", "nextVal", at), dcU.getRowCount())

        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testCompareAttributes(self):
        """Test case - compare object attributes -"""
        try:
            dcU = DataCategory("A", self.__attributeList, self.__rowListUnicode)
            dcM = DataCategory("A", self.__attributeListMiss, self.__rowListUnicodeMiss)
            na = len(dcU.getAttributeList())
            t1, t2, t3 = dcU.cmpAttributeNames(dcU)
            self.assertEqual(len(t1), 0)
            self.assertEqual(len(t3), 0)
            self.assertEqual(len(t2), na)
            t1, t2, t3 = dcU.cmpAttributeNames(dcM)
            self.assertEqual(len(t1), 0)
            self.assertEqual(len(t3), 3)
            self.assertEqual(len(t2), na)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    #

    def testCompareValues(self):
        """Test case - compare object values -"""
        try:
            dcU = DataCategory("A", self.__attributeList, self.__rowListUnicode)
            dcM = DataCategory("A", self.__attributeListMiss, self.__rowListUnicodeMiss)
            na = dcU.getAttributeList()
            self.assertGreaterEqual(len(na), 1)
            tupL = dcU.cmpAttributeValues(dcU)
            for tup in tupL:
                self.assertEqual(tup[1], True)
            tupL = dcU.cmpAttributeValues(dcM)
            for tup in tupL:
                if tup[0] in ["colC", "colD"]:
                    self.assertEqual(tup[1], False)
                else:
                    self.assertEqual(tup[1], True)
            #
            dcX = DataCategory("A", self.__attributeList, self.__rowListUnicode)
            self.assertTrue(dcX.setValue(u"134ĆćĈĉĊċČčĎďĐđĒēĠġĢģĤĥĦħĨxyz", attributeName="colD", rowIndex=dcX.getRowCount() - 2))
            tupL = dcU.cmpAttributeValues(dcX)
            for tup in tupL:
                if tup[0] in ["colD"]:
                    self.assertEqual(tup[1], False)
                else:
                    self.assertEqual(tup[1], True)

        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    #

    def testCondSelectValues(self):
        """Test case - value selections -"""
        try:
            dcM = DataCategory("A", self.__attributeListMiss, self.__rowListUnicodeMiss)
            # self.__testRowUnicodeMiss = [u'someData', 100222, None, '?', '.', u'abcdĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨxyz', 234.2345]
            # self.__attributeListMiss
            atL = dcM.getAttributeList()
            for ii, at in enumerate(atL[1:]):
                self.assertEqual(len(dcM.selectIndices(self.__testRowUnicodeMiss[ii], at)), dcM.getRowCount())
            #
            logger.debug("Window %r", [tt for tt in window(atL)])
            for atW in window(atL, size=1):
                self.assertEqual(len(dcM.selectValueListWhere(atW, self.__testRowUnicodeMiss[-1], self.__attributeListMiss[-1])), dcM.getRowCount())
            for atW in window(atL, size=2):
                self.assertEqual(len(dcM.selectValueListWhere(atW, self.__testRowUnicodeMiss[-1], self.__attributeListMiss[-1])), dcM.getRowCount())
            for atW in window(atL, size=3):
                self.assertEqual(len(dcM.selectValueListWhere(atW, self.__testRowUnicodeMiss[-1], self.__attributeListMiss[-1])), dcM.getRowCount())
            for atW in window(atL, size=4):
                self.assertEqual(len(dcM.selectValueListWhere(atW, self.__testRowUnicodeMiss[-1], self.__attributeListMiss[-1])), dcM.getRowCount())

        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testCondOpSelectValues(self):
        """Test case - indices and value selections using conditions with operators"""
        try:
            dcM = DataCategory("A", self.__attributeListMiss, self.__rowListUnicodeMiss)
            atL = dcM.getAttributeList()
            cndL1 = [(self.__attributeListMiss[-1], "eq", self.__testRowUnicodeMiss[-1])]
            cndL2 = [(self.__attributeListMiss[-1], "ne", self.__testRowUnicodeMiss[-1])]
            cndL3 = [(self.__attributeListMiss[-1], "in", self.__testRowUnicodeMiss)]
            cndL4 = [(self.__attributeListMiss[-1], "not in", self.__testRowUnicodeMiss)]
            #
            self.assertEqual(len(dcM.selectIndicesWhereOpConditions(cndL1)), dcM.getRowCount())
            self.assertEqual(len(dcM.selectIndicesWhereOpConditions(cndL2)), 0)
            self.assertEqual(len(dcM.selectIndicesWhereOpConditions(cndL3)), dcM.getRowCount())
            self.assertEqual(len(dcM.selectIndicesWhereOpConditions(cndL4)), 0)
            #
            for at in atL[1:-1]:
                self.assertEqual(len(dcM.selectValuesWhereOpConditions(at, cndL1)), dcM.getRowCount())
                self.assertEqual(len(dcM.selectValuesWhereOpConditions(at, cndL2)), 0)
                self.assertEqual(len(dcM.selectValuesWhereOpConditions(at, cndL3)), dcM.getRowCount())
                self.assertEqual(len(dcM.selectValuesWhereOpConditions(at, cndL4)), 0)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()


def suiteBase():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(DataCategoryTests("testBaseBasicAscii"))
    suiteSelect.addTest(DataCategoryTests("testBaseBasicAsciiDiff"))
    suiteSelect.addTest(DataCategoryTests("testBaseMethodsAscii"))
    suiteSelect.addTest(DataCategoryTests("testBaseMethodsUnicode"))
    suiteSelect.addTest(DataCategoryTests("testBaseBasicUnicode"))
    return suiteSelect


def suiteSubclass():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(DataCategoryTests("testBasicAscii"))
    suiteSelect.addTest(DataCategoryTests("testBasicAsciiDiff"))
    suiteSelect.addTest(DataCategoryTests("testBasicUnicode"))
    suiteSelect.addTest(DataCategoryTests("testEditRemoveRow"))
    suiteSelect.addTest(DataCategoryTests("testEditRowAccessors"))
    suiteSelect.addTest(DataCategoryTests("testEditAttributes"))
    suiteSelect.addTest(DataCategoryTests("testEditExtend"))
    suiteSelect.addTest(DataCategoryTests("testGetValues"))
    suiteSelect.addTest(DataCategoryTests("testGetSelectValues"))
    suiteSelect.addTest(DataCategoryTests("testSetValues"))
    suiteSelect.addTest(DataCategoryTests("testReplaceValues"))
    suiteSelect.addTest(DataCategoryTests("testCompareAttributes"))
    suiteSelect.addTest(DataCategoryTests("testCompareValues"))
    suiteSelect.addTest(DataCategoryTests("testCondSelectValues"))
    suiteSelect.addTest(DataCategoryTests("testCondOpSelectValues"))
    #
    return suiteSelect


if __name__ == "__main__":
    #
    mySuite = suiteBase()
    unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)

    mySuite = suiteSubclass()
    unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)
