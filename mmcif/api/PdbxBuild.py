##
# File:      PdbxBuild.py
# Orignal:   2009-Oct-13  Jdw
#
# Updates:
# 12-Mar-2012  jdw  Create full parent relations  methods in dictionary API.
#                     Provide isEnumerated test.
# 12-Aug-2012  jdw  Add alternative alternate metadata attribute method placeholders
# 30-Aug-2012  jdw  Implementation of alternate metadata.
# 21-Sep-2012  jdw  Adjust the presententation and sorting in dump and print methods.
# 23-Oct-2012  jdw  Adjust path and reorganize
# 10-Mar-2014  jdw  class DictionaryApi(object) in this module is deprecated -- Please use
#                   this class from dictionary/DictionaryApi()
##
"""
Utility classes for PDBx/mmCIF dictionary and data file management.
"""

from __future__ import absolute_import
from __future__ import print_function
from six.moves import zip
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import sys
from pdbx_v2.reader.PdbxReader import PdbxReader
from pdbx_v2.writer.PdbxWriter import PdbxWriter
from pdbx_v2.reader.PdbxContainers import *
from pdbx_v2.reader.DataCategory import DataCategory


class MethodDefinition(object):

    def __init__(self, method_id, code='calculate', language='Python', inline=None):
        self.method_id = method_id
        self.language = language
        self.code = code
        self.inline = inline

    def getId(self):
        return self.method_id

    def getLanguage(self):
        return self.language

    def getInline(self):
        return self.inline

    def printIt(self, fh=sys.stderr):
        fh.write("------------- Method definition -------------\n")
        fh.write("Id:           %s\n" % self.method_id)
        fh.write("Code:         %s\n" % self.code)
        fh.write("Language:     %s\n" % str(self.language))
        fh.write("Inline text:  %s\n" % str(self.inline))


class MethodReference(object):

    def __init__(self, method_id, type='attribute', category=None, attribute=None):
        self.method_id = method_id
        self.type = type
        self.categoryName = category
        self.attributeName = attribute

    def getId(self):
        return self.method_id

    def getType(self):
        return self.type

    def getCategoryName(self):
        return self.categoryName

    def getAttributeName(self):
        return self.attributeName

    def printIt(self, fh=sys.stderr):
        fh.write("--------------- Method Reference -----------------\n")
        fh.write("Id:             %s\n" % self.method_id)
        fh.write("Type:           %s\n" % self.type)
        fh.write("Category name:  %s\n" % str(self.categoryName))
        fh.write("Attribute name: %s\n" % str(self.attributeName))


