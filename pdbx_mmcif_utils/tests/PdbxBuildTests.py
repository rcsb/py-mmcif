##
#
# File:    PdbxBuildTests.py
# Author:  jdw
# Date:    12-October-2009
# Version: 0.001
##
"""
Test cases for dictionary and data file access and construction including dictionary methods.

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

from pdbx_v2.reader.PdbxBuild import PdbxBuild


class PdbxBuildTests(unittest.TestCase):

    def setUp(self):
        self.lfh = sys.stdout
        self.verbose = True
        self.pathPdbxDictionary = "../tests/mmcif_pdbx_w_methods.dic"
        self.pathPdbxV40Dictionary = "../tests/mmcif_pdbx_v40.dic"
        self.pathPdbxDataFile = "../tests/1kip.cif"
        self.pathBigPdbxDataFile = "../tests/1ffk.cif"

    def tearDown(self):
        pass

    def testReadDictionary(self):
        """Test case -  read and dump logical structure of dictionary
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            myBuild = PdbxBuild(self.verbose)
            myDict = myBuild.readDictionary(self.pathPdbxDictionary)
            fh = open("dumpDictionary.out", 'w')
            myBuild.dumpDictionary(fh)
            fh.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

    def testReadDataFile(self):
        """Test case -  read and dump logical structure of data file
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            #
            myBuild = PdbxBuild(self.verbose)
            myDict = myBuild.readDataFile(self.pathPdbxDataFile)
            fh = open("dumpDataFile.out", 'w')
            myBuild.dumpDataFile(fh)
            fh.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

    def testReadBigDataFile(self):
        """Test case -  read and dump logical structure of data file
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            #
            myBuild = PdbxBuild(self.verbose)
            myDict = myBuild.readDataFile(self.pathBigPdbxDataFile)
            fh = open("dumpDataFile.out", 'w')
            myBuild.dumpDataFile(fh)
            fh.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

    def testReadWriteDictionary(self):
        """Test case -  read/write test for dictionary
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            #
            myBuild = PdbxBuild(self.verbose)
            myDict = myBuild.readDictionary(self.pathPdbxDictionary)
            myDict = myBuild.writeDictionary("dictDump.dic")

        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

    def testReadWriteDataFile(self):
        """Test case -  read/write test for data file
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            #
            myBuild = PdbxBuild(self.verbose)
            myData = myBuild.readDataFile(self.pathPdbxDataFile)
            myData = myBuild.writeDataFile("fileDump.cif")
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

    def testReadDictionaryMethods(self):
        """Test case -  read dictionary methods -
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            #
            myBuild = PdbxBuild(self.verbose)
            myDict = myBuild.readDictionary(self.pathPdbxDictionary)
            fh = open("dumpMethods.out", 'w')
            myBuild.dumpMethods(fh)
            fh.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

    def testInvokeDictionaryMethods(self):
        """Test case -  invoke dictionary methods -
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            #
            # myBuild=PdbxBuild(self.verbose)
            myBuild = PdbxBuild(True)
            myDict = myBuild.readDictionary(self.pathPdbxDictionary)
            myData = myBuild.readDataFile(self.pathPdbxDataFile)
            myBuild.invokeMethods()
            myBuild.writeDataFile("fileDumpMethods.cif")
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

    def testADumpDictionaryEnums(self):
        """Test case -  read and dump enums in dictionary
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            myBuild = PdbxBuild(self.verbose)
            myDict = myBuild.readDictionary(self.pathPdbxV40Dictionary)
            fh = open("dumpEnums.out", 'w')
            dApi = myBuild.getDictionary()
            dApi.dumpEnumFeatures(fh)
            fh.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

    def testDumpDictionaryContents(self):
        """Test case -  output everything -
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            #
            #
            myBuild = PdbxBuild(self.verbose)
            myDict = myBuild.readDictionary(self.pathPdbxDictionary)
            myData = myBuild.readDataFile(self.pathPdbxDataFile)
            fh = open("dumpFile.out", 'w')
            myBuild.dumpMethods(fh)
            dApi = myBuild.getDictionary()
            if (dApi is not None):
                dApi.dumpCategoryIndex(fh)
                dApi.dumpFeatures(fh)
            fh.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()


def suiteBuildTests():
    suiteSelect = unittest.TestSuite()
    if False:
        suiteSelect.addTest(PdbxBuildTests("testADumpDictionaryEnums"))
        suiteSelect.addTest(PdbxBuildTests("testDumpDictionaryContents"))
        suiteSelect.addTest(PdbxBuildTests("testReadDictionaryMethods"))
        suiteSelect.addTest(PdbxBuildTests("testReadWriteDataFile"))
        suiteSelect.addTest(PdbxBuildTests("testReadWriteDictionary"))
        suiteSelect.addTest(PdbxBuildTests("testReadBigDataFile"))
        suiteSelect.addTest(PdbxBuildTests("testReadDataFile"))
        suiteSelect.addTest(PdbxBuildTests("testReadDictionary"))
    #
    suiteSelect.addTest(PdbxBuildTests("testInvokeDictionaryMethods"))


    return suiteSelect


if __name__ == '__main__':
    # unittest.main()
    mySuite = suiteBuildTests()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
