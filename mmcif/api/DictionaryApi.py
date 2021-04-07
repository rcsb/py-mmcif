##
# File:    DictionaryApi.py
# Author:  jdw
# Date:    11-August-2013
# Version: 0.001
#
# Updates:
#  20-Aug-2013  Jdw manage all data sections -
#   2-Oct-2013  Jdw add alternative methods for extracting full parent and child lists
#   6-Oct-2013  Jdw provide ordering options for history and revision dates
#  10-Dec-2013  jdw return sorted unique list of enumerations with details.
#  14-Feb-2014  jdw fix attribute index lookup.
#  08-Mar-2014  jdw add method getEnumerationClosedFlag(self,category,attribute)
#   9-Sep-2018  jdw add priority to method definition constructor
#   7-Dec-2018  jdw add constructor parameter replaceDefinition=False to allow replacing
#                   defintions during consolidation
#   3-Feb-2019  jdw add method getFullDescendentList()
#  12-Apr-2019  jdw add methods getItemSubCategoryLabelList() and  getItemSubCategoryList()
#  26-May-2019  jdw extend api for mehhods
#  28-Jul-2019  jdw retain dictionary ordering for categories and attributes (suppress sorting)
#  15-Aug-2019  jdw improve handling of dictionary and dictionary history categories for concatenated dictionaries
#   6-Sep-2019  jdw cleanup enum details
#   5-Apr-2021  jdw add getItemValueConditionDependentList()
##
"""
Accessors for PDBx/mmCIF dictionary attributes -
"""
from __future__ import absolute_import

import logging
import sys

from collections import OrderedDict
from six.moves import zip, zip_longest

from mmcif.api.DataCategory import DataCategory
from mmcif.api.Method import MethodDefinition, MethodReference
from mmcif.api.PdbxContainers import CifName

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


logger = logging.getLogger(__name__)

# pylint: disable=too-many-lines


