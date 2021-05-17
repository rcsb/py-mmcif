##
#
# File:    testCifQuoting.py
# Author:  E. Peisach
# Date:    10-May-2020
# Version: 0.001
#
# Updates:
##
"""
Test cases for reading and writing mmCIF data files using Python Wrapper
to ensure quoting is case insensitive
"""
from __future__ import absolute_import

import logging
import os
import sys
import time
import unittest

from mmcif.io.IoAdapterCore import IoAdapterCore as IoAdapter
from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import DataContainer
from mmcif.io.PdbxReader import PdbxReader
from mmcif.io.PdbxWriter import PdbxWriter

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


class QuotingTests(unittest.TestCase):
    def setUp(self):
        self.__lfh = sys.stdout
        self.__verbose = True
        #
        self.__pathOutputFile = os.path.join(HERE, "test-output", "myPdbxCaseFile.cif")
        self.__pathOutputFile2 = os.path.join(HERE, "test-output", "myPdbxCaseFile2.cif")
        self.__pathOutputDir = os.path.join(HERE, "test-output")

        self.__startTime = time.time()
        logger.debug("Running tests on version %s", __version__)
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testPdbxFileCase(self):
        """Test case sensitive PdxWriter"""

        if os.path.exists(self.__pathOutputFile):
            os.unlink(self.__pathOutputFile)

        curContainer = self.__generateData()
        myDataList = [curContainer]
        try:
            with open(self.__pathOutputFile, "w") as ofh:
                pdbxW = PdbxWriter(ofh)
                pdbxW.write(myDataList)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

        self.__testReaders(self.__pathOutputFile)

    def testIoFileCase(self):
        """Test case sensitive IoAdapter writer"""

        if os.path.exists(self.__pathOutputFile2):
            os.unlink(self.__pathOutputFile2)

        curContainer = self.__generateData()

        myDataList = [curContainer]
        io = IoAdapter(raiseExceptions=True)
        ok = io.writeFile(self.__pathOutputFile2, containerList=myDataList)
        self.assertTrue(ok, "Writing data test")

        self.__testReaders(self.__pathOutputFile2)

    def __testReaders(self, fPath):
        """Tests python and IoAdapter readers and checks values"""
        # Python reader

        myContainerList = []
        with open(fPath, "r") as ifh:
            pRd = PdbxReader(ifh)
            pRd.read(myContainerList)

        self.__testValues(myContainerList)

        # C++ IoAdapter reader
        try:
            io = IoAdapter(raiseExceptions=True)
            containerList = io.readFile(fPath, outDirPath=self.__pathOutputDir)
            logger.debug("Read %d data blocks", len(containerList))
            self.assertEqual(len(containerList), 1)
        except Exception as e:
            logger.error("Failing with %s", str(e))
            self.fail()

        self.__testValues(containerList)

    def __generateData(self):
        """Generates data for test. __testValues must be in sync"""
        curContainer = DataContainer("myblock")
        aCat = DataCategory("pdbx_test")
        aCat.appendAttribute("ordinal")
        aCat.appendAttribute("details")
        aCat.append([1, "data_my_big_data_file"])
        aCat.append([2, "loop_my_big_data_loop"])
        aCat.append([3, "save_my_big_data_saveframe"])
        aCat.append([4, "_category.item"])
        aCat.append([5, "Data_my_big_data_file"])
        aCat.append([6, "Loop_my_big_data_loop"])
        aCat.append([7, "Save_my_big_data_saveframe"])
        aCat.append([8, "DatA_my_big_data_file"])
        curContainer.append(aCat)

        return curContainer

    def __testValues(self, containerList):
        """Test read data"""
        self.assertEqual(len(containerList), 1)
        c0 = containerList[0]
        catObj = c0.getObj("pdbx_test")
        self.assertIsNotNone(catObj)
        self.assertEqual(catObj.getValue("details", 7), "DatA_my_big_data_file")


def suiteFileCase():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(QuotingTests("testPdbxFileCase"))
    suiteSelect.addTest(QuotingTests("testIoFileCase"))
    #
    return suiteSelect


if __name__ == "__main__":
    #
    mySuite = suiteFileCase()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
