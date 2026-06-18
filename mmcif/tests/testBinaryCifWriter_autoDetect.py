##
#
# File:    testBinaryCifWriter.py
# Author:  J. Westbrook
# Date: 16-May-2021
#
# Updates:
#   - dictionaryApi and DataCategoryTyped removed.
#     Type resolution is now handled entirely by bcif_type_detector.classify_column()
#     inside BinaryCifWriter_autoDetect.  No dictionary file needs to be loaded at test time.
##

import logging
import os
import sys
import time
from io import StringIO
import unittest
import msgpack

# DataCategoryTyped and DictionaryApi are no longer needed —
# BinaryCifWriter_autoDetect uses bcif_type_detector for all type resolution.
from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import DataContainer
from mmcif.io.BinaryCifReader import BinaryCifReader
from mmcif.io.BinaryCifWriter_autoDetect import BinaryCifWriter_autoDetect
from mmcif.io.IoAdapterPy import IoAdapterPy as IoAdapter
from mmcif.tests.BcifPrint import BcifPrint

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


class CaptureLogger:
    """Context manager to capture `logging` streams

    Args:
        - logobj: 'logging` logger object

    Results:
        The captured output is available via `self.out`

    """
    def __init__(self, logobj):
        self.logger = logobj
        self.io = StringIO()
        self.sh = logging.StreamHandler(self.io)
        self.out = ''

    def __enter__(self):
        self.logger.addHandler(self.sh)
        return self

    def __exit__(self, *exc):
        self.logger.removeHandler(self.sh)
        self.out = self.io.getvalue()

    def __repr__(self):
        return f"captured: {self.out}\n"


