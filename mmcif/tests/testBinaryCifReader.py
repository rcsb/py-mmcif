##
#
# File:    testBinaryCifReader.py
# Author:  J. Westbrook
# Date: 16-May-2021
##

import gzip
import logging
import os
import sys
import time
import unittest

import msgpack
from mmcif.io.BinaryCifReader import BinaryCifReader
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


class BinaryCifReaderTests(unittest.TestCase):
    def setUp(self):
        #
        self.__pathOutputDir = os.path.join(HERE, "test-output")
        #
        self.__locatorRcsbBcifGzip = "https://models.rcsb.org/1bna.bcif.gz"
        #
        # RCSB examples produced with MolStar
        self.__pathRcsbBcifGzip = os.path.join(HERE, "data", "1bna.bcif.gz")
        self.__pathRcsbBcifTranslated = os.path.join(self.__pathOutputDir, "1bna-translated.cif")
        #
        #  PDBDEV examples produced with MolStar
        self.__pathPdbdevBcif = os.path.join(HERE, "data", "PDBDEV_00000041.bcif")
        self.__pathPdbdevBcifGzip = os.path.join(HERE, "data", "PDBDEV_00000041.bcif.gz")
        self.__pathPdbdevBcifTranslated = os.path.join(self.__pathOutputDir, "PDBDEV_00000041-translated.cif")

        # Examples from Python-IHM
        self.__pathIhmBcifGzip = os.path.join(HERE, "data", "PDBDEV_00000001_IHM.bcif.gz")
        self.__pathIhmBcifTranslated = os.path.join(self.__pathOutputDir, "PDBDEV_00000001_IHM-translated.cif")
        #
        self.__msgPathTest27Path = os.path.join(self.__pathOutputDir, "msgpack-test-py27.dat")
        self.__startTime = time.time()
        logger.debug("Running tests on version %s", __version__)
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testMsgpackEncoding(self):
        #
        with gzip.open(self.__pathIhmBcifGzip, mode="rb") as inpF:
            bD = msgpack.unpack(inpF)
            logger.info("GZIP IHM bD.keys() %r", bD.keys())
            logger.info("encoder %r", bD[b"encoder"] if b"encoder" in bD else bD["encoder"])
            self.assertTrue(b"dataBlocks" in bD)
        #
        with gzip.open(self.__pathRcsbBcifGzip, mode="rb") as inpF:
            bD = msgpack.unpack(inpF)
            logger.info("GZIP RCSB bD.keys() %r", bD.keys())
            logger.info("encoder %r", bD[b"encoder"] if b"encoder" in bD else bD["encoder"])
            self.assertTrue(u"dataBlocks" in bD)

        with open(self.__pathPdbdevBcif, mode="rb") as inpF:
            bD = msgpack.unpack(inpF)
            logger.info("PDBDEV bD.keys() %r", bD.keys())
            logger.info("encoder %r", bD[b"encoder"] if b"encoder" in bD else bD["encoder"])
            self.assertTrue(u"dataBlocks" in bD)
        #

    def testDeserializeLocalRcsb(self):
        try:
            bcr = BinaryCifReader(storeStringsAsBytes=False)
            cL0 = bcr.deserialize(self.__pathRcsbBcifGzip)
            ioPy = IoAdapter()
            ok = ioPy.writeFile(self.__pathRcsbBcifTranslated, cL0)
            self.assertTrue(ok)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testDeserializeLocalPdbdev(self):
        try:
            bcr = BinaryCifReader(storeStringsAsBytes=False)
            cL0 = bcr.deserialize(self.__pathPdbdevBcifGzip)
            ioPy = IoAdapter()
            ok = ioPy.writeFile(self.__pathPdbdevBcifTranslated, cL0)
            self.assertTrue(ok)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testDeserializeRemoteMolStar(self):
        try:
            bcr = BinaryCifReader(storeStringsAsBytes=False)
            cL0 = bcr.deserialize(self.__locatorRcsbBcifGzip)
            ioPy = IoAdapter()
            ok = ioPy.writeFile(self.__pathRcsbBcifTranslated, cL0)
            self.assertTrue(ok)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    def testDeserializeIhm(self):
        try:
            bcr = BinaryCifReader(storeStringsAsBytes=True)
            cL1 = bcr.deserialize(self.__pathIhmBcifGzip)
            ioPy = IoAdapter()
            ok = ioPy.writeFile(self.__pathIhmBcifTranslated, cL1)
            self.assertTrue(ok)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()


def suiteBCifReader():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(BinaryCifReaderTests("testDeserializeLocalRcsb"))
    suiteSelect.addTest(BinaryCifReaderTests("testDeserializeRemoteMolStar"))
    suiteSelect.addTest(BinaryCifReaderTests("testDeserializeLocalPdbdev"))
    suiteSelect.addTest(BinaryCifReaderTests("testDeserializeIhm"))    
    return suiteSelect


if __name__ == "__main__":

    mySuite = suiteBCifReader()
    unittest.TextTestRunner(verbosity=2, descriptions=False).run(mySuite)
