##
# File:    PdbxReadWriteTests.py
# Author:  jdw
# Date:    3-Oct-2017
# Version: 0.001
#
# Updated:
#
##
"""  Various tests cases for PDBx/mmCIF data file and dictionary reader and writer.
"""

from __future__ import absolute_import

from six.moves import range
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import sys
import unittest
import time
import os
import os.path


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    from mmcif import __version__
except Exception as e:
    sys.path.insert(0, os.path.dirname(HERE))
    from mmcif import __version__


from mmcif.io.PdbxReader import PdbxReader
from mmcif.io.PdbxWriter import PdbxWriter
from mmcif.api.DataCategory import DataCategory
from mmcif.api.DataCategoryBase import DataCategoryBase
from mmcif.api.PdbxContainers import DataContainer


class PdbxReadWriteTests(unittest.TestCase):

    def setUp(self):
        self.lfh = sys.stdout
        self.verbose = False
        #
        self.__pathPdbxDataFile = os.path.join(HERE, "data", "specialTestFile.cif")
        self.__pathBigPdbxDataFile = os.path.join(HERE, "data", "1ffk.cif")

        self.__pathOutputFile1 = os.path.join(HERE, "test-output", "testOutputDataFile1.cif")
        self.__pathOutputFile2 = os.path.join(HERE, "test-output", "testOutputDataFile2.cif")
        self.__pathOutputFile3 = os.path.join(HERE, "test-output", "testOutputDataFileStopToken3.cif")
        #
        self.__pathTestFile = os.path.join(HERE, "data", "testSingleRow.cif")
        self.__pathTestFileStop = os.path.join(HERE, "data", "testFileWithStopTokens.cif")
        #
        self.__startTime = time.time()
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)\n" % (self.id(),
                                                              time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                              endTime - self.__startTime))

    def testSingleRow(self):
        """Test case -  read /write single row and null row in data file
        """
        try:
            #
            myDataList = []
            #ofh = open(self.__pathOutputFile1, "w")
            curContainer = DataContainer("myblock")
            aCat = DataCategory("pdbx_seqtool_mapping_ref")
            aCat.appendAttribute("ordinal")
            aCat.appendAttribute("entity_id")
            aCat.appendAttribute("auth_mon_id")
            aCat.appendAttribute("auth_mon_num")
            aCat.appendAttribute("pdb_chain_id")
            aCat.appendAttribute("ref_mon_id")
            aCat.appendAttribute("ref_mon_num")
            aCat.appendAttribute("details")
            aCat.append([1, 2, 3, 4, 5, 6, 7, 'data_my_big_data_file'])
            aCat.append([1, 2, 3, 4, 5, 6, 7, 'loop_my_big_data_loop'])
            aCat.append([1, 2, 3, 4, 5, 6, 7, 'save_my_big_data_saveframe'])
            aCat.append([1, 2, 3, 4, 5, 6, 7, '_category.item'])
            # aCat.dumpIt()
            curContainer.append(aCat)
            #
            bCat = curContainer.getObj("pdbx_seqtool_mapping_ref")
            logger.debug("----attribute list %r\n" % bCat.getAttributeList())
            row = bCat.getRow(0)
            logger.debug("----ROW %r\n" % row)
            #
            with open(self.__pathOutputFile2, "w") as ofh:
                myDataList.append(curContainer)
                pdbxW = PdbxWriter(ofh)
                pdbxW.write(myDataList)

            self.assertEqual(len(myDataList), 1)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testSingleRowFile(self):
        """Test case -  read /write single row and null row in data file
        """
        try:
            #
            myDataList = []
            ifh = open(self.__pathTestFile, "r")
            pRd = PdbxReader(ifh)
            pRd.read(myDataList)
            ifh.close()

            myBlock = myDataList[0]
            myCat = myBlock.getObj('symmetry')
            logger.debug("----attribute list %r\n" % myCat.getAttributeList())
            row = myCat.getRow(0)
            logger.debug("----ROW %r\n" % row)
            #
            # myCat.dumpIt()

            with open(self.__pathOutputFile2, "w") as ofh:
                pdbxW = PdbxWriter(ofh)
                pdbxW.write(myDataList)

            self.assertEqual(len(myDataList), 1)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testSimpleInitialization(self):
        """Test case -  Simple initialization of a data category and data block
        """
        try:
            #
            fn = self.__pathOutputFile1
            attributeNameList = ['aOne', 'aTwo', 'aThree', 'aFour', 'aFive', 'aSix', 'aSeven', 'aEight', 'aNine', 'aTen']
            rowList = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                       ]
            nameCat = 'myCategory'
            #
            #
            curContainer = DataContainer("myblock")
            aCat = DataCategory(nameCat, attributeNameList, rowList)
            # aCat.printIt()
            curContainer.append(aCat)
            # curContainer.printIt()
            #
            myContainerList = []
            myContainerList.append(curContainer)
            ofh = open(fn, "w")
            pdbxW = PdbxWriter(ofh)
            pdbxW.write(myContainerList)
            ofh.close()

            myContainerList = []
            ifh = open(fn, "r")
            pRd = PdbxReader(ifh)
            pRd.read(myContainerList)
            ifh.close()
            for container in myContainerList:
                for objName in container.getObjNameList():
                    name, aList, rList = container.getObj(objName).get()
                    logger.debug("Recovered data category  %s\n" % name)
                    logger.debug("Attribute list           %r\n" % repr(aList))
                    logger.debug("Row list                 %r\n" % repr(rList))
            self.assertEqual(len(myContainerList), 1)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testWriteDataFile(self):
        """Test case -  write data file
        """
        try:
            #
            myDataList = []
            curContainer = DataContainer("myblock")
            aCat = DataCategory("pdbx_seqtool_mapping_ref")
            aCat.appendAttribute("ordinal")
            aCat.appendAttribute("entity_id")
            aCat.appendAttribute("auth_mon_id")
            aCat.appendAttribute("auth_mon_num")
            aCat.appendAttribute("pdb_chain_id")
            aCat.appendAttribute("ref_mon_id")
            aCat.appendAttribute("ref_mon_num")
            aCat.append([1, 2, 3, 4, 5, 6, 7])
            aCat.append([1, 2, 3, 4, 5, 6, 7])
            aCat.append([1, 2, 3, 4, 5, 6, 7])
            aCat.append([1, 2, 3, 4, 5, 6, 7])
            aCat.append([7, 6, 5, 4, 3, 2, 1])
            # aCat.printIt()
            curContainer.append(aCat)
            # curContainer.printIt()
            #
            myDataList.append(curContainer)
            with open(self.__pathOutputFile1, "w") as ofh:
                pdbxW = PdbxWriter(ofh)
                pdbxW.write(myDataList)
            self.assertEqual(len(myDataList), 1)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testUpdateDataFile(self):
        """Test case -  update data file
        """
        try:
            # Create a initial data file --
            #
            myDataList = []

            curContainer = DataContainer("myblock")
            aCat = DataCategory("pdbx_seqtool_mapping_ref")
            aCat.appendAttribute("ordinal")
            aCat.appendAttribute("entity_id")
            aCat.appendAttribute("auth_mon_id")
            aCat.appendAttribute("auth_mon_num")
            aCat.appendAttribute("pdb_chain_id")
            aCat.appendAttribute("ref_mon_id")
            aCat.appendAttribute("ref_mon_num")
            aCat.append([9, 2, 3, 4, 5, 6, 7])
            aCat.append([10, 2, 3, 4, 5, 6, 7])
            aCat.append([11, 2, 3, 4, 5, 6, 7])
            aCat.append([12, 2, 3, 4, 5, 6, 7])

            curContainer.append(aCat)
            myDataList.append(curContainer)
            ofh = open(self.__pathOutputFile1, "w")
            pdbxW = PdbxWriter(ofh)
            pdbxW.write(myDataList)
            ofh.close()
            #
            #
            # Read and update the data -
            #
            myDataList = []
            ifh = open(self.__pathOutputFile1, "r")
            pRd = PdbxReader(ifh)
            pRd.read(myDataList)
            ifh.close()
            #
            myBlock = myDataList[0]
            # myBlock.printIt()
            myCat = myBlock.getObj('pdbx_seqtool_mapping_ref')
            # myCat.printIt()
            for iRow in range(0, myCat.getRowCount()):
                myCat.setValue('some value', 'ref_mon_id', iRow)
                myCat.setValue(100, 'ref_mon_num', iRow)
            with open(self.__pathOutputFile2, "w") as ofh:
                pdbxW = PdbxWriter(ofh)
                pdbxW.write(myDataList)

            #
            self.assertEqual(len(myDataList), 1)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testReadDataFile(self):
        """Test case -  read data file
        """
        try:
            #
            myDataList = []
            ifh = open(self.__pathPdbxDataFile, "r")
            pRd = PdbxReader(ifh)
            pRd.read(myDataList)
            ifh.close()
            self.assertEqual(len(myDataList), 1)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testReadWriteDataFile(self):
        """Test case -  data file read write test
        """
        try:
            myDataList = []
            with open(self.__pathPdbxDataFile, "r") as ifh:
                pRd = PdbxReader(ifh)
                pRd.read(myDataList)

            with open(self.__pathOutputFile1, "w") as ofh:
                pWr = PdbxWriter(ofh)
                pWr.write(myDataList)
            self.assertEqual(len(myDataList), 1)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testReadWriteListAccessors(self):
        """Test cases -  for list style data access.
        """
        try:
            dc = DataCategoryBase('test', attributeNameList=['a', 'b', 'c', 'd'])

            dc.append([1, 2, 3, 4])
            dc.append([1, 2, 3, 4])
            dc.append([1, 2, 3, 4])
            dc.append([1, 2, 3, 4, 5, 6, 7])
            dc.append([1, 2, 3, 4])

            dc.insert(0, [4, 3, 2, 1])

            logger.debug("Full  %r\n" % dc)
            logger.debug("slice %r\n" % dc[2:4])
            logger.debug("last  %r\n" % dc[-1])

            for r in dc:
                logger.debug("row data %r\n" % r)

            dc.setMapping('ATTRIBUTE')
            for r in dc:
                logger.debug("row attrib dict %r\n" % r)

            dc.setMapping('ITEM')
            for r in dc:
                logger.debug("row item dict %r\n" % r)

            dc.setMapping('DATA')

            logger.debug("row 3 %r\n" % dc[3])
            tmp = dc[3]
            dc[3] = []
            logger.debug("row 3 %r\n" % dc[3])
            dc[3] = tmp
            logger.debug("row 3 %r\n" % dc[3])

            dc.setMapping('ATTRIBUTE')
            tmp = dc[3]

            dt = {}
            for k, v in tmp.items():
                dt[k] = 10000
            logger.debug("row dict %r\n" % dt)

            dc[3] = dt
            logger.debug("row 3%r\n" % dc[3])
            dc[3] = tmp

            dc.setMapping('ITEM')
            tmp = dc[3]

            dt = {}
            for k, v in tmp.items():
                dt[k] = 10001
            logger.debug("row dict %r\n" % dt)

            dc[3] = dt
            logger.debug("row 3 %r\n" % dc[3])

            logger.debug("print raw     %r\n" % dc)
            logger.debug("print string  %s\n" % dc)
            self.assertEqual(1, 1)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testUpdateAttribute(self):
        """Test case -  udpdate entry_id
        """
        ifn = self.__pathBigPdbxDataFile
        ofn = self.__pathOutputFile2
        try:
            #
            myContainerList = []
            with open(ifn, "r") as ifh:
                pRd = PdbxReader(ifh)
                pRd.read(myContainerList)
            #
            dsId = "D_000000"
            atName = 'entry_id'
            for container in myContainerList:
                container.setName(dsId)
                # remove category citation
                container.remove('citation')
                for objName in container.getObjNameList():
                    dcObj = container.getObj(objName)
                    if dcObj.hasAttribute(atName):
                        for iRow in range(0, dcObj.getRowCount()):
                            dcObj.setValue(dsId, attributeName=atName, rowIndex=iRow)
                    elif objName.lower() == 'entry':
                        dcObj.setValue(dsId, attributeName='id', rowIndex=0)

            #
            with open(ofn, "w") as ofh:
                pWr = PdbxWriter(ofh)
                pWr.write(myContainerList)
            self.assertEqual(len(myContainerList), 1)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testReadWriteDataFileStop(self):
        """Test case -  data file read write test with stop tokens
        """
        try:
            myDataList = []
            with open(self.__pathTestFileStop, "r") as ifh:
                pRd = PdbxReader(ifh)
                pRd.read(myDataList)

            with open(self.__pathOutputFile3, "w") as ofh:
                pWr = PdbxWriter(ofh)
                pWr.write(myDataList)
            self.assertEqual(len(myDataList), 1)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()