class DictionaryApi(object):
    def __init__(self, containerList, consolidate=True, expandItemLinked=False, replaceDefinition=False, **kwargs):
        """Return an instance of the mmCIF dictionary API.

        Args:
            containerList (list): list of definition or data containers holding dictionary content
            consolidate (bool, optional): consolidate dictionary attributes within a single definition. Defaults to True.
            expandItemLinked (bool, optional): distribute item and item linked attributes defined for the parent
                                               to child definitions. Defaults to False.
            replaceDefinition (bool, optional): duplicate definitions replace prior definitions. Defaults to False.
        """
        _ = kwargs
        #
        self.__containerList = containerList
        self.__replaceDefinition = replaceDefinition
        #
        if consolidate:
            self.__consolidateDefinitions()
        #
        if expandItemLinked:
            self.__expandLoopedDefinitions()

        self.__fullIndex = OrderedDict()

        # ---
        #
        # Map category name to the unique list of attributes
        self.__catNameIndex = OrderedDict()
        # Map category name to the unique list of item names
        self.__catNameItemIndex = OrderedDict()
        # Full unique list of item names -
        self.__itemNameList = []
        #
        # Map dictionary objects names to definition containers -
        self.__definitionIndex = OrderedDict()
        #
        # data section/objects of the dictionary by category name -
        self.__dataIndex = OrderedDict()
        #
        # Map of types id->(regex,primitive_type)
        self.__typesDict = OrderedDict()
        #
        self.__enumD = {
            "ENUMERATION_VALUE": ("item_enumeration", "value"),
            "ENUMERATION_DETAIL": ("item_enumeration", "detail"),
            "ENUMERATION_TYPE_UNITS": ("item_enumeration", "rcsb_type_units_code"),
            "ENUMERATION_DETAIL_BRIEF": ("item_enumeration", "rcsb_detail_brief"),
            "ENUMERATION_TUPLE": ("item_enumeration", None),
            "ITEM_LINKED_PARENT": ("item_linked", "parent_name"),
            "ITEM_LINKED_CHILD": ("item_linked", "child_name"),
            "DATA_TYPE_CODE": ("item_type", "code"),
            "DATA_TYPE_REGEX": ("item_type_list", "construct"),
            "DATA_TYPE_PRIMITIVE": ("item_type_list", "primitive_code"),
            "ITEM_NAME": ("item", "name"),
            "ITEM_CATEGORY_ID": ("item", "category_id"),
            "ITEM_MANDATORY_CODE": ("item", "mandatory_code"),
            "ITEM_DESCRIPTION": ("item_description", "description"),
            "ITEM_UNITS": ("item_units", "code"),
            "ITEM_DEFAULT_VALUE": ("item_default", "value"),
            "ITEM_EXAMPLE_CASE": ("item_examples", "case"),
            "ITEM_EXAMPLE_DETAIL": ("item_examples", "detail"),
            "ITEM_RANGE_MAXIMUM": ("item_range", "maximum"),
            "ITEM_RANGE_MINIMUM": ("item_range", "minimum"),
            "CATEGORY_KEY_ITEMS": ("category_key", "name"),
            "CATEGORY_EXAMPLE_CASE": ("category_examples", "case"),
            "CATEGORY_EXAMPLE_DETAIL": ("category_examples", "detail"),
            "CATEGORY_MANDATORY_CODE": ("category", "mandatory_code"),
            "CATEGORY_DESCRIPTION": ("category", "description"),
            "CATEGORY_NX_MAPPING_DETAILS": ("category", "NX_mapping_details"),
            #
            "DATA_TYPE_CODE_NDB": ("ndb_item_type", "code"),
            "ITEM_DESCRIPTION_NDB": ("ndb_item_description", "description"),
            "ENUMERATION_VALUE_NDB": ("ndb_item_enumeration", "value"),
            "ENUMERATION_DETAIL_NDB": ("ndb_item_enumeration", "detail"),
            "ITEM_MANDATORY_CODE_NDB": ("ndb_item", "mandatory_code"),
            "ITEM_EXAMPLE_CASE_NDB": ("ndb_item_examples", "case"),
            "ITEM_EXAMPLE_DETAIL_NDB": ("ndb_item_examples", "detail"),
            "ITEM_RANGE_MAXIMUM_NDB": ("ndb_item_range", "maximum"),
            "ITEM_RANGE_MINIMUM_NDB": ("ndb_item_range", "minimum"),
            "CATEGORY_EXAMPLE_CASE_NDB": ("ndb_category_examples", "case"),
            "CATEGORY_EXAMPLE_DETAIL_NDB": ("ndb_category_examples", "detail"),
            "CATEGORY_DESCRIPTION_NDB": ("ndb_category_description", "description"),
            #
            "DATA_TYPE_CODE_PDBX": ("pdbx_item_type", "code"),
            "ITEM_DESCRIPTION_PDBX": ("pdbx_item_description", "description"),
            "ENUMERATION_VALUE_PDBX": ("pdbx_item_enumeration", "value"),
            "ENUMERATION_DETAIL_PDBX": ("pdbx_item_enumeration", "detail"),
            "ENUMERATION_TYPE_UNITS_PDBX": ("pdbx_item_enumeration", "type_units_code"),
            "ENUMERATION_DETAIL_BRIEF_PDBX": ("pdbx_item_enumeration", "detail_brief"),
            "ITEM_MANDATORY_CODE_PDBX": ("pdbx_item", "mandatory_code"),
            "ITEM_EXAMPLE_CASE_PDBX": ("pdbx_item_examples", "case"),
            "ITEM_EXAMPLE_DETAIL_PDBX": ("pdbx_item_examples", "detail"),
            "ITEM_RANGE_MAXIMUM_PDBX": ("pdbx_item_range", "maximum"),
            "ITEM_RANGE_MINIMUM_PDBX": ("pdbx_item_range", "minimum"),
            "CATEGORY_EXAMPLE_CASE_PDBX": ("pdbx_category_examples", "case"),
            "CATEGORY_EXAMPLE_DETAIL_PDBX": ("pdbx_category_examples", "detail"),
            "CATEGORY_DESCRIPTION_PDBX": ("pdbx_category_description", "description"),
            #
            "CATEGORY_CONTEXT": ("pdbx_category_context", "type"),
            "CATEGORY_GROUP": ("category_group", "id"),
            "ITEM_CONTEXT": ("pdbx_item_context", "type"),
            "ENUMERATION_CLOSED_FLAG": ("pdbx_item_enumeration_details", "closed_flag"),
            #
            "ITEM_RELATED_FUNCTION_CODE": ("item_related", "function_code"),
            "ITEM_RELATED_RELATED_NAME": ("item_related", "related_name"),
            "ITEM_ALIAS_ALIAS_NAME": ("item_aliases", "alias_name"),
            "ITEM_ALIAS_DICTIONARY": ("item_aliases", "dictionary"),
            "ITEM_ALIAS_VERSION": ("item_aliases", "version"),
            "ITEM_DEPENDENT_DEPENDENT_NAME": ("item_dependent", "dependent_name"),
            "ITEM_SUB_CATEGORY_ID": ("item_sub_category", "id"),
            "ITEM_SUB_CATEGORY_LABEL": ("item_sub_category", "pdbx_label"),
            "ITEM_TYPE_CONDITIONS_CODE": ("item_type_conditions", "code"),
            #
            "ITEM_VALUE_CONDITION_DEPENDENT_NAME": ("pdbx_item_value_condition", "dependent_item_name"),
            #
            "ITEM_LINKED_PDBX_ID": ("pdbx_item_linked", "id"),
            "ITEM_LINKED_PDBX_CONDITION_ID": ("pdbx_item_linked", "condition_id"),
            "ITEM_LINKED_PDBX_PARENT_NAME": ("pdbx_item_linked", "parent_name"),
            "ITEM_LINKED_PDBX_CHILD_NAME": ("pdbx_item_linked", "child_name"),
            #
            "ITEM_LINKED_PDBX_CONDITION_CHILD_NAME": ("pdbx_item_linked", "condition_child_name"),
            "ITEM_LINKED_PDBX_CONDITION_CHILD_VALUE": ("pdbx_item_linked", "condition_child_value"),
            "ITEM_LINKED_PDBX_CONDITION_CHILD_TARGET_NAME": ("pdbx_item_linked", "condition_child_target_name"),
            "ITEM_LINKED_PDBX_CONDITION_CHILD_CMP_OP": ("pdbx_item_linked", "condition_child_cmp_op"),
            "ITEM_LINKED_PDBX_CONDITION_LOG_OP": ("pdbx_item_linked", "condition_log_op"),
        }
        #
        self.__methodDict = OrderedDict()
        self.__methodIndex = OrderedDict()
        #
        self.__makeIndex()
        self.__getMethods()
        #
        self.__fullParentD, self.__fullChildD = self.__makeFullParentChildDictionaries()
        #
        #
        self.__dataBlockDictList = []
        self.__dictionaryDictList = []
        #
        self.__subCategoryDict = OrderedDict()
        self.__categoryGroupDict = OrderedDict()
        self.__groupIndex = False
        self.__groupChildIndex = OrderedDict()
        #
        # Data sections -
        #
        self.__dictionaryHistoryList = []
        self.__itemUnitsDict = OrderedDict()
        self.__itemUnitsConversionList = []
        self.__itemLinkedGroupDict = OrderedDict()
        self.__itemLinkedGroupItemDict = OrderedDict()
        #
        self.__dictionaryIncludeDict = OrderedDict()
        self.__categoryIncludeDict = OrderedDict()
        self.__itemIncludeDict = OrderedDict()
        #
        self.__dictionaryComponentList = []
        self.__dictionaryComponentHistoryDict = OrderedDict()
        #
        self.__itemValueConditionDict = OrderedDict()
        self.__compOpDict = OrderedDict()
        #
        self.__getDataSections()
        #

    def testCache(self):
        return len(self.__containerList) > 0

    #
    #  Methods for data sections --
    #

    def getItemValueConditionDict(self):
        try:
            return self.__itemValueConditionDict if self.__itemValueConditionDict else {}
        except Exception:
            return {}

    def getComparisonOperators(self):
        try:
            return list(self.__compOpDict.keys()) if self.__compOpDict else []
        except Exception:
            return []

    def getComparisonOperatorDict(self):
        try:
            return self.__compOpDict if self.__compOpDict else {}
        except Exception:
            return {}

    #
    def getDictionaryVersion(self):
        try:
            return ",".join([str(tD["version"]) for tD in self.__dictionaryDictList])
        except Exception:
            return None

    def getDictionaryTitle(self):
        try:
            return ",".join([str(tD["title"]) for tD in self.__dictionaryDictList])
        except Exception:
            return None

    def getDictionaryUpdate(self, order="reverse"):
        """Get details from the first/last history element."""
        try:
            if order == "reverse":
                tD = self.__dictionaryHistoryList[-1]
            else:
                tD = self.__dictionaryHistoryList[0]

            return tD["update"]

        except Exception:
            return None

    def getDictionaryRevisionCount(self):
        """Get the count of revision history records."""
        try:
            return len(self.__dictionaryHistoryList)
        except Exception:
            return 0

    def getDictionaryHistory(self, order="reverse"):
        """Returns the revision history as a list of tuples [(version,update,revisionText,dictionary),...]"""
        oL = []
        try:
            if order == "reverse":
                for tD in reversed(self.__dictionaryHistoryList):
                    oL.append((tD["version"], tD["update"], tD["revision"], tD["dictionary"]))
            else:
                for tD in self.__dictionaryHistoryList:
                    oL.append((tD["version"], tD["update"], tD["revision"], tD["dictionary"]))
        except Exception:
            pass
        return oL

    #
    def getDictionaryComponentDetails(self):
        """Returns the component dictionary list as tuples [(version,title,dictionary_component_id),...]"""
        oL = []
        try:
            for tD in self.__dictionaryComponentList:
                oL.append((tD["version"], tD["title"], tD["dictionary_component_id"]))
        except Exception:
            pass
        return oL

    def getDictionaryComponentCount(self):
        """Get the count of dictionary components."""
        try:
            return len(self.__dictionaryComponentList)
        except Exception:
            return 0

    def getDictionaryComponents(self):
        """Get the list of dictionary components."""
        try:
            return list(self.__dictionaryComponentHistoryDict.keys())
        except Exception:
            return []

    def getDictionaryComponentHistory(self, dictionaryComponentId, order="reverse"):
        """Returns the revision history as a list of tuples [(version,update,revisionText,dictionary),...]"""
        oL = []
        try:
            if order == "reverse":
                for tD in reversed(self.__dictionaryComponentHistoryDict[dictionaryComponentId]):
                    oL.append((tD["version"], tD["update"], tD["revision"], tD["dictionary_component_id"]))
            else:
                for tD in self.__dictionaryComponentHistoryDict[dictionaryComponentId]:
                    oL.append((tD["version"], tD["update"], tD["revision"], tD["dictionary_component_id"]))
        except Exception:
            pass
        return oL

    #
    def __makeCategoryGroupIndex(self):
        catNameList = self.getCategoryList()
        # add categories in group to self.__categoryGroupDict[<groupName>]['categories']
        for catName in catNameList:
            groupNameList = self.getCategoryGroupList(catName)
            # logger.info("Category %s group list %r\n" % (catName,groupNameList))
            for groupName in groupNameList:
                if groupName not in self.__categoryGroupDict:
                    #  handle undefined category group ?
                    tD = OrderedDict()
                    tD["description"] = None
                    tD["parent_id"] = None
                    tD["categories"] = []
                    self.__categoryGroupDict[groupName] = tD
                self.__categoryGroupDict[groupName]["categories"].append(catName)
        #
        for groupName in self.__categoryGroupDict:
            # logger.info("Group %s count %r\n" % (groupName, len(self.__categoryGroupDict[groupName]['categories'])))
            if "categories" in self.__categoryGroupDict[groupName]:
                self.__categoryGroupDict[groupName]["categories"].sort()
        self.__groupChildIndex = OrderedDict()
        for groupName, gD in self.__categoryGroupDict.items():
            if "parent" in gD:
                self.__groupChildIndex.setdefault(gD["parent"], []).append(groupName)
        #
        self.__groupIndex = True

    #
    def getCategoryGroupDescription(self, groupName):
        try:
            return self.__categoryGroupDict[groupName]["description"]
        except Exception:
            return None

    def getCategoryGroupParent(self, groupName):
        try:
            return self.__categoryGroupDict[groupName]["parent_id"]
        except Exception:
            return None

    def getCategoryGroupChildGroups(self, parentGroupName):
        try:
            return self.__groupChildIndex[parentGroupName]
        except Exception:
            return []

    def getCategoryGroupCategories(self, groupName, followChildren=False):
        try:
            if not self.__groupIndex:
                self.__makeCategoryGroupIndex()
            #
            if followChildren:
                cL = []
                grpL = [groupName]
                grpL.extend(self.getCategoryGroupChildGroups(groupName))
                for grp in grpL:
                    cL.extend(self.__categoryGroupDict[grp]["categories"] if grp in self.__categoryGroupDict else [])
                return sorted(set(cL))
            else:
                return self.__categoryGroupDict[groupName]["categories"] if groupName in self.__categoryGroupDict else []
            #
        except Exception:
            logger.exception("DictionaryApi.getCategoryGroupCategories failed for group %s", groupName)
        return []

    def getCategoryGroups(self):
        try:
            kL = self.__categoryGroupDict.keys()
            return kL
        except Exception:
            return []

    #
    def getParentCategories(self, categoryName):
        itemNameList = self.getItemNameList(categoryName)
        parentCategories = set()
        for itemName in itemNameList:
            categoryName = CifName.categoryPart(itemName)
            attributeName = CifName.attributePart(itemName)
            parentItemList = self.getFullParentList(categoryName, attributeName)
            for parentItem in parentItemList:
                parentCategoryName = CifName.categoryPart(parentItem)
                parentCategories.add(parentCategoryName)
        return list(parentCategories)

    def getChildCategories(self, categoryName):
        itemNameList = self.getItemNameList(categoryName)
        childCategories = set()
        for itemName in itemNameList:
            categoryName = CifName.categoryPart(itemName)
            attributeName = CifName.attributePart(itemName)
            childItemList = self.getFullChildList(categoryName, attributeName)
            for childItem in childItemList:
                childCategoryName = CifName.categoryPart(childItem)
                childCategories.add(childCategoryName)
        return list(childCategories)

    #
    def definitionExists(self, definitionName):
        if definitionName in self.__definitionIndex:
            return True
        return False

    def getTypeConditionsCode(self, category, attribute):
        return self.__get("ITEM_TYPE_CONDITIONS_CODE", category, attribute)

    def getItemDependentNameList(self, category, attribute):
        return self.__getList("ITEM_DEPENDENT_DEPENDENT_NAME", category, attribute)

    def getItemValueConditionDependentList(self, category, attribute):
        return self.__getList("ITEM_VALUE_CONDITION_DEPENDENT_NAME", category, attribute)

    def getItemSubCategoryIdList(self, category, attribute):
        return self.__getList("ITEM_SUB_CATEGORY_ID", category, attribute)

    def getItemSubCategoryLabelList(self, category, attribute):
        return self.__getList("ITEM_SUB_CATEGORY_LABEL", category, attribute)

    def getItemSubCategoryList(self, category, attribute):
        aL = []

        itemName = CifName.itemName(category, attribute)

        obL = self.__definitionIndex[itemName] if itemName in self.__definitionIndex else None
        for ob in obL:
            tObj = ob.getObj(self.__enumD["ITEM_SUB_CATEGORY_ID"][0])
            if tObj is not None:
                atId = self.__enumD["ITEM_SUB_CATEGORY_ID"][1]
                atLabel = self.__enumD["ITEM_SUB_CATEGORY_LABEL"][1]
                for row in tObj.getRowList():
                    # logger.info("subcategories for %s row is %r" % (itemName, row))
                    idVal = row[tObj.getIndex(atId)] if tObj.hasAttribute(atId) else None
                    labVal = row[tObj.getIndex(atLabel)] if tObj.hasAttribute(atLabel) else None
                    aL.append((idVal, labVal))
        return aL

    def getItemAliasList(self, category, attribute):
        aNL = self.__getListAll("ITEM_ALIAS_ALIAS_NAME", category, attribute)
        aDL = self.__getListAll("ITEM_ALIAS_DICTIONARY", category, attribute)
        aVL = self.__getListAll("ITEM_ALIAS_VERSION", category, attribute)
        aL = []
        for aN, aD, aV in zip(aNL, aDL, aVL):
            aL.append((aN, aD, aV))
        return aL

    def getEnumListWithDetail(self, category, attribute):
        eVL = self.__getListAll("ENUMERATION_VALUE", category, attribute)
        eDL = self.__getListAll("ENUMERATION_DETAIL", category, attribute)
        rL = []
        dD = {}
        if len(eVL) == len(eDL):
            for eV, eD in zip(eVL, eDL):
                if not eD or eD in [".", "?"]:
                    dD[eV] = (eV, None)
                else:
                    dD[eV] = (eV, eD)
        else:
            for eV in eVL:
                dD[eV] = (eV, None)
        #
        for ky in sorted(dD.keys()):
            rL.append(dD[ky])
        return rL

    def getEnumListAltWithFullDetails(self, category, attribute):
        rL = []
        dD = {}
        try:
            eVL = self.__getListAll("ENUMERATION_VALUE_PDBX", category, attribute)
            eDL = self.__getListAll("ENUMERATION_DETAIL_PDBX", category, attribute)
            eBL = self.__getListAll("ENUMERATION_DETAIL_BRIEF_PDBX", category, attribute)
            eUL = self.__getListAll("ENUMERATION_TYPE_UNITS_PDBX", category, attribute)
            rL = []
            dD = {}
            for eV, eD, eB, eU in zip_longest(eVL, eDL, eBL, eUL):
                oL = [v if v and v not in [".", "?"] else None for v in [eV, eD, eB, eU]]
                dD[eV] = tuple(oL)
            for ky in sorted(dD.keys()):
                rL.append(dD[ky])
            if rL:
                return rL
            #
            eVL = self.__getListAll("ENUMERATION_VALUE", category, attribute)
            eDL = self.__getListAll("ENUMERATION_DETAIL", category, attribute)
            eBL = self.__getListAll("ENUMERATION_DETAIL_BRIEF", category, attribute)
            eUL = self.__getListAll("ENUMERATION_TYPE_UNITS", category, attribute)
            rL = []
            dD = {}
            for eV, eD, eB, eU in zip_longest(eVL, eDL, eBL, eUL):
                oL = [v if v and v not in [".", "?"] else None for v in [eV, eD, eB, eU]]
                dD[eV] = tuple(oL)
            for ky in sorted(dD.keys()):
                rL.append(dD[ky])
        except Exception as e:
            logger.exception("Failing dD %r rL %r with %s", dD, rL, str(e))
        return rL

    def getEnumListWithFullDetails(self, category, attribute):
        rL = []
        dD = {}
        try:
            eVL = self.__getListAll("ENUMERATION_VALUE", category, attribute)
            eDL = self.__getListAll("ENUMERATION_DETAIL", category, attribute)
            eBL = self.__getListAll("ENUMERATION_DETAIL_BRIEF", category, attribute)
            eUL = self.__getListAll("ENUMERATION_TYPE_UNITS", category, attribute)
            #
            for eV, eD, eB, eU in zip_longest(eVL, eDL, eBL, eUL):
                oL = [v if v and v not in [".", "?"] else None for v in [eV, eD, eB, eU]]
                dD[eV] = tuple(oL)
            for ky in sorted(dD.keys()):
                rL.append(dD[ky])
        except Exception as e:
            logger.info("eVL %r", eVL)
            logger.info("eDL %r", eDL)
            logger.info("eBL %r", eBL)
            logger.info("eUL %r", eUL)
            logger.exception("Failing category %s attribute %s dD %r rL %r with %s", category, attribute, dD, rL, str(e))
        return rL

    def getEnumListAltWithDetail(self, category, attribute):
        eVL = self.__getListAll("ENUMERATION_VALUE_PDBX", category, attribute)
        eDL = self.__getListAll("ENUMERATION_DETAIL_PDBX", category, attribute)

        rL = []
        dD = {}
        if len(eVL) == len(eDL):
            for eV, eD in zip(eVL, eDL):
                if not eD or eD in [".", "?"]:
                    dD[eV] = (eV, None)
                else:
                    dD[eV] = (eV, eD)
        else:
            for eV in eVL:
                dD[eV] = (eV, None)
        #
        for ky in sorted(dD.keys()):
            rL.append(dD[ky])
        #
        if not rL:
            return self.getEnumListWithDetail(category, attribute)
        else:
            return rL

    def getItemRelatedList(self, category, attribute):
        rNL = self.__getListAll("ITEM_RELATED_RELATED_NAME", category, attribute)
        rFL = self.__getListAll("ITEM_RELATED_FUNCTION_CODE", category, attribute)
        rL = []
        for rN, rF in zip(rNL, rFL):
            rL.append((rN, rF))
        return rL

    def getTypeCode(self, category, attribute):
        return self.__get("DATA_TYPE_CODE", category, attribute, followAncestors=True)

    def getTypeCodeAlt(self, category, attribute, fallBack=True):
        v = self.getTypeCodePdbx(category, attribute)
        if v is None:
            v = self.getTypeCodeNdb(category, attribute)
        if fallBack and v is None:
            v = self.getTypeCode(category, attribute)
        return v

    def getTypeCodeNdb(self, category, attribute):
        return self.__get("DATA_TYPE_CODE_NDB", category, attribute, followAncestors=False)

    def getTypeCodePdbx(self, category, attribute):
        return self.__get("DATA_TYPE_CODE_PDBX", category, attribute, followAncestors=False)

    def getDefaultValue(self, category, attribute):
        return self.__get("ITEM_DEFAULT_VALUE", category, attribute)

    def getMandatoryCode(self, category, attribute):
        return self.__get("ITEM_MANDATORY_CODE", category, attribute)

    def getMandatoryCodeAlt(self, category, attribute, fallBack=True):
        v = self.getMandatoryCodePdbx(category, attribute)
        if v is None:
            v = self.getMandatoryCodeNdb(category, attribute)
        if fallBack and v is None:
            v = self.getMandatoryCode(category, attribute)
        return v

    def getMandatoryCodeNdb(self, category, attribute):
        return self.__get("ITEM_MANDATORY_CODE_NDB", category, attribute)

    def getMandatoryCodePdbx(self, category, attribute):
        return self.__get("ITEM_MANDATORY_CODE_PDBX", category, attribute)

    def getTypeRegex(self, category, attribute):
        code = self.getTypeCode(category, attribute)
        if code in self.__typesDict:
            return self.__typesDict[code][1]
        return None

    def getTypeRegexAlt(self, category, attribute, fallBack=True):
        v = self.getTypeRegexPdbx(category, attribute)
        if v is None:
            v = self.getTypeRegexNdb(category, attribute)
        if fallBack and v is None:
            v = self.getTypeRegex(category, attribute)
        return v

    def getTypeRegexNdb(self, category, attribute):
        code = self.getTypeCodeNdb(category, attribute)
        if code in self.__typesDict:
            return self.__typesDict[code][1]
        return None

    def getTypeRegexPdbx(self, category, attribute):
        code = self.getTypeCodePdbx(category, attribute)
        if code in self.__typesDict:
            return self.__typesDict[code][1]
        return None

    def getTypePrimitive(self, category, attribute):
        code = self.getTypeCode(category, attribute)
        if code in self.__typesDict:
            return self.__typesDict[code][0]
        return None

    def getTypeDetail(self, category, attribute):
        code = self.getTypeCode(category, attribute)
        if code in self.__typesDict:
            return self.__typesDict[code][2]
        return None

    def getContextList(self, category, attribute):
        return self.__getList("ITEM_CONTEXT", category, attribute)

    def getCategoryContextList(self, category):
        return self.__getList("CATEGORY_CONTEXT", category, attribute=None)

    def getEnumList(self, category, attribute, sortFlag=True):
        if sortFlag:
            return self.__getList("ENUMERATION_VALUE", category, attribute)
        else:
            return self.__getListAll("ENUMERATION_VALUE", category, attribute)

    def getEnumListAlt(self, category, attribute, fallBack=True, sortFlag=True):
        vL = self.getEnumListPdbx(category, attribute, sortFlag=sortFlag)
        if not vL:
            vL = self.getEnumListNdb(category, attribute, sortFlag=sortFlag)
        if fallBack and not vL:
            vL = self.getEnumList(category, attribute, sortFlag=sortFlag)
        return vL

    def getEnumListNdb(self, category, attribute, sortFlag=True):
        if sortFlag:
            return self.__getList("ENUMERATION_VALUE_NDB", category, attribute)
        else:
            return self.__getListAll("ENUMERATION_VALUE_NDB", category, attribute)

    def getEnumListPdbx(self, category, attribute, sortFlag=True):
        if sortFlag:
            return self.__getList("ENUMERATION_VALUE_PDBX", category, attribute)
        else:
            return self.__getListAll("ENUMERATION_VALUE_PDBX", category, attribute)

    def isEnumerated(self, category, attribute):
        return len(self.__getList("ENUMERATION_VALUE", category, attribute)) > 0

    def isEnumeratedAlt(self, category, attribute, fallBack=True):
        eC = len(self.__getList("ENUMERATION_VALUE_PDBX", category, attribute))
        if eC == 0:
            eC = len(self.__getList("ENUMERATION_VALUE_NDB", category, attribute))
        if fallBack and (eC == 0):
            eC = len(self.__getList("ENUMERATION_VALUE", category, attribute))
        return eC > 0

    def getEnumerationClosedFlag(self, category, attribute):
        return self.__get("ENUMERATION_CLOSED_FLAG", category, attribute)

    def getUltimateParent(self, category, attribute):
        """Return the first ultimate parent item for the input item."""
        #        pL=self.__getList('ITEM_LINKED_PARENT',category,attribute)
        pL = self.getFullParentList(category, attribute)
        itemName = CifName.itemName(category, attribute)
        while pL and (pL[0] != itemName):
            attN = CifName.attributePart(pL[0])
            catN = CifName.categoryPart(pL[0])
            itemName = pL[0]
            pL = self.getFullParentList(catN, attN)
            # pL=self.__getList('ITEM_LINKED_PARENT',catN,attN)
        return itemName

    def getParentList(self, category, attribute, stripSelfParent=False):
        if stripSelfParent:
            itemName = CifName.itemName(category, attribute)
            pL = self.__getList("ITEM_LINKED_PARENT", category, attribute)
            if pL:
                try:
                    pL.remove(itemName)
                except Exception:
                    pass
            return pL
        else:
            return self.__getList("ITEM_LINKED_PARENT", category, attribute)

    def getChildList(self, category, attribute):
        return self.__getList("ITEM_LINKED_CHILD", category, attribute)

    def getFullChildList(self, category, attribute):
        try:
            itemName = CifName.itemName(category, attribute)
            return self.__fullChildD[itemName]
        except Exception:
            return []

    def getFullDescendentList(self, category, attribute):
        itemNameL = []
        try:
            itemName = CifName.itemName(category, attribute)
            itemNameL = self.__fullChildD[itemName] if itemName in self.__fullChildD else []
            itemNameL = list(set(itemNameL))
            if itemNameL:
                begLen = 0
                endLen = 1
                #
                while endLen > begLen:
                    begLen = len(itemNameL)
                    for itemName in itemNameL:
                        if itemName in self.__fullChildD:
                            itemNameL.extend(self.__fullChildD[itemName])
                    itemNameL = list(set(itemNameL))
                    endLen = len(itemNameL)

        except Exception as e:
            logger.exception("Failing for %s %s with %s", category, attribute, str(e))
        return itemNameL

    def getFullParentList(self, category, attribute, stripSelfParent=False):
        try:
            itemName = CifName.itemName(category, attribute)
            pL = self.__fullParentD[itemName]
            if stripSelfParent:
                if pL:
                    try:
                        pL.remove(itemName)
                    except Exception:
                        pass
                return pL
            else:
                return pL
        except Exception:
            return []

    def getUnits(self, category, attribute):
        return self.__get("ITEM_UNITS", category, attribute)

    def getImplicitList(self):
        iL = []
        for name, dL in self.__definitionIndex.items():
            for dD in dL:
                dType = dD.getType()
                if dType == "definition" and dD.isAttribute():
                    catN = CifName.categoryPart(name)
                    attN = CifName.attributePart(name)
                    if self.__get("ITEM_MANDATORY_CODE", catN, attN) == "implicit":
                        if name not in iL:
                            iL.append(name)
        return iL

    def getDescription(self, category, attribute):
        return self.__get("ITEM_DESCRIPTION", category, attribute)

    def getDescriptionAlt(self, category, attribute, fallBack=True):
        v = self.getDescriptionPdbx(category, attribute)
        if v is None:
            v = self.getDescriptionNdb(category, attribute)
        if fallBack and v is None:
            v = self.getDescription(category, attribute)
        return v

    def getDescriptionNdb(self, category, attribute):
        return self.__get("ITEM_DESCRIPTION_NDB", category, attribute)

    def getDescriptionPdbx(self, category, attribute):
        return self.__get("ITEM_DESCRIPTION_PDBX", category, attribute)

    def getExampleList(self, category, attribute):
        exCL = self.__getListAll("ITEM_EXAMPLE_CASE", category, attribute)
        exDL = self.__getListAll("ITEM_EXAMPLE_DETAIL", category, attribute)
        exL = []
        if len(exCL) == len(exDL):
            for exC, exD in zip(exCL, exDL):
                exL.append((exC, exD))
        else:
            for exC in exCL:
                exL.append((exC, None))
        return exL

    def getExampleListAlt(self, category, attribute, fallBack=True):
        vL = self.getExampleListPdbx(category, attribute)
        if not vL:
            vL = self.getExampleListNdb(category, attribute)
        if fallBack and not vL:
            vL = self.getExampleList(category, attribute)
        return vL

    def getExampleListNdb(self, category, attribute):
        exCL = self.__getListAll("ITEM_EXAMPLE_CASE_NDB", category, attribute)
        exDL = self.__getListAll("ITEM_EXAMPLE_DETAIL_NDB", category, attribute)
        exL = []
        if len(exCL) == len(exDL):
            for exC, exD in zip(exCL, exDL):
                exL.append((exC, exD))
        else:
            for exC in exCL:
                exL.append((exC, None))
        return exL

    def getExampleListPdbx(self, category, attribute):
        exCL = self.__getListAll("ITEM_EXAMPLE_CASE_PDBX", category, attribute)
        exDL = self.__getListAll("ITEM_EXAMPLE_DETAIL_PDBX", category, attribute)
        exL = []
        if len(exCL) == len(exDL):
            for exC, exD in zip(exCL, exDL):
                exL.append((exC, exD))
        else:
            for exC in exCL:
                exL.append((exC, None))
        return exL

    def getBoundaryList(self, category, attribute):
        minL = self.__getListAll("ITEM_RANGE_MINIMUM", category, attribute)
        maxL = self.__getListAll("ITEM_RANGE_MAXIMUM", category, attribute)
        bL = []
        for vMin, vMax in zip(minL, maxL):
            bL.append((vMin, vMax))
        return bL

    def getBoundaryListAlt(self, category, attribute, fallBack=True):
        vL = self.getBoundaryListPdbx(category, attribute)
        if not vL:
            vL = self.getBoundaryListNdb(category, attribute)
        if fallBack and not vL:
            vL = self.getBoundaryList(category, attribute)
        return vL

    def getBoundaryListNdb(self, category, attribute):
        minL = self.__getListAll("ITEM_RANGE_MINIMUM_NDB", category, attribute)
        maxL = self.__getListAll("ITEM_RANGE_MAXIMUM_NDB", category, attribute)
        bL = []
        for vMin, vMax in zip(minL, maxL):
            bL.append((vMin, vMax))
        #
        return bL

    def getBoundaryListPdbx(self, category, attribute):
        minL = self.__getListAll("ITEM_RANGE_MINIMUM_PDBX", category, attribute)
        maxL = self.__getListAll("ITEM_RANGE_MAXIMUM_PDBX", category, attribute)
        bL = []
        for vMin, vMax in zip(minL, maxL):
            bL.append((vMin, vMax))
        #
        return bL

    def getCategoryKeyList(self, category):
        return self.__getList("CATEGORY_KEY_ITEMS", category, attribute=None)

    def getCategoryGroupList(self, category):
        return self.__getList("CATEGORY_GROUP", category, attribute=None)

    def getCategoryMandatoryCode(self, category):
        return self.__get("CATEGORY_MANDATORY_CODE", category, attribute=None)

    def getCategoryDescription(self, category):
        return self.__get("CATEGORY_DESCRIPTION", category, attribute=None)

    def getCategoryNxMappingDetails(self, category):
        return self.__get("CATEGORY_NX_MAPPING_DETAILS", category, attribute=None)

    def getCategoryDescriptionAlt(self, category, fallBack=True):
        v = self.getCategoryDescriptionPdbx(category)
        if v is None:
            v = self.getCategoryDescriptionNdb(category)
        if fallBack and v is None:
            v = self.getCategoryDescription(category)
        return v

    def getCategoryDescriptionNdb(self, category):
        val = self.__get("CATEGORY_DESCRIPTION_NDB", category, attribute=None)
        return val

    def getCategoryDescriptionPdbx(self, category):
        val = self.__get("CATEGORY_DESCRIPTION_PDBX", category, attribute=None)
        return val

    def getCategoryExampleList(self, category):
        exCL = self.__getListAll("CATEGORY_EXAMPLE_CASE", category, attribute=None)
        exDL = self.__getListAll("CATEGORY_EXAMPLE_DETAIL", category, attribute=None)
        exL = []
        if len(exCL) == len(exDL):
            for exC, exD in zip(exCL, exDL):
                exL.append((exC, exD))
        else:
            for exC in exCL:
                exL.append((exC, None))
        return exL

    def getCategoryExampleListAlt(self, category, fallBack=True):
        vL = self.getCategoryExampleListPdbx(category)
        if not vL:
            vL = self.getCategoryExampleListNdb(category)
        if fallBack and not vL:
            vL = self.getCategoryExampleList(category)
        return vL

    def getCategoryExampleListNdb(self, category):
        exCL = self.__getListAll("CATEGORY_EXAMPLE_CASE_NDB", category, attribute=None)
        exDL = self.__getListAll("CATEGORY_EXAMPLE_DETAIL_NDB", category, attribute=None)
        exL = []
        if len(exCL) == len(exDL):
            for exC, exD in zip(exCL, exDL):
                exL.append((exC, exD))
        else:
            for exC in exCL:
                exL.append((exC, None))
        return exL

    def getCategoryExampleListPdbx(self, category):
        exCL = self.__getListAll("CATEGORY_EXAMPLE_CASE_PDBX", category, attribute=None)
        exDL = self.__getListAll("CATEGORY_EXAMPLE_DETAIL_PDBX", category, attribute=None)
        exL = []
        if len(exCL) == len(exDL):
            for exC, exD in zip(exCL, exDL):
                exL.append((exC, exD))
        else:
            for exC in exCL:
                exL.append((exC, None))

        return exL

    def getParentDictionary(self):
        """Create a dictionary of parents relations accross all definnitions
        as {child : [parent, parent,...]

        Exclude self parents.
        """
        parentD = {}
        pAtN = self.__enumD["ITEM_LINKED_PARENT"][1]
        cAtN = self.__enumD["ITEM_LINKED_CHILD"][1]

        for dObj in self.__containerList:
            dc = dObj.getObj(self.__enumD["ITEM_LINKED_PARENT"][0])
            if dc is not None:
                idxP = dc.getIndex(pAtN)
                idxC = dc.getIndex(cAtN)
                for row in dc.getRowList():
                    pVal = row[idxP]
                    cVal = row[idxC]
                    if pVal == cVal:
                        continue
                    if cVal not in parentD:
                        parentD[cVal] = []
                    parentD[cVal].append(pVal)
        #
        return parentD

    def getItemLinkedConditions(self):
        """Create a dictionary of conditional item link relationships.

        Returns:
         (dict):  {{parent_name, child_name}: [{"id": , "condition_id": , "condition_child_name": , "condition_child_value": ,
                                                "condition_child_cmp_op": , "condition_log_op": ,}, {},...]}

        Example:

        loop_
        _pdbx_item_linked.id
        _pdbx_item_linked.condition_id
        _pdbx_item_linked.parent_name
        _pdbx_item_linked.child_name
        #
        _pdbx_item_linked.condition_child_name
        _pdbx_item_linked.condition_child_value
        _pdbx_item_linked.condition_child_cmp_op
        _pdbx_item_linked.condition_child_target_name
        _pdbx_item_linked.condition_child_log_op
        1 1 '_entity_poly_seq.num'  '_atom_site.label_seq_id'  '_atom_site.label_entity_id'  .            'eq'  '_entity.id'  .
        2 1 '_entity_poly_seq.num'  '_atom_site.label_seq_id'  '_entity.type'              'polymer'      'eq'  .             'and'

        """
        rD = OrderedDict()
        try:
            for ob in self.__containerList:
                if ob.getType() == "data":
                    continue
                tl = ob.getObj(self.__enumD["ITEM_LINKED_PDBX_ID"][0])
                if tl is not None:
                    for row in tl.getRowList():
                        if (
                            tl.hasAttribute(self.__enumD["ITEM_LINKED_PDBX_ID"][1])
                            and tl.hasAttribute(self.__enumD["ITEM_LINKED_PDBX_CONDITION_ID"][1])
                            and tl.hasAttribute(self.__enumD["ITEM_LINKED_PDBX_CHILD_NAME"][1])
                            and tl.hasAttribute(self.__enumD["ITEM_LINKED_PDBX_PARENT_NAME"][1])
                        ):
                            tD = OrderedDict()
                            tD["id"] = row[tl.getIndex(self.__enumD["ITEM_LINKED_PDBX_ID"][1])]
                            tD["condition_id"] = row[tl.getIndex(self.__enumD["ITEM_LINKED_PDBX_CONDITION_ID"][1])]
                            parentName = row[tl.getIndex(self.__enumD["ITEM_LINKED_PDBX_PARENT_NAME"][1])]
                            childName = row[tl.getIndex(self.__enumD["ITEM_LINKED_PDBX_CHILD_NAME"][1])]
                            #
                            tD["condition_child_name"] = (
                                row[tl.getIndex(self.__enumD["ITEM_LINKED_PDBX_CONDITION_CHILD_NAME"][1])]
                                if tl.hasAttribute(self.__enumD["ITEM_LINKED_PDBX_CONDITION_CHILD_NAME"][1])
                                else None
                            )
                            tD["condition_child_value"] = (
                                row[tl.getIndex(self.__enumD["ITEM_LINKED_PDBX_CONDITION_CHILD_VALUE"][1])]
                                if tl.hasAttribute(self.__enumD["ITEM_LINKED_PDBX_CONDITION_CHILD_VALUE"][1])
                                else None
                            )
                            tD["condition_child_cmp_op"] = (
                                row[tl.getIndex(self.__enumD["ITEM_LINKED_PDBX_CONDITION_CHILD_CMP_OP"][1])]
                                if tl.hasAttribute(self.__enumD["ITEM_LINKED_PDBX_CONDITION_CHILD_CMP_OP"][1])
                                else None
                            )
                            tD["condition_child_target_name"] = (
                                row[tl.getIndex(self.__enumD["ITEM_LINKED_PDBX_CONDITION_CHILD_TARGET_NAME"][1])]
                                if tl.hasAttribute(self.__enumD["ITEM_LINKED_PDBX_CONDITION_CHILD_TARGET_NAME"][1])
                                else None
                            )
                            tD["condition_log_op"] = (
                                row[tl.getIndex(self.__enumD["ITEM_LINKED_PDBX_CONDITION_LOG_OP"][1])]
                                if tl.hasAttribute(self.__enumD["ITEM_LINKED_PDBX_CONDITION_LOG_OP"][1])
                                else None
                            )
                            #
                            rD.setdefault((parentName, childName), []).append(tD)
        except Exception as e:
            logger.exception("Failing with %s", str(e))

        return rD

    def __makeFullParentChildDictionaries(self):
        """Create a dictionaries of full parent/child relations accross all definnitions

        as  fullParentD[child]=[parent,parent,...]
        and fullChildD[parent]=[child,child,...]

        Exclude self parents.
        """
        fullParentD = {}
        fullChildD = {}
        pAtN = self.__enumD["ITEM_LINKED_PARENT"][1]
        cAtN = self.__enumD["ITEM_LINKED_CHILD"][1]

        for dObj in self.__containerList:
            # logger.info("\n\nSearching object  %s\n" % dObj.getName())
            dc = dObj.getObj(self.__enumD["ITEM_LINKED_PARENT"][0])
            if dc is not None:
                idxP = dc.getIndex(pAtN)
                idxC = dc.getIndex(cAtN)
                for row in dc.getRowList():
                    pVal = row[idxP]
                    cVal = row[idxC]
                    # logger.info("%s found parent %s child %s \n" % (dObj.getName(),pVal,cVal))
                    if pVal == cVal:
                        continue
                    if cVal not in fullParentD:
                        fullParentD[cVal] = []
                    fullParentD[cVal].append(pVal)
                    #
                    if pVal not in fullChildD:
                        fullChildD[pVal] = []
                    fullChildD[pVal].append(cVal)

        #
        return fullParentD, fullChildD

    #
    def __get(self, enumCode, category, attribute=None, followAncestors=False):
        """Return the last occurrence of the input dictionary metadata.  If the value
        for the input category/attribute is null/missing then optionally check for
        an ancestor value.
        """
        v0 = self.__getValue(enumCode, category, attribute)
        if not followAncestors:
            return v0
        else:
            if (v0 is None) or (not v0) or (v0 in [".", "?"]):
                pItem = self.getUltimateParent(category, attribute)
                if (pItem is not None) and pItem and (pItem != CifName.itemName(category, attribute)):
                    logger.debug("Reassigning enum code %s  category %s attribute %s to parent %r", enumCode, category, attribute, pItem)
                    return self.__getValue(enumCode, CifName.categoryPart(pItem), CifName.attributePart(pItem))
        return v0

    #
    def __getValue(self, enumCode, category, attribute=None):
        """Returns the last occurrence of the input dictionary metadata (enumCode) for the input category/attribute
        encountered in the list of objects stored at the indicated definition index.

        """
        eS = None
        if enumCode not in self.__enumD:
            return eS

        if attribute is not None:
            nm = "_" + category + "." + attribute
        else:
            nm = category

        if nm in self.__definitionIndex:
            dObjL = self.__definitionIndex[nm]
            for dObj in dObjL:
                dc = dObj.getObj(self.__enumD[enumCode][0])
                if dc is not None:
                    atN = self.__enumD[enumCode][1]
                    rL = dc.getRowList()
                    if rL:
                        row = rL[0]
                        if atN is not None:
                            if dc.hasAttribute(atN):
                                eS = row[dc.getIndex(atN)]
                        else:
                            eS = [rv for rv in row]
        return eS

    def __getList(self, enumCode, category, attribute=None):
        """ Return the list of unique values """
        return list(set(self.__getListAll(enumCode, category, attribute)))

    def __getListAll(self, enumCode, category, attribute=None):
        """ Return a list of all values  """
        eL = []
        if enumCode not in self.__enumD:
            return eL

        if attribute is not None:
            nm = "_" + category + "." + attribute
        else:
            nm = category

        if nm in self.__definitionIndex:
            dObjL = self.__definitionIndex[nm]
            for dObj in dObjL:
                dc = dObj.getObj(self.__enumD[enumCode][0])
                if dc is not None:
                    atN = self.__enumD[enumCode][1]
                    for row in dc.getRowList():
                        if atN is not None:
                            if dc.hasAttribute(atN):
                                eL.append(row[dc.getIndex(atN)])
                        else:
                            eL = [rv for rv in row]

        return eL

    def getMethodIndex(self):
        return self.__methodIndex

    def __makeIndex(self):
        """Create indices of definitions, categories and items."""
        iD = OrderedDict()
        for dD in self.__containerList:
            name = dD.getName()
            dType = dD.getType()
            #
            if name not in self.__fullIndex:
                self.__fullIndex[name] = []
            self.__fullIndex[name].append(dD)
            #
            if dType == "definition" and dD.isCategory():
                if name not in self.__catNameIndex:
                    self.__catNameIndex[name] = []
                if name not in self.__catNameItemIndex:
                    self.__catNameItemIndex[name] = []
                if name not in self.__definitionIndex:
                    self.__definitionIndex[name] = []
                self.__definitionIndex[name].append(dD)

            elif dType == "definition" and dD.isAttribute():
                catN = CifName.categoryPart(name)
                attN = CifName.attributePart(name)
                if catN not in self.__catNameItemIndex:
                    self.__catNameItemIndex[catN] = []
                if name not in self.__catNameItemIndex:
                    self.__catNameItemIndex[catN].append(name)

                if catN not in self.__catNameIndex:
                    self.__catNameIndex[catN] = []
                if attN not in self.__catNameIndex[catN]:
                    self.__catNameIndex[catN].append(attN)
                if name not in self.__definitionIndex:
                    self.__definitionIndex[name] = []
                self.__definitionIndex[name].append(dD)
                iD[name] = name
            elif dType == "data":
                for nm in dD.getObjNameList():
                    if nm not in self.__dataIndex:
                        self.__dataIndex[nm] = dD.getObj(nm)
            else:
                pass
        #
        self.__itemNameList = list(iD.keys())

    def getDefinitionIndex(self):
        return self.__definitionIndex

    def getFullIndex(self):
        return self.__fullIndex

    def getMethod(self, mId):
        if mId in self.__methodDict:
            return self.__methodDict[mId]
        else:
            return None

    def getCategoryList(self):
        return list(self.__catNameIndex.keys())

    def getCategoryIndex(self):
        return self.__catNameIndex

    def getAttributeNameList(self, category):
        try:
            return self.__catNameIndex[category]
        except Exception:
            pass
        return []

    def getItemNameList(self, category):
        try:
            return self.__catNameItemIndex[category]
        except Exception:
            pass
        return []

    def getSubCategoryDescription(self, subCategoryName):
        if subCategoryName in self.__subCategoryDict:
            return self.__subCategoryDict[subCategoryName]
        else:
            return ""

    def __getMethods(self):
        self.__methodDict = OrderedDict()
        self.__methodIndex = OrderedDict()
        for ob in self.__containerList:
            if ob.getType() == "data":
                ml = ob.getObj("method_list")
                if ml is not None:
                    # Use row order as priority
                    for ii, row in enumerate(ml.getRowList(), 1):
                        if ml.hasAttribute("id") and ml.hasAttribute("code") and ml.hasAttribute("language") and ml.hasAttribute("implementation_source"):
                            tInline = row[ml.getIndex("inline")] if ml.hasAttribute("inline") else None
                            tImpl = row[ml.getIndex("implementation")] if ml.hasAttribute("implementation") else None
                            mth = MethodDefinition(
                                row[ml.getIndex("id")], row[ml.getIndex("code")], row[ml.getIndex("language")], tInline, ii, tImpl, row[ml.getIndex("implementation_source")]
                            )
                            self.__methodDict[row[ml.getIndex("id")]] = mth

                ml = ob.getObj("datablock_methods")
                if ml is not None:
                    for row in ml.getRowList():
                        if ml.hasAttribute("method_id"):
                            # mth = MethodReference(row[ml.getIndex('method_id')], 'datablock', ob.getName(), None)
                            mth = MethodReference(row[ml.getIndex("method_id")], "datablock", None, None)
                            if ob.getName() in self.__methodIndex:
                                self.__methodIndex[ob.getName()].append(mth)
                            else:
                                self.__methodIndex[ob.getName()] = []
                                self.__methodIndex[ob.getName()].append(mth)
            elif ob.getType() == "definition":
                mi = ob.getObj("category_methods")
                if mi is not None:
                    for row in mi.getRowList():
                        if mi.hasAttribute("method_id"):
                            mth = MethodReference(row[mi.getIndex("method_id")], "category", ob.getName(), None)
                            if ob.getName() in self.__methodIndex:
                                self.__methodIndex[ob.getName()].append(mth)
                            else:
                                self.__methodIndex[ob.getName()] = []
                                self.__methodIndex[ob.getName()].append(mth)
                mi = ob.getObj("item_methods")
                if mi is not None:
                    for row in mi.getRowList():
                        if mi.hasAttribute("method_id"):
                            mth = MethodReference(row[mi.getIndex("method_id")], "attribute", CifName.categoryPart(ob.getName()), CifName.attributePart(ob.getName()))
                            if ob.getName() in self.__methodIndex:
                                self.__methodIndex[ob.getName()].append(mth)
                            else:
                                self.__methodIndex[ob.getName()] = []
                                self.__methodIndex[ob.getName()].append(mth)
            else:
                pass
        return self.__methodIndex

    def dumpCategoryIndex(self, fh=sys.stdout):
        for k, vL in self.__catNameIndex.items():
            uvL = list(set(vL))
            fh.write("Category: %s has %d attributes\n" % (k, len(uvL)))
            for v in sorted(uvL):
                fh.write("  Attribute: %s\n" % v)

    def dumpMethods(self, fh=sys.stdout):
        for k, vL in self.__methodIndex.items():
            fh.write("Method index key: %s length %d\n" % (k, len(vL)))
            for v in vL:
                v.printIt(fh)
        #
        fh.write("Inline method details\n")
        for k, vL in self.__methodIndex.items():
            fh.write("\n------------------------------------\n")
            fh.write("Method index key: %s\n" % k)
            for v in vL:
                fh.write("Method ID: %r\n" % v.getId())
                if self.getMethod(v.getId()):
                    fh.write("%r" % v)
                    # fh.write("Method text: %s\n" % self.getMethod(v.getId()).getInline())
                else:
                    fh.write("Missing method for %r" % v.getId())

    def dumpEnumFeatures(self, fh=sys.stdout):
        for k, vL in self.__catNameIndex.items():
            uvL = list(set(vL))
            for v in sorted(uvL):
                itL = self.getEnumList(k, v)
                if itL:
                    fh.write("-----------------------------------------------\n")
                    fh.write("       Category : %s\n" % k)
                    fh.write("       Attribute: %s\n" % v)
                    fh.write("     Description: \n%s\n" % self.getDescription(k, v))
                    fh.write("            Type: %s\n" % self.getTypeCode(k, v))
                    fh.write("  Primitive type: %s\n" % self.getTypePrimitive(k, v))
                    fh.write("      Regex type: %s\n" % self.getTypeRegex(k, v))
                    fh.write("      Enum list length %d\n" % len(itL))
                    for it in itL:
                        fh.write("      Enum: %s\n" % it)

    def dumpFeatures(self, fh=sys.stdout):
        for k, vL in self.__catNameIndex.items():
            uvL = list(set(vL))
            fh.write("-----------------------------------------------\n")
            fh.write("Category: %s has %d attributes\n" % (k, len(uvL)))
            fh.write("     Category description: %s\n" % self.getCategoryDescription(k))
            fh.write(" Alt category description: %s\n" % self.getCategoryDescriptionAlt(k))

            fh.write("         Category context: %s\n" % self.getCategoryContextList(k))

            ctL = self.getCategoryExampleList(k)
            if ctL:
                fh.write("    Category example list length %d\n" % len(ctL))
                for ct1, ct2 in ctL:
                    fh.write("      Example   case: %s\n" % ct1)
                    fh.write("      Example detail: %s\n" % ct2)

            ctL = self.getCategoryExampleListAlt(k)
            if ctL:
                fh.write("    Alt category example list length %d\n" % len(ctL))
                for ct1, ct2 in ctL:
                    fh.write("     Alt example   case: %s\n" % ct1)
                    fh.write("     Alt example detail: %s\n" % ct2)

            for v in sorted(uvL):
                fh.write("  Attribute: %s\n" % v)
                fh.write("     Description: %s\n" % self.getDescription(k, v))
                fh.write(" Alt description: %s\n" % self.getDescriptionAlt(k, v))
                fh.write("            Type: %s\n" % self.getTypeCode(k, v))
                fh.write("        Alt Type: %s\n" % self.getTypeCodeAlt(k, v))
                fh.write("  Primitive type: %s\n" % self.getTypePrimitive(k, v))
                fh.write("      Regex type: %s\n" % self.getTypeRegex(k, v))
                fh.write("         Context: %s\n" % self.getContextList(k, v))
                #
                fh.write(" Type conditions: %s\n" % self.getTypeConditionsCode(k, v))
                fh.write("   Subcategories: %s\n" % self.getItemSubCategoryIdList(k, v))
                #
                itL = self.getEnumList(k, v)
                if itL:
                    fh.write("      Enum list length %d\n" % len(itL))
                    for it in itL:
                        fh.write("      Enum: %s\n" % it)

                itL = self.getParentList(k, v)
                if itL:
                    fh.write("    Parent list length %d\n" % len(itL))
                    for it in itL:
                        fh.write("      Parent: %s\n" % it)
                itL = self.getChildList(k, v)
                if itL:
                    fh.write("    Child list length %d\n" % len(itL))
                    for it in itL:
                        fh.write("      Child: %s\n" % it)

                itL = self.getExampleList(k, v)
                if itL:
                    fh.write("    Example list length %d\n" % len(itL))
                    for it1, it2 in itL:
                        fh.write("      Example   case: %s\n" % it1)
                        fh.write("      Example detail: %s\n" % it2)

                itL = self.getBoundaryList(k, v)
                if itL:
                    fh.write("    Boundary list length %d\n" % len(itL))
                    for (it1, it2) in itL:
                        fh.write("      Boundary condition (min,max):  (%s,%s)\n" % (it1, it2))

                itL = self.getEnumListAlt(k, v)
                if itL:
                    fh.write("      Alt enum list length %d\n" % len(itL))
                    for it in itL:
                        fh.write("      Alt enum: %s\n" % it)

                itL = self.getExampleListAlt(k, v)
                if itL:
                    fh.write("    Alt example list length %d\n" % len(itL))
                    for it1, it2 in itL:
                        fh.write("      Alt example   case: %s\n" % it1)
                        fh.write("      Alt example detail: %s\n" % it2)

                itL = self.getBoundaryListAlt(k, v)
                if itL:
                    fh.write("    Alt boundary list length %d\n" % len(itL))
                    for (it1, it2) in itL:
                        fh.write("      Alt boundary condition (min,max):  (%s,%s)\n" % (it1, it2))

                itL = self.getItemRelatedList(k, v)
                if itL:
                    fh.write("    Related name list length %d\n" % len(itL))
                    for (it1, it2) in itL:
                        fh.write("      Related item name   %s function code %s\n" % (it1, it2))

                itL = self.getItemAliasList(k, v)
                if itL:
                    fh.write("    Alias name list length %d\n" % len(itL))
                    for (it1, it2, it3) in itL:
                        fh.write("      Alias name   %s dictionary %s version %s\n" % (it1, it2, it3))

                itL = self.getItemDependentNameList(k, v)
                if itL:
                    fh.write("    Dependent name list length %d\n" % len(itL))
                    for it1 in itL:
                        fh.write("      Dependent item name   %s\n" % it1)

    def dumpDataSections(self, fh=sys.stdout):
        fh.write("Datablock:  %r\n" % list(self.__dataBlockDictList))
        fh.write("Dictionary: %r\n" % list(self.__dictionaryDictList))
        fh.write("Dictionary History: %r\n" % self.__dictionaryHistoryList)
        fh.write("Subcategories: %r\n" % list(self.__subCategoryDict.items()))
        fh.write("Category groups:  %r\n" % list(self.__categoryGroupDict.items()))
        fh.write("Item units:  %r\n" % list(self.__itemUnitsDict.items()))
        fh.write("Item units conversions: %r \n" % self.__itemUnitsConversionList)
        fh.write("Item linked groups: %r\n" % list(self.__itemLinkedGroupDict.items()))
        fh.write("Item linked group item list: %r\n" % list(self.__itemLinkedGroupItemDict.items()))

    def dumpItemLinkedGroups(self, fh=sys.stdout):
        for categoryId, lgList in self.__itemLinkedGroupDict.items():
            for lg in lgList:
                if (categoryId, lg[1]) in self.__itemLinkedGroupItemDict:
                    fh.write("  Category  %s   linked group %s:\n" % (categoryId, lg[1]))
                    lgIList = self.__itemLinkedGroupItemDict[(categoryId, lg[1])]
                    for lgI in lgIList:
                        fh.write("    group %s --- child item %s   parent item %s\n" % (lg[1], lgI[0], lgI[1]))

    def __addItemLinkToDef(self, dObj, parentName, childName):
        """Add the input link relationship to the input definition object."""
        if dObj.exists("item_linked"):
            # update in place --
            cObj = dObj.getObj("item_linked")
            iFound = False
            idxP = cObj.getIndex("parent_name")
            idxC = cObj.getIndex("child_name")
            for row in cObj.getRowList():
                if parentName == row[idxP] and childName == row[idxC]:
                    iFound = True
                    break
            if not iFound:
                nRows = cObj.getRowCount()
                cObj.setValue(childName, "child_name", nRows)
                cObj.setValue(parentName, "parent_name", nRows)
                logger.debug("Appending item link in category %s", dObj.getName())
            return True
        else:
            # create new category and append to input object
            cObj = DataCategory("item_linked", attributeNameList=["child_name", "parent_name"])
            cObj.append([childName, parentName])
            dObj.append(cObj)
            logger.debug("Created new item link in category %s", dObj.getName())
            return True

    def __expandLoopedDefinitions(self):
        """Handle definitions containing looped item and item_linked categories --"""
        fullIndex = OrderedDict()
        for dD in self.__containerList:
            name = dD.getName()
            if name not in fullIndex:
                fullIndex[name] = []
            fullIndex[name].append(dD)

        for name, dObjL in fullIndex.items():
            if dObjL:
                ob = dObjL[0]
                if (ob.getType() == "definition") and ob.exists("item_linked"):
                    cObj = ob.getObj("item_linked")
                    if cObj.getRowCount() > 0:
                        idxP = cObj.getIndex("parent_name")
                        idxC = cObj.getIndex("child_name")
                        itemName = ob.getName()
                        logger.debug("Current target item %s", itemName)
                        cObjNext = DataCategory("item_linked", attributeNameList=["child_name", "parent_name"])
                        #
                        # Distribute the data for each row --
                        iChanges = 0
                        for row in cObj.getRowList():
                            #
                            parentItemName = row[idxP]
                            childItemName = row[idxC]
                            if parentItemName == childItemName:
                                continue
                            if childItemName != itemName:
                                iChanges += 1
                                if childItemName in fullIndex:
                                    #
                                    # Add this p/c link to the child definition -
                                    #
                                    self.__addItemLinkToDef(fullIndex[childItemName][0], parentItemName, childItemName)
                                else:
                                    # error missing child definition object.
                                    logger.warning("Missing child item %s", childItemName)
                            else:
                                cObjNext.append([row[idxC], row[idxP]])
                        if cObjNext.getRowCount() > 0:
                            ob.replace(cObjNext)
                        else:
                            ob.remove("item_linked")

    def __consolidateDefinitions(self):
        """Consolidate definitions into a single save frame section per definition."""
        fullIndex = OrderedDict()
        for dD in self.__containerList:
            name = dD.getName()
            if name not in fullIndex:
                fullIndex[name] = []
            fullIndex[name].append(dD)

        # preserve the original order of sections -
        #
        nList = []
        for dObj in self.__containerList:
            nm = dObj.getName()
            if nm not in nList:
                nList.append(nm)
        #
        for name, dObjL in fullIndex.items():
            if len(dObjL) > 1:
                for dD in dObjL[1:]:
                    xList = dD.getObjNameList()
                    for nm in xList:
                        if nm not in dObjL[0].getObjNameList():
                            logger.debug("Adding %s to %s", nm, name)
                            catObj = dD.getObj(nm)
                            dObjL[0].append(catObj)
                        elif self.__replaceDefinition:
                            logger.debug("Replacing dictionary %s in %s", nm, name)
                            catObj = dD.getObj(nm)
                            dObjL[0].replace(catObj)

        # create a new list of consolidated objects in original list order
        dList = []
        for nm in nList:
            if nm in fullIndex:
                dl = fullIndex[nm]
                dList.append(dl[0])
            else:
                logger.info("+DictionaryApi().__consolidate() missing object name %s", nm)
        # update lists
        self.__containerList = dList

    def getDataTypeList(self):
        """Return list of tuples containing ('code','primitive_code','construct','detail' )"""
        rowList = []
        for code in sorted(self.__typesDict.keys()):
            tup = self.__typesDict[code]
            rowList.append((code, tup[0], tup[1], tup[2]))
        return rowList

    def getSubCategoryList(self):
        """Return list of tuples containing ('id', 'description')"""
        rowList = []
        for tId in sorted(self.__subCategoryDict.keys()):
            description = self.__subCategoryDict[tId]
            rowList.append((tId, description))
        return rowList

    def getUnitsList(self):
        """Return list of tuples containing ('id', 'description')"""
        rowList = []
        for tId in sorted(self.__itemUnitsDict.keys()):
            description = self.__itemUnitsDict[tId]
            rowList.append((tId, description))
        return rowList

    def getUnitsConversionList(self):
        """Return list of tuples containing ('from_code','to_code','operator','factor')"""
        return self.__itemUnitsConversionList

    def __getDataSections(self):
        """"""
        for ob in self.__containerList:

            if ob.getType() == "data":
                logger.debug("Adding data sections from container name %s  type  %s", ob.getName(), ob.getType())
                #  add detail to data type tuple
                tl = ob.getObj("item_type_list")
                if tl is not None:
                    for row in tl.getRowList():
                        if tl.hasAttribute("code") and tl.hasAttribute("primitive_code") and tl.hasAttribute("construct") and tl.hasAttribute("detail"):
                            self.__typesDict[row[tl.getIndex("code")]] = (row[tl.getIndex("primitive_code")], row[tl.getIndex("construct")], row[tl.getIndex("detail")])

                tl = ob.getObj("datablock")
                if tl is not None:
                    rL = tl.getRowList()
                    if rL:
                        if tl.hasAttribute("id") and tl.hasAttribute("description"):
                            tD = OrderedDict()
                            row = rL[0]
                            tD["id"] = row[tl.getIndex("id")]
                            tD["description"] = row[tl.getIndex("description")]
                            self.__dataBlockDictList.append(tD)

                tl = ob.getObj("dictionary")
                if tl is not None:
                    rL = tl.getRowList()
                    if rL:
                        tD = OrderedDict()
                        row = rL[0]
                        if tl.hasAttribute("datablock_id"):
                            tD["datablock_id"] = row[tl.getIndex("datablock_id")]
                        if tl.hasAttribute("title"):
                            tD["title"] = row[tl.getIndex("title")]
                        if tl.hasAttribute("version"):
                            tD["version"] = row[tl.getIndex("version")]
                        self.__dictionaryDictList.append(tD)
                tl = ob.getObj("dictionary_history")
                if tl is not None:
                    # history as a list of dictionaries -
                    dName = ob.getName()
                    for row in tl.getRowList():
                        if tl.hasAttribute("version") and tl.hasAttribute("revision") and tl.hasAttribute("update"):
                            tD = OrderedDict()
                            tD["version"] = row[tl.getIndex("version")]
                            tD["revision"] = row[tl.getIndex("revision")]
                            tD["update"] = row[tl.getIndex("update")]
                            tD["dictionary"] = dName
                            self.__dictionaryHistoryList.append(tD)

                # JDW
                tl = ob.getObj("pdbx_include_dictionary")
                if tl is not None:
                    for row in tl.getRowList():
                        tD = OrderedDict()
                        if tl.hasAttribute("dictionary_id"):
                            tD["dictionary_id"] = row[tl.getIndex("dictionary_id")]
                        if tl.hasAttribute("dictionary_locator"):
                            tD["dictionary_locator"] = row[tl.getIndex("dictionary_locator")]
                        if tl.hasAttribute("include_mode"):
                            tD["include_mode"] = row[tl.getIndex("include_mode")]
                        if tl.hasAttribute("dictionary_namespace"):
                            tD["dictionary_namespace_prefix"] = row[tl.getIndex("dictionary_namespace_prefix")]
                        if tl.hasAttribute("dictionary_namespace_replace"):
                            tD["dictionary_namespace_prefix"] = row[tl.getIndex("dictionary_namespace_prefix_replace")]
                        #
                        self.__dictionaryIncludeDict[tD["dictionary_id"]] = tD
                    #
                    tl = ob.getObj("pdbx_include_category")
                    if tl is not None:
                        for row in tl.getRowList():
                            tD = OrderedDict()
                            if tl.hasAttribute("dictionary_id"):
                                tD["dictionary_id"] = row[tl.getIndex("dictionary_id")]
                            if tl.hasAttribute("category_id"):
                                tD["category_id"] = row[tl.getIndex("category_id")]
                            if tl.hasAttribute("include_as_category_id"):
                                tD["include_as_category_id"] = row[tl.getIndex("include_as_category_id")]
                            if tl.hasAttribute("include_mode"):
                                tD["include_mode"] = row[tl.getIndex("include_mode")]
                            #
                            self.__categoryIncludeDict.setdefault(tD["dictionary_id"], {}).setdefault(tD["category_id"], tD)
                    tl = ob.getObj("pdbx_include_item")
                    if tl is not None:
                        for row in tl.getRowList():
                            tD = OrderedDict()
                            if tl.hasAttribute("dictionary_id"):
                                tD["dictionary_id"] = row[tl.getIndex("dictionary_id")]
                            if tl.hasAttribute("item_name"):
                                tD["item_name"] = row[tl.getIndex("item_name")]
                            if tl.hasAttribute("include_as_item_name"):
                                tD["include_as_item_name"] = row[tl.getIndex("include_as_item_name")]
                            if tl.hasAttribute("include_mode"):
                                tD["include_mode"] = row[tl.getIndex("include_mode")]
                            #
                            categoryId = CifName.categoryPart(tD["item_name"])
                            self.__itemIncludeDict.setdefault(tD["dictionary_id"], {}).setdefault(categoryId, {}).setdefault(tD["item_name"], tD)

                tl = ob.getObj("dictionary_history")
                if tl is not None:
                    # history as a list of dictionaries -
                    dName = ob.getName()
                    for row in tl.getRowList():
                        if tl.hasAttribute("version") and tl.hasAttribute("revision") and tl.hasAttribute("update"):
                            tD = OrderedDict()
                            tD["version"] = row[tl.getIndex("version")]
                            tD["revision"] = row[tl.getIndex("revision")]
                            tD["update"] = row[tl.getIndex("update")]
                            tD["dictionary"] = dName
                            self.__dictionaryHistoryList.append(tD)
                #
                tl = ob.getObj("pdbx_dictionary_component")
                if tl is not None:
                    for row in tl.getRowList():
                        tD = OrderedDict()
                        if tl.hasAttribute("dictionary_component_id"):
                            tD["dictionary_component_id"] = row[tl.getIndex("dictionary_component_id")]
                        if tl.hasAttribute("title"):
                            tD["title"] = row[tl.getIndex("title")]
                        if tl.hasAttribute("version"):
                            tD["version"] = row[tl.getIndex("version")]
                        self.__dictionaryComponentList.append(tD)

                    tl = ob.getObj("pdbx_dictionary_component_history")
                    if tl is not None:
                        for row in tl.getRowList():
                            if tl.hasAttribute("version") and tl.hasAttribute("revision") and tl.hasAttribute("update"):
                                tD = OrderedDict()
                                tD["version"] = row[tl.getIndex("version")]
                                tD["revision"] = row[tl.getIndex("revision")]
                                tD["update"] = row[tl.getIndex("update")]
                                tD["dictionary_component_id"] = row[tl.getIndex("dictionary_component_id")]
                                self.__dictionaryComponentHistoryDict.setdefault(tD["dictionary_component_id"], []).append(tD)

                # JDW
                tl = ob.getObj("sub_category")
                if tl is not None:
                    # subcategories as a dictionary by id
                    self.__subCategoryDict = OrderedDict()
                    for row in tl.getRowList():
                        if tl.hasAttribute("id") and tl.hasAttribute("description"):
                            self.__subCategoryDict[row[tl.getIndex("id")]] = row[tl.getIndex("description")]

                tl = ob.getObj("category_group_list")
                if tl is not None:
                    # category groups as a dictionary by id of tuples
                    self.__categoryGroupDict = OrderedDict()
                    for row in tl.getRowList():
                        if tl.hasAttribute("id") and tl.hasAttribute("description") and tl.hasAttribute("parent_id"):
                            tD = OrderedDict()
                            tD["description"] = row[tl.getIndex("description")]
                            tD["parent_id"] = row[tl.getIndex("parent_id")]
                            tD["categories"] = []
                            self.__categoryGroupDict[row[tl.getIndex("id")]] = tD

                tl = ob.getObj("item_units_list")
                if tl is not None:
                    # units as a dictionary by code
                    self.__itemUnitsDict = OrderedDict()
                    for row in tl.getRowList():
                        if tl.hasAttribute("code") and tl.hasAttribute("detail"):
                            self.__itemUnitsDict[row[tl.getIndex("code")]] = row[tl.getIndex("detail")]

                tl = ob.getObj("item_units_conversion")
                if tl is not None:
                    # units conversion as a simple list now
                    self.__itemUnitsConversionList = []
                    for row in tl.getRowList():
                        if tl.hasAttribute("from_code") and tl.hasAttribute("to_code") and tl.hasAttribute("operator") and tl.hasAttribute("factor"):
                            self.__itemUnitsConversionList.append(
                                (row[tl.getIndex("from_code")], row[tl.getIndex("to_code")], row[tl.getIndex("operator")], row[tl.getIndex("factor")])
                            )

                tl = ob.getObj("pdbx_item_linked_group")
                if tl is not None:
                    # parent-child collections   [category_id] -> [(1,...),(3,...),(4,...) ]
                    self.__itemLinkedGroupDict = OrderedDict()
                    for row in tl.getRowList():
                        if (
                            tl.hasAttribute("category_id")
                            and tl.hasAttribute("link_group_id")
                            and tl.hasAttribute("label")
                            and tl.hasAttribute("context")
                            and tl.hasAttribute("condition_id")
                        ):
                            categoryId = row[tl.getIndex("category_id")]
                            if categoryId not in self.__itemLinkedGroupDict:
                                self.__itemLinkedGroupDict[categoryId] = []
                            self.__itemLinkedGroupDict[categoryId].append(
                                (row[tl.getIndex("category_id")], row[tl.getIndex("link_group_id")], row[tl.getIndex("context")], row[tl.getIndex("condition_id")])
                            )

                tl = ob.getObj("pdbx_item_linked_group_list")
                if tl is not None:
                    # parent-child collections   [(category_id,link_group_id)] -> [(child_name,parent_name,parent_category),(,...),(,...) ]
                    self.__itemLinkedGroupItemDict = OrderedDict()
                    for row in tl.getRowList():
                        if (
                            tl.hasAttribute("child_category_id")
                            and tl.hasAttribute("link_group_id")
                            and tl.hasAttribute("child_name")
                            and tl.hasAttribute("parent_name")
                            and tl.hasAttribute("parent_category_id")
                        ):
                            childCategoryId = row[tl.getIndex("child_category_id")]
                            linkGroupId = row[tl.getIndex("link_group_id")]
                            if (childCategoryId, linkGroupId) not in self.__itemLinkedGroupItemDict:
                                self.__itemLinkedGroupItemDict[(childCategoryId, linkGroupId)] = []
                            self.__itemLinkedGroupItemDict[(childCategoryId, linkGroupId)].append(
                                (row[tl.getIndex("child_name")], row[tl.getIndex("parent_name")], row[tl.getIndex("parent_category_id")])
                            )
                #
                tl = ob.getObj("pdbx_item_value_condition_list")
                if tl is not None:
                    for row in tl.getRowList():
                        if (
                            tl.hasAttribute("dependent_item_name")
                            and tl.hasAttribute("dependent_item_cmp_op")
                            and tl.hasAttribute("target_item_name")
                            and tl.hasAttribute("cond_id")
                        ):
                            tD = OrderedDict()
                            tD["cond_id"] = row[tl.getIndex("cond_id")]
                            tD["target_item_name"] = row[tl.getIndex("target_item_name")]
                            tD["dependent_item_name"] = row[tl.getIndex("dependent_item_name")]
                            tD["dependent_item_cmp_op"] = row[tl.getIndex("dependent_item_cmp_op")]
                            tD["target_item_value"] = row[tl.getIndex("target_item_value")] if tl.hasAttribute("target_item_value") else None
                            tD["dependent_item_value"] = row[tl.getIndex("dependent_item_value")] if tl.hasAttribute("dependent_item_value") else None
                            tD["log_op"] = row[tl.getIndex("log_op")] if tl.hasAttribute("log_op") else "and"
                            self.__itemValueConditionDict.setdefault(tD["target_item_name"], {}).setdefault(tD["dependent_item_name"], []).append(tD)
                #
                tl = ob.getObj("pdbx_comparison_operator_list")
                if tl is not None:
                    for row in tl.getRowList():
                        if tl.hasAttribute("code") and tl.hasAttribute("description"):
                            tD = OrderedDict()
                            tD["code"] = row[tl.getIndex("code")]
                            tD["description"] = row[tl.getIndex("description")]
                            self.__compOpDict[tD["code"]] = tD["description"]
