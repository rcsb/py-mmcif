##
# File:    DictionaryReadWriteTests.py
# Author:  jdw
# Date:    9-Mar-2018
# Version: 0.001
##
"""
Test cases for simple dictionary read and write operations.

"""
from __future__ import absolute_import

import logging
import os
import sys
import time
import unittest

from mmcif.io.IoAdapterPy import IoAdapterPy

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


class DictionaryReadWriteTests(unittest.TestCase):
    def setUp(self):
        self.__lfh = sys.stdout
        self.__verbose = False
        self.__pathPdbxDictionary = os.path.join(HERE, "data", "mmcif_pdbx_v5_next.dic")
        self.__startTime = time.time()
        logger.debug("Testing version %s", __version__)
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testReadDictionary(self):
        """Test case -  read logical structure of dictionary
        """
        try:
            myIo = IoAdapterPy(self.__verbose, self.__lfh)
            containerList = myIo.readFile(inputFilePath=self.__pathPdbxDictionary)
            logger.debug("container list is  %s", ([c.getName() for c in containerList]))
            self.assertGreaterEqual(len(containerList), 400)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testReadWriteDictionary(self):
        """Test case -  read and dump logical structure of dictionary
        """
        try:
            myIo = IoAdapterPy(self.__verbose, self.__lfh)
            containerList = myIo.readFile(inputFilePath=self.__pathPdbxDictionary)
            ok = myIo.writeFile(outputFilePath=os.path.join(HERE, "test-output", "test-dict-out.dic"), containerList=containerList)
            self.assertTrue(ok)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()


def suiteReadWriteTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(DictionaryReadWriteTests("testReadDictionary"))
    suiteSelect.addTest(DictionaryReadWriteTests("testReadWriteDictionary"))
    return suiteSelect


if __name__ == "__main__":

    mySuite = suiteReadWriteTests()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
