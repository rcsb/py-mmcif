##
# File:    Dictionary2DDLm.py
# Author:  jdw
# Date:    9-Mar-2018
# Version: 0.001
##
"""
Tests cases for Dictionary API generating alternative DDLm metadata format.

"""
from __future__ import absolute_import

import logging
import os
import sys
import time
import unittest

from mmcif.api.DataCategory import DataCategory
from mmcif.api.DictionaryApi import DictionaryApi
from mmcif.api.PdbxContainers import CifName, DataContainer, DefinitionContainer
from mmcif.io.IoAdapterPy import IoAdapterPy

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

try:
    from mmcif import __version__
except ImportError:
    sys.path.insert(0, TOPDIR)
    from mmcif import __version__


__docformat__ = "google en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Dictionary2DDLmTests(unittest.TestCase):
    def setUp(self):
        self.__lfh = sys.stdout
        self.__verbose = True
        self.__pathPdbxDictionary = os.path.join(HERE, "data", "mmcif_pdbx_v5_next.dic")
        self.__containerList = None
        self.__startTime = time.time()
        logger.debug("Testing version %s", __version__)
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testGenDDLm(self):
        """Generating alternative DDLm metadata format. (starting point)"""
        try:
            myIo = IoAdapterPy(self.__verbose, self.__lfh)
            self.__containerList = myIo.readFile(inputFilePath=self.__pathPdbxDictionary)
            dApi = DictionaryApi(containerList=self.__containerList, consolidate=True, verbose=self.__verbose)
            parentD = dApi.getParentDictionary()
            #
            oCList = []
            dDef = DataContainer("mmcif_pdbx_ddlm_auto")
            dc = DataCategory("dictionary")
            dc.appendAttribute("title")
            dc.appendAttribute("class")
            dc.appendAttribute("version")
            dc.appendAttribute("date")
            dc.appendAttribute("ddl_conformance")
            dc.appendAttribute("text")
            dc.append(["mmcif_pdbx_ddlm_auto", "Instance", "latest", "2018-03-09", "ddlm best effort", "Software converted PDBx dictionary using DDLm semantics"])
            dDef.append(dc)
            oCList.append(dDef)

            catIdx = dApi.getCategoryIndex()
            for catName in sorted(catIdx.keys()):
                attNameList = catIdx[catName]
                # created definition container -
                cDef = DefinitionContainer(catName)
                oCList.append(cDef)
                #
                dc = DataCategory("definition")
                dc.appendAttribute("id")
                dc.appendAttribute("scope")
                dc.appendAttribute("class")
                dc.appendAttribute("update")
                dc.append([catName, "Category", "Loop", "2018-03-09"])
                cDef.append(dc)
                val = dApi.getCategoryDescription(category=catName)
                dc = DataCategory("description")
                dc.appendAttribute("text")
                dc.append([val])
                cDef.append(dc)
                #
                dc = DataCategory("name")
                dc.appendAttribute("category_id")
                dc.appendAttribute("object_id")

                valList = dApi.getCategoryGroupList(category=catName)
                pcg = catName
                for val in valList:
                    if val != "inclusive_group":
                        pcg = val
                        break
                dc.append([catName, pcg])
                cDef.append(dc)

                valList = dApi.getCategoryKeyList(category=catName)
                if not valList:
                    self.__lfh.write("Missing caegory key for category %s\n" % catName)
                else:
                    dc = DataCategory("category")
                    dc.appendAttribute("key_id")
                    kItemName = CifName.itemName(catName, "synthetic_key")
                    dc.append([kItemName])
                    cDef.append(dc)

                    iDef = DefinitionContainer(kItemName)
                    self.__makeKeyItem(catName, "synthetic_key", valList, iDef)
                    oCList.append(iDef)

                for attName in attNameList:
                    itemName = CifName.itemName(catName, attName)
                    iDef = DefinitionContainer(itemName)

                    oCList.append(iDef)

                    #
                    dc = DataCategory("definition")
                    dc.appendAttribute("id")
                    dc.appendAttribute("scope")
                    dc.appendAttribute("class")
                    dc.appendAttribute("update")
                    dc.append([itemName, "Item", "Single", "2013-08-22"])
                    iDef.append(dc)
                    #
                    val = dApi.getDescription(category=catName, attribute=attName)
                    dc = DataCategory("description")
                    dc.appendAttribute("text")
                    dc.append([val])
                    iDef.append(dc)
                    #
                    dc = DataCategory("name")
                    dc.appendAttribute("category_id")
                    dc.appendAttribute("object_id")
                    #
                    if itemName in parentD:
                        dc.appendAttribute("linked_item_id")
                        dc.append([catName, attName, parentD[itemName][0]])
                    else:
                        dc.append([catName, attName])
                    iDef.append(dc)
                    #
                    #
                    aliasList = dApi.getItemAliasList(category=catName, attribute=attName)
                    if aliasList:
                        dc = DataCategory("alias")
                        dc.appendAttribute("definition_id")
                        for alias in aliasList:
                            dc.append([alias[0]])
                        iDef.append(dc)

                    enList = dApi.getEnumListAltWithDetail(category=catName, attribute=attName)

                    tC = dApi.getTypeCode(category=catName, attribute=attName)
                    tcontainer = "Single"
                    purpose = "Describe"
                    source = "Recorded"
                    contents = "Text"
                    #
                    if tC is None:
                        self.__lfh.write("Missing data type attribute %s\n" % attName)
                    elif tC in ["code", "atcode", "name", "idname", "symop", "fax", "phone", "email", "code30", "ec-type"]:
                        purpose = "Encode"
                        contents = "Text"
                        source = "Assigned"
                    elif tC in ["ucode"]:
                        purpose = "Encode"
                        contents = "Code"
                        source = "Assigned"
                    elif tC in ["line", "uline", "text"]:
                        purpose = "Describe"
                        source = "Recorded"
                        contents = "Text"
                    elif tC in ["int"]:
                        purpose = "Number"
                        source = "Recorded"
                        contents = "Integer"
                    elif tC in ["int-range"]:
                        purpose = "Number"
                        source = "Recorded"
                        contents = "Range"
                    elif tC in ["float"]:
                        purpose = "Measurand"
                        source = "Recorded"
                        contents = "Real"
                    elif tC in ["float-range"]:
                        purpose = "Measurand"
                        source = "Recorded"
                        contents = "Range"
                    elif tC.startswith("yyyy"):
                        source = "Assigned"
                        contents = "Date"
                        purpose = "Describe"

                    if enList:
                        purpose = "State"

                    dc = DataCategory("type")
                    dc.appendAttribute("purpose")
                    dc.appendAttribute("source")
                    dc.appendAttribute("contents")
                    dc.appendAttribute("container")
                    dc.append([purpose, source, contents, tcontainer])
                    iDef.append(dc)
                    #
                    if enList:
                        dc = DataCategory("enumeration_set")
                        dc.appendAttribute("state")
                        dc.appendAttribute("detail")
                        for en in enList:
                            dc.append([en[0], en[1]])
                        iDef.append(dc)

                    dfv = dApi.getDefaultValue(category=catName, attribute=attName)
                    bvList = dApi.getBoundaryList(category=catName, attribute=attName)
                    if ((dfv is not None) and (dfv not in ["?", "."])) or bvList:
                        row = []
                        dc = DataCategory("enumeration")
                        if dfv is not None:
                            dc.appendAttribute("default")
                            row.append(dfv)
                        if bvList:
                            dc.appendAttribute("range")
                            mminVp = -1000000
                            mmaxVp = 10000000
                            mminV = mmaxVp
                            mmaxV = mminVp
                            for bv in bvList:
                                minV = float(bv[0]) if bv[0] != "." else mminVp
                                maxV = float(bv[1]) if bv[1] != "." else mmaxVp
                                mminV = min(mminV, minV)
                                mmaxV = max(mmaxV, maxV)
                            if mminV == mminVp:
                                mminV = ""
                            if mmaxV == mmaxVp:
                                mmaxV = ""
                            row.append(str(mminV) + ":" + str(mmaxV))

                        dc.append(row)
                        iDef.append(dc)

            myIo.writeFile(outputFilePath=os.path.join(HERE, "test-output", "mmcif_pdbx_ddlm_auto.dic"), containerList=oCList)

        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def __makeKeyItem(self, catName, attName, keyItemList, iDef):
        itemName = CifName.itemName(catName, attName)

        #
        dc = DataCategory("definition")
        dc.appendAttribute("id")
        dc.appendAttribute("scope")
        dc.appendAttribute("class")
        dc.appendAttribute("update")
        dc.append([itemName, "Item", "Single", "2013-08-22"])
        iDef.append(dc)
        #
        dc = DataCategory("description")
        dc.appendAttribute("text")
        dc.append(["synthentic componsite key"])
        iDef.append(dc)
        #
        dc = DataCategory("name")
        dc.appendAttribute("category_id")
        dc.appendAttribute("object_id")
        dc.append([catName, attName])
        iDef.append(dc)
        tcontainer = "Set"
        purpose = "Composite"
        source = "Derived"
        contents = "Name"
        dimension = "[%d]" % len(keyItemList)
        #

        dc = DataCategory("type")
        dc.appendAttribute("purpose")
        dc.appendAttribute("source")
        dc.appendAttribute("contents")
        dc.appendAttribute("container")
        dc.appendAttribute("dimension")
        dc.append([purpose, source, contents, tcontainer, dimension])
        iDef.append(dc)

        dc = DataCategory("method")
        dc.appendAttribute("purpose")
        dc.appendAttribute("expression")

        tmpl = """

                      With row as %s

                           %s = [%s]

        """
        mText = tmpl % (catName, itemName, ",".join(keyItemList))
        dc.append(["Evaluation", mText])
        iDef.append(dc)


def suiteDictionary2DDLm():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(Dictionary2DDLmTests("testGenDDLm"))
    return suiteSelect


if __name__ == "__main__":
    mySuite = suiteDictionary2DDLm()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
