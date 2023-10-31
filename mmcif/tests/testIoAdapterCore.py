##
#
# File:    IoAdapterCoreTests.py
# Author:  J. Westbrook
# Date:    01-Aug-2017
# Version: 0.001
#
# Updates:
#   2-Oct-2017 jdw  adjust block count on dictionary test
#   4-Oct-2017 jdw  verified the package IoAdapter default preference works.
#   7-Dec-2017 jdw  path all output files
#   9-Jan-2018 jdw  update tests for new binding library - add logging framework
##
"""
Test cases for reading and updating mmCIF data files using Python Wrapper
IoAdapterCore wrapper which provides an API to the C++ CifFile class
library of file and dictionary tools conforming to our native Python library.
"""
from __future__ import absolute_import

import logging
import os
import sys
import time
import unittest

from mmcif.io.IoAdapterCore import IoAdapterCore as IoAdapter
from mmcif.io.PdbxExceptions import PdbxError, PdbxSyntaxError
# from mmcif.api.DictionaryApi import DictionaryApi

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


class IoAdapterTests(unittest.TestCase):

    # def shortDescription():

    def setUp(self):
        self.__lfh = sys.stdout
        self.__verbose = True
        #
        self.__pathPdbxDataFile = os.path.join(HERE, "data", "1kip.cif")
        self.__pathBigPdbxDataFile = os.path.join(HERE, "data", "1ffk.cif.gz")
        self.__pathPdbxDictFile = os.path.join(HERE, "data", "mmcif_pdbx_v5_next.dic")
        #
        self.__pathErrPdbxDataFile = os.path.join(HERE, "data", "1bna-errors.cif")
        self.__pathQuotesPdbxDataFile = os.path.join(HERE, "data", "specialTestFile.cif")
        #
        self.__pathOutputPdbxFile = os.path.join(HERE, "test-output", "myPdbxOutputFile.cif")
        self.__pathOutputPdbxFileSelect = os.path.join(HERE, "test-output", "myPdbxOutputFileSelect.cif")
        self.__pathOutputPdbxFileExclude = os.path.join(HERE, "test-output", "myPdbxOutputFileExclude.cif")
        #
        self.__pathQuotesOutputPdbxFile = os.path.join(HERE, "test-output", "myPdbxQuotesOutputFile.cif")
        self.__pathBigOutputDictFile = os.path.join(HERE, "test-output", "myDictOutputFile.cif")
        #
        self.__pathUnicodePdbxFile = os.path.join(HERE, "data", "unicode-test.cif")
        self.__pathCharRefPdbxFile = os.path.join(HERE, "data", "unicode-char-ref-test.cif")
        #
        self.__pathOutputUnicodePdbxFile = os.path.join(HERE, "test-output", "out-unicode-test.cif")
        self.__pathOutputCharRefPdbxFile = os.path.join(HERE, "test-output", "out-unicode-char-ref-test.cif")
        #
        self.__pathRcsbBcifGzip = os.path.join(HERE, "data", "1bna.bcif.gz")
        self.__pathOutputRcsbBcifTranslated = os.path.join(HERE, "test-output", "1bna-translated-from-bcif.cif")
        self.__pathOutputPdbxBcif = os.path.join(HERE, "test-output", "1kip-generated.bcif")
        self.__pathOutputPdbxBcifTyped = os.path.join(HERE, "test-output", "1kip-generated-typed.bcif")

        self.__pathOutputDir = os.path.join(HERE, "test-output")
        self.__startTime = time.time()
        logger.debug("Running tests on version %s", __version__)
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testFileReaderUtf8(self):
        self.__testFileReader(self.__pathPdbxDataFile, enforceAscii=False)

    def testFileReaderBigUtf8(self):
        self.__testFileReader(self.__pathBigPdbxDataFile, enforceAscii=False)

    def testFileReaderQuotesUtf8(self):
        self.__testFileReader(self.__pathQuotesPdbxDataFile, enforceAscii=False)

    def testFileReaderUnicodeUtf8(self):
        # core parser will only parse ascii so this must fail
        # self.__testFileReader(self.__pathUnicodePdbxFile, enforceAscii=False)
        self.__testFileReaderExceptionHandler2(self.__pathUnicodePdbxFile, enforceAscii=False)

    def testFileReaderAscii(self):
        self.__testFileReader(self.__pathPdbxDataFile, enforceAscii=True)

    def testFileReaderBigAscii(self):
        self.__testFileReader(self.__pathBigPdbxDataFile, enforceAscii=True)

    def testFileReaderQuotesAscii(self):
        self.__testFileReader(self.__pathQuotesPdbxDataFile, enforceAscii=True)

    def __testFileReader(self, fp, enforceAscii=False, raiseExceptions=True):
        """Test case -  read PDBx file"""
        try:
            io = IoAdapter(raiseExceptions=raiseExceptions)
            containerList = io.readFile(fp, enforceAscii=enforceAscii, outDirPath=self.__pathOutputDir)
            logger.debug("Read %d data blocks", len(containerList))
            self.assertEqual(len(containerList), 1)
        except Exception as e:
            logger.error("Failing with %s", str(e))
            self.fail()

    def testDictReaderUtf8(self):
        self.__testDictReader(self.__pathPdbxDictFile, enforceAscii=False)

    def testDictReaderAscii(self):
        self.__testDictReader(self.__pathPdbxDictFile, enforceAscii=True)

    def __testDictReader(self, fp, enforceAscii=False):
        """Test case -  read PDBx dictionary file"""
        try:
            io = IoAdapter(raiseExceptions=False)
            containerList = io.readFile(fp, enforceAscii=enforceAscii, outDirPath=self.__pathOutputDir)
            logger.info("Read %d data blocks", len(containerList))
            # for container in containerList:
            #     container.printIt()
            #
            self.assertTrue(len(containerList) > 0)
        except Exception as e:
            logger.error("Failing with %s", str(e))
            self.fail()

    #
    def testFileWIthSyntaxErrorHander1(self):
        self.__testFileReaderExceptionHandler1(self.__pathErrPdbxDataFile, enforceAscii=False)

    def testFileWIthSyntaxErrorHander2(self):
        self.__testFileReaderExceptionHandler1(self.__pathErrPdbxDataFile, enforceAscii=False)

    def testFileWIthUnicodeErrorHander2(self):
        self.__testFileReaderExceptionHandler2(self.__pathUnicodePdbxFile, enforceAscii=False)

    def __testFileReaderExceptionHandler1(self, fp, enforceAscii=False):
        """Test case -  read selected categories from PDBx file and handle exceptions"""
        io = IoAdapter(raiseExceptions=True)
        self.assertRaises(PdbxSyntaxError, io.readFile, fp, enforceAscii=enforceAscii, outDirPath=self.__pathOutputDir)

    def __testFileReaderExceptionHandler2(self, fp, enforceAscii=False):
        """Test case -  read selected categories from PDBx and handle exceptions"""
        ok = True
        try:
            io = IoAdapter(raiseExceptions=True)
            containerList = io.readFile(fp, enforceAscii=enforceAscii, outDirPath=self.__pathOutputDir)
            self.assertGreaterEqual(len(containerList), 1)
            #
        except PdbxSyntaxError as e:
            logger.debug("Expected syntax failure %s", str(e))
            self.assertTrue(ok)
        except PdbxError as e:
            logger.debug("Expected character encoding failure %s", str(e))
            self.assertTrue(ok)
        except Exception as e:
            logger.error("Unexpected exception %s", type(e).__name__)
            self.fail("Unexpected exception raised: " + str(e))
        else:
            self.fail("Expected exception not raised")

    def testFileReaderProcessErrors(self):
        self.__testFileReader(self.__pathErrPdbxDataFile, enforceAscii=False, raiseExceptions=False)
        self.__testFileReader(self.__pathUnicodePdbxFile, enforceAscii=True, raiseExceptions=False)

    def testFileReaderWriter(self):
        self.__testFileReaderWriter(self.__pathBigPdbxDataFile, self.__pathOutputPdbxFile)

    @unittest.skip("Dictionary test skipping")
    def testDictReaderWriter(self):
        self.__testFileReaderWriter(self.__pathPdbxDictFile, self.__pathBigOutputDictFile)

    def testFileReaderWriterQuotes(self):
        self.__testFileReaderWriter(self.__pathQuotesPdbxDataFile, self.__pathQuotesOutputPdbxFile)

    #
    def testFileReaderWriterUnicode(self):
        self.__testFileReaderWriter(self.__pathUnicodePdbxFile, self.__pathOutputUnicodePdbxFile, enforceAscii=True)

    def testFileReaderWriterCharRef(self):
        self.__testFileReaderWriter(self.__pathCharRefPdbxFile, self.__pathOutputCharRefPdbxFile, enforceAscii=True)

    def __testFileReaderWriter(self, ifp, ofp, **kwargs):
        """Test case -  read and then write PDBx file or dictionary"""
        try:
            io = IoAdapter(raiseExceptions=True, useCharRefs=True)
            containerList = io.readFile(ifp, enforceAscii=True, outDirPath=self.__pathOutputDir)
            logger.debug("Read %d data blocks", len(containerList))
            ok = io.writeFile(ofp, containerList=containerList, **kwargs)
            self.assertTrue(ok)
        except Exception as e:
            logger.error("Failing with %s", str(e))
            self.fail()

    def testFileReaderWriterSelect(self):
        self.__testFileReaderWriterSelect(self.__pathBigPdbxDataFile, self.__pathOutputPdbxFileSelect, selectList=["atom_site"])

    def testFileReaderWriterExclude(self):
        self.__testFileReaderWriterSelect(self.__pathBigPdbxDataFile, self.__pathOutputPdbxFileExclude, selectList=["atom_site"], excludeFlag=True)

    def __testFileReaderWriterSelect(self, ifp, ofp, selectList=None, excludeFlag=False):
        """Test case -  read and then write PDBx file with selection."""
        try:
            io = IoAdapter(raiseExceptions=True, useCharRefs=True)
            containerList = io.readFile(ifp, enforceAscii=True, selectList=selectList, excludeFlag=excludeFlag, outDirPath=self.__pathOutputDir)
            logger.debug("Read %d data blocks", len(containerList))
            ok = io.writeFile(ofp, containerList=containerList, enforceAscii=True)
            self.assertTrue(ok)
        except Exception as e:
            logger.error("Failing with %s", str(e))
            self.fail()

    def testBcifReaderWriter(self):
        self.__testBcifToCif(self.__pathRcsbBcifGzip, self.__pathOutputRcsbBcifTranslated)
        self.__testCifToBcif(self.__pathPdbxDataFile, self.__pathOutputPdbxBcif, self.__pathOutputPdbxBcifTyped)

    def __testBcifToCif(self, ifp, ofp):
        """Test case -  read binary (BCIF) PDBx file."""
        try:
            io = IoAdapter(raiseExceptions=True)
            containerList = io.readFile(ifp, enforceAscii=False, fmt="bcif", outDirPath=self.__pathOutputDir)
            logger.info("Read %d data blocks from BCIF file %r", len(containerList), ifp)
            ok = len(containerList) > 0
            self.assertTrue(ok)
            ok = io.writeFile(ofp, containerList=containerList, enforceAscii=False)
            logger.info("Wrote %d data blocks to mmCIF file (%r) %r", ok, len(containerList), ofp)
            self.assertTrue(ok)
            containerListTranslated = io.readFile(ofp, enforceAscii=False, fmt="mmcif", outDirPath=self.__pathOutputDir)
            logger.info("Read %d data blocks from translated mmCIF file %r", len(containerListTranslated), ofp)
            ok = len(containerListTranslated) > 0
            self.assertTrue(ok)
            ok = len(containerListTranslated) == len(containerList)
            self.assertTrue(ok)
        except Exception as e:
            logger.exception("Failing input %s and output %s with %s", ifp, ofp, str(e))
            self.fail()

    def __testCifToBcif(self, ifp, ofp, ofpTyped):
        """Test case -  write binary (BCIF) PDBx file."""
        try:
            io = IoAdapter(raiseExceptions=True)
            containerList = io.readFile(ifp, enforceAscii=False, fmt="mmcif", outDirPath=self.__pathOutputDir)
            logger.info("Read %d data blocks from mmCIF file %r", len(containerList), ifp)
            ok = len(containerList) > 0
            self.assertTrue(ok)
            #
            logger.info("Skipping test of writing BCIF file WITH typing until dictionary reading is fixed (%r)", ofpTyped)
            # # Test writing to file WITH typing
            # ioDict = IoAdapter(raiseExceptions=False)
            # dApiContainerList = ioDict.readFile(self.__pathPdbxDictFile, enforceAscii=False, outDirPath=self.__pathOutputDir)
            # ok = len(dApiContainerList) > 0
            # self.assertTrue(ok)
            # dApi = DictionaryApi(containerList=dApiContainerList, consolidate=True)
            # ok = io.writeFile(ofpTyped, containerList=containerList, enforceAscii=False, fmt="bcif", applyTypes=True, dictionaryApi=dApi, useStringTypes=False, copyInputData=True)
            # logger.info("Wrote %d data blocks to typed BCIF file (%r) %r", ok, len(containerList), ofpTyped)
            # self.assertTrue(ok)
            # Test writing to file WITHOUT typing (treat everything as a string) -- this keeps everything the exact same as the input
            ok = io.writeFile(ofp, containerList=containerList, enforceAscii=False, fmt="bcif", applyTypes=False, useStringTypes=True, copyInputData=False)
            logger.info("Wrote %d data blocks to untyped BCIF file (%r) %r", ok, len(containerList), ofp)
            self.assertTrue(ok)
            containerListBcif = io.readFile(ofp, enforceAscii=False, fmt="bcif", outDirPath=self.__pathOutputDir)
            logger.info("Read %d data blocks from translated BCIF file %r", len(containerListBcif), ofp)
            ok = len(containerListBcif) > 0
            self.assertTrue(ok)
            ok = len(containerListBcif) == len(containerList)
            self.assertTrue(ok)
            cCif = containerList[0]
            cBcif = containerListBcif[0]
            ok = True
            for cat in cCif.getObjNameList():
                for attr in cCif.getObj(cat).getAttributeList():
                    matchOk = cCif.getObj(cat).getAttributeValueList(attr) == cBcif.getObj(cat).getAttributeValueList(attr)
                    logger.debug("Category and attribute %r %r: %r", cat, attr, matchOk)
                    if not matchOk:
                        ok = False
            self.assertTrue(ok)
        except Exception as e:
            logger.exception("Failing input %s and output %s with %s", ifp, ofp, str(e))
            self.fail()


