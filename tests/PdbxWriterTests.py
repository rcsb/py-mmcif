##
# File:    PdbxWriterTests.py
# Author:  jdw
# Date:    2-Oct-2017
# Version: 0.001
#
# Update:
##
"""
Test implementing PDBx/mmCIF write and formatting operations.

"""
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
from mmcif.api.PdbxContainers import DataContainer


class PdbxWriterTests(unittest.TestCase):

    def setUp(self):
        self.lfh = sys.stderr
        self.verbose = False
        #
        self.__pathPdbxDataFile = os.path.join(HERE, "data", "1kip.cif")
        self.__pathBigPdbxDataFile = os.path.join(HERE, "data", "1ffk.cif")
        self.__pathOutputFile1 = os.path.join(HERE, "test-output", "testOutputDataFile.cif")
        self.__pathOutputFile2 = os.path.join(HERE, "test-output", "testOutputDataFile.cif")
        #
        self.__startTime = time.time()
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)\n" % (self.id(),
                                                              time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                              endTime - self.__startTime))

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
            aCat.append((1, 2, 3, 4, '55555555555555555555555555555555555555555555', 6, 7))
            aCat.append((1, 2, 3, 4, '5555', 6, 7))
            aCat.append((1, 2, 3, 4, '5555555555', 6, 7))
            aCat.append((1, 2, 3, 4, '5', 6, 7))
            curContainer.append(aCat)
            myDataList.append(curContainer)
            with open(self.__pathOutputFile1, "w") as ofh:
                pdbxW = PdbxWriter(ofh)
                pdbxW.setAlignmentFlag(flag=True)
                pdbxW.write(myDataList)
            self.assertEqual(len(myDataList), 1)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testUpdateDataFile(self):
        """Test case -  write data file
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
            aCat.append((1, 2, 3, 4, 5, 6, 7))
            aCat.append((1, 2, 3, 4, 5, 6, 7))
            aCat.append((1, 2, 3, 4, 5, 6, 7))
            aCat.append((1, 2, 3, 4, 5, 6, 7))
            curContainer.append(aCat)
            myDataList.append(curContainer)
            with open(self.__pathOutputFile1, "w") as ofh:
                pdbxW = PdbxWriter(ofh)
                pdbxW.write(myDataList)
            #
            # Read and update the data -
            #
            myDataList = []
            with open(self.__pathOutputFile1, "r") as ifh:
                pRd = PdbxReader(ifh)
                pRd.read(myDataList)
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
            self.assertEqual(len(myDataList), 1)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testReadWriteDataFile(self):
        """Test case -  data file read write test
        """

        try:
            #
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


def writerSuite():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(PdbxWriterTests("testWriteDataFile"))
    suiteSelect.addTest(PdbxWriterTests("testUpdateDataFile"))
    suiteSelect.addTest(PdbxWriterTests("testReadWriteDataFile"))
    return suiteSelect


if __name__ == '__main__':
    if (True):
        mySuite = writerSuite()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
    #
