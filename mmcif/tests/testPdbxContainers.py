##
# File:    testPdbxContainer.py
# Author:  ep
# Date:    6-Apri-2023
# Version: 0.001
#
# Update:
##
"""
Test container PdbxContainers functionality
"""
__docformat__ = "google en"
__author__ = "Ezra Peisach"
__email__ = "peisach@rcsb.rutgers.edu"
__license__ = "Apache 2.0"


import logging
import os
import os.path
import sys
import time
import unittest

from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import DataContainer

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

try:
    from mmcif import __version__
except ImportError:
    sys.path.insert(0, TOPDIR)
    from mmcif import __version__


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class PdbxContainersTests(unittest.TestCase):
    def setUp(self):
        self.lfh = sys.stderr
        self.verbose = False
        #
        self.__startTime = time.time()
        logger.debug("Running tests on version %s", __version__)
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def __createContainer(self):
        """Creates a containter with data"""

        curContainer = DataContainer("myblock")

        # Create category
        aCat = DataCategory("pdbx_seqtool_mapping_ref")
        aCat.appendAttribute("ordinal")
        aCat.appendAttribute("entity_id")
        aCat.appendAttribute("auth_mon_id")
        aCat.appendAttribute("auth_mon_num")
        aCat.appendAttribute("pdb_chain_id")
        aCat.appendAttribute("ref_mon_id")
        aCat.appendAttribute("ref_mon_num")
        aCat.append((1, 2, 3, 4, "55555555555555555555555555555555555555555555", 6, 7))
        aCat.append((1, 2, 3, 4, "5555", 6, 7))

        curContainer.append(aCat)

        return curContainer

    def testGeneral(self):
        """Tests some simple aspects
        """

        blk = self.__createContainer()

        self.assertEqual(blk.getName(), "myblock")
        blk.setName("New")
        self.assertEqual(blk.getName(), "New")

    def testRename(self):
        """Tests if renaming category results in old name still available in
        getObj()
        """

        blk = self.__createContainer()

        curName = "pdbx_seqtool_mapping_ref"
        newName = "newName"

        # Current - access to curName ok, newName gives nothing
        self.assertEqual(blk.getObjNameList(), [curName])
        self.assertTrue(blk.exists(curName))
        self.assertFalse(blk.exists(newName))
        self.assertIsNotNone(blk.getObj(curName))
        self.assertIsNone(blk.getObj(newName))

        # Now rename
        # Test non existant
        self.assertFalse(blk.rename("noname", "othernoname"))

        # Expect nothing changed
        self.assertEqual(blk.getObjNameList(), [curName])
        self.assertTrue(blk.exists(curName))
        self.assertFalse(blk.exists(newName))
        self.assertIsNotNone(blk.getObj(curName))
        self.assertIsNone(blk.getObj(newName))

        # Rename proper
        self.assertTrue(blk.rename(curName, newName))

        # Expect nothing changed
        self.assertEqual(blk.getObjNameList(), [newName])
        self.assertFalse(blk.exists(curName))
        self.assertTrue(blk.exists(newName))
        self.assertIsNone(blk.getObj(curName))
        self.assertIsNotNone(blk.getObj(newName))


def containerSuite():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(PdbxContainersTests("testGeneral"))
    suiteSelect.addTest(PdbxContainersTests("testRename"))
    return suiteSelect


if __name__ == "__main__":
    mySuite = containerSuite()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
#
