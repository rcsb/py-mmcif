##
# File:    DictionaryInclude.py
# Author:  jdw
# Date:    31-Mar-2021
# Version: 0.001
##
"""
Tests cases for dictionary composition/include processing.

"""
from __future__ import absolute_import, print_function

import logging
import os
import sys
import time
import unittest

from mmcif.api.DictionaryApi import DictionaryApi
from mmcif.api.DictionaryInclude import DictionaryInclude
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


class DictionaryIncludeTests(unittest.TestCase):
    def setUp(self):
        self.__pathDdlIncludeDictionary = os.path.join(HERE, "data", "mmcif_ddl-generator.dic")
        self.__pathDdlGeneratedDictionary = os.path.join(HERE, "data", "mmcif_ddl_generated.dic")
        self.__pathDdlDictionary = os.path.join(HERE, "data", "mmcif_ddl.dic")
        self.__startTime = time.time()
        logger.debug("Running tests on version %s", __version__)
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testDDLInclude(self):
        """Test case -  DDL composition/include tests"""
        try:
            myIo = IoAdapter(raiseExceptions=True)
            containerList = myIo.readFile(inputFilePath=self.__pathDdlIncludeDictionary)
            logger.info("Starting container list length (%d)", len(containerList))
            dIncl = DictionaryInclude()
            inclL = dIncl.processIncludedContent(containerList)
            logger.info("Processed included container length (%d)", len(inclL))

            ok = myIo.writeFile(outputFilePath=os.path.join(HERE, "test-output", "mmcif_ddl_generated.dic"), containerList=inclL)
            self.assertTrue(ok)
            #
            myIo = IoAdapter(raiseExceptions=True)
            crefL = myIo.readFile(inputFilePath=self.__pathDdlDictionary)
            logger.info("Reference object count (%d)", len(crefL))
            self.assertGreaterEqual(len(crefL), 257)
            #
            cD = {incl.getName(): True for incl in inclL}
            for cref in crefL:
                if cref.getName() not in cD:
                    logger.info("In reference missing in included file %r", cref.getName())
            #
            cD = {cref.getName(): True for cref in crefL}
            for incl in inclL:
                if incl.getName() not in cD:
                    logger.info("Included but missing in reference %r", incl.getName())
            #
            self.assertGreaterEqual(len(inclL), 258)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testDDLApi(self):
        """Test case -  DDL API linkage counts"""
        try:
            myIo = IoAdapter(raiseExceptions=True)
            containerList = myIo.readFile(inputFilePath=self.__pathDdlGeneratedDictionary)
            dApi = DictionaryApi(containerList=containerList, consolidate=True, expandItemLinked=True)
            cL = dApi.getCategoryList()
            logger.info("Category length %r", len(cL))
            self.assertGreaterEqual(len(cL), 63)
            cL = dApi.getFullChildList("category", "id")
            logger.info("Children of category.id (%d)", len(cL))
            self.assertGreaterEqual(len(cL), 11)
            #
            cL = dApi.getFullDescendentList("category", "id")
            logger.info("Descendents of category.id (%d)", len(cL))
            self.assertGreaterEqual(len(cL), 13)
            #
            cL = dApi.getFullChildList("item", "name")
            logger.info("Children of item.name (%d)", len(cL))
            self.assertGreaterEqual(len(cL), 36)
            cL = dApi.getFullDescendentList("item", "name")
            logger.info("Descendents of item.name (%d)", len(cL))
            self.assertGreaterEqual(len(cL), 38)
            #

            val = dApi.getDictionaryVersion()
            self.assertEqual(val, "2.2.2")
            val = dApi.getDictionaryTitle()
            self.assertEqual(val, "mmcif_ddl.dic")
            val = dApi.getDictionaryUpdate(order="reverse")
            self.assertEqual(val, "2020-06-05")
            val = dApi.getDictionaryRevisionCount()
            self.assertGreaterEqual(val, 78)
            valL = dApi.getDictionaryHistory(order="reverse")
            self.assertGreaterEqual(len(valL), 78)
            #
            val = dApi.getDictionaryComponentCount()
            self.assertGreaterEqual(val, 6)
            #
            valL = dApi.getDictionaryComponentDetails()
            self.assertGreaterEqual(len(valL), 6)

            valL = dApi.getDictionaryComponents()
            self.assertGreaterEqual(len(valL), 6)
            for dictionaryComponentId in dApi.getDictionaryComponents():
                valL = dApi.getDictionaryComponentHistory(dictionaryComponentId, order="reverse")
                self.assertGreaterEqual(len(valL), 2)

            #
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()


def suiteDictionaryIncludeTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(DictionaryIncludeTests("testDDLInclude"))
    suiteSelect.addTest(DictionaryIncludeTests("testDDLApi"))
    return suiteSelect


if __name__ == "__main__":
    mySuite = suiteDictionaryIncludeTests()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
