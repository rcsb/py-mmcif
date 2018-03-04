##
# File:    DictionaryApiTests.py
# Author:  jdw
# Date:    8-Aug-2017
# Version: 0.001
##
"""
Tests cases for Dictionary API.

"""
from __future__ import absolute_import
from __future__ import print_function

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import sys
import unittest
import traceback
import time
import json
import os

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

from mmcif.io.IoAdapterPy import IoAdapterPy as IoAdapter
from mmcif.api.DictionaryApi import DictionaryApi
from mmcif.api.PdbxContainers import CifName


class DictionaryApiTests(unittest.TestCase):

    def setUp(self):
        self.__lfh = sys.stderr
        self.__verbose = False
        # self.__pathMmCifDictionary = "./data/mmcif_std.dic"
        # self.__pathPdbxDictionary = "./data/mmcif_pdbx_w_methods.dic"
        # self.__pathPdbxV40Dictionary = "./data/mmcif_pdbx_v40.dic"
        # self.__pathPdbxV50Dictionary = "./data/mmcif_pdbx_v5_next.dic"
        # self.__pathNmrStarDictionary = "./data/mmcif_nmr-star.dic"
        # self.__pathPdbxDictionary=self.__pathPdbxV50Dictionary
        # self.__pathPdbxDictionary=self.__pathMmCifDictionary
        # self.__pathPdbxDictionary = self.__pathNmrStarDictionary
        self.__pathPdbxV50Dictionary = os.path.join(HERE, "data", "mmcif_pdbx_v5_next.dic")
        self.__pathPdbxDictionary = os.path.join(HERE, "data", "mmcif_pdbx_v5_next.dic")
        self.__startTime = time.time()
        logger.debug("Starting %s at %s" % (self.id(),
                                            time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)\n" % (self.id(),
                                                              time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                              endTime - self.__startTime))

    def testDumpEnums(self):
        """Test case -  to verify enum ordering -
        """

        try:
            myIo = IoAdapter(raiseExceptions=True)
            self.__containerList = myIo.readFile(inputFilePath=self.__pathPdbxV50Dictionary)
            dApi = DictionaryApi(containerList=self.__containerList, consolidate=True, verbose=self.__verbose)
            #
            eList = dApi.getEnumListAlt(category="pdbx_audit_support", attribute="country")
            logger.debug("Item %s Enum list sorted  %r\n" % ('country', eList))
            eList = dApi.getEnumListAlt(category="pdbx_audit_support", attribute="country", sortFlag=False)
            logger.debug("Item %s Enum list unsorted  %r\n" % ('country', eList))
            eList = dApi.getEnumListAltWithDetail(category="pdbx_audit_support", attribute="country")
            logger.debug("Item %s Enum with detail list  %r\n" % ('country', eList))
            self.assertGreater(len(eList), 100)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testDumpIndex(self):
        """Test case -  dump methods for dictionary metadata
        """

        try:
            myIo = IoAdapter(raiseExceptions=True)
            self.__containerList = myIo.readFile(inputFilePath=self.__pathPdbxV50Dictionary)
            dApi = DictionaryApi(containerList=self.__containerList, consolidate=True, verbose=self.__verbose)
            if self.__verbose:
                dApi.dumpCategoryIndex(fh=self.__lfh)
            logger.debug("Index = %r\n" % dApi.getItemNameList('pdbx_nmr_spectral_dim'))
            logger.debug("Index = %r\n" % dApi.getAttributeNameList('pdbx_nmr_spectral_dim'))
            catIndex = dApi.getCategoryIndex()
            logger.debug("Index = %r\n" % catIndex['pdbx_nmr_spectral_dim'])
            self.assertIsNotNone(catIndex['pdbx_nmr_spectral_dim'])
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testDumpDictionary(self):
        """Test case -  dump methods for dictionary metadata
        """

        try:
            myIo = IoAdapter(raiseExceptions=True)
            self.__containerList = myIo.readFile(inputFilePath=self.__pathPdbxDictionary)
            dApi = DictionaryApi(containerList=self.__containerList, consolidate=True, verbose=self.__verbose)
            # dApi.dumpCategoryIndex(fh=self.__lfh)
            # dApi.dumpEnumFeatures(fh=self.__lfh)
            # dApi.dumpFeatures(fh=self.__lfh)
            # dApi.dumpMethods(fh=self.__lfh)

            logger.debug('+++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
            groupList = dApi.getCategoryGroups()
            logger.debug('groupList %s\n' % groupList)
            for group in groupList:
                logger.debug('Group %s category list %s\n' % (group, dApi.getCategoryGroupCategories(groupName=group)))
            self.assertGreater(len(groupList), 10)
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testConsolidateDictionary(self):
        """Test case -  dump methods for dictionary metadata
        """

        try:
            myIo = IoAdapter(raiseExceptions=True)
            self.__containerList = myIo.readFile(inputFilePath=self.__pathPdbxDictionary)
            dApi = DictionaryApi(containerList=self.__containerList, consolidate=True, expandItemLinked=False, verbose=self.__verbose)
            for itemName in ['_entity.id', '_entity_poly_seq.num', '_atom_site.label_asym_id',
                             '_struct_asym.id', '_chem_comp.id', 'chem_comp_atom.comp_id', 'chem_comp_bond.comp_id']:
                categoryName = CifName.categoryPart(itemName)
                attributeName = CifName.attributePart(itemName)
                logger.debug("Full parent list for  %s : %s\n" % (itemName, dApi.getFullParentList(categoryName, attributeName)))
                logger.debug("Full child  list for  %s : %s\n" % (itemName, dApi.getFullChildList(categoryName, attributeName)))
                logger.debug("Ultimate parent for  %s : %s\n" % (itemName, dApi.getUltimateParent(categoryName, attributeName)))
                logger.debug("Type code for  %s : %s\n" % (itemName, dApi.getTypeCode(categoryName, attributeName)))
                self.assertIsNotNone(dApi.getTypeCode(categoryName, attributeName))
        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()

    def testGetAdjacentCategories(self):
        """Test case -
        """

        try:
            myIo = IoAdapter(raiseExceptions=True)
            self.__containerList = myIo.readFile(inputFilePath=self.__pathPdbxDictionary)
            dApi = DictionaryApi(containerList=self.__containerList, consolidate=True, verbose=self.__verbose)
            cList = dApi.getCategoryList()
            cI = {}
            for c in cList:
                chL = dApi.getChildCategories(c)
                pL = dApi.getParentCategories(c)
                for ch in chL:
                    if (ch, c) not in cI:
                        cI[(ch, c)] = 1
                    else:
                        cI[(ch, c)] += 1
                for p in pL:
                    if (c, p) not in cI:
                        cI[(c, p)] = 1
                    else:
                        cI[(c, p)] += 1
            linkL = []
            for s, t in cI.keys():
                d = {'source': s, 'target': t, 'type': 'link'}
                linkL.append(d)

            if self.__verbose:
                print(json.dumps(linkL, sort_keys=True, indent=4, separators=(',', ': ')))
            self.assertGreater(len(linkL), 50)

        except Exception as e:
            logger.exception("Failing with %s" % str(e))
            self.fail()


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
    if (True):
        mySuite = suiteDictionaryApiTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

        mySuite = suiteConsolidateTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

        mySuite = suiteAdjacentTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

        mySuite = suiteDictionaryApiEnumTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

        mySuite = suiteIndexTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
