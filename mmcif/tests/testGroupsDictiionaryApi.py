##
# File:    GroupDictionaryApiTests.py
# Author:  jdw
# Date:    8-Mar-2018
# Version: 0.001
##
"""
Dictionary API examples of category group traversal and hierarchies,
"""
from __future__ import absolute_import, print_function

import logging
import os
import sys
import time
import unittest

from mmcif.api.DictionaryApi import DictionaryApi
from mmcif.api.PdbxContainers import CifName
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
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class GroupDictionaryApiTests(unittest.TestCase):
    def setUp(self):
        self.__lfh = sys.stderr
        self.__verbose = False
        self.__pathPdbxDictionary = os.path.join(HERE, "data", "mmcif_pdbx_v5_next.dic")
        # self.__pathPdbxDictionary = os.path.join(HERE, "data", "mmcif_pdbx_v50.dic")
        self.__containerList = None
        self.__startTime = time.time()
        logger.debug("Running tests on version %s", __version__)
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))
        self.__groupClassTupL = [
            ("atom_group", "STRUCTURE"),
            ("array_data_group", "MX"),
            ("axis_group", "MX"),
            ("audit_group", "DB"),
            ("cell_group", "MX"),
            ("chemical_group", "SAMPLE"),
            ("chem_comp_group", "SAMPLE"),
            ("chem_comp_dictionary_group", "SAMPLE"),
            ("chem_comp_model_group", "SAMPLE"),
            ("bird_dictionary_group", "SAMPLE"),
            ("bird_family_dictionary_group", "SAMPLE"),
            ("chem_link_group", "SAMPLE"),
            ("citation_group", "DB"),
            ("computing_group", "MX"),
            ("compliance_group", "DB"),
            ("database_group", "DB"),
            ("diffrn_group", "MX"),
            ("em_group", "EM"),
            ("em_legacy_group", "EM"),
            ("emdb_admin_group", "EM"),
            ("emdb_extension_group", "EM"),
            ("entity_group", "SAMPLE"),
            ("entry_group", "DB"),
            ("exptl_group", "MX"),
            ("geom_group", "STRUCTURE"),
            ("iucr_group", "DB"),
            ("nmr_group", "NMR"),
            ("pdb_group", "DB"),
            ("phasing_group", "MX"),
            ("refine_group", "MX"),
            ("refln_group", "MX"),
            ("struct_group", "STRUCTURE"),
            ("symmetry_group", "MX"),
            ("pdbx_erf_group", "STRUCTURE"),
            ("ccp4_group", "MX"),
            ("ndb_group", "STRUCTURE"),
            ("protein_production_group", "SAMPLE"),
            ("solution_scattering_group", "SAS"),
            ("validate_group", "STRUCTURE"),
            ("view_group", "STRUCTURE"),
            ("em_specimen", "EM"),
            ("em_sample", "EM"),
            ("em_crystallography", "EM"),
            ("em_fitting", "EM"),
            ("em_tomography", "EM"),
            ("em_imaging", "EM"),
            ("em_reconstruction", "EM"),
            ("em_symmetry_group", "EM"),
            ("em_experiment", "EM"),
            ("em_symmetry", "EM"),
            ("emd_group", "EM"),
            ("dcc_group", "MX"),
            ("xfel_group", "MX"),
            ("diffrn_data_set_group", "MX"),
            ("branch_group", "SAMPLE"),
        ]
        self.__unlinkedCategoryClassTup = [
            ("pdbx_exptl_pd", "MX"),
            ("pdbx_coordinate_model", "STRUCTURE"),
            ("pdbx_bond_distance_limits", "STRUCTURE"),
            ("pdbx_unobs_or_zero_occ_residues", "STRUCTURE"),
            ("pdbx_unobs_or_zero_occ_atoms", "STRUCTURE"),
            ("pdbx_struct_mod_residue", "STRUCTURE"),
            ("pdbx_molecule", "SAMPLE"),
            ("pdbx_molecule_features", "SAMPLE"),
            ("pdbx_distant_solvent_atoms", "STRUCTURE"),
            ("pdbx_struct_special_symmetry", "MX"),
            ("pdbx_linked_entity_list", "SAMPLE"),
            ("pdbx_seq_map_depositor_info", "SAMPLE"),
            ("pdbx_molecule_features_depositor_info", "SAMPLE"),
            ("pdbx_chem_comp_instance_depositor_info", "SAMPLE"),
            ("pdbx_depui_status_flags", "DB"),
            ("pdbx_depui_upload", "DB"),
            ("pdbx_depui_validation_status_flags", "DB"),
            ("pdbx_depui_entity_status_flags", "DB"),
            ("pdbx_depui_entity_features", "DB"),
            ("pdbx_deposition_message_info", "DB"),
            ("pdbx_deposition_message_file_reference", "DB"),
            ("pdbx_depui_entry_details", "DB"),
            ("pdbx_data_processing_status", "DB"),
            ("pdbx_pdb_compnd", "SAMPLE"),
            ("pdbx_pdb_source", "SAMPLE"),
            ("pdbx_sequence_annotation", "SAMPLE"),
            ("pdbx_post_process_details", "DB"),
            ("pdbx_post_process_status", "DB"),
            ("pdbx_missing_residue_list", "SAMPLE"),
            ("pdbx_data_processing_cell", "MX"),
            ("pdbx_data_processing_reflns", "MX"),
            ("pdbx_data_processing_detector", "MX"),
            ("pdbx_tableinfo", "DB"),
            ("pdbx_columninfo", "DB"),
            ("pdbx_nmr_computing", "NMR"),
            ("pdbx_crystal_alignment", "MX"),
            ("pdbx_biocurator_comment", "DB"),
            ("pdbx_data_section_audit", "DB"),
            ("pdbx_depositor_comment", "DB"),
        ]

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testClassifyByGroup(self):
        """Test case -  organize dictionary items by classes: SAMPLE, MX, NMR, EM, STRUCTURE, and DB"""
        try:
            myIo = IoAdapter(raiseExceptions=True)
            self.__containerList = myIo.readFile(inputFilePath=self.__pathPdbxDictionary)
            dApi = DictionaryApi(containerList=self.__containerList, consolidate=True, verbose=self.__verbose)
            #
            itemList = []
            groupList = dApi.getCategoryGroups()
            categoryList = dApi.getCategoryList()
            for category in categoryList:
                itemList.extend(dApi.getItemNameList(category))
            itemList = sorted(set(itemList))

            logger.info("Total category length %d", len(categoryList))
            logger.info("Total definition length %d", len(itemList))

            logger.info("group length %s", len(groupList))
            logger.debug("groupList %r", groupList)
            #
            findUnlinked = False
            if findUnlinked:
                tSet = set(["pdbx_group", "inclusive_group"])
                for category in categoryList:
                    gList = dApi.getCategoryGroupList(category)
                    gSet = set(gList)
                    if gSet == tSet:
                        logger.info("unqualified %s", category)

                    # logger.info("%s -> %r", category, gList)
                    if not gList:
                        logger.info("--- No category group assignment for %s", category)
            #
            classD = {}
            # Add category group members -
            for groupName, className in self.__groupClassTupL:
                categoryL = dApi.getCategoryGroupCategories(groupName, followChildren=True)
                for category in categoryL:
                    classD.setdefault(className, []).extend(dApi.getItemNameList(category))
            #
            # Add unlinked categories
            #
            for category, className in self.__unlinkedCategoryClassTup:
                classD.setdefault(className, []).extend(dApi.getItemNameList(category))
            #
            sumItem = 0
            classItemD = {}
            for className, itemL in classD.items():
                numItem = len(set(itemL))
                sumItem += numItem
                logger.info("class %s items %d", className, len(set(itemL)))
                for item in itemL:
                    classItemD[item] = True
            #
            logger.info("Sum classified items is %d", sumItem)
            logger.info("classified items %d", len(classItemD))
            #
            logger.debug("classItemD.items() %r", list(classItemD.items())[:10])

            missingGroupL = []

            jj = 0
            for item in itemList:
                if item not in classItemD:
                    jj += 1
                    category = CifName.categoryPart(item)
                    logger.info("%d item %r category %r", jj, item, category)
                    missingGroupL.extend(dApi.getCategoryGroupList(category))
            #
            logger.info("missing groups %r", sorted(set(missingGroupL)))

        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()


def suiteDictionaryApiGroupTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(GroupDictionaryApiTests("testClassifyByGroup"))
    return suiteSelect


if __name__ == "__main__":
    mySuite = suiteDictionaryApiGroupTests()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
