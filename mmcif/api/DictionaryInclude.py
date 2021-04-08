##
# File:    DictionaryApi.py
# Author:  jdw
# Date:    11-August-2013
# Version: 0.001
#
# Updates:
##
"""
Handle PDBx/mmCIF dictionary extension/component include processing.

"""

import logging

from collections import OrderedDict

from mmcif.api.PdbxContainers import CifName
from mmcif.io.IoAdapterPy import IoAdapterPy

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


logger = logging.getLogger(__name__)


class DictionaryInclude(object):
    def __init__(self):
        #
        self.__itemNameRelatives = [
            "_item.name",
            "_item_examples.name",
            "_ndb_item_description.name",
            "_item_related.name",
            "_category_key.name",
            "_item_structure.name",
            "_item_methods.name",
            "_item_aliases.name",
            "_item_dependent.dependent_name",
            "_item_default.name",
            "_pdbx_item_examples.name",
            "_item_units.name",
            "_item_related.related_name",
            "_item_description.name",
            "_item_dependent.name",
            "_item_range.name",
            "_item_sub_category.name",
            "_pdbx_item_range.name",
            "_pdbx_item_linked.condition_child_name",
            "_ndb_item_examples.name",
            "_pdbx_item_value_condition.item_name",
            "_ndb_item_range.name",
            "_item_linked.child_name",
            "_pdbx_item_description.name",
            "_pdbx_item_context.item_name",
            "_pdbx_item_enumeration_details.name",
            "_pdbx_item_linked_group_list.child_name",
            "_pdbx_item_linked_group_list.parent_name",
            "_pdbx_item_value_condition_list.target_item_name",
            "_ndb_item_enumeration.name",
            "_pdbx_item_linked.child_name",
            "_pdbx_item_value_condition.dependent_item_name",
            "_pdbx_item_enumeration.name",
            "_item_linked.parent_name",
            "_pdbx_item_value_condition_list.dependent_item_name",
            "_item_type.name",
            "_item_type_conditions.name",
            "_pdbx_item_linked.parent_name",
            "_item_enumeration.name",
        ]
        self.__categoryIdRelatives = [
            "_category.id",
            "_category_key.id",
            "_pdbx_item_linked_group.category_id",
            "_pdbx_category_examples.id",
            "_item.category_id",
            "_pdbx_category_context.category_id",
            "_pdbx_item_linked_group_list.parent_category_id",
            "_category_group.category_id",
            "_pdbx_category_description.id",
            "_ndb_category_examples.id",
            "_category_examples.id",
            "_category_methods.category_id",
            "_ndb_category_description.id",
            "_pdbx_item_linked_group_list.child_category_id",
        ]
        #
        self.__locatorIndexD = {}

    def processIncludedContent(self, containerList, cleanup=False):
        """Process any dictionary, category or item include instructions in any data containers in the
        input list of dictionary data and definition containers.

        Args:
            containerList (list): list of input PdbxContainer data or definition container objects
            cleanup (bool, optional): flag to remove generator category objects after parsing (default: False)

        Returns:
            (list): list of data and definition containers incorporating included content

        """
        includeD = self.__getIncludeInstructions(containerList, cleanup=cleanup)
        includeContentD = self.__fetchIncludedContent(includeD, cleanup=cleanup)
        return self.__addIncludedContent(containerList, includeContentD)

    def __addIncludedContent(self, containerList, includeContentD):
        """Incorporate included content described in the input dictionary of include instructions produced by
        internal method __getIncludeInstructions().

        Args:
            containerList (list): list of input PdbxContainer data or definition container objects
            includeContentD (dict): {"dictionaryIncludeDict": {dictionary_id: {...include details...}},
                                    "categoryIncludeDict": {dictionary_id: {category_id: {...include details... }}},
                                    "itemIncludeDict": {dictionary_id: {category_id: {itemName: {...include details...}}}}
                                    }

        Returns:
            (list): list of data and definition containers incorporating included content
        """
        # Index the current container list...
        cD = OrderedDict()
        datablockName = "unnamed_1"
        for container in containerList:
            if container.getType() == "data":
                datablockName = container.getName()
            # Handle potentially unconsolidated definitions --
            cD.setdefault(datablockName, OrderedDict()).setdefault(container.getName(), []).append(container)
        #
        #
        for datablockName in cD:
            if datablockName in includeContentD:
                if "replace" in includeContentD[datablockName]:
                    # Organize the replacements by name
                    replaceDefinitionD = OrderedDict()
                    replaceDataD = OrderedDict()
                    for container in includeContentD[datablockName]["replace"]:
                        if container.getType() == "definition":
                            replaceDefinitionD.setdefault(container.getName(), []).append(container)
                        else:
                            replaceDataD.setdefault(datablockName, []).append(container)
                    #
                    for rN, rL in replaceDefinitionD.items():
                        if rN in cD[datablockName]:
                            cD[datablockName][rN] = rL
                    # replace data sections in the base container
                    baseContainer = cD[datablockName][datablockName][0]
                    for rN, containerL in replaceDataD.items():
                        for container in containerL:
                            for nm in container.getObjNameList():
                                obj = container.getObj(nm)
                                baseContainer.replace(obj)
                    #
                if "extend" in includeContentD[datablockName]:
                    extendDataD = OrderedDict()
                    for container in includeContentD[datablockName]["extend"]:
                        if container.getType() == "definition":
                            cD.setdefault(datablockName, OrderedDict()).setdefault(container.getName(), []).append(container)
                        else:
                            extendDataD.setdefault(datablockName, []).append(container)
                    # extend data sections in the base container
                    baseContainer = cD[datablockName][datablockName][0]
                    for rN, containerL in extendDataD.items():
                        for container in containerL:
                            for nm in container.getObjNameList():
                                obj = container.getObj(nm)
                                if baseContainer.exists(nm):
                                    baseObj = baseContainer.getObj(nm)
                                    for ii in range(obj.getRowCount()):
                                        rowD = obj.getRowAttributeDict(ii)
                                        baseObj.append(rowD)
                                else:
                                    baseContainer.append(obj)
        #
        # Unwind the container index
        #
        fullL = []
        for datablockName in cD:
            for cL in cD[datablockName].values():
                fullL.extend(cL)
        #
        return fullL

    def __getIncludeInstructions(self, containerList, cleanup=False):
        """Extract include instructions from categories pdbx_include_dictionary,  pdbx_include_category, and pdbx_include_item.

        Args:
          containerList (list): list of input PdbxContainer data or definition container objects
          cleanup (optional, bool): flag to remove generator category objects after parsing (default: False)

        Returns:
            (dict): {"dictionaryIncludeDict": {dictionary_id: {...include details...}},
                     "categoryIncludeDict": {dictionary_id: {category_id: {...include details... }}},
                     "itemIncludeDict": {dictionary_id: {category_id: {itemName: {...include details...}}}}
                    }
        """
        includeD = OrderedDict()
        try:
            unNamed = 1
            for container in containerList:
                if container.getType() == "data":
                    dictionaryIncludeDict = OrderedDict()
                    categoryIncludeDict = OrderedDict()
                    itemIncludeDict = OrderedDict()
                    if container.getName():
                        datablockName = container.getName()
                    else:
                        datablockName = str(unNamed)
                        unNamed += 1
                    logger.debug("Adding data sections from container name %s  type  %s", datablockName, container.getType())
                    tl = container.getObj("pdbx_include_dictionary")
                    if tl is not None:
                        for row in tl.getRowList():
                            tD = OrderedDict()
                            for atName in ["dictionary_id", "dictionary_locator", "include_mode", "dictionary_namespace_prefix", "dictionary_namespace_prefix_replace"]:
                                tD[atName] = row[tl.getIndex(atName)] if tl.hasAttribute(atName) else None
                            dictionaryIncludeDict[tD["dictionary_id"]] = tD
                        #
                        tl = container.getObj("pdbx_include_category")
                        if tl is not None:
                            for row in tl.getRowList():
                                tD = OrderedDict()
                                for atName in ["dictionary_id", "category_id", "include_as_category_id", "include_mode"]:
                                    tD[atName] = row[tl.getIndex(atName)] if tl.hasAttribute(atName) else None
                                categoryIncludeDict.setdefault(tD["dictionary_id"], {}).setdefault(tD["category_id"], tD)
                        #
                        tl = container.getObj("pdbx_include_item")
                        if tl is not None:
                            for row in tl.getRowList():
                                tD = OrderedDict()
                                for atName in ["dictionary_id", "item_name", "include_as_item_name", "include_mode"]:
                                    tD[atName] = row[tl.getIndex(atName)] if tl.hasAttribute(atName) else None
                                categoryId = CifName.categoryPart(tD["item_name"])
                                itemIncludeDict.setdefault(tD["dictionary_id"], {}).setdefault(categoryId, {}).setdefault(tD["item_name"], tD)
                    if cleanup:
                        for catName in ["pdbx_include_dictionary", "pdbx_include_category", "pdbx_include_item"]:
                            if container.exists(catName):
                                container.remove(catName)
                    #
                    includeD[datablockName] = {
                        "dictionaryIncludeDict": dictionaryIncludeDict,
                        "categoryIncludeDict": categoryIncludeDict,
                        "itemIncludeDict": itemIncludeDict,
                    }
        except Exception as e:
            logger.exception("Include processing failing with %s", str(e))
        return includeD

    def __fetchIncludedContent(self, includeD, cleanup=False):
        """Fetch included content following the instructions encoded in the input data structure.

        Args:
            includeD (dict): (dict): {"dictionaryIncludeDict": {dictionary_id: {...include details...}},
                                      "categoryIncludeDict": {dictionary_id: {category_id: {...include details... }}},
                                      "itemIncludeDict": {dictionary_id: {category_id: {itemName: {...include details...}}}}
                                       }
            cleanup (optional, bool): flag to remove generator category objects after parsing (default: false)

        Returns:
            (dict): {datablockName: {"extend": [container,...], "replace": [container, ...]}, ... }
        """

        includeDataD = {}
        try:
            for datablockName, inclD in includeD.items():
                cL = []
                for dictName, iD in inclD["dictionaryIncludeDict"].items():
                    locator = iD["dictionary_locator"]
                    if locator in self.__locatorIndexD:
                        logger.info("Skipping redundant include for %r at %r", dictName, locator)
                        continue
                    self.__locatorIndexD[locator] = dictName
                    #
                    # --- Fetch the dictionary component -
                    #
                    containerList = self.processIncludedContent(self.__fetchLocator(locator), cleanup=cleanup)
                    #
                    nsPrefix = iD["dictionary_namespace_prefix"]
                    nsPrefixReplace = iD["dictionary_namespace_prefix_replace"]
                    dictInclMode = iD["include_mode"]
                    dataIncludeMode = iD["data_include_mode"] if "data_include_mode" in iD else "extend"
                    catInclD = inclD["categoryIncludeDict"][dictName] if dictName in inclD["categoryIncludeDict"] else None
                    itemInclD = inclD["itemIncludeDict"][dictName] if dictName in inclD["itemIncludeDict"] else None
                    #
                    #  Do data sections first.
                    for container in containerList:
                        if container.getType() == "data":
                            logger.debug("Including data container %r with %r", container.getName(), container.getObjNameList())
                            cL.append((container, dataIncludeMode))
                    #
                    if catInclD or itemInclD:
                        # Process only explicitly included categories/items in the dictionary component
                        if catInclD:
                            for container in containerList:
                                if container.getType() == "data":
                                    continue
                                cName = container.getName()
                                catName = cName if container.isCategory() else CifName.categoryPart(cName)
                                #
                                if catName in catInclD:
                                    if container.isAttribute() and itemInclD and catName in itemInclD and cName in itemInclD[catName]:
                                        inclMode = itemInclD[catName][cName]["include_mode"] if itemInclD[catName][cName]["include_mode"] else dictInclMode
                                        cL.append((self.__renameItem(container, itemInclD[catName][cName]["include_as_item_name"]), inclMode))
                                    else:
                                        inclMode = catInclD[catName]["include_mode"] if catInclD[catName]["include_mode"] else dictInclMode
                                        cL.append((self.__renameCategory(container, catInclD[catName]["include_as_category_id"]), inclMode))
                        elif itemInclD:
                            # Process only explicitly included items exclusive of explicitly included categories in the dictionary component
                            for container in containerList:
                                if container.getType() == "data":
                                    continue
                                cName = container.getName()
                                catName = cName if container.isCategory() else CifName.categoryPart(cName)
                                #
                                if container.isAttribute() and catName in itemInclD and cName in itemInclD[catName]:
                                    inclMode = itemInclD[catName][cName]["include_mode"] if itemInclD[catName][cName]["include_mode"] else dictInclMode
                                    cL.append((self.__renameItem(container, itemInclD[catName][cName]["include_as_item_name"]), inclMode))
                    else:
                        # Process the full content of the dictionary component
                        for container in containerList:
                            if container.getType() == "data":
                                continue
                            cName = container.getName()
                            catName = cName if container.isCategory() else CifName.categoryPart(cName)
                            #
                            if container.isAttribute():
                                newName = self.__substituteItemPrefix(cName, nsPrefix, nsPrefixReplace)
                                cL.append((self.__renameItem(container, newName), dictInclMode))
                            else:
                                newName = self.__substituteCategoryPrefix(catName, nsPrefix, nsPrefixReplace)
                                cL.append((self.__renameCategory(container, newName), dictInclMode))
                #
                for container, inclMode in cL:
                    if inclMode == "replace":
                        includeDataD.setdefault(datablockName, {}).setdefault("replace", []).append(container)
                    elif inclMode == "extend":
                        logger.debug("%r extending with %r", datablockName, container.getName())
                        includeDataD.setdefault(datablockName, {}).setdefault("extend", []).append(container)
                #
            for nm in includeDataD:
                numReplace = len(includeDataD[nm]["replace"]) if "replace" in includeDataD[nm] else 0
                numExtend = len(includeDataD[nm]["extend"]) if "extend" in includeDataD[nm] else 0
                logger.debug("includeDataD %s replace (%d) extend (%d)", nm, numReplace, numExtend)
            #
        except Exception as e:
            logger.exception("Failing with %s", str(e))

        return includeDataD

    def __fetchLocator(self, locator, **kwargs):
        """"""
        try:
            containerList = []
            workPath = kwargs.get("workPath", None)
            enforceAscii = kwargs.get("enforceAscii", False)
            raiseExceptions = kwargs.get("raiseExceptions", True)
            useCharRefs = kwargs.get("useCharRefs", True)
            #
            myIo = IoAdapterPy(raiseExceptions=raiseExceptions, useCharRefs=useCharRefs)
            containerList = myIo.readFile(locator, enforceAscii=enforceAscii, outDirPath=workPath)
            logger.info("Fetched %r dictionary container length (%d)", locator, len(containerList) if containerList else 0)
            logger.debug("%r", [container.getName() for container in containerList])
        except Exception as e:
            logger.exception("Failing for %s with %s", locator, str(e))
        return containerList

    def __substituteCategoryPrefix(self, catName, curPrefix, newPrefix):
        return catName.replace(curPrefix, newPrefix, 1) if catName and catName.startswith(curPrefix) else catName

    def __substituteItemPrefix(self, itemName, curPrefix, newPrefix):
        atName = CifName.attributePart(itemName)
        atName = atName.replace(curPrefix, newPrefix, 1) if atName and atName.startswith(curPrefix) else atName
        catName = CifName.categoryPart(itemName)
        catName = catName.replace(curPrefix, newPrefix, 1) if atName and catName.startswith(curPrefix) else catName
        return CifName.itemName(catName, atName)

    def __renameItem(self, container, newItemName):
        if not container and not container.isAttribute() or not newItemName:
            return container
        #
        itemNameCur = container.getName()
        if itemNameCur == newItemName:
            return container
        #
        try:
            for item in self.__itemNameRelatives:
                catName = CifName.categoryPart(item)
                if container.exists(catName):
                    cObj = container.getObj(catName)
                    atName = CifName.attributePart(item)
                    if cObj.hasAttribute(atName):
                        for iRow in range(cObj.getRowCount()):
                            curVal = cObj.getValue(atName, iRow)
                            if curVal == itemNameCur:
                                cObj.setValue(newItemName, atName, iRow)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return container

    def __renameCategory(self, container, newCategoryName):
        if not container and not container.isCategory() or not newCategoryName:
            return container
        #
        catNameCur = container.getName()
        if catNameCur == newCategoryName:
            return container
        try:
            for item in self.__categoryIdRelatives:
                catName = CifName.categoryPart(item)
                if container.exists(catName):
                    cObj = container.getObj(catName)
                    atName = CifName.attributePart(item)
                    if cObj.hasAttribute(atName):
                        for iRow in range(cObj.getRowCount()):
                            testVal = cObj.getValue(atName, iRow)
                            if testVal == catNameCur:
                                cObj.setValue(newCategoryName, atName, iRow)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return container
