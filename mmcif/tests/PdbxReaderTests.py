##
# File:    PdbxReaderTests.py
# Author:  jdw
# Date:    3-Oct-2017
# Version: 0.001
#
# Update:
#
##
"""
Test cases for reading PDBx/mmCIF data files PdbxReader class -

"""
from __future__ import absolute_import
import sys
import unittest
import time
import os
import os.path

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

try:
    from mmcif import __version__
except Exception as e:
    sys.path.insert(0, TOPDIR)
    from mmcif import __version__


from mmcif.io.PdbxReader import PdbxReader

# from mmcif.api.PdbxContainers import *


class PdbxReaderTests(unittest.TestCase):

    def setUp(self):
        self.lfh = sys.stderr
        self.verbose = False
        #
        self.__pathPdbxDataFile = os.path.join(HERE, "data", "1kip.cif")
        self.__pathBigPdbxDataFile = os.path.join(HERE, "data", "1ffk.cif")
        self.__pathSFDataFile = os.path.join(HERE, "data", "example_sf.cif")
        #
        #
        self.__startTime = time.time()
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)\n" % (self.id(),
                                                              time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                              endTime - self.__startTime))

    def testReadSmallDataFile(self):
        """Test case -  read data file
        """
        try:
            #
            myDataList = []
            ifh = open(self.__pathPdbxDataFile, "r")
            pRd = PdbxReader(ifh)
            pRd.read(myDataList)
            ifh.close()
            #
            self.assertEqual(len(myDataList), 1)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testReadBigDataFile(self):
        """Test case -  read large data file
        """
        try:
            #
            myDataList = []
            ifh = open(self.__pathBigPdbxDataFile, "r")
            pRd = PdbxReader(ifh)
            pRd.read(myDataList)
            ifh.close()
            self.assertEqual(len(myDataList), 1)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testReadSFDataFile(self):
        """Test case -  read PDB structure factor data  file and compute statistics on f/sig(f).
        """
        try:
            #
            myContainerList = []
            ifh = open(self.__pathSFDataFile, "r")
            pRd = PdbxReader(ifh)
            pRd.read(myContainerList)
            c0 = myContainerList[0]
            #
            catObj = c0.getObj("refln")
            if catObj is None:
                return False

            nRows = catObj.getRowCount()
            #
            # Get column name index.
            #
            itDict = {}
            itNameList = catObj.getItemNameList()
            for idxIt, itName in enumerate(itNameList):
                itDict[str(itName).lower()] = idxIt
                #
            idf = itDict['_refln.f_meas_au']
            idsigf = itDict['_refln.f_meas_sigma_au']
            minR = 100
            maxR = -1
            sumR = 0
            icount = 0
            for row in catObj.getRowList():
                try:
                    f = float(row[idf])
                    sigf = float(row[idsigf])
                    ratio = sigf / f
                    #self.lfh.write(" %f %f %f\n" % (f,sigf,ratio))
                    maxR = max(maxR, ratio)
                    minR = min(minR, ratio)
                    sumR += ratio
                    icount += 1
                except:
                    continue

            ifh.close()
            logger.debug("f/sig(f) min %f max %f avg %f count %d\n" % (minR, maxR, sumR / icount, icount))
            self.assertEqual(icount, 99242)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()


def sfSuite():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(PdbxReaderTests("testReadSFDataFile"))
    return suiteSelect


def simpleSuite():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(PdbxReaderTests("testReadSmallDataFile"))
    suiteSelect.addTest(PdbxReaderTests("testReadBigDataFile"))
    return suiteSelect

if __name__ == '__main__':
    if (True):
        mySuite = simpleSuite()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
    #
    if (True):
        mySuite = sfSuite()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
