##
#
# File:    PdbxDictionaryAccessTests.py
# Author:  jdw
# Date:    12-October-2011
# Version: 0.001
#
# Updates:
#
# 2012-01-16 jdw Refactor writer module
# 2012-08-30 jdw Tests for alternate meta data -
# 2012-10-23 jdw Recheck and update test paths
##
"""
Test cases for dictionary access methods -- 

"""
from __future__ import absolute_import
__docformat__ = "restructuredtext en"
__author__    = "John Westbrook"
__email__     = "jwest@rcsb.rutgers.edu"
__license__   = "Creative Commons Attribution 3.0 Unported"
__version__   = "V0.01"

import sys, unittest, traceback
import sys, time, os, os.path, shutil

from pdbx_v2.reader.PdbxBuild  import PdbxBuild


class PdbxDictAccessTests(unittest.TestCase):

    def setUp(self):
        self.lfh=sys.stdout
        self.verbose=False
        self.pathPdbxDictionary     = "../tests/mmcif_pdbx_w_methods.dic"
        self.pathPdbxDataFile       = "../tests/1kip.cif"
        self.pathBigPdbxDataFile    = "../tests/1ffk.cif"
        self.pathPdbxDictionaryV5   = "../tests/mmcif_pdbx_v5_next.dic"       

    def tearDown(self):
        pass

    def xtestReadDictionary(self): 
        """Test case -  read and dump logical structure of dictionary
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            myBuild=PdbxBuild(self.verbose)
            myDict=myBuild.readDictionary(self.pathPdbxDictionary)
            fh = open("dumpDictionary.out",'w')            
            myBuild.dumpDictionary(fh)
            fh.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

    def xtestReadWriteDictionary(self): 
        """Test case -  read/write test for dictionary
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            #
            myBuild=PdbxBuild(self.verbose)
            myDict=myBuild.readDictionary(self.pathPdbxDictionary)
            myDict=myBuild.writeDictionary("dictDump.dic")
            
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
            myBuild=PdbxBuild(self.verbose)
            myDict=myBuild.readDictionary(self.pathPdbxDictionary)
            myData=myBuild.readDataFile(self.pathPdbxDataFile)
            fh = open("dumpFile.out",'w')
            myBuild.dumpMethods(fh)
            dApi=myBuild.getDictionary()
            if (dApi is not None):
                dApi.dumpCategoryIndex(fh)
                dApi.dumpFeatures(fh)
            fh.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()


    def testDumpDictionaryContentsAlt(self): 
        """Test case -  alternate data attributes 
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            #
            #
            myBuild=PdbxBuild(self.verbose)
            myDict=myBuild.readDictionary(self.pathPdbxDictionaryV5)
            fh = open("dumpFileV5.out",'w')
            myBuild.dumpMethods(fh)
            dApi=myBuild.getDictionary()
            if (dApi is not None):
                dApi.dumpCategoryIndex(fh)
                dApi.dumpFeatures(fh)
            fh.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()


    def xtestDumpDictionaryContents(self): 
        """Test case -  output everything - 
        """
        self.lfh.write("\nStarting %s %s\n" % (self.__class__.__name__,
                                               sys._getframe().f_code.co_name))
        try:
            #
            myBuild=PdbxBuild(self.verbose)
            myDict=myBuild.readDictionary(self.pathPdbxDictionary)
            dApi=myBuild.getDictionary()
            if (dApi is not None):
                bL=dApi.getBoundaryList('chemical_conn_atom','charge')
                self.lfh.write('boundary list = %r\n' % bL)
                #dApi.dumpCategoryIndex(fh)
                #dApi.dumpFeatures(fh)
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

def suiteDictAccessTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(PdbxDictAccessTests("testDumpDictionaryContents"))
    suiteSelect.addTest(PdbxDictAccessTests("testDumpDictionaryContentsAlt"))
    return suiteSelect        


if __name__ == '__main__':
    #unittest.main()
    mySuite=suiteDictAccessTests()
    unittest.TextTestRunner(verbosity=2).run(mySuite)  
