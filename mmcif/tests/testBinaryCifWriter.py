##
#
# File:    testBinaryCifWriter.py
# Author:  J. Westbrook
# Date: 16-May-2021
##

import logging
import os
import sys
import time
import unittest

from mmcif.api.DataCategoryTyped import DataCategoryTyped
from mmcif.api.DictionaryApi import DictionaryApi
from mmcif.api.PdbxContainers import DataContainer
from mmcif.io.BinaryCifReader import BinaryCifReader
from mmcif.io.BinaryCifWriter import BinaryCifWriter
from mmcif.io.IoAdapterPy import IoAdapterPy as IoAdapter

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

try:
    from mmcif import __version__
except ImportError:
    sys.path.insert(0, TOPDIR)
    from mmcif import __version__


__docformat__ = "google en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class BinaryCifWriterTests(unittest.TestCase):
    def setUp(self):
        #
        self.__pathOutputDir = os.path.join(HERE, "test-output")
        self.__pathTextCif = os.path.join(HERE, "data", "1bna.cif")
        self.__testBcifOutput = os.path.join(self.__pathOutputDir, "1bna-generated.bcif")
        self.__testBcifTranslated = os.path.join(self.__pathOutputDir, "1bna-generated-translated.bcif")
        #
        self.__pathPdbxDictionary = os.path.join(HERE, "data", "mmcif_pdbx_v5_next.dic")
        myIo = IoAdapter(raiseExceptions=True)
        self.__containerList = myIo.readFile(inputFilePath=self.__pathPdbxDictionary)
        self.__dApi = DictionaryApi(containerList=self.__containerList, consolidate=True)
        #
        self.__floatTolerance = 1.0e-10
        self.__startTime = time.time()
        logger.debug("Running tests on version %s", __version__)
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testSerialize(self):
        try:
            for storeStringsAsBytes in [True, False]:
                tcL = []
                ioPy = IoAdapter()
                containerList = ioPy.readFile(self.__pathTextCif)
                for container in containerList:
                    cName = container.getName()
                    tc = DataContainer(cName)
                    for catName in container.getObjNameList():
                        dObj = container.getObj(catName)
                        tObj = DataCategoryTyped(dObj, dictionaryApi=self.__dApi, copyInputData=True)
                        tc.append(tObj)
                    tcL.append(tc)
                #
                bcw = BinaryCifWriter(self.__dApi, storeStringsAsBytes=storeStringsAsBytes, applyTypes=False, useFloat64=True)
                bcw.serialize(self.__testBcifOutput, tcL)
                self.assertEqual(containerList[0], containerList[0])
                self.assertEqual(tcL[0], tcL[0])

                bcr = BinaryCifReader(storeStringsAsBytes=storeStringsAsBytes)
                cL = bcr.deserialize(self.__testBcifOutput)
                #
                ioPy = IoAdapter()
                ok = ioPy.writeFile(self.__testBcifTranslated, cL)
                self.assertTrue(ok)
                self.assertTrue(self.__same(tcL[0], cL[0]))
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def __same(self, cA, cB):
        """[summary]

        Args:
            cA (DataCategoryTyped): object
            cB (DataCategory): object

        Returns:
            [type]: [description]
        """
        if cA.getName() != cB.getName():
            logger.info("name(A) %s ne name(B) %s", cA.getName(), cA.getName())
            return False
        aNmL = cA.getObjNameList()
        bNmL = cB.getObjNameList()
        if len(aNmL) != len(bNmL):
            logger.info("length(A) %r ne length(B) %r", len(aNmL), len(bNmL))
            return False
        #
        if sorted(bNmL) != sorted(bNmL):
            logger.info("sorted  name list(A) ne name list(B) %r", set(aNmL) - set(bNmL))
            return False
        if bNmL != bNmL:
            logger.info("unsorted name list(A) ne name list(B) %r", set(aNmL) - set(bNmL))
            return False
        for aNm in aNmL:
            aObj = cA.getObj(aNm)
            bObj = cB.getObj(aNm)
            # if aObj != bObj:
            #    logger.info("object(a) %r ne object(b) %r", aObj.getName(), bObj.getName())
            #    logger.info("aObj.__dict__ %r", aObj.__dict__)
            #    logger.info("bObj.__dict__ %r", bObj.__dict__)
            ta, _, tb = aObj.cmpAttributeNames(bObj)
            if ta or tb:
                logger.info("attributes differ (a not b) %r  (b not a) %r", ta, tb)
                return False

            vDiffL = aObj.cmpAttributeValues(bObj, ignoreOrder=False, floatAbsTolerance=self.__floatTolerance, floatRelTolerance=self.__floatTolerance)
            #
            if vDiffL:
                for vDiff in vDiffL:
                    if not vDiff[1]:
                        logger.info("values differ for attribute %r", vDiff[0])
                        #
                        ii = aObj.getAttributeIndex(vDiff[0])
                        aCol = aObj.getColumn(ii)
                        jj = bObj.getAttributeIndex(vDiff[0])
                        bCol = bObj.getColumn(jj)
                        logger.info("aCol %r", aCol)
                        logger.info("bCol %r", bCol)

                        #
                        return False
        #
        return True


def suiteBcifWriter():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(BinaryCifWriterTests("testSerialize"))

    return suiteSelect


if __name__ == "__main__":

    mySuite = suiteBcifWriter()
    unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)
