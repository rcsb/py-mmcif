##
# File:    StarReaderTests.py
# Author:  jdw
# Date:    5-Oct-2017
# Version: 0.001
##
"""
Test cases for simple star file reader/writer  --

"""
from __future__ import absolute_import
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import sys
import unittest
import traceback

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

# from mmcif.api.PdbxContainers import *
# from mmcif.api.DataCategory import DataCategory
from mmcif.io.IoAdapterPy import IoAdapterPy as IoAdapter


class StarReaderTests(unittest.TestCase):

    def setUp(self):
        self.__lfh = sys.stdout
        self.__verbose = False
        self.__pathStarFileList = [os.path.join(HERE, "data", "chemical_shifts_example.str"), os.path.join(HERE, "data", "CCPN_H1GI.nef")]
        self.__startTime = time.time()
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)\n" % (self.id(),
                                                              time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                              endTime - self.__startTime))

    def testReadStarFile(self):
        """Test case -  read star file -
        """
        try:
            for fp in self.__pathStarFileList:
                myIo = IoAdapter(self.__verbose, self.__lfh)
                self.__containerList = myIo.readFile(inputFile=fp)
                logger.debug("container list is  %r\n" % ([(c.getName(), c.getType()) for c in self.__containerList]))
                for c in self.__containerList:
                    c.setType('data')
                dir, fnOut = os.path.split(fp)
                ok = myIo.writeFile(outputFile=fnOut + ".cif", containerList=self.__containerList[1:])
                self.assertEqual(ok, True)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testReadWriteStarFile(self):
        """Test case -  star file read and write  ...
        """
        try:
            for fp in self.__pathStarFileList:
                myIo = IoAdapter(self.__verbose, self.__lfh)
                self.__containerList = myIo.readFile(inputFile=fp)
                #
                # containerList is a flat list of containers in the order parsed.
                #
                # Create an index from the linear list data_ save_ sections and names --
                #
                # There can multiple data blocks where each data section is followed
                # by save frames --    Names can be repeated and the application must
                # create an appropriate index of the data and save sections according
                # it own requirements.
                #
                #
                iD = {}
                iDN = {}
                dL = []
                for container in self.__containerList:
                    if container.getType() == "data":
                        dL.append(container)
                        if container.getName() not in iD:
                            curContainerName = container.getName()
                            iD[curContainerName] = []
                            iDN[curContainerName] = []
                        else:
                            logger.debug("Duplicate data block %s\n" % container.getName())
                    else:
                        iD[curContainerName].append(container)
                        iDN[curContainerName].append(container.getName())
                #
                # get the reference data out of the 2nd  data block --
                #
                if len(dL) > 1:
                    c1 = dL[1]
                    if 'chemical_shift_reference_1' in iDN[c1.getName()]:
                        idx = iDN[c1.getName()].index('chemical_shift_reference_1')
                        sf0 = iD[c1.getName()][idx]
                        catObj = sf0.getObj('Chem_shift_ref')
                        aL = catObj.getAttributeList()
                        rowL = catObj.getRowList()
                        logger.debug("Attribute list %s\n" % aL)
                        rowL = catObj.getRowList()
                        for ii, row in enumerate(rowL):
                            logger.debug("  %4d  %r\n" % (ii, row))
                dir, fnOut = os.path.split(fp)
                ok = myIo.writeFile(outputFile=fnOut + ".out", containerList=self.__containerList, useStopTokens=True)
                self.assertEqual(ok, True)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()


def suiteStarReaderTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(StarReaderTests("testReadStarFile"))
    suiteSelect.addTest(StarReaderTests("testReadWriteStarFile"))
    return suiteSelect


if __name__ == '__main__':
    if (True):
        mySuite = suiteStarReaderTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