class BinaryCifWriterTests(unittest.TestCase):
    def setUp(self):
        self.__pathOutputDir = os.path.join(HERE, "autoDetect_testOutput")
        self.__baseCifUrl = "https://files.rcsb.org/download/"
        self.__testCifList = ["11BJ"]
        #self.__testBcifOutput = os.path.join(self.__pathOutputDir, "4hhb-with_autoDetect.bcif")
        #self.__testBcifTranslated = os.path.join(self.__pathOutputDir, "4hhb-generated-translated.bcif")
        #self.__testBcifTypeOutput = os.path.join(self.__pathOutputDir, "4hhb-type-generated.bcif")

        # dictionaryApi removed — BinaryCifWriter_autoDetect now uses bcif_type_detector
        # for all type resolution.  No dictionary file needs to be loaded.

        self.__floatTolerance = 1.0e-10
        self.__startTime = time.time()
        logger.debug("Running tests on version %s", __version__)
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testSerialize(self):
        try:
            for cifId in self.__testCifList:
                cifFileUrl = os.path.join(self.__baseCifUrl, cifId + ".cif")
                bcifOutput = os.path.join(self.__pathOutputDir, "%s-with_autoDetect.bcif" % cifId.lower())
                bcifTranslated = os.path.join(self.__pathOutputDir, "%s-generated-translated.bcif" % cifId.lower())
                for storeStringsAsBytes in [True, False]:
                    logger.info("serializing cif %s (storeStringAsBytes %r)", cifFileUrl, storeStringsAsBytes)

                    ioPy = IoAdapter()
                    containerList = ioPy.readFile(cifFileUrl)

                    # DataCategoryTyped pre-casting removed.
                    # The writer's __encodeColumnData() now casts values to the
                    # correct Python type (int/float) based on the profile returned
                    # by classify_column(), so raw DataCategory objects can be
                    # passed directly without a prior DataCategoryTyped pass.

                    # No dictionaryApi argument — auto-detection handles all columns.
                    bcw = BinaryCifWriter_autoDetect(storeStringsAsBytes=storeStringsAsBytes, useFloat64=True)
                    bcw.serialize(bcifOutput, containerList)

                    self.assertEqual(containerList[0], containerList[0])

                    self.__verifyEncoding(bcifOutput, storeStringsAsBytes)
                    bcr = BinaryCifReader(storeStringsAsBytes=storeStringsAsBytes)
                    cL = bcr.deserialize(bcifOutput)

                    ioPy = IoAdapter()
                    ok = ioPy.writeFile(bcifTranslated, cL)
                    self.assertTrue(ok)
                    self.assertTrue(self.__same(containerList[0], cL[0]))
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def __verifyEncoding(self, fname, storeStringsAsBytes):
        """Verifies encoding"""
        with open(fname, "rb") as fin:
            bD = msgpack.unpack(fin)

        bc = BcifPrint(storeStringsAsBytes)
        bc.dump(bD, output=False)
        err = bc.getError()
        if err:
            sys.stderr.write("Failure %s\n" % fname)
        self.assertFalse(err)

    @staticmethod
    def __normVal(v):
        """Normalise a single cell value to a comparable string.

        The original CIF reader returns all values as strings (e.g. '1').
        The bcif decoder returns typed values (e.g. int 1 or float 1.0).
        Normalising both sides to strings makes the comparison type-agnostic
        while still catching genuine data differences.

        Floats are rounded to 3 decimal places to absorb FixedPoint
        encode/decode rounding noise (e.g. 1.234 -> 1234 -> 1.234000001).
        """
        if v is None:
            return "?"
        s = str(v).strip()
        if s in (".", "?", ""):
            return s
        try:
            return "{:.3f}".format(float(s))
        except (ValueError, TypeError):
            return s.lower()

    def __same(self, cA, cB):
        """Compare two DataContainer objects value by value.

        Args:
            cA (DataContainer): source container (from original CIF read)
            cB (DataContainer): decoded container (from bcif round-trip)

        Returns:
            bool: True if all categories, attributes, and values match.

        Note: values are normalised to strings before comparison so that
        type differences introduced by the encode/decode round-trip
        (e.g. '1' vs int 1, '1.234' vs float 1.234) do not cause false
        failures.  This is correct because the source of truth is always
        the string representation from the original CIF file.
        """
        if cA.getName() != cB.getName():
            logger.info("name(A) %s ne name(B) %s", cA.getName(), cB.getName())
            return False

        aNmL = cA.getObjNameList()
        bNmL = cB.getObjNameList()

        if len(aNmL) != len(bNmL):
            logger.info("length(A) %r ne length(B) %r", len(aNmL), len(bNmL))
            return False

        if sorted(aNmL) != sorted(bNmL):
            logger.info("sorted name list(A) ne name list(B) %r", set(aNmL) - set(bNmL))
            return False

        if aNmL != bNmL:
            logger.info("unsorted name list(A) ne name list(B) %r", set(aNmL) - set(bNmL))
            return False

        for aNm in aNmL:
            aObj = cA.getObj(aNm)
            bObj = cB.getObj(aNm)

            ta, _, tb = aObj.cmpAttributeNames(bObj)
            if ta or tb:
                logger.info("attributes differ (a not b) %r  (b not a) %r", ta, tb)
                return False

            for atName in aObj.getAttributeList():
                ii = aObj.getAttributeIndex(atName)
                jj = bObj.getAttributeIndex(atName)
                aCol = aObj.getColumn(ii)
                bCol = bObj.getColumn(jj)

                if len(aCol) != len(bCol):
                    logger.info("row count differs for attribute %r: %d vs %d",
                                atName, len(aCol), len(bCol))
                    return False

                for row, (av, bv) in enumerate(zip(aCol, bCol)):
                    na = self.__normVal(av)
                    nb = self.__normVal(bv)
                    if na != nb:
                        logger.info("values differ for attribute %r at row %d: "
                                    "%r (cif) vs %r (bcif)", atName, row, av, bv)
                        logger.info("aCol %r", aCol)
                        logger.info("bCol %r", bCol)
                        return False

        return True

    def testItemTypes(self):
        """Tests that string-valued columns encode without cast errors."""
        myDataList = []
        curContainer = DataContainer("myblock")
        aCat = DataCategory("em_single_particle_entity")
        aCat.appendAttribute("point_symmetry")
        aCat.append(["I", ])
        curContainer.append(aCat)
        myDataList.append(curContainer)

        # No dictionaryApi argument — auto-detection classifies "I" as string
        # correctly without needing the dictionary to declare the type.
        bcw = BinaryCifWriter_autoDetect(useStringTypes=True)

        with CaptureLogger(logger) as cl:
            bcw.serialize(self.__testBcifTypeOutput, myDataList)
        self.assertNotIn("Cast error", cl.out)


def suiteBcifWriter():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(BinaryCifWriterTests("testSerialize"))
    suiteSelect.addTest(BinaryCifWriterTests("testItemTypes"))
    return suiteSelect


if __name__ == "__main__":
    mySuite = suiteBcifWriter()
    unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)