class DictionaryApi(object):

    def __init__(self, dictObjList, verbose=False):
        self.dictObjList = dictObjList
        self.fullIndex = {}

        # self.dict={}
        # for d in self.dictObjList:
        #    if (not self.dict.has_key(d.getName())):
        #        self.dict[d.getName()]=[]
        #    self.dict[d.getName()].append(d)
        #
        #
        # Map category name to the unique list of attributes
        self.catNameIndex = {}
        #
        # Map dictionary objects names to definition containers -
        self.definitionIndex = {}
        #
        # data section/objects of the dictionary by category name -
        self.dataIndex = {}
        #
        # Map of types id->(regex,primitive_type)
        self.typesDict = {}
        #
        self.enumD = {'ENUMERATION_VALUE': ('item_enumeration', 'value'),
                      'ENUMERATION_DETAIL': ('item_enumeration', 'detail'),
                      'ENUMERATION_TUPLE': ('item_enumeration', None),
                      'ITEM_LINKED_PARENT': ('item_linked', 'parent_name'),
                      'ITEM_LINKED_CHILD': ('item_linked', 'child_name'),
                      'DATA_TYPE_CODE': ('item_type', 'code'),
                      'DATA_TYPE_REGEX': ('item_type_list', 'construct'),
                      'DATA_TYPE_PRIMITIVE': ('item_type_list', 'primitive_code'),
                      'ITEM_MANDATORY_CODE': ('item', 'mandatory_code'),
                      'ITEM_DESCRIPTION': ('item_description', 'description'),
                      'ITEM_UNITS': ('item_units', 'code'),
                      'ITEM_MANDATORY_CODE': ('item', 'mandatory_code'),
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
                      'ITEM_CONTEXT': ('pdbx_item_context', 'type'),
                      'ENUMERATION_CLOSED_FLAG': ('pdbx_item_enumeration_details', 'closed_flag')
                      }
        #
        self.methodDict = {}
        self.methodIndex = {}
        #
        self.__getIndex()
        self.__getMethods()
        self.__getTypes()

    def definitionExists(self, definitionName):
        if definitionName in self.definitionIndex:
            return True
        return False

    def getTypeCode(self, category, attribute):
        return self.__get('DATA_TYPE_CODE', category, attribute)

    def getTypeCodeAlt(self, category, attribute, fallBack=True):
        v = self.getTypeCodePdbx(category, attribute)
        if v is None:
            v = self.getTypeCodeNdb(category, attribute)
        if fallBack and v is None:
            v = self.getTypeCode(category, attribute)
        return v

    def getTypeCodeNdb(self, category, attribute):
        return self.__get('DATA_TYPE_CODE_NDB', category, attribute)

    def getTypeCodePdbx(self, category, attribute):
        return self.__get('DATA_TYPE_CODE_PDBX', category, attribute)

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
        code = self.__get('DATA_TYPE_CODE', category, attribute)
        if code in self.typesDict:
            return self.typesDict[code][1]
        return None

    def getTypeRegexAlt(self, category, attribute, fallBack=True):
        v = self.getTypeRegexPdbx(category, attribute)
        if v is None:
            v = self.getTypeRegexNdb(category, attribute)
        if fallBack and v is None:
            v = self.getTypeRegex(category, attribute)
        return v

    def getTypeRegexNdb(self, category, attribute):
        code = self.__get('DATA_TYPE_CODE_NDB', category, attribute)
        if code in self.typesDict:
            return self.typesDict[code][1]
        return None

    def getTypeRegexPdbx(self, category, attribute):
        code = self.__get('DATA_TYPE_CODE_PDBX', category, attribute)
        if code in self.typesDict:
            return self.typesDict[code][1]
        return None

    def getTypePrimitive(self, category, attribute):
        code = self.__get('DATA_TYPE_CODE', category, attribute)
        if code in self.typesDict:
            return self.typesDict[code][0]
        return None

    def getContextList(self, category, attribute):
        return self.__getList('ITEM_CONTEXT', category, attribute)

    def getCategoryContextList(self, category):
        return self.__getList('CATEGORY_CONTEXT', category, attribute=None)

    def getEnumList(self, category, attribute):
        return self.__getList('ENUMERATION_VALUE', category, attribute)

    def getEnumListAlt(self, category, attribute, fallBack=True):
        vL = self.getEnumListPdbx(category, attribute)
        if len(vL) < 1:
            vL = self.getEnumListNdb(category, attribute)
        if fallBack and len(vL) < 1:
            vL = self.getEnumList(category, attribute)
        return vL

    def getEnumListNdb(self, category, attribute):
        return self.__getList('ENUMERATION_VALUE_NDB', category, attribute)

    def getEnumListPdbx(self, category, attribute):
        return self.__getList('ENUMERATION_VALUE_PDBX', category, attribute)

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

    def getParentList(self, category, attribute):
        return self.__getList('ITEM_LINKED_PARENT', category, attribute)

    def getChildList(self, category, attribute):
        return self.__getList('ITEM_LINKED_CHILD', category, attribute)

    def getUnits(self, category, attribute):
        return self.__get('ITEM_UNITS', category, attribute)

    def getImplicitList(self):
        iL = []
        for name, dL in self.definitionIndex.items():
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
        for exC, exD in zip(exCL, exDL):
            exL.append((exC, exD))
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
        for exC, exD in zip(exCL, exDL):
            exL.append((exC, exD))
        return exL

    def getExampleListPdbx(self, category, attribute):
        exCL = self.__getListAll('ITEM_EXAMPLE_CASE_PDBX', category, attribute)
        exDL = self.__getListAll('ITEM_EXAMPLE_DETAIL_PDBX', category, attribute)
        exL = []
        for exC, exD in zip(exCL, exDL):
            exL.append((exC, exD))
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
        for exC, exD in zip(exCL, exDL):
            exL.append((exC, exD))
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
        for exC, exD in zip(exCL, exDL):
            exL.append((exC, exD))
        return exL

    def getCategoryExampleListPdbx(self, category):
        exCL = self.__getListAll('CATEGORY_EXAMPLE_CASE_PDBX', category, attribute=None)
        exDL = self.__getListAll('CATEGORY_EXAMPLE_DETAIL_PDBX', category, attribute=None)
        exL = []
        for exC, exD in zip(exCL, exDL):
            exL.append((exC, exD))
        return exL

    def getParentDictionary(self):
        """ Create a dictionary of parents relations accross all definnitions

            as d[child]=[parent,parent,...]

            Exclude self parents.
        """
        parentD = {}
        pAtN = self.enumD['ITEM_LINKED_PARENT'][1]
        cAtN = self.enumD['ITEM_LINKED_CHILD'][1]

        for dObj in self.dictObjList:
            dc = dObj.getObj(self.enumD['ITEM_LINKED_PARENT'][0])
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

    def dumpEnumFeatures(self, fh=sys.stdout):
        for k, vL in self.catNameIndex.items():
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
        for k, vL in self.catNameIndex.items():
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

    #
    def __get(self, enumCode, category, attribute=None):
        """ Returns the last occurrence of the input dictionary metadata (enumCode) for the input category/attribute
            encountered in the list of objects stored at the indicated definition index.

        """
        eS = None
        if enumCode not in self.enumD:
            return eS

        if (attribute is not None):
            nm = "_" + category + "." + attribute
        else:
            nm = category

        if nm in self.definitionIndex:
            dObjL = self.definitionIndex[nm]
            for dObj in dObjL:
                dc = dObj.getObj(self.enumD[enumCode][0])
                if dc is not None:
                    atN = self.enumD[enumCode][1]
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
        if enumCode not in self.enumD:
            return eL

        if (attribute is not None):
            nm = "_" + category + "." + attribute
        else:
            nm = category

        if nm in self.definitionIndex:
            dObjL = self.definitionIndex[nm]
            for dObj in dObjL:
                dc = dObj.getObj(self.enumD[enumCode][0])
                if dc is not None:
                    atN = self.enumD[enumCode][1]
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
        if enumCode not in self.enumD:
            return eL

        if (attribute is not None):
            nm = "_" + category + "." + attribute
        else:
            nm = category

        if nm in self.definitionIndex:
            dObjL = self.definitionIndex[nm]
            for dObj in dObjL:
                dc = dObj.getObj(self.enumD[enumCode][0])
                if dc is not None:
                    atN = self.enumD[enumCode][1]
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
        return self.methodIndex

    def categoryPart(self, name):
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

    def attributePart(self, name):
        i = name.find(".")
        if i == -1:
            return None
        else:
            return name[i + 1:]

    def __getIndex(self):
        for d in self.dictObjList:
            name = d.getName()
            type = d.getType()
            #
            if name not in self.fullIndex:
                self.fullIndex[name] = []
            self.fullIndex[name].append(d)
            #
            if (type == "definition" and d.isCategory()):
                if name not in self.catNameIndex:
                    self.catNameIndex[name] = []
                if name not in self.definitionIndex:
                    self.definitionIndex[name] = []
                self.definitionIndex[name].append(d)

            elif (type == "definition" and d.isAttribute()):
                catN = CifName.categoryPart(name)
                attN = CifName.attributePart(name)
                if catN not in self.catNameIndex:
                    self.catNameIndex[catN] = []
                if attN not in self.catNameIndex:
                    self.catNameIndex[catN].append(attN)
                if name not in self.definitionIndex:
                    self.definitionIndex[name] = []
                self.definitionIndex[name].append(d)
            elif (type == "data"):
                for nm in d.getObjNameList():
                    if nm not in self.dataIndex:
                        self.dataIndex[nm] = d.getObj(nm)
            else:
                pass

    def getDefinitionIndex(self):
        return self.definitionIndex

    def getFullIndex(self):
        return self.fullIndex

    def getMethod(self, id):
        if id in self.methodDict:
            return self.methodDict[id]
        else:
            return None

    def getCategoryList(self):
        return list(self.catNameIndex.keys())

    def getCategoryIndex(self):
        return self.catNameIndex

    def __getMethods(self):
        self.methodDict = {}
        self.methodIndex = {}
        for ob in self.dictObjList:
            if (ob.getType() == 'data'):
                ml = ob.getObj('method_list')
                if ml is not None:
                    for row in ml.getRowList():
                        if ml.hasAttribute('id') and ml.hasAttribute('inline'):
                            mth = MethodDefinition(row[ml.getIndex('id')], row[ml.getIndex('code')], row[ml.getIndex('language')], row[ml.getIndex('inline')])
                            self.methodDict[row[ml.getIndex('id')]] = mth

                ml = ob.getObj('datablock_methods')
                if ml is not None:
                    for row in ml.getRowList():
                        if ml.hasAttribute('method_id'):
                            mth = MethodReference(row[ml.getIndex('method_id')], 'datablock', ob.getName(), None)
                            if (ob.getName() in self.methodIndex):
                                self.methodIndex[ob.getName()].append(mth)
                            else:
                                self.methodIndex[ob.getName()] = []
                                self.methodIndex[ob.getName()].append(mth)
            elif (ob.getType() == 'definition'):
                mi = ob.getObj('category_methods')
                if mi is not None:
                    for row in mi.getRowList():
                        if mi.hasAttribute('method_id'):
                            mth = MethodReference(row[mi.getIndex('method_id')], 'category', ob.getName(), None)
                            if (ob.getName() in self.methodIndex):
                                self.methodIndex[ob.getName()].append(mth)
                            else:
                                self.methodIndex[ob.getName()] = []
                                self.methodIndex[ob.getName()].append(mth)
                mi = ob.getObj('item_methods')
                if mi is not None:
                    for row in mi.getRowList():
                        if mi.hasAttribute('method_id'):
                            mth = MethodReference(row[mi.getIndex('method_id')], 'attribute',
                                                  CifName.categoryPart(ob.getName()),
                                                  CifName.attributePart(ob.getName()))
                            if (ob.getName() in self.methodIndex):
                                self.methodIndex[ob.getName()].append(mth)
                            else:
                                self.methodIndex[ob.getName()] = []
                                self.methodIndex[ob.getName()].append(mth)
            else:
                pass
        return self.methodIndex

    def __getTypes(self):
        for ob in self.dictObjList:
            if (ob.getType() == 'data'):
                tl = ob.getObj('item_type_list')
                if tl is not None:
                    for row in tl.getRowList():
                        if tl.hasAttribute('code') and tl.hasAttribute('primitive_code') and tl.hasAttribute('construct'):
                            self.typesDict[row[tl.getIndex('code')]] = (row[tl.getIndex('primitive_code')], row[tl.getIndex('construct')])

    def dumpCategoryIndex(self, fh=sys.stdout):
        for k, vL in self.catNameIndex.items():
            uvL = list(set(vL))
            fh.write("Category: %s has %d attributes\n" % (k, len(uvL)))
            for v in sorted(uvL):
                fh.write("  Attribute: %s\n" % v)

    def dumpMethods(self, fh=sys.stdout):
        for k, vL in self.methodIndex.items():
            fh.write("Method index key: %s length %d\n" % (k, len(vL)))
            for v in vL:
                v.printIt(fh)
        #
        for k, vL in self.methodIndex.items():
            fh.write("\n------------------------------------\n")
            fh.write("Method inline text: %s\n" % k)
            for v in vL:
                fh.write("Method text: %s\n" % self.getMethod(v.getId()).getInline())


