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

import logging
import os
import os.path
import sys
import time
import unittest

from mmcif.io.PdbxReader import PdbxReader

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

try:
    from mmcif import __version__
except ImportError:
    sys.path.insert(0, TOPDIR)
    from mmcif import __version__


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
        logger.debug("Running tests on version %s", __version__)
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

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
            logger.exception("Failing with %s", str(e))
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
            logger.exception("Failing with %s", str(e))
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

            # nRows = catObj.getRowCount()
            #
            # Get column name index.
            #
            itDict = {}
            itNameList = catObj.getItemNameList()
            for idxIt, itName in enumerate(itNameList):
                itDict[str(itName).lower()] = idxIt
                #
            idf = itDict["_refln.f_meas_au"]
            idsigf = itDict["_refln.f_meas_sigma_au"]
            minR = 100
            maxR = -1
            sumR = 0
            icount = 0
            for row in catObj.getRowList():
                try:
                    fV = float(row[idf])
                    sigf = float(row[idsigf])
                    ratio = sigf / fV
                    # self.lfh.write(" %f %f %f\n" % (f,sigf,ratio))
                    maxR = max(maxR, ratio)
                    minR = min(minR, ratio)
                    sumR += ratio
                    icount += 1
                except Exception:
                    continue

            ifh.close()
            logger.debug("f/sig(f) min %f max %f avg %f count %d", minR, maxR, sumR / icount, icount)
            self.assertEqual(icount, 99242)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
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


if __name__ == "__main__":

    mySuite = simpleSuite()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
    #

    mySuite = sfSuite()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
