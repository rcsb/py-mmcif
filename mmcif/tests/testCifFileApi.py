##
# File:    CifFileApiTests.py
# Author:  J. Westbrook
# Date:    28-Oct-2018
#
# Updates:
#
##
"""
Test cases for deprated Python wrapper for C++ CifFile class library of file and dictionary tools.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import os
import sys
import unittest

from mmcif.core.mmciflib import ParseCifSimple  # pylint: disable=no-name-in-module,import-error
from mmcif.io.CifFile import CifFile

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))


class CifFileApiTests(unittest.TestCase):
    def setUp(self):
        self.__lfh = sys.stdout
        self.__verbose = True
        #
        self.__pathPdbxDataFile = os.path.join(HERE, "data", "1kip.cif")
        self.__pathBigPdbxDataFile = os.path.join(HERE, "data", "1ffk.cif")

        self.__pathPdbxDictFile = os.path.join(HERE, "data", "mmcif_pdbx_v5_next.dic")

        self.__pathOutputPdbxFile = os.path.join(HERE, "test-output", "myPdbxOutputFile.cif")
        self.__pathBigOutputPdbxFile = os.path.join(HERE, "test-output", "myBigPdbxOutputFile.cif")

        self.__logFileName = os.path.join(HERE, "test-output", "ciffile-logfile.log")

    def tearDown(self):
        pass

    def testReadDataFile(self):
        """Test case -  read chemical dictionary and create index
        """
        try:
            blockNameList = []
            myReader = ParseCifSimple(self.__pathPdbxDataFile, False, 0, 255, "?", self.__logFileName)
            blockNameList = myReader.GetBlockNames(blockNameList)
            #
            for blockName in blockNameList:
                block = myReader.GetBlock(blockName)
                tableNameList = []
                tableNameList = block.GetTableNames(tableNameList)
                for tableName in tableNameList:
                    table = block.GetTable(tableName)
                    columnNameList = table.GetColumnNames()
                    logger.debug("Table %s colunms %r", tableName, columnNameList)
                    numRows = table.GetNumRows()
                    rowList = []
                    for iRow in range(0, numRows):
                        row = table.GetRow(iRow)
                        rowList.append(row)
                    logger.debug("table %s row length %d", tableName, len(rowList))
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testReadCifFile(self):
        """Test case -  deprecated CifFile api read, access and write test
        """

        try:
            blockNameList = []
            cf = CifFile(self.__pathPdbxDataFile)
            myReader = cf.getCifFile()
            blockNameList = myReader.GetBlockNames(blockNameList)
            logger.debug("Block list %r", repr(blockNameList))
            #
            for blockName in blockNameList:
                block = myReader.GetBlock(blockName)
                tableNameList = []
                tableNameList = block.GetTableNames(tableNameList)
                for tableName in tableNameList:
                    table = block.GetTable(tableName)
                    columnNameList = table.GetColumnNames()
                    logger.debug("Column list %r", repr(columnNameList))
                    numRows = table.GetNumRows()
                    rowList = []
                    for iRow in range(0, numRows):
                        row = table.GetRow(iRow)
                        rowList.append(row)
            cf.write(self.__pathOutputPdbxFile)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()


def suiteReadWriteTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(CifFileApiTests("testReadDataFile"))
    suiteSelect.addTest(CifFileApiTests("testReadCifFile"))
    return suiteSelect


if __name__ == "__main__":
    #
    mySuite = suiteReadWriteTests()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