def suiteFileReaderRaw():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(IoAdapterTests("testFileReaderUtf8"))
    suiteSelect.addTest(IoAdapterTests("testFileReaderBigUtf8"))
    suiteSelect.addTest(IoAdapterTests("testFileReaderQuotesUtf8"))
    #
    return suiteSelect


def suiteFileReaderAscii():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(IoAdapterTests("testFileReaderAscii"))
    suiteSelect.addTest(IoAdapterTests("testFileReaderBigAscii"))
    suiteSelect.addTest(IoAdapterTests("testFileReaderQuotesAscii"))
    return suiteSelect


def suiteFileReaderExceptions():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(IoAdapterTests("testFileWIthSyntaxErrorHander1"))
    suiteSelect.addTest(IoAdapterTests("testFileWIthSyntaxErrorHander2"))
    #
    suiteSelect.addTest(IoAdapterTests("testFileWIthUnicodeErrorHander2"))
    return suiteSelect


def suiteFileReaderProcessErrors():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(IoAdapterTests("testFileReaderProcessErrors"))
    return suiteSelect


def suiteDictReader():
    suiteSelect = unittest.TestSuite()
    # suiteSelect.addTest(IoAdapterTests("testDictReaderAscii"))
    suiteSelect.addTest(IoAdapterTests("testDictReaderUtf8"))
    return suiteSelect


