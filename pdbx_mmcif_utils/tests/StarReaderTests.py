##
# File:    StarReaderTests.py
# Author:  jdw
# Date:    7-Oct-2014
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
import sys
import time
import os
import os.path
import json

from pdbx_v2.adapter.IoAdapterPy import IoAdapterPy
from pdbx_v2.reader.PdbxContainers import *
from pdbx_v2.reader.DataCategory import DataCategory


class StarReaderTests(unittest.TestCase):

    def setUp(self):
        self.__lfh = sys.stdout
        self.__verbose = False
        # self.__pathStarFile="../tests/D_2000000000_cs_P1.str"
        self.__pathStarFileList = ["../tests/D_2000000000_cs_P1.str"]
        # self.__pathStarFileList=["../tests/CCPN_CASD155.nef","../tests/CCPN_CASD179.nef","../tests/CCPN_H1GI.nef","../tests/CCPN_H1GI_alt.nef"]

    def tearDown(self):
        pass

    def testReadStarFile(self):
        """Test case -  read star file -
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__,
                                                       sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            for fp in self.__pathStarFileList:
                myIo = IoAdapterPy(self.__verbose, self.__lfh)
                self.__containerList = myIo.readFile(inputFile=fp)
                self.__lfh.write("container list is  %r\n" % ([(c.getName(), c.getType()) for c in self.__containerList]))
                for c in self.__containerList:
                    c.setType('data')
                dir, fnOut = os.path.split(fp)
                myIo.writeFile(outputFile=fnOut + ".cif", containerList=self.__containerList[1:])
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))

    def testReadWriteStarFile(self):
        """Test case -  read and write the ...
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__,
                                                       sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

        try:
            for fp in self.__pathStarFileList:
                myIo = IoAdapterPy(self.__verbose, self.__lfh)
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
                            self.__lfh.write("Duplicate data block %s\n" % container.getName())
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
                        self.__lfh.write("Attribute list %s\n" % aL)
                        rowL = catObj.getRowList()
                        for ii, row in enumerate(rowL):
                            self.__lfh.write("  %4d  %r\n" % (ii, row))
                dir, fnOut = os.path.split(fp)
                myIo.writeFile(outputFile=fnOut + ".out", containerList=self.__containerList, useStopTokens=True)
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))


def suiteStarReaderTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(StarReaderTests("testReadStarFile"))
    suiteSelect.addTest(StarReaderTests("testReadWriteStarFile"))
    return suiteSelect


if __name__ == '__main__':
    if (True):
        mySuite = suiteStarReaderTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