class PdbxBuild(object):

    def __init__(self, verbose=False, log=sys.stderr):
        #
        self.verbose = verbose
        self.__lfh = log
        #
        self.dictFileName = None
        self.dataFileName = None
        # list of dictionary data & definition containers
        self.myDictList = []
        self.myDictIndex = {}
        self.dApi = None
        #
        # list of data containers
        self.myDataList = []
        self.myDataIndex = {}
        #
        # list of ddl dictionary data and definition containers -
        self.ddlFileName = None
        self.myDdlDictList = []
        self.myDdlDictIndex = {}
        self.ddlParentIndex = {}
        self.ddlChildIndex = {}
        self.ddlImplicitList = []
        self.ddlApi = None
        #
        self.renamedDictList = []
        self.renamedDictIndex = {}
        #

    def setDdlFilePath(self, fileName):
        self.ddlFileName = fileName
        self.__readDdlDictionary()

    def __readDdlDictionary(self):
        ''' Read the DDL dictionary and populate some key internal data
        structures.
        '''
        ifh = open(self.ddlFileName, "r")
        pRd = PdbxReader(ifh)
        pRd.read(self.myDdlDictList)
        ifh.close()
        #        i=0
        #        for d in self.myDdlDictList:
        #            self.myDdlDictIndex[d.getName()]=i
        #            i+=1
        self.ddlApi = DictionaryApi(self.myDdlDictList, True)
        self.myDdlDictIndex = self.ddlApi.getFullIndex()
        for nm, dObjL in self.myDdlDictIndex.items():
            for dObj in dObjL:
                if dObj.getType() == "definition" and dObj.isAttribute():
                    catName = CifName.categoryPart(nm)
                    attName = CifName.attributePart(nm)
                    self.ddlParentIndex[nm] = self.ddlApi.getParentList(catName, attName)
                    self.ddlChildIndex[nm] = self.ddlApi.getChildList(catName, attName)
        #
        self.ddlImplicitList = self.ddlApi.getImplicitList()

        return self.myDdlDictList

    def __addItemAlias(self, dObj, oldName, newName):
        if "item_aliases" in dObj.getObjNameList():
            aCat = dObj.getObj("item_aliases")
        else:
            aCat = DataCategory("item_aliases")
            aCat.appendAttribute("alias_name")
            aCat.appendAttribute("dictionary")
            aCat.appendAttribute("version")
            aCat.append({})
            dObj.append(aCat)

        aCat.setValue("cif_rcsb.dic", "dictionary", 1)
        aCat.setValue("1.1", "version", 1)
        aCat.setValue(oldName, "alias_name", 1)

    def __addCategoryDefinitionContext(self, dObj, type):

        if "pdbx_category_context" in dObj.getObjNameList():
            aCat = dObj.getObj("pdbx_category_context")
        else:
            aCat = DataCategory("pdbx_category_context")
            aCat.appendAttribute("type")
            aCat.appendAttribute("category_id")
            aCat.append({})
            dObj.append(aCat)

        aCat.setValue(type, "type", 1)
        aCat.setValue(dObj.getName(), "category_id", 1)

    def __addItemDefinitionContext(self, dObj, type):

        if "pdbx_item_context" in dObj.getObjNameList():
            aCat = dObj.getObj("pdbx_item_context")
        else:
            aCat = DataCategory("pdbx_item_context")
            aCat.appendAttribute("type")
            aCat.appendAttribute("item_name")
            aCat.append({})
            dObj.append(aCat)

        aCat.setValue(type, "type", 1)
        aCat.setValue(dObj.getName(), "item_name", 1)

    def __reformatDefinition(self, dObj):
        dataCatList = dObj.getObjNameList()
        for dataCat in dataCatList:
            catObj = dObj.getObj(dataCat)
            catName = catObj.getName()
            attNameList = catObj.getAttributeList()
            for attName in attNameList:
                targetItem = "_" + catName + "." + attName
                if (targetItem in ['_category.description', '_item_description.description']):
                    desT = catObj.getValue(attName, 1)
                    if desT.find("\n") == -1:
                        catObj.setValue(desT.strip(), attName, 1)

    def __rename(self, oldName, newName, nameType, fh=sys.stdout):
        """First perform the rename operation on any definition
           with name 'oldName'.

           """
        if oldName in self.myDictIndex:
            for dObj in self.myDictIndex[oldName]:
                self.__renameDefinition(dObj, oldName, newName, nameType)
                #
                dObj.setName(newName)
                self.renamedDictList.append(dObj)
                # if not self.renamedDictIndex.has_key(newName):
                #    self.renamedDictIndex[newName]=[]
                # self.renamedDictIndex[newName].append(dObj)
        else:
            pass

    def __dumpDefinition(self, dObj, fh):
        name = dObj.getName()
        if dObj.isCategory():
            fh.write("\nCategory definition: %s\n" % name)
        elif dObj.isAttribute():
            fh.write("\nAttribute definition: %s\n" % name)
        else:
            pass

        # Dump the content of the defintion -
        dataCatList = dObj.getObjNameList()
        for dataCat in dataCatList:
            catObj = dObj.getObj(dataCat)
            catName = catObj.getName()
            attNameList = catObj.getAttributeList()
            for attName in attNameList:
                targetItem = "_" + catName + "." + attName
                fh.write("  Category %s attribute: %s\n" % (catName, attName))
                fh.write("  First value: %s\n" % catObj.getValue(attName, 1))

    def __renameDefinition(self, dObj, oldName, newName, nameType):
        #
        # Rename values of category identifiers or item names within the
        # the input definition from oldName to newName.
        #
        eList = ['_category.description', '_category_examples.case', '_item_examples.case', '_item_description.description',
                 '_ndb_category_description,description', '_ndb_category_examples.case',
                 '_ndb_item_examples.case', '_ndb_item_description.description']
        #
        defCatList = dObj.getObjNameList()
        for defCat in defCatList:
            catObj = dObj.getObj(defCat)
            catName = catObj.getName()
            attNameList = catObj.getAttributeList()
            for attName in attNameList:
                curItem = "_" + catName + "." + attName
                if (nameType == "category" and (curItem == "_category.id" or curItem in self.ddlChildIndex['_category.id'])):
                    # rename the category identifier any of its children
                    catObj.replaceValue(oldName, newName, attName)
                elif (nameType == "attribute" and (curItem == "_item.name" or curItem in self.ddlChildIndex['_item.name'])):
                    # rename the attribute identifier any of its children
                    catObj.replaceValue(oldName, newName, attName)
                else:
                    pass
                # Try to catch names in examples and descriptions -
                if (nameType == 'category' and (curItem in eList)):
                    catObj.replaceSubstring(oldName, newName, attName)
                    oldNameU = oldName.upper()
                    newNameU = newName.upper()
                    catObj.replaceSubstring(oldNameU, newNameU, attName)
                elif (nameType == 'attribute' and (curItem in eList)):
                    catObj.replaceSubstring(oldName, newName, attName)
                else:
                    pass

    def getDictionary(self):
        return self.dApi

    def __consolidateDefinitions(self):
        """ Consolidate definitions into a single saveframe section per definition.
        """
        # preserve the original order of sections -
        nList = []
        for dObj in self.myDictList:
            nm = dObj.getName()
            if nm not in nList:
                nList.append(nm)
        #
        for name, dObjL in self.myDictIndex.items():
            if len(dObjL) > 1:
                for d in dObjL[1:]:
                    xList = d.getObjNameList()
                    for nm in xList:
                        if nm not in dObjL[0].getObjNameList():
                            catObj = d.getObj(nm)
                            dObjL[0].append(catObj)

        # create a new list of consolidated objects in original list order
        dList = []
        for nm in nList:
            if nm in self.myDictIndex:
                dl = self.myDictIndex[nm]
                dList.append(dl[0])
            else:
                print("unknown", nm)

        # update lists
        self.myDictList = dList
        self.dApi = DictionaryApi(self.myDictList, True)
        self.myDictIndex = self.dApi.getFullIndex()
        return self.myDictList

    def readDictionary(self, fileName, consolidate=False):
        self.dictFileName = fileName
        ifh = open(fileName, "r")
        pRd = PdbxReader(ifh)
        pRd.read(self.myDictList)
        ifh.close()

        # i=0
        # for d in self.myDictList:
        #    self.myDictIndex[d.getName()]=i
        #    i+=1

        self.dApi = DictionaryApi(self.myDictList, True)
        self.myDictIndex = self.dApi.getFullIndex()
        if (consolidate):
            self.__consolidateDefinitions()

        return self.myDictList

    def getMethods(self):
        return self.dApi.getMethods()

    def getMethod(self, id):
        return self.dApi.getMethod(id)

    def writeDictionary(self, fileName):
        #
        ofh = open(fileName, "w")
        pWr = PdbxWriter(ofh)
        pWr.write(self.myDictList)
        ofh.close()

    def writeRenamedDictionary(self, fileName):
        #
        ofh = open(fileName, "w")
        pWr = PdbxWriter(ofh)
        pWr.write(self.renamedDictList)
        ofh.close()

    def writeDictionaryObjList(self, fileName, objList):
        #
        ofh = open(fileName, "w")
        pWr = PdbxWriter(ofh)
        pWr.write(objList)
        ofh.close()

    def readDataFile(self, fileName):
        self.dataFileName = fileName
        ifh = open(fileName, "r")
        pRd = PdbxReader(ifh)
        pRd.read(self.myDataList)
        ifh.close()
        i = 0
        for d in self.myDataList:
            self.myDataIndex[d.getName()] = i
            i += 1
        return self.myDataList

    def writeDataFile(self, fileName):
        ofh = open(fileName, "w")
        pWr = PdbxWriter(ofh)
        pWr.write(self.myDataList)
        ofh.close()

    def invokeMethods(self, fh=sys.stderr):
        mI = self.dApi.getMethodIndex()
        lenD = len(mI)
        i = 0
        for k, mRefL in mI.items():
            for mRef in mRefL:
                i += 1
                id = mRef.getId()
                type = mRef.getType()
                categoryName = mRef.getCategoryName()
                attributeName = mRef.getAttributeName()
                if (self.verbose):
                    fh.write("\n")
                    fh.write("++++++++++++++++++--------------------\n")
                    fh.write("Invoking dictionary method on file object: %s (%d/%d)\n" % (k, i, lenD))
                    fh.write(" + Method id: %s\n" % id)
                    fh.write(" + Type:      %s\n" % type)
                    fh.write(" + Category:  %s\n" % categoryName)
                    fh.write(" + Attribute: %s\n" % attributeName)
                #
                if type == "datablock":
                    if (self.verbose):
                        fh.write("Invoke datablock method %s\n" % id)
                    # self.invokeDataBlockMethod(type,self.dApi.getMethod(id))
                    # continue
                #
                for db in self.myDataList:
                    if type == "category":
                        if not db.exists(categoryName):
                            dc = DataCategory(categoryName)
                            db.append(dc)
                        dObj = db.getObj(categoryName)
                        dObj.invokeCategoryMethod(type, self.dApi.getMethod(id), db)
                    elif type == "attribute":
                        if not db.exists(categoryName):
                            dc = DataCategory(categoryName)
                            db.append(dc)
                        dObj = db.getObj(categoryName)
                        dObj.invokeAttributeMethod(attributeName, type, self.dApi.getMethod(id), db)
                    elif type == "datablock":
                        fh.write("Invoke datablock method %s\n" % id)
                        db.invokeDataBlockMethod(type, self.dApi.getMethod(id), db)
                    else:
                        pass

    def renameDefinition(self, currentName, NewName, nameType, fh=sys.stdout):
        self.__rename(currentName, NewName, nameType, fh)

    def renameDefinitionList(self, renameList, aliasDict, fh=sys.stdout):
        """Make one pass over all of the containers in the dictionary
           making all of the replacements in the renameList

           """
        for nameType, oldName, newName in renameList:
            if oldName in self.myDictIndex:
                for dObj in self.myDictIndex[oldName]:
                    self.__renameDefinition(dObj, oldName, newName, nameType)
                    dObj.setName(newName)
                    self.renamedDictList.append(dObj)
                    # if not self.renamedDictIndex.has_key(newName):
                    #    self.renamedDictIndex[newName]=[]
                    # self.renamedDictIndex[newName].append(dObj)
                    #
                    if dObj.isAttribute():
                        self.__addItemAlias(dObj, oldName, newName)
                        self.__addItemDefinitionContext(dObj, 'RCSB_LOCAL')
                    elif dObj.isCategory():
                        self.__addCategoryDefinitionContext(dObj, 'RCSB_LOCAL')
            else:
                pass

        # Now re-check for other substitutions in rename list -
        for dObj in self.renamedDictList:
            for nameType, oldName, newName in renameList:
                self.__renameDefinition(dObj, oldName, newName, nameType)
            for oldName, newName in aliasDict.items():
                if oldName.startswith("_"):
                    nameType = "attribute"
                else:
                    nameType = "category"
                self.__renameDefinition(dObj, oldName, newName, nameType)

            self.__reformatDefinition(dObj)

        return self.renamedDictList

    def dumpMethods(self, fh=sys.stdout):
        self.dApi.dumpMethods(fh)

    def dumpDictionary(self, fh=sys.stdout):
        lenD = len(self.myDictList)
        fh.write("\n--------------------------------------------\n")
        fh.write("\n-----------DUMP DICTIONARY------------------\n")
        fh.write("Dictionary object list length is: %d\n" % lenD)
        i = 1
        for dObj in self.myDictList:
            if len(dObj.getName()) > 0:
                fh.write("\n")
                fh.write("++++++++++++++++++--------------------\n")
                fh.write("Dumping dictionary object named: %s (%d/%d)\n" %
                         (dObj.getName(), i, lenD))
                dObj.printIt(fh)
            i += 1
    #

    def dumpDataFile(self, fh=sys.stdout):
        lenD = len(self.myDataList)
        fh.write("\n--------------------------------------------\n")
        fh.write("\n-----------DUMP DATAFILE--------------------\n")
        fh.write("Data object list length is: %d\n" % lenD)
        i = 1
        for dObj in self.myDataList:
            fh.write("\n")
            fh.write("++++++++++++++++++--------------------\n")
            fh.write("Dumping data file object named: %s (%d/%d)\n" %
                     (dObj.getName(), i, lenD))
            dObj.printIt(fh)
            i += 1
    #

    def dumpDictionaryAliases(self, fh=sys.stdout):
        """ Return alias dictionary and a complete list of all definitions (name,type)
        """
        lenD = len(self.myDictList)
        fh.write("\n--------------------------------------------\n")
        fh.write("\n-----------DUMP DICTIONARY------------------\n")
        fh.write("Dictionary object list length is: %d\n" % lenD)
        i = 1
        nList = []
        aDict = {}
        for dObj in self.myDictList:
            type = dObj.getType()
            if (type == "definition"):
                name = str(dObj.getName()).strip()
                if dObj.isCategory():
                    fh.write("  Category: %s\n" % name)
                    nList.append((name, "category"))
                elif dObj.isAttribute():
                    nList.append((name, "attribute"))
                    if name.startswith("_pdbx_") or (name.find(".pdbx_") > 0):
                        fh.write("  PDBX Attribute: %s\n" % name)
                        aliasCat = dObj.getObj("item_aliases")
                        if (aliasCat is not None):
                            # aliasCat.printIt(fh)
                            for row in aliasCat.getRowList():
                                if (aliasCat.hasAttribute("dictionary") and aliasCat.hasAttribute("alias_name")
                                        and (row[aliasCat.getIndex('dictionary')] == "cif_rcsb.dic")):
                                    fh.write("       RCSB alias name is %s\n" % row['alias_name'])
                                    alias = row[aliasCat.getIndex('alias_name')]
                                    aDict[alias] = name
                    elif name.startswith("_ndb_"):
                        fh.write("  NDB Attribute: %s\n" % name)
                    elif name.startswith("_em_"):
                        fh.write("  EM Attribute: %s\n" % name)
                    else:
                        pass
                else:
                    pass
            i += 1
        #
        for k, v in aDict.items():
            fh.write("alias %s  name %s\n" % (k, v))
        #
        return (aDict, nList)