def suiteReaderUnicode():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(IoAdapterTests("testFileReaderUnicodeUtf8"))
    return suiteSelect


def suiteReaderWriter():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(IoAdapterTests("testFileReaderWriter"))
    # suiteSelect.addTest(IoAdapterTests("testDictReaderWriter"))
    return suiteSelect


def suiteReaderWriterSelect():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(IoAdapterTests("testFileReaderWriterSelect"))
    suiteSelect.addTest(IoAdapterTests("testFileReaderWriterExclude"))
    return suiteSelect


def suiteReaderWriterUnicode():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(IoAdapterTests("testFileReaderWriterCharRef"))
    suiteSelect.addTest(IoAdapterTests("testFileReaderWriterUnicode"))
    return suiteSelect


def suiteReaderWriterBcif():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(IoAdapterTests("testBcifReaderWriter"))
    return suiteSelect


if __name__ == "__main__":
    #

    mySuite = suiteFileReaderRaw()
    unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)

    mySuite = suiteFileReaderAscii()
    unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)

    mySuite = suiteReaderWriter()
    unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)

    mySuite = suiteFileReaderExceptions()
    unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)

    mySuite = suiteFileReaderProcessErrors()
    unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)

    mySuite = suiteDictReader()
    unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)

    mySuite = suiteReaderUnicode()
    unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)

    mySuite = suiteReaderWriterUnicode()
    unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)

    mySuite = suiteReaderWriterSelect()
    unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)

    mySuite = suiteReaderWriterBcif()
    unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)
#
