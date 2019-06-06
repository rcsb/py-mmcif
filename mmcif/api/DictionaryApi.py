##
#
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
#  14-Feb-2014  jdw fix atribute index lookup.
#  08-Mar-2014  jdw add method getEnumerationClosedFlag(self,category,attribute)
#   9-Sep-2018  jdw add priority to method definition constructor
#   7-Dec-2018  jdw add constructor parameter replaceDefinition=False to allow replacing
#                   defintions during consolidation
#   3-Feb-2019  jdw add method getFullDecendentList()
#  12-Apr-2019  jdw add methods getItemSubCategoryLabelList() and  getItemSubCategoryList()
#  26-May-2019  jdw extend api for mehhods
##
"""
Accessors for PDBx/mmCIF dictionaries -

"""
from __future__ import absolute_import

import logging
import sys

from mmcif.api.DataCategory import DataCategory
from mmcif.api.Method import MethodDefinition, MethodReference
from mmcif.api.PdbxContainers import CifName

from six.moves import zip

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


logger = logging.getLogger(__name__)


class DictionaryApi(object):

    def __init__(self, containerList, consolidate=True, expandItemLinked=False, replaceDefinition=False, verbose=False):
        self.__verbose = verbose
        self.__debug = False
        #
        self.__containerList = containerList
        self.__replaceDefinition = replaceDefinition
        #
        if (consolidate):
            self.__consolidateDefinitions()

        #
        if (expandItemLinked):
            self.__expandLoopedDefinitions()

        self.__fullIndex = {}

        # ---
        #
        # Map category name to the unique list of attributes
        self.__catNameIndex = {}
        # Map category name to the unique list of item names
        self.__catNameItemIndex = {}
        # Full unique list of item names -
        self.__itemNameList = []
        #
        # Map dictionary objects names to definition containers -
        self.__definitionIndex = {}
        #
        # data section/objects of the dictionary by category name -
        self.__dataIndex = {}
        #
        # Map of types id->(regex,primitive_type)
        self.__typesDict = {}
        #
        self.__enumD = {'ENUMERATION_VALUE': ('item_enumeration', 'value'),
                        'ENUMERATION_DETAIL': ('item_enumeration', 'detail'),
                        'ENUMERATION_TUPLE': ('item_enumeration', None),
                        'ITEM_LINKED_PARENT': ('item_linked', 'parent_name'),
                        'ITEM_LINKED_CHILD': ('item_linked', 'child_name'),
                        'DATA_TYPE_CODE': ('item_type', 'code'),
                        'DATA_TYPE_REGEX': ('item_type_list', 'construct'),
                        'DATA_TYPE_PRIMITIVE': ('item_type_list', 'primitive_code'),
                        'ITEM_NAME': ('item', 'name'),
                        'ITEM_CATEGORY_ID': ('item', 'category_id'),
                        'ITEM_MANDATORY_CODE': ('item', 'mandatory_code'),
                        'ITEM_DESCRIPTION': ('item_description', 'description'),
                        'ITEM_UNITS': ('item_units', 'code'),
                        'ITEM_DEFAULT_VALUE': ('item_default', 'value'),
                        'ITEM_EXAMPLE_CASE': ('item_examples', 'case'),
                        'ITEM_EXAMPLE_DETAIL': ('item_examples', 'detail'),
                        'ITEM_RANGE_MAXIMUM': ('item_range', 'maximum'),
                        'ITEM_RANGE_MINIMUM': ('item_range', 'minimum'),
                        'CATEGORY_KEY_ITEMS': ('category_key', 'name'),
                        'CATEGORY_EXAMPLE_CASE': ('category_examples', 'case'),
                        'CATEGORY_EXAMPLE_DETAIL': ('category_examples', 'detail'),
                        'CATEGORY_MANDATORY_CODE': ('category', 'mandatory_code'),
                        'CATEGORY_DESCRIPTION': ('category', 'description'),
                        #
                        'DATA_TYPE_CODE_NDB': ('ndb_item_type', 'code'),
                        'ITEM_DESCRIPTION_NDB': ('ndb_item_description', 'description'),
                        'ENUMERATION_VALUE_NDB': ('ndb_item_enumeration', 'value'),
                        'ENUMERATION_DETAIL_NDB': ('ndb_item_enumeration', 'detail'),
                        'ITEM_MANDATORY_CODE_NDB': ('ndb_item', 'mandatory_code'),
                        'ITEM_EXAMPLE_CASE_NDB': ('ndb_item_examples', 'case'),
                        'ITEM_EXAMPLE_DETAIL_NDB': ('ndb_item_examples', 'detail'),
                        'ITEM_RANGE_MAXIMUM_NDB': ('ndb_item_range', 'maximum'),
                        'ITEM_RANGE_MINIMUM_NDB': ('ndb_item_range', 'minimum'),
                        'CATEGORY_EXAMPLE_CASE_NDB': ('ndb_category_examples', 'case'),
                        'CATEGORY_EXAMPLE_DETAIL_NDB': ('ndb_category_examples', 'detail'),
                        'CATEGORY_DESCRIPTION_NDB': ('ndb_category_description', 'description'),
                        #
                        'DATA_TYPE_CODE_PDBX': ('pdbx_item_type', 'code'),
                        'ITEM_DESCRIPTION_PDBX': ('pdbx_item_description', 'description'),
                        'ENUMERATION_VALUE_PDBX': ('pdbx_item_enumeration', 'value'),
                        'ENUMERATION_DETAIL_PDBX': ('pdbx_item_enumeration', 'detail'),
                        'ITEM_MANDATORY_CODE_PDBX': ('pdbx_item', 'mandatory_code'),
                        'ITEM_EXAMPLE_CASE_PDBX': ('pdbx_item_examples', 'case'),
                        'ITEM_EXAMPLE_DETAIL_PDBX': ('pdbx_item_examples', 'detail'),
                        'ITEM_RANGE_MAXIMUM_PDBX': ('pdbx_item_range', 'maximum'),
                        'ITEM_RANGE_MINIMUM_PDBX': ('pdbx_item_range', 'minimum'),
                        'CATEGORY_EXAMPLE_CASE_PDBX': ('pdbx_category_examples', 'case'),
                        'CATEGORY_EXAMPLE_DETAIL_PDBX': ('pdbx_category_examples', 'detail'),
                        'CATEGORY_DESCRIPTION_PDBX': ('pdbx_category_description', 'description'),
                        #
                        'CATEGORY_CONTEXT': ('pdbx_category_context', 'type'),
                        'CATEGORY_GROUP': ('category_group', 'id'),
                        'ITEM_CONTEXT': ('pdbx_item_context', 'type'),
                        'ENUMERATION_CLOSED_FLAG': ('pdbx_item_enumeration_details', 'closed_flag'),
                        #
                        'ITEM_RELATED_FUNCTION_CODE': ('item_related', 'function_code'),
                        'ITEM_RELATED_RELATED_NAME': ('item_related', 'related_name'),

                        'ITEM_ALIAS_ALIAS_NAME': ('item_aliases', 'alias_name'),
                        'ITEM_ALIAS_DICTIONARY': ('item_aliases', 'dictionary'),
                        'ITEM_ALIAS_VERSION': ('item_aliases', 'version'),

                        'ITEM_DEPENDENT_DEPENDENT_NAME': ('item_dependent', 'dependent_name'),
                        'ITEM_SUB_CATEGORY_ID': ('item_sub_category', 'id'),
                        'ITEM_SUB_CATEGORY_LABEL': ('item_sub_category', 'pdbx_label'),
                        'ITEM_TYPE_CONDITIONS_CODE': ('item_type_conditions', 'code')
                        }
        #
        self.__methodDict = {}
        self.__methodIndex = {}
        #
        self.__makeIndex()
        self.__getMethods()
        #
        self.__fullParentD, self.__fullChildD = self.__makeFullParentChildDictionaries()
        #
        # content sections
        self.__dataBlockDict = {}
        self.__dictionaryDict = {}
        self.__subCategoryDict = {}
        self.__categoryGroupDict = {}
        self.__groupIndex = False
        #
        # Data sections -
        #
        self.__dictionaryHistoryList = []
        self.__itemUnitsDict = {}
        self.__itemUnitsConversionList = []
        self.__itemLinkedGroupDict = {}
        self.__itemLinkedGroupItemDict = {}
        #
        self.__getDataSections()
        #

    #
    #  Methods for data sections --
    #
    def getDictionaryVersion(self):
        try:
            return self.__dictionaryDict['version']
        except Exception:
            return None

    def getDictionaryTitle(self):
        try:
            return self.__dictionaryDict['title']
        except Exception:
            return None

    def getDictionaryUpdate(self, order='reverse'):
        """ Get details from the last history element.
        """
        try:
            if order == 'reverse':
                tD = self.__dictionaryHistoryList[-1]
            else:
                tD = self.__dictionaryHistoryList[0]

            return tD['update']

        except Exception:
            return None

    def getDictionaryRevisionCount(self):
        """ Get details from the last history element.
        """
        try:
            return len(self.__dictionaryHistoryList)
        except Exception:
            return 0

    def getDictionaryHistory(self, order='reverse'):
        """ Returns the revision history as a listr of tuples [(version,update,revisionText),...]
        """
        oL = []
        try:
            if order == 'reverse':
                for tD in reversed(self.__dictionaryHistoryList):
                    oL.append((tD['version'], tD['update'], tD['revision']))
            else:
                for tD in self.__dictionaryHistoryList:
                    oL.append((tD['version'], tD['update'], tD['revision']))
        except Exception:
            pass
        return oL

    def __makeCategoryGroupIndex(self):
        catNameList = self.getCategoryList()
        # add categories in group to self.__categoryGroupDict[<groupName>]['categories']
        for catName in catNameList:
            groupNameList = self.getCategoryGroupList(catName)
            # logger.info("Category %s group list %r\n" % (catName,groupNameList))
            for groupName in groupNameList:
                if groupName not in self.__categoryGroupDict:
                    #  handle undefined category group ?
                    tD = {}
                    tD['description'] = None
                    tD['parent_id'] = None
                    tD['categories'] = []
                    self.__categoryGroupDict[groupName] = tD

                self.__categoryGroupDict[groupName]['categories'].append(catName)
        #
        for groupName in self.__categoryGroupDict.keys():
            # logger.info("Group %s count %r\n" % (groupName, len(self.__categoryGroupDict[groupName]['categories'])))
            if 'categories' in self.__categoryGroupDict[groupName]:
                self.__categoryGroupDict[groupName]['categories'].sort()
        self.__groupIndex = True

    #
    def getCategoryGroupDescription(self, groupName):
        try:
            return self.__categoryGroupDict[groupName]['description']
        except Exception:
            return None

    def getCategoryGroupParent(self, groupName):
        try:
            return self.__categoryGroupDict[groupName]['parent_id']
        except Exception:
            return None

    def getCategoryGroupCategories(self, groupName):
        try:
            if not self.__groupIndex:
                self.__makeCategoryGroupIndex()
            return self.__categoryGroupDict[groupName]['categories']
        except Exception:
            logger.exception("DictionaryApi.getCategoryGroupCategories failed for group %s \n" % groupName)

        return []

    def getCategoryGroups(self):
        try:
            kL = sorted(self.__categoryGroupDict.keys())
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
    # def XgetItemNameList(self):
    #    return self.__itemNameList

    #
    def definitionExists(self, definitionName):
        if definitionName in self.__definitionIndex:
            return True
        return False

    def getTypeConditionsCode(self, category, attribute):
        return self.__get('ITEM_TYPE_CONDITIONS_CODE', category, attribute)

    def getItemDependentNameList(self, category, attribute):
        return self.__getList('ITEM_DEPENDENT_DEPENDENT_NAME', category, attribute)

    def getItemSubCategoryIdList(self, category, attribute):
        return self.__getList('ITEM_SUB_CATEGORY_ID', category, attribute)

    def getItemSubCategoryLabelList(self, category, attribute):
        return self.__getList('ITEM_SUB_CATEGORY_LABEL', category, attribute)

    def getItemSubCategoryList(self, category, attribute):
        aL = []

        itemName = CifName.itemName(category, attribute)

        obL = self.__definitionIndex[itemName] if itemName in self.__definitionIndex else None
        for ob in obL:
            tObj = ob.getObj(self.__enumD['ITEM_SUB_CATEGORY_ID'][0])
            if tObj is not None:
                atId = self.__enumD['ITEM_SUB_CATEGORY_ID'][1]
                atLabel = self.__enumD['ITEM_SUB_CATEGORY_LABEL'][1]
                for row in tObj.getRowList():
                    # logger.info("subcategories for %s row is %r" % (itemName, row))
                    idVal = row[tObj.getIndex(atId)] if tObj.hasAttribute(atId) else None
                    labVal = row[tObj.getIndex(atLabel)] if tObj.hasAttribute(atLabel) else None
                    aL.append((idVal, labVal))
        return aL

    def getItemAliasList(self, category, attribute):
        aNL = self.__getListAll('ITEM_ALIAS_ALIAS_NAME', category, attribute)
        aDL = self.__getListAll('ITEM_ALIAS_DICTIONARY', category, attribute)
        aVL = self.__getListAll('ITEM_ALIAS_VERSION', category, attribute)
        aL = []
        for aN, aD, aV in zip(aNL, aDL, aVL):
            aL.append((aN, aD, aV))
        return aL

    def getEnumListWithDetail(self, category, attribute):
        eVL = self.__getListAll('ENUMERATION_VALUE', category, attribute)
        eDL = self.__getListAll('ENUMERATION_DETAIL', category, attribute)
        rL = []
        d = {}
        if len(eVL) == len(eDL):
            for eV, eD in zip(eVL, eDL):
                d[eV] = (eV, eD)
        else:
            for eV in eVL:
                d[eV] = (eV, None)
        #
        for ky in sorted(d.keys()):
            rL.append(d[ky])
        return rL

    def getEnumListAltWithDetail(self, category, attribute):
        eVL = self.__getListAll('ENUMERATION_VALUE_PDBX', category, attribute)
        eDL = self.__getListAll('ENUMERATION_DETAIL_PDBX', category, attribute)

        rL = []
        d = {}
        if len(eVL) == len(eDL):
            for eV, eD in zip(eVL, eDL):
                d[eV] = (eV, eD)
        else:
            for eV in eVL:
                d[eV] = (eV, None)
        #
        for ky in sorted(d.keys()):
            rL.append(d[ky])
        #
        if len(rL) < 1:
            return self.getEnumListWithDetail(category, attribute)
        else:
            return rL

    def getItemRelatedList(self, category, attribute):
        rNL = self.__getListAll('ITEM_RELATED_RELATED_NAME', category, attribute)
        rFL = self.__getListAll('ITEM_RELATED_FUNCTION_CODE', category, attribute)
        rL = []
        for rN, rF in zip(rNL, rFL):
            rL.append((rN, rF))
        return rL

    def getTypeCode(self, category, attribute):
        return self.__get('DATA_TYPE_CODE', category, attribute, followAncestors=True)

    def getTypeCodeAlt(self, category, attribute, fallBack=True):
        v = self.getTypeCodePdbx(category, attribute)
        if v is None:
            v = self.getTypeCodeNdb(category, attribute)
        if fallBack and v is None:
            v = self.getTypeCode(category, attribute)
        return v

    def getTypeCodeNdb(self, category, attribute):
        return self.__get('DATA_TYPE_CODE_NDB', category, attribute, followAncestors=False)

    def getTypeCodePdbx(self, category, attribute):
        return self.__get('DATA_TYPE_CODE_PDBX', category, attribute, followAncestors=False)

    def getDefaultValue(self, category, attribute):
        return self.__get('ITEM_DEFAULT_VALUE', category, attribute)

    def getMandatoryCode(self, category, attribute):
        return self.__get('ITEM_MANDATORY_CODE', category, attribute)

    def getMandatoryCodeAlt(self, category, attribute, fallBack=True):
        v = self.getMandatoryCodePdbx(category, attribute)
        if v is None:
            v = self.getMandatoryCodeNdb(category, attribute)
        if fallBack and v is None:
            v = self.getMandatoryCode(category, attribute)
        return v

    def getMandatoryCodeNdb(self, category, attribute):
        return self.__get('ITEM_MANDATORY_CODE_NDB', category, attribute)

    def getMandatoryCodePdbx(self, category, attribute):
        return self.__get('ITEM_MANDATORY_CODE_PDBX', category, attribute)

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
        return self.__getList('ITEM_CONTEXT', category, attribute)

    def getCategoryContextList(self, category):
        return self.__getList('CATEGORY_CONTEXT', category, attribute=None)

    def getEnumList(self, category, attribute, sortFlag=True):
        if sortFlag:
            return self.__getList('ENUMERATION_VALUE', category, attribute)
        else:
            return self.__getListAll('ENUMERATION_VALUE', category, attribute)

    def getEnumListAlt(self, category, attribute, fallBack=True, sortFlag=True):
        vL = self.getEnumListPdbx(category, attribute, sortFlag=sortFlag)
        if len(vL) < 1:
            vL = self.getEnumListNdb(category, attribute, sortFlag=sortFlag)
        if fallBack and len(vL) < 1:
            vL = self.getEnumList(category, attribute, sortFlag=sortFlag)
        return vL

    def getEnumListNdb(self, category, attribute, sortFlag=True):
        if sortFlag:
            return self.__getList('ENUMERATION_VALUE_NDB', category, attribute)
        else:
            return self.__getListAll('ENUMERATION_VALUE_NDB', category, attribute)

    def getEnumListPdbx(self, category, attribute, sortFlag=True):
        if sortFlag:
            return self.__getList('ENUMERATION_VALUE_PDBX', category, attribute)
        else:
            return self.__getListAll('ENUMERATION_VALUE_PDBX', category, attribute)

    def isEnumerated(self, category, attribute):
        return (len(self.__getList('ENUMERATION_VALUE', category, attribute)) > 0)

    def isEnumeratedAlt(self, category, attribute, fallBack=True):
        eC = len(self.__getList('ENUMERATION_VALUE_PDBX', category, attribute))
        if (eC == 0):
            eC = len(self.__getList('ENUMERATION_VALUE_NDB', category, attribute))
        if (fallBack and (eC == 0)):
            eC = len(self.__getList('ENUMERATION_VALUE', category, attribute))
        return (eC > 0)

    def getEnumerationClosedFlag(self, category, attribute):
        return self.__get('ENUMERATION_CLOSED_FLAG', category, attribute)

    def getUltimateParent(self, category, attribute):
        """  Return the first ultimate parent item for the input item.
        """
        #        pL=self.__getList('ITEM_LINKED_PARENT',category,attribute)
        pL = self.getFullParentList(category, attribute)
        itemName = CifName.itemName(category, attribute)
        while ((len(pL) > 0) and (pL[0] != itemName)):
            attN = CifName.attributePart(pL[0])
            catN = CifName.categoryPart(pL[0])
            itemName = pL[0]
            pL = self.getFullParentList(catN, attN)
            # pL=self.__getList('ITEM_LINKED_PARENT',catN,attN)
        return itemName

    def getParentList(self, category, attribute, stripSelfParent=False):
        if stripSelfParent:
            itemName = CifName.itemName(category, attribute)
            pL = self.__getList('ITEM_LINKED_PARENT', category, attribute)
            if len(pL) > 0:
                try:
                    pL.remove(itemName)
                except Exception:
                    pass
            return pL
        else:
            return self.__getList('ITEM_LINKED_PARENT', category, attribute)

    def getChildList(self, category, attribute):
        return self.__getList('ITEM_LINKED_CHILD', category, attribute)

    def getFullChildList(self, category, attribute):
        try:
            itemName = CifName.itemName(category, attribute)
            return self.__fullChildD[itemName]
        except Exception:
            return []

    def getFullDecendentList(self, category, attribute):
        itemNameL = []
        try:
            itemName = CifName.itemName(category, attribute)
            itemNameL = self.__fullChildD[itemName] if itemName in self.__fullChildD else []
            itemNameL = list(set(itemNameL))
            if len(itemNameL) > 0:
                begLen = 0
                endLen = 1
                #
                while (endLen > begLen):
                    begLen = len(itemNameL)
                    for itemName in itemNameL:
                        if itemName in self.__fullChildD:
                            itemNameL.extend(self.__fullChildD[itemName])
                    itemNameL = list(set(itemNameL))
                    endLen = len(itemNameL)

        except Exception as e:
            logger.exception("Failing for %s %s with %s" % (category, attribute, str(e)))
        return itemNameL

    def XgetFullParentList(self, category, attribute):
        try:
            itemName = CifName.itemName(category, attribute)
            return self.__fullParentD[itemName]
        except Exception:
            return []

    def getFullParentList(self, category, attribute, stripSelfParent=False):
        try:
            itemName = CifName.itemName(category, attribute)
            pL = self.__fullParentD[itemName]
            if stripSelfParent:
                if len(pL) > 0:
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
        return self.__get('ITEM_UNITS', category, attribute)

    def getImplicitList(self):
        iL = []
        for name, dL in self.__definitionIndex.items():
            for d in dL:
                type = d.getType()
                if (type == "definition" and d.isAttribute()):
                    catN = CifName.categoryPart(name)
                    attN = CifName.attributePart(name)
                    if (self.__get('ITEM_MANDATORY_CODE', catN, attN) == 'implicit'):
                        if name not in iL:
                            iL.append(name)
        return iL

    def getDescription(self, category, attribute):
        return self.__get('ITEM_DESCRIPTION', category, attribute)

    def getDescriptionAlt(self, category, attribute, fallBack=True):
        v = self.getDescriptionPdbx(category, attribute)
        if v is None:
            v = self.getDescriptionNdb(category, attribute)
        if fallBack and v is None:
            v = self.getDescription(category, attribute)
        return v

    def getDescriptionNdb(self, category, attribute):
        return self.__get('ITEM_DESCRIPTION_NDB', category, attribute)

    def getDescriptionPdbx(self, category, attribute):
        return self.__get('ITEM_DESCRIPTION_PDBX', category, attribute)

    def getExampleList(self, category, attribute):
        exCL = self.__getListAll('ITEM_EXAMPLE_CASE', category, attribute)
        exDL = self.__getListAll('ITEM_EXAMPLE_DETAIL', category, attribute)
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
        if len(vL) < 1:
            vL = self.getExampleListNdb(category, attribute)
        if fallBack and len(vL) < 1:
            vL = self.getExampleList(category, attribute)
        return vL

    def getExampleListNdb(self, category, attribute):
        exCL = self.__getListAll('ITEM_EXAMPLE_CASE_NDB', category, attribute)
        exDL = self.__getListAll('ITEM_EXAMPLE_DETAIL_NDB', category, attribute)
        exL = []
        if len(exCL) == len(exDL):
            for exC, exD in zip(exCL, exDL):
                exL.append((exC, exD))
        else:
            for exC in exCL:
                exL.append((exC, None))
        return exL

    def getExampleListPdbx(self, category, attribute):
        exCL = self.__getListAll('ITEM_EXAMPLE_CASE_PDBX', category, attribute)
        exDL = self.__getListAll('ITEM_EXAMPLE_DETAIL_PDBX', category, attribute)
        exL = []
        if len(exCL) == len(exDL):
            for exC, exD in zip(exCL, exDL):
                exL.append((exC, exD))
        else:
            for exC in exCL:
                exL.append((exC, None))
        return exL

    def getBoundaryList(self, category, attribute):
        minL = self.__getListAll('ITEM_RANGE_MINIMUM', category, attribute)
        maxL = self.__getListAll('ITEM_RANGE_MAXIMUM', category, attribute)
        bL = []
        for vMin, vMax in zip(minL, maxL):
            bL.append((vMin, vMax))
        return bL

    def getBoundaryListAlt(self, category, attribute, fallBack=True):
        vL = self.getBoundaryListPdbx(category, attribute)
        if len(vL) < 1:
            vL = self.getBoundaryListNdb(category, attribute)
        if fallBack and len(vL) < 1:
            vL = self.getBoundaryList(category, attribute)
        return vL

    def getBoundaryListNdb(self, category, attribute):
        minL = self.__getListAll('ITEM_RANGE_MINIMUM_NDB', category, attribute)
        maxL = self.__getListAll('ITEM_RANGE_MAXIMUM_NDB', category, attribute)
        bL = []
        for vMin, vMax in zip(minL, maxL):
            bL.append((vMin, vMax))
        #
        return bL

    def getBoundaryListPdbx(self, category, attribute):
        minL = self.__getListAll('ITEM_RANGE_MINIMUM_PDBX', category, attribute)
        maxL = self.__getListAll('ITEM_RANGE_MAXIMUM_PDBX', category, attribute)
        bL = []
        for vMin, vMax in zip(minL, maxL):
            bL.append((vMin, vMax))
        #
        return bL

    def getCategoryKeyList(self, category):
        return self.__getList('CATEGORY_KEY_ITEMS', category, attribute=None)

    def getCategoryGroupList(self, category):
        return self.__getList('CATEGORY_GROUP', category, attribute=None)

    def getCategoryMandatoryCode(self, category):
        return self.__get('CATEGORY_MANDATORY_CODE', category, attribute=None)

    def getCategoryDescription(self, category):
        return self.__get('CATEGORY_DESCRIPTION', category, attribute=None)

    def getCategoryDescriptionAlt(self, category, fallBack=True):
        v = self.getCategoryDescriptionPdbx(category)
        if v is None:
            v = self.getCategoryDescriptionNdb(category)
        if (fallBack and v is None):
            v = self.getCategoryDescription(category)
        return v

    def getCategoryDescriptionNdb(self, category):
        val = self.__get('CATEGORY_DESCRIPTION_NDB', category, attribute=None)
        return val

    def getCategoryDescriptionPdbx(self, category):
        val = self.__get('CATEGORY_DESCRIPTION_PDBX', category, attribute=None)
        return val

    def getCategoryExampleList(self, category):
        exCL = self.__getListAll('CATEGORY_EXAMPLE_CASE', category, attribute=None)
        exDL = self.__getListAll('CATEGORY_EXAMPLE_DETAIL', category, attribute=None)
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
        if len(vL) < 1:
            vL = self.getCategoryExampleListNdb(category)
        if fallBack and len(vL) < 1:
            vL = self.getCategoryExampleList(category)
        return vL

    def getCategoryExampleListNdb(self, category):
        exCL = self.__getListAll('CATEGORY_EXAMPLE_CASE_NDB', category, attribute=None)
        exDL = self.__getListAll('CATEGORY_EXAMPLE_DETAIL_NDB', category, attribute=None)
        exL = []
        if len(exCL) == len(exDL):
            for exC, exD in zip(exCL, exDL):
                exL.append((exC, exD))
        else:
            for exC in exCL:
                exL.append((exC, None))
        return exL

    def getCategoryExampleListPdbx(self, category):
        exCL = self.__getListAll('CATEGORY_EXAMPLE_CASE_PDBX', category, attribute=None)
        exDL = self.__getListAll('CATEGORY_EXAMPLE_DETAIL_PDBX', category, attribute=None)
        exL = []
        if len(exCL) == len(exDL):
            for exC, exD in zip(exCL, exDL):
                exL.append((exC, exD))
        else:
            for exC in exCL:
                exL.append((exC, None))

        return exL

    def getParentDictionary(self):
        """ Create a dictionary of parents relations accross all definnitions

            as d[child]=[parent,parent,...]

            Exclude self parents.
        """
        parentD = {}
        pAtN = self.__enumD['ITEM_LINKED_PARENT'][1]
        cAtN = self.__enumD['ITEM_LINKED_CHILD'][1]

        for dObj in self.__containerList:
            dc = dObj.getObj(self.__enumD['ITEM_LINKED_PARENT'][0])
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

    def __makeFullParentChildDictionaries(self):
        """ Create a dictionaries of full parent/child relations accross all definnitions

            as  fullParentD[child]=[parent,parent,...]
            and fullChildD[parent]=[child,child,...]

            Exclude self parents.
        """
        fullParentD = {}
        fullChildD = {}
        pAtN = self.__enumD['ITEM_LINKED_PARENT'][1]
        cAtN = self.__enumD['ITEM_LINKED_CHILD'][1]

        for dObj in self.__containerList:
            # logger.info("\n\nSearching object  %s\n" % dObj.getName())
            dc = dObj.getObj(self.__enumD['ITEM_LINKED_PARENT'][0])
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

    def __get(self, enumCode, category, attribute=None, followAncestors=False):
        """  Return the last occurrence of the input dictionary metadata.  If the value
             for the input category/attribute is null/missing then optionally check for
             an ancestor value.
        """
        v0 = self.__getValue(enumCode, category, attribute)
        if not followAncestors:
            return v0
        else:
            if ((v0 is None) or (len(v0) < 1) or (v0 in ['.', '?'])):
                pItem = self.getUltimateParent(category, attribute)
                if ((pItem is not None) and (len(pItem) > 0) and (pItem != CifName.itemName(category, attribute))):
                    if self.__debug:
                        logger.info("DictionaryApi.__get() Reassigning enum code %s  category %s attribute %s to parent %r\n" %
                                    (enumCode, category, attribute, pItem))

                    return self.__getValue(enumCode, CifName.categoryPart(pItem), CifName.attributePart(pItem))

        return v0

    #
    def __getValue(self, enumCode, category, attribute=None):
        """ Returns the last occurrence of the input dictionary metadata (enumCode) for the input category/attribute
            encountered in the list of objects stored at the indicated definition index.

        """
        eS = None
        if enumCode not in self.__enumD:
            return eS

        if (attribute is not None):
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
                    if len(rL) > 0:
                        row = rL[0]
                        if atN is not None:
                            if (dc.hasAttribute(atN)):
                                eS = row[dc.getIndex(atN)]
                        else:
                            tL = []
                            for rv in row:
                                tL.append(rv)
                            eS = tL
        return eS

    def __getList(self, enumCode, category, attribute=None):
        ''' Return the unique list of values '''
        eL = []
        if enumCode not in self.__enumD:
            return eL

        if (attribute is not None):
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
                            if (dc.hasAttribute(atN)):
                                eL.append(row[dc.getIndex(atN)])
                        else:
                            tL = []
                            for rv in row:
                                tL.append(rv)
                            eL.append(tL)
        eS = set(eL)
        eL = list(eS)
        return eL

    def __getListAll(self, enumCode, category, attribute=None):
        ''' Return a list of all values  '''
        eL = []
        if enumCode not in self.__enumD:
            return eL

        if (attribute is not None):
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
                            if (dc.hasAttribute(atN)):
                                eL.append(row[dc.getIndex(atN)])
                        else:
                            tL = []
                            for rv in row:
                                tL.append(rv)
                            eL.append(tL)

        return eL

    def getMethodIndex(self):
        return self.__methodIndex

    def __makeIndex(self):
        """  Create indices of definitions, categories and items.
        """
        iD = {}
        for d in self.__containerList:
            name = d.getName()
            type = d.getType()
            #
            if name not in self.__fullIndex:
                self.__fullIndex[name] = []
            self.__fullIndex[name].append(d)
            #
            if (type == "definition" and d.isCategory()):
                if name not in self.__catNameIndex:
                    self.__catNameIndex[name] = []
                if name not in self.__catNameItemIndex:
                    self.__catNameItemIndex[name] = []
                if name not in self.__definitionIndex:
                    self.__definitionIndex[name] = []
                self.__definitionIndex[name].append(d)

            elif (type == "definition" and d.isAttribute()):
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
                self.__definitionIndex[name].append(d)
                iD[name] = name
            elif (type == "data"):
                for nm in d.getObjNameList():
                    if nm not in self.__dataIndex:
                        self.__dataIndex[nm] = d.getObj(nm)
            else:
                pass
        #
        self.__itemNameList = sorted(iD.keys())

    def getDefinitionIndex(self):
        return self.__definitionIndex

    def getFullIndex(self):
        return self.__fullIndex

    def getMethod(self, id):
        if id in self.__methodDict:
            return self.__methodDict[id]
        else:
            return None

    def getCategoryList(self):
        return sorted(self.__catNameIndex.keys())

    def getCategoryIndex(self):
        return self.__catNameIndex

    def getAttributeNameList(self, category):
        try:
            return sorted(self.__catNameIndex[category])
        except Exception:
            pass
        return []

    def getItemNameList(self, category):
        try:
            return sorted(self.__catNameItemIndex[category])
        except Exception:
            pass
        return []

    def getSubCategoryDescription(self, subCategoryName):
        if subCategoryName in self.__subCategoryDict:
            return self.__subCategoryDict[subCategoryName]
        else:
            return ''

    def __getMethods(self):
        self.__methodDict = {}
        self.__methodIndex = {}
        for ob in self.__containerList:
            if (ob.getType() == 'data'):
                ml = ob.getObj('method_list')
                if ml is not None:
                    # Use row order as priority
                    for ii, row in enumerate(ml.getRowList(), 1):
                        if ml.hasAttribute('id') and ml.hasAttribute('code') and ml.hasAttribute('language') and ml.hasAttribute('implementation_source'):
                            tInline = row[ml.getIndex('inline')] if ml.hasAttribute('inline') else None
                            tImpl = row[ml.getIndex('implementation')] if ml.hasAttribute('implementation') else None
                            mth = MethodDefinition(row[ml.getIndex('id')], row[ml.getIndex('code')], row[ml.getIndex('language')],
                                                   tInline, ii, tImpl, row[ml.getIndex('implementation_source')])
                            self.__methodDict[row[ml.getIndex('id')]] = mth

                ml = ob.getObj('datablock_methods')
                if ml is not None:
                    for row in ml.getRowList():
                        if ml.hasAttribute('method_id'):
                            #mth = MethodReference(row[ml.getIndex('method_id')], 'datablock', ob.getName(), None)
                            mth = MethodReference(row[ml.getIndex('method_id')], 'datablock', None, None)
                            if (ob.getName() in self.__methodIndex):
                                self.__methodIndex[ob.getName()].append(mth)
                            else:
                                self.__methodIndex[ob.getName()] = []
                                self.__methodIndex[ob.getName()].append(mth)
            elif (ob.getType() == 'definition'):
                mi = ob.getObj('category_methods')
                if mi is not None:
                    for row in mi.getRowList():
                        if mi.hasAttribute('method_id'):
                            mth = MethodReference(row[mi.getIndex('method_id')], 'category', ob.getName(), None)
                            if (ob.getName() in self.__methodIndex):
                                self.__methodIndex[ob.getName()].append(mth)
                            else:
                                self.__methodIndex[ob.getName()] = []
                                self.__methodIndex[ob.getName()].append(mth)
                mi = ob.getObj('item_methods')
                if mi is not None:
                    for row in mi.getRowList():
                        if mi.hasAttribute('method_id'):
                            mth = MethodReference(row[mi.getIndex('method_id')], 'attribute',
                                                  CifName.categoryPart(ob.getName()),
                                                  CifName.attributePart(ob.getName()))
                            if (ob.getName() in self.__methodIndex):
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
                    #fh.write("Method text: %s\n" % self.getMethod(v.getId()).getInline())
                else:
                    fh.write("Missing method for %r" % v.getId())
                    

    def dumpEnumFeatures(self, fh=sys.stdout):
        for k, vL in self.__catNameIndex.items():
            uvL = list(set(vL))
            for v in sorted(uvL):
                itL = self.getEnumList(k, v)
                if len(itL) > 0:
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
            if len(ctL) > 0:
                fh.write("    Category example list length %d\n" % len(ctL))
                for ct1, ct2 in ctL:
                    fh.write("      Example   case: %s\n" % ct1)
                    fh.write("      Example detail: %s\n" % ct2)

            ctL = self.getCategoryExampleListAlt(k)
            if len(ctL) > 0:
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
                if len(itL) > 0:
                    fh.write("      Enum list length %d\n" % len(itL))
                    for it in itL:
                        fh.write("      Enum: %s\n" % it)

                itL = self.getParentList(k, v)
                if len(itL) > 0:
                    fh.write("    Parent list length %d\n" % len(itL))
                    for it in itL:
                        fh.write("      Parent: %s\n" % it)
                itL = self.getChildList(k, v)
                if len(itL) > 0:
                    fh.write("    Child list length %d\n" % len(itL))
                    for it in itL:
                        fh.write("      Child: %s\n" % it)

                itL = self.getExampleList(k, v)
                if len(itL) > 0:
                    fh.write("    Example list length %d\n" % len(itL))
                    for it1, it2 in itL:
                        fh.write("      Example   case: %s\n" % it1)
                        fh.write("      Example detail: %s\n" % it2)

                itL = self.getBoundaryList(k, v)
                if len(itL) > 0:
                    fh.write("    Boundary list length %d\n" % len(itL))
                    for (it1, it2) in itL:
                        fh.write("      Boundary condition (min,max):  (%s,%s)\n" % (it1, it2))

                itL = self.getEnumListAlt(k, v)
                if len(itL) > 0:
                    fh.write("      Alt enum list length %d\n" % len(itL))
                    for it in itL:
                        fh.write("      Alt enum: %s\n" % it)

                itL = self.getExampleListAlt(k, v)
                if len(itL) > 0:
                    fh.write("    Alt example list length %d\n" % len(itL))
                    for it1, it2 in itL:
                        fh.write("      Alt example   case: %s\n" % it1)
                        fh.write("      Alt example detail: %s\n" % it2)

                itL = self.getBoundaryListAlt(k, v)
                if len(itL) > 0:
                    fh.write("    Alt boundary list length %d\n" % len(itL))
                    for (it1, it2) in itL:
                        fh.write("      Alt boundary condition (min,max):  (%s,%s)\n" % (it1, it2))

                itL = self.getItemRelatedList(k, v)
                if len(itL) > 0:
                    fh.write("    Related name list length %d\n" % len(itL))
                    for (it1, it2) in itL:
                        fh.write("      Related item name   %s function code %s\n" % (it1, it2))

                itL = self.getItemAliasList(k, v)
                if len(itL) > 0:
                    fh.write("    Alias name list length %d\n" % len(itL))
                    for (it1, it2, it3) in itL:
                        fh.write("      Alias name   %s dictionary %s version %s\n" % (it1, it2, it3))

                itL = self.getItemDependentNameList(k, v)
                if len(itL) > 0:
                    fh.write("    Dependent name list length %d\n" % len(itL))
                    for it1 in itL:
                        fh.write("      Dependent item name   %s\n" % it1)

    def dumpDataSections(self, fh=sys.stdout):
        fh.write("Datablock:  %r\n" % list(self.__dataBlockDict.items()))
        fh.write("Dictionary: %r\n" % list(self.__dictionaryDict.items()))
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

    def XcategoryPart(self, name):
        tname = ""
        if name.startswith("_"):
            tname = name[1:]
        else:
            tname = name

        i = tname.find(".")
        if i == -1:
            return tname
        else:
            return tname[:i]

    def XattributePart(self, name):
        i = name.find(".")
        if i == -1:
            return None
        else:
            return name[i + 1:]

    def __newDataCategory(self, categoryName, attributeNameList):
        """  create a new data category -
        """
        aCat = DataCategory(categoryName)
        for attributeName in attributeNameList:
            aCat.appendAttribute(attributeName)
        return aCat

    def __addItemLinkToDef(self, dObj, parent_name, child_name):
        """  Add the input link relationship to the input definition object.
        """
        if dObj.exists('item_linked'):
            # update in place --
            cObj = dObj.getObj('item_linked')
            iFound = False
            idxP = cObj.getIndex('parent_name')
            idxC = cObj.getIndex('child_name')
            for row in cObj.getRowList():
                if parent_name == row[idxP] and child_name == row[idxC]:
                    iFound = True
                    break
            if not iFound:
                nRows = cObj.getRowCount()
                cObj.setValue(child_name, 'child_name', nRows)
                cObj.setValue(parent_name, 'parent_name', nRows)
                if (self.__debug):
                    logger.info("+DictionaryApi.__addItemLinkToDef() appending item link in category %s\n" % dObj.getName())
            return True
        else:
            # create new category and append to input object
            cObj = self.__newDataCategory('item_linked', ['child_name', 'parent_name'])
            cObj.append([child_name, parent_name])
            dObj.append(cObj)
            if (self.__debug):
                logger.info("+DictionaryApi.__addItemLinkToDef() created new item link in category %s\n" % dObj.getName())
            return True

    def __expandLoopedDefinitions(self):
        """  Handle definitions containing looped item and item_linked categories --
        """
        fullIndex = {}
        for d in self.__containerList:
            name = d.getName()
            if name not in fullIndex:
                fullIndex[name] = []
            fullIndex[name].append(d)

        for name, dObjL in fullIndex.items():
            if len(dObjL) > 0:
                ob = dObjL[0]
                if (ob.getType() == 'definition') and ob.exists('item_linked'):
                    cObj = ob.getObj('item_linked')
                    if cObj.getRowCount() > 0:
                        idxP = cObj.getIndex('parent_name')
                        idxC = cObj.getIndex('child_name')
                        itemName = ob.getName()
                        if (self.__debug):
                            logger.info("\n\n+DictionaryApi.__expandLoopedDefinitions() current target item %s\n" % itemName)
                        cObjNext = self.__newDataCategory('item_linked', ['child_name', 'parent_name'])
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
                                    logger.info("+DictionaryApi.__expandLoopedDefinitions() missing child item %s\n" % (childItemName))
                            else:
                                cObjNext.append([row[idxC], row[idxP]])
                        if cObjNext.getRowCount() > 0:
                            ob.replace(cObjNext)
                        else:
                            ob.remove('item_linked')

    def __expandLoopedDefinitionsSAVE(self):
        """  Handle definitions containing looped item and item_linkded categories --
        """
        fullIndex = {}
        for d in self.__containerList:
            name = d.getName()
            if name not in fullIndex:
                fullIndex[name] = []
            fullIndex[name].append(d)

        for name, dObjL in fullIndex.items():
            if len(dObjL) > 0:
                ob = dObjL[0]
                if (ob.getType() == 'definition') and ob.exists('item_linked'):
                    cObj = ob.getObj('item_linked')
                    if cObj.getRowCount() > 1:
                        idxP = cObj.getIndex('parent_name')
                        idxC = cObj.getIndex('child_name')
                        itemName = ob.getName()

                        cObjNext = self.__newDataCategory('item_linked', ['child_name', 'parent_name'])
                        #
                        # Distribute the data for each row --
                        iChanges = 0
                        for row in cObj.getRowList():
                            #
                            parentItemName = row[idxP]
                            childItemName = row[idxC]
                            if childItemName != itemName:
                                iChanges += 1
                                if childItemName in fullIndex:
                                    #
                                    # Add this p/c link to the child definition -
                                    #
                                    self.__addItemLinkToDef(fullIndex[childItemName][0], parentItemName, childItemName)
                                else:
                                    # error missing child definition object.
                                    logger.info("+DictionaryApi.__expandLoopedDefinitions() missing child item %s\n" % (childItemName))
                            else:
                                cObjNext.append([row[idxC], row[idxP]])
                        if cObjNext.getRowCount() > 0 and iChanges > 0:
                            ob.replace(cObjNext)
                        else:
                            ob.remove('item_linked')

        for name, dObjL in fullIndex.items():
            if len(dObjL) > 0:
                ob = dObjL[0]
                if (ob.getType() == 'definition') and ob.exists('item_linked'):
                    cObj = ob.getObj('item_linked')
                    if cObj.getRowCount() > 0:
                        idxP = cObj.getIndex('parent_name')
                        idxC = cObj.getIndex('child_name')
                        itemName = ob.getName()
                        iChanges = 0
                        for row in cObj.getRowList():
                            #
                            parentItemName = row[idxP]
                            childItemName = row[idxC]
                            if childItemName != itemName:
                                logger.info("+DictionaryApi.__expandLoopedDefinitions() item name %s child item %s\n" % (itemName, childItemName))
                                iChanges += 1
                                if childItemName in fullIndex:
                                    #
                                    # Add this p/c link to the child definition -
                                    #
                                    self.__addItemLinkToDef(fullIndex[childItemName][0], parentItemName, childItemName)
                                else:
                                    # error missing child definition object.
                                    logger.info("+DictionaryApi.__expandLoopedDefinitions() missing definition child item %s\n" % (childItemName))
                        if iChanges > 0:
                            ob.remove('item_linked')

    def __consolidateDefinitions(self):
        """ Consolidate definitions into a single save frame section per definition.
        """
        fullIndex = {}
        for d in self.__containerList:
            name = d.getName()
            if name not in fullIndex:
                fullIndex[name] = []
            fullIndex[name].append(d)

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
                for d in dObjL[1:]:
                    xList = d.getObjNameList()
                    for nm in xList:
                        if nm not in dObjL[0].getObjNameList():
                            if (self.__debug):
                                logger.debug("Adding %s to %s\n" % (nm, name))
                            catObj = d.getObj(nm)
                            dObjL[0].append(catObj)
                        elif self.__replaceDefinition:
                            logger.debug("Replacing dictionary %s in %s" % (nm, name))
                            catObj = d.getObj(nm)
                            dObjL[0].replace(catObj)

        # create a new list of consolidated objects in original list order
        dList = []
        for nm in nList:
            if nm in fullIndex:
                dl = fullIndex[nm]
                dList.append(dl[0])
            else:
                logger.info("+DictionaryApi().__consolidate() missing object name %s\n" % nm)
        # update lists
        self.__containerList = dList

    def getDataTypeList(self):
        """ Return list of tuples containing ('code','primitive_code','construct','detail' )
        """
        rowList = []
        for code in sorted(self.__typesDict.keys()):
            tup = self.__typesDict[code]
            rowList.append((code, tup[0], tup[1], tup[2]))
        return rowList

    def getSubCategoryList(self):
        """ Return list of tuples containing ('id', 'description')
        """
        rowList = []
        for id in sorted(self.__subCategoryDict.keys()):
            description = self.__subCategoryDict[id]
            rowList.append((id, description))
        return rowList

    def getUnitsList(self):
        """ Return list of tuples containing ('id', 'description')
        """
        rowList = []
        for id in sorted(self.__itemUnitsDict.keys()):
            description = self.__itemUnitsDict[id]
            rowList.append((id, description))
        return rowList

    def getUnitsConversionList(self):
        """  Return list of tuples containing ('from_code','to_code','operator','factor')
        """
        return self.__itemUnitsConversionList

    def __getDataSections(self):
        """
        """
        for ob in self.__containerList:

            if (ob.getType() == 'data'):
                if (self.__debug):
                    logger.info("+DictionaryApi().__getDataSections() adding data container name %s  type  %s  \n" % (ob.getName(), ob.getType()))
                #  add detail to data type tuple
                tl = ob.getObj('item_type_list')
                if tl is not None:
                    for row in tl.getRowList():
                        if tl.hasAttribute('code') and tl.hasAttribute('primitive_code') and tl.hasAttribute('construct') and tl.hasAttribute('detail'):
                            self.__typesDict[row[tl.getIndex('code')]] = (row[tl.getIndex('primitive_code')], row[tl.getIndex('construct')], row[tl.getIndex('detail')])

                tl = ob.getObj('datablock')
                if tl is not None:
                    rL = tl.getRowList()
                    if len(rL) > 0:
                        self.__dataBlockDict = {}
                        if tl.hasAttribute('id') and tl.hasAttribute('description'):
                            row = rL[0]
                            self.__dataBlockDict['id'] = row[tl.getIndex('id')]
                            self.__dataBlockDict['description'] = row[tl.getIndex('description')]

                tl = ob.getObj('dictionary')
                if tl is not None:
                    rL = tl.getRowList()
                    if len(rL) > 0:
                        self.__dictionaryDict = {}
                        row = rL[0]
                        if tl.hasAttribute('datablock_id'):
                            self.__dictionaryDict['datablock_id'] = row[tl.getIndex('datablock_id')]
                        if tl.hasAttribute('title'):
                            self.__dictionaryDict['title'] = row[tl.getIndex('title')]
                        if tl.hasAttribute('version'):
                            self.__dictionaryDict['version'] = row[tl.getIndex('version')]

                tl = ob.getObj('dictionary_history')
                if tl is not None:
                    # history as a list of dictionaries -
                    self.__dictionaryHistoryList = []
                    for row in tl.getRowList():
                        if tl.hasAttribute('version') and tl.hasAttribute('revision') and tl.hasAttribute('update'):
                            tD = {}
                            tD['version'] = row[tl.getIndex('version')]
                            tD['revision'] = row[tl.getIndex('revision')]
                            tD['update'] = row[tl.getIndex('update')]
                            self.__dictionaryHistoryList.append(tD)

                tl = ob.getObj('sub_category')
                if tl is not None:
                    # subcategories as a dictionary by id
                    self.__subCategoryDict = {}
                    for row in tl.getRowList():
                        if tl.hasAttribute('id') and tl.hasAttribute('description'):
                            self.__subCategoryDict[row[tl.getIndex('id')]] = row[tl.getIndex('description')]

                tl = ob.getObj('category_group_list')
                if tl is not None:
                    # category groups as a dictionary by id of tuples
                    self.__categoryGroupDict = {}
                    for row in tl.getRowList():
                        if tl.hasAttribute('id') and tl.hasAttribute('description') and tl.hasAttribute('parent_id'):
                            tD = {}
                            tD['description'] = row[tl.getIndex('description')]
                            tD['parent_id'] = row[tl.getIndex('parent_id')]
                            tD['categories'] = []
                            self.__categoryGroupDict[row[tl.getIndex('id')]] = tD

                tl = ob.getObj('item_units_list')
                if tl is not None:
                    # units as a dictionary by code
                    self.__itemUnitsDict = {}
                    for row in tl.getRowList():
                        if tl.hasAttribute('code') and tl.hasAttribute('detail'):
                            self.__itemUnitsDict[row[tl.getIndex('code')]] = row[tl.getIndex('detail')]

                tl = ob.getObj('item_units_conversion')
                if tl is not None:
                    # units conversion as a simple list now
                    self.__itemUnitsConversionList = []
                    for row in tl.getRowList():
                        if tl.hasAttribute('from_code') and tl.hasAttribute('to_code') and tl.hasAttribute('operator') and tl.hasAttribute('factor'):
                            self.__itemUnitsConversionList.append(
                                (row[
                                    tl.getIndex('from_code')], row[
                                    tl.getIndex('to_code')], row[
                                    tl.getIndex('operator')], row[
                                    tl.getIndex('factor')]))

                tl = ob.getObj('pdbx_item_linked_group')
                if tl is not None:
                    # parent-child collections   [category_id] -> [(1,...),(3,...),(4,...) ]
                    self.__itemLinkedGroupDict = {}
                    for row in tl.getRowList():
                        if tl.hasAttribute('category_id') and tl.hasAttribute('link_group_id') and tl.hasAttribute(
                                'label') and tl.hasAttribute('context') and tl.hasAttribute('condition_id'):
                            category_id = row[tl.getIndex('category_id')]
                            if category_id not in self.__itemLinkedGroupDict:
                                self.__itemLinkedGroupDict[category_id] = []
                            self.__itemLinkedGroupDict[category_id].append((row[tl.getIndex('category_id')], row[tl.getIndex('link_group_id')],
                                                                            row[tl.getIndex('context')], row[tl.getIndex('condition_id')]))

                tl = ob.getObj('pdbx_item_linked_group_list')
                if tl is not None:
                    # parent-child collections   [(category_id,link_group_id)] -> [(child_name,parent_name,parent_category),(,...),(,...) ]
                    self.__itemLinkedGroupItemDict = {}
                    for row in tl.getRowList():
                        if tl.hasAttribute('child_category_id') and tl.hasAttribute('link_group_id') and tl.hasAttribute(
                                'child_name') and tl.hasAttribute('parent_name') and tl.hasAttribute('parent_category_id'):
                            child_category_id = row[tl.getIndex('child_category_id')]
                            link_group_id = row[tl.getIndex('link_group_id')]
                            if (child_category_id, link_group_id) not in self.__itemLinkedGroupItemDict:
                                self.__itemLinkedGroupItemDict[(child_category_id, link_group_id)] = []
                            self.__itemLinkedGroupItemDict[
                                (child_category_id, link_group_id)].append(
                                (row[
                                    tl.getIndex('child_name')], row[
                                    tl.getIndex('parent_name')], row[
                                    tl.getIndex('parent_category_id')]))
