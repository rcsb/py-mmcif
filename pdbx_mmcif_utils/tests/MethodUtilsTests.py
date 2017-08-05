##
#
# File:    MethodUtilsTests.py
# Author:  jdw
# Date:    12-Aug-2013 jdw
# Version: 0.001
##
"""
Test cases for dictionary method management and invocation.

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
import shutil

from pdbx_v2.dictionary.MethodUtils import MethodUtils
from pdbx_v2.adapter.IoAdapterPy import IoAdapterPy


class MethodUtilsTests(unittest.TestCase):

    def setUp(self):
        self.__lfh = sys.stdout
        self.__verbose = False
        self.__pathPdbxDictionary = "../tests/mmcif_pdbx_w_methods.dic"
        self.__pathPdbxV40Dictionary = "../tests/mmcif_pdbx_v40.dic"
        self.__pathPdbxDataFile = "../tests/1kip.cif"
        self.__pathBigPdbxDataFile = "../tests/1ffk.cif"

    def tearDown(self):
        pass

    def testDumpDictionaryMethods(self):
        """Test case -  dump methods for dictionary metadata
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__,
                                                       sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            myIo = IoAdapterPy(self.__verbose, self.__lfh)
            self.__dictContainerList = myIo.readFile(inputFile=self.__pathPdbxDictionary)
            mU = MethodUtils(dictContainerList=self.__dictContainerList, verbose=self.__verbose, log=self.__lfh)
            mU.dumpMethods(fh=self.__lfh)
            mU.dumpDictionary(fh=self.__lfh)

        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))

    def testInvokeDictionaryMethods(self):
        """Test case -  invoke dictionary methods -
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__,
                                                       sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

        try:
            myIo = IoAdapterPy(self.__verbose, self.__lfh)
            self.__dictContainerList = myIo.readFile(inputFile=self.__pathPdbxDictionary)
            self.__dataContainerList = myIo.readFile(inputFile=self.__pathPdbxDataFile)

            #
            mU = MethodUtils(dictContainerList=self.__dictContainerList, verbose=self.__verbose, log=self.__lfh)
            mU.setDataContainerList(dataContainerList=self.__dataContainerList)
            mU.invokeMethods()
            dataContainerList = mU.getDataContainerList()
            myIo.writeFile(outputFile="test-methods.cif", containerList=dataContainerList)
        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))


def suiteMethodUtilsTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(MethodUtilsTests("testDumpDictionaryMethods"))
    suiteSelect.addTest(MethodUtilsTests("testInvokeDictionaryMethods"))
    return suiteSelect


if __name__ == '__main__':
    if (True):
        mySuite = suiteMethodUtilsTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
