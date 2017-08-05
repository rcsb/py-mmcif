##
# File:    DictionaryApiTests.py
# Author:  jdw
# Date:    12-Aug-2013
# Version: 0.001
##
"""
Tests cases for Dictionary API.

"""
from __future__ import absolute_import
from __future__ import print_function
__docformat__ = "restructuredtext en"
__author__    = "John Westbrook"
__email__     = "jwest@rcsb.rutgers.edu"
__license__   = "Creative Commons Attribution 3.0 Unported"
__version__   = "V0.01"

import sys, unittest, traceback
import sys, time, os, os.path, shutil, json

from pdbx_v2.adapter.IoAdapterPy       import IoAdapterPy
from pdbx_v2.dictionary.DictionaryApi  import DictionaryApi
from pdbx_v2.reader.PdbxContainers    import CifName

class DictionaryApiTests(unittest.TestCase):
    def setUp(self):
        self.__lfh=sys.stderr
        self.__verbose=True
        self.__pathMmCifDictionary=   "../tests/mmcif_std.dic"
        self.__pathPdbxDictionary=   "../tests/mmcif_pdbx_w_methods.dic"
        self.__pathPdbxV40Dictionary="../tests/mmcif_pdbx_v40.dic"
        #
        self.__pathPdbxV50Dictionary="../tests/mmcif_pdbx_v5_next.dic"
        self.__pathNmrStarDictionary="../tests/mmcif_nmr-star.dic"
        #self.__pathPdbxDictionary=self.__pathPdbxV50Dictionary
        #self.__pathPdbxDictionary=self.__pathMmCifDictionary
        self.__pathPdbxDictionary=self.__pathNmrStarDictionary

    def tearDown(self):
        pass

    def testDumpEnums(self): 
        """Test case -  to verify enum ordering - 
        """
        startTime=time.clock()        
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__,
                                                       sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            myIo=IoAdapterPy(self.__verbose,self.__lfh)
            self.__containerList=myIo.readFile(inputFile=self.__pathPdbxV50Dictionary)
            dApi=DictionaryApi(containerList=self.__containerList,consolidate=True,verbose=self.__verbose,log=self.__lfh)
            #
            eList=dApi.getEnumListAlt(category="pdbx_audit_support",attribute="country")
            self.__lfh.write("Item %s Enum list sorted  %r\n" % ('country',eList))
            eList=dApi.getEnumListAlt(category="pdbx_audit_support",attribute="country",sortFlag=False)
            self.__lfh.write("Item %s Enum list unsorted  %r\n" % ('country',eList))
            eList=dApi.getEnumListAltWithDetail(category="pdbx_audit_support",attribute="country")
            self.__lfh.write("Item %s Enum with detail list  %r\n" % ('country',eList))
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

        endTime=time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                     sys._getframe().f_code.co_name,
                                                                     time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                     endTime-startTime))

    def testDumpIndex(self): 
        """Test case -  dump methods for dictionary metadata
        """
        startTime=time.clock()        
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__,
                                                       sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            myIo=IoAdapterPy(self.__verbose,self.__lfh)
            self.__containerList=myIo.readFile(inputFile=self.__pathPdbxV50Dictionary)
            dApi=DictionaryApi(containerList=self.__containerList,consolidate=True,verbose=self.__verbose,log=self.__lfh)
            dApi.dumpCategoryIndex(fh=self.__lfh)
            self.__lfh.write("Index = %r\n" %  dApi.getItemNameList('pdbx_nmr_spectral_dim'))
            self.__lfh.write("Index = %r\n" %  dApi.getAttributeNameList('pdbx_nmr_spectral_dim'))
            catIndex = dApi.getCategoryIndex()
            self.__lfh.write("Index = %r\n" %  catIndex['pdbx_nmr_spectral_dim'] )            
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

        endTime=time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                     sys._getframe().f_code.co_name,
                                                                     time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                     endTime-startTime))

    def testDumpDictionary(self): 
        """Test case -  dump methods for dictionary metadata
        """
        startTime=time.clock()        
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__,
                                                       sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            myIo=IoAdapterPy(self.__verbose,self.__lfh)
            self.__containerList=myIo.readFile(inputFile=self.__pathPdbxDictionary)
            dApi=DictionaryApi(containerList=self.__containerList,consolidate=True,verbose=self.__verbose,log=self.__lfh)
            #dApi.dumpCategoryIndex(fh=self.__lfh)
            #dApi.dumpEnumFeatures(fh=self.__lfh)
            #dApi.dumpFeatures(fh=self.__lfh)
            #dApi.dumpMethods(fh=self.__lfh)
            
            self.__lfh.write('+++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
            groupList=dApi.getCategoryGroups()
            self.__lfh.write('groupList %s\n' % groupList)
            for group in groupList:
                self.__lfh.write('Group %s category list %s\n' % (group,dApi.getCategoryGroupCategories(groupName=group)))
                
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

        endTime=time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                     sys._getframe().f_code.co_name,
                                                                     time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                     endTime-startTime))

    def testConsolidateDictionary(self): 
        """Test case -  dump methods for dictionary metadata
        """
        startTime=time.clock()        
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__,
                                                       sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            myIo=IoAdapterPy(self.__verbose,self.__lfh)
            self.__containerList=myIo.readFile(inputFile=self.__pathPdbxDictionary)
            dApi=DictionaryApi(containerList=self.__containerList,consolidate=True,expandItemLinked=False,verbose=self.__verbose,log=self.__lfh)
            for itemName in ['_entity.id','_entity_poly_seq.num','_atom_site.label_asym_id','_struct_asym.id','_chem_comp.id','chem_comp_atom.comp_id','chem_comp_bond.comp_id']:
                categoryName=CifName.categoryPart(itemName)
                attributeName=CifName.attributePart(itemName)
                self.__lfh.write("Full parent list for  %s : %s\n" % (itemName,dApi.getFullParentList(categoryName,attributeName)))
                self.__lfh.write("Full child  list for  %s : %s\n" % (itemName,dApi.getFullChildList(categoryName,attributeName)))
                self.__lfh.write("Ultimate parent for  %s : %s\n" % (itemName,dApi.getUltimateParent(categoryName,attributeName)))                
                self.__lfh.write("Type code for  %s : %s\n" % (itemName,dApi.getTypeCode(categoryName,attributeName)))                

        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

        endTime=time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                     sys._getframe().f_code.co_name,
                                                                     time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                     endTime-startTime))
    def testGetAdjacentCategories(self): 
        """Test case -  
        """
        startTime=time.clock()        
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__,
                                                       sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            myIo=IoAdapterPy(self.__verbose,self.__lfh)
            self.__containerList=myIo.readFile(inputFile=self.__pathPdbxDictionary)
            dApi=DictionaryApi(containerList=self.__containerList,consolidate=True,verbose=self.__verbose,log=self.__lfh)
            cList=dApi.getCategoryList()
            cI={}
            for c in cList:
                chL=dApi.getChildCategories(c)
                pL=dApi.getParentCategories(c)
                for ch in chL:
                    if (ch,c) not in cI:
                        cI[(ch,c)]=1
                    else:
                        cI[(ch,c)]+=1
                for p in pL:
                    if (c,p) not in cI:
                        cI[(c,p)]=1
                    else:
                        cI[(c,p)]+=1
            linkL=[]
            for s,t in cI.keys():
                d={'source': s, 'target': t, 'type': 'link'}
                linkL.append(d)

            print(json.dumps(linkL,sort_keys=True,indent=4, separators=(',', ': ')))
                    
                
        except:
            traceback.print_exc(file=sys.stdout)
            self.fail()

        endTime=time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                     sys._getframe().f_code.co_name,
                                                                     time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                     endTime-startTime))

def suiteIndexTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(DictionaryApiTests("testDumpIndex"))
    return suiteSelect

def suiteDictionaryApiTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(DictionaryApiTests("testDumpDictionary"))
    return suiteSelect


def suiteConsolidateTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(DictionaryApiTests("testConsolidateDictionary"))
    return suiteSelect

def suiteAdjacentTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(DictionaryApiTests("testGetAdjacentCategories"))
    return suiteSelect

def suiteDictionaryApiEnumTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(DictionaryApiTests("testDumpEnums"))
    return suiteSelect

if __name__ == '__main__':
    if (False):
        mySuite=suiteDictionaryApiTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

        mySuite=suiteConsolidateTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

        mySuite=suiteDictionaryApiTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

        mySuite=suiteAdjacentTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

        mySuite=suiteDictionaryApiEnumTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

    mySuite=suiteIndexTests()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
