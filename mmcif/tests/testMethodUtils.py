##
#
# File:    MethodUtilsTests.py
# Author:  jdw
# Date:    2-Oct-2017 jdw
# Version: 0.001
##
"""
Test cases for dictionary method management and invocation.

"""
from __future__ import absolute_import

import logging
import os
import os.path
import sys
import time
import unittest

from mmcif.api.MethodUtils import MethodUtils
from mmcif.io.IoAdapterPy import IoAdapterPy as IoAdapter

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

try:
    from mmcif import __version__
except ImportError:
    sys.path.insert(0, TOPDIR)
    from mmcif import __version__


__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class MethodUtilsTests(unittest.TestCase):
    def setUp(self):
        self.__lfh = sys.stdout
        self.__verbose = False

        self.__pathPdbxDataFile = os.path.join(HERE, "data", "1kip.cif")
        self.__pathPdbxDictFile = os.path.join(HERE, "data", "mmcif_pdbx_v5_next_w_methods.dic")
        self.__pathOutFile = os.path.join(HERE, "test-output", "test-after-invoke-methods.cif")

        self.__startTime = time.time()
        logger.debug("Running tests on version %s", __version__)
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testGetDictionaryMethods(self):
        """Test case -  dump methods for dictionary metadata"""
        try:
            myIo = IoAdapter(self.__verbose, self.__lfh)
            dictContainerList = myIo.readFile(inputFilePath=self.__pathPdbxDictFile)
            mU = MethodUtils(dictContainerList=dictContainerList, verbose=self.__verbose)
            mU.dumpMethods(fh=self.__lfh)
            #
            mD = mU.getMethods()
            self.assertEqual(len(mD), 5)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testInvokeDictionaryMethods(self):
        """Test case -  invoke dictionary methods -"""
        try:
            myIo = IoAdapter(self.__verbose, self.__lfh)
            dictContainerList = myIo.readFile(inputFilePath=self.__pathPdbxDictFile)
            dataContainerList = myIo.readFile(inputFilePath=self.__pathPdbxDataFile)

            #
            mU = MethodUtils(dictContainerList=dictContainerList, verbose=self.__verbose)
            mU.setDataContainerList(dataContainerList=dataContainerList)
            mU.invokeMethods()
            logger.debug("Write data file after invoking methods")
            dataContainerList = mU.getDataContainerList()
            ok = myIo.writeFile(outputFilePath=self.__pathOutFile, containerList=dataContainerList)
            #
            self.assertEqual(ok, True)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()


def suiteMethodUtilsTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(MethodUtilsTests("testGetDictionaryMethods"))
    suiteSelect.addTest(MethodUtilsTests("testInvokeDictionaryMethods"))
    return suiteSelect


if __name__ == "__main__":

    mySuite = suiteMethodUtilsTests()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