def simpleSuite():
    suiteSelect = unittest.TestSuite()
    # suiteSelect.addTest(PdbxReadWriteTests("testWriteDataFile"))
    suiteSelect.addTest(PdbxReadWriteTests("testUpdateDataFile"))
    return suiteSelect


def simpleSuite2():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(PdbxReadWriteTests("testReadWriteDataFile"))
    return suiteSelect


def simpleSuite3():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(PdbxReadWriteTests("testSingleRow"))
    suiteSelect.addTest(PdbxReadWriteTests("testSingleRowFile"))
    suiteSelect.addTest(PdbxReadWriteTests("testReadWriteListAccessors"))

    return suiteSelect


def quotingCasesSuite():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(PdbxReadWriteTests("testReadWriteDataFile"))
    return suiteSelect


def attributeUpdateSuite():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(PdbxReadWriteTests("testUpdateAttribute"))
    return suiteSelect


def suiteReadWithStopTokens():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(PdbxReadWriteTests("testReadWriteDataFileStop"))
    return suiteSelect


if __name__ == '__main__':
    #
    if (True):
        mySuite = simpleSuite()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
        #
        mySuite = simpleSuite2()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
        #
        mySuite = simpleSuite3()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
        #
        mySuite = quotingCasesSuite()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

        mySuite = attributeUpdateSuite()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

        mySuite = suiteReadWithStopTokens()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
