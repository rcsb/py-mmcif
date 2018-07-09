##
#
# File:     DataCategory.py
# Original: 02-Feb-2009   jdw
#
# Update:
#   14-Nov-2012   jdw refactoring
#   17-Nov-2012   jdw self._rowList becomes data
#   21-Feb-2013   jdw add selectIndices(), selectValueWhere and selectValuesWhere.
#   10-Apr-2013   jdw add convenience method getValueOrDefault()
#   20-Jul-2015   jdw add selectIndicesFromList()
#   01-Aug-2017   jdw migrate portions to public repo
##
"""

A collection of container classes supporting the PDBx/mmCIF storage model.

"""
from __future__ import absolute_import

import logging
import sys

from mmcif.api.DataCategoryBase import DataCategoryBase

from six.moves import range, zip

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


logger = logging.getLogger(__name__)


class DataCategory(DataCategoryBase):
    """  Methods for creating, accessing, and formatting PDBx/mmCif data categories.
    """

    def __init__(self, name, attributeNameList=None, rowList=None, raiseExceptions=True, copyInputData=True):
        """Summary

        Args:
            name (TYPE): Description
            attributeNameList (None, optional): Description
            rowList (None, optional): Description
            raiseExceptions (bool, optional): Description
        """
        super(DataCategory, self).__init__(name, attributeNameList, rowList, raiseExceptions=raiseExceptions, copyInputData=copyInputData)
        #
        self.__verbose = False
        self._currentRowIndex = 0
        self.__currentAttribute = None
        #

    def setVerboseMode(self, bool):
        self.__verbose = bool

    def getCurrentAttribute(self):
        return self.__currentAttribute

    def getRowIndex(self):
        return self._currentRowIndex

    def getFullRow(self, index):
        """ Return a full row based on the length of the the attribute list or a row initialized with missing values
        """
        try:
            if (len(self.data[index]) < self._numAttributes):
                for ii in range(self._numAttributes - len(self.data[index])):
                    self.data[index].append('?')
            return self.data[index]
        except Exception as e:
            return ['?' for ii in range(self._numAttributes)]

    def getAttributeListWithOrder(self):
        oL = []
        for ii, att in enumerate(self._attributeNameList):
            oL.append((att, ii))
        return oL

    def appendAttributeExtendRows(self, attributeName, defaultValue="?"):
        attributeNameLC = attributeName.lower()
        if attributeNameLC in self._catalog:
            i = self._attributeNameList.index(self._catalog[attributeNameLC])
            self._attributeNameList[i] = attributeName
            self._catalog[attributeNameLC] = attributeName
            logger.info("Appending existing attribute %s\n" % attributeName)
        else:
            self._attributeNameList.append(attributeName)
            self._catalog[attributeNameLC] = attributeName
            # add a placeholder to any existing rows for the new attribute.
            if (len(self.data) > 0):
                for row in self.data:
                    row.append(defaultValue)
            #
        self._numAttributes = len(self._attributeNameList)
        return self._numAttributes

    def getValue(self, attributeName=None, rowIndex=None):
        if attributeName is None:
            attribute = self.__currentAttribute
        else:
            attribute = attributeName
        if rowIndex is None:
            rowI = self._currentRowIndex
        else:
            rowI = rowIndex

        if isinstance(attribute, str) and isinstance(rowI, int):
            try:
                return self.data[rowI][self._attributeNameList.index(attribute)]
            except (IndexError):
                raise IndexError
        raise IndexError(attribute)

    def getValueOrDefault(self, attributeName=None, rowIndex=None, defaultValue=''):
        """  Within the current category return the value of input attribute in the input rowIndex [0-based].

             On error or if the value missing or null return the default value. Empty values returned as is.

             Exceptions on for unknown attributeNames and out-of-range indices.
        """
        if attributeName is None:
            attribute = self.__currentAttribute
        else:
            attribute = attributeName
        if rowIndex is None:
            rowI = self._currentRowIndex
        else:
            rowI = rowIndex

        if isinstance(attribute, self._string_types) and isinstance(rowI, int):
            try:
                tV = self.data[rowI][self._attributeNameList.index(attribute)]
                if ((tV is None) or (tV in ['.', '?'])):
                    return defaultValue
                else:
                    return tV
            except Exception as e:
                # logger.exception("Failing attributeName %s rowIndex %r defaultValue %r" % (attributeName, rowIndex, defaultValue))
                raise e
        else:
            raise ValueError
        #
        return defaultValue

    def getFirstValueOrDefault(self, attributeNameList, rowIndex=0, defaultValue=''):
        """ Return the value from the first non-null attribute found in the input attribute list
            from the row (rowIndex) in the current category object.
        """
        try:
            for at in attributeNameList:
                if self.hasAttribute(at):
                    tV = self.getValue(at, rowIndex)
                    if ((tV is None) or (tV in ['', '.', '?'])):
                        continue
                    else:
                        return tV
        except Exception as e:
            raise e

        return defaultValue

    def setValue(self, value, attributeName=None, rowIndex=None):
        """ Set the value of an existing attribute.  rowIndex values >=0, where
            the category will be extended in length as needed.
        """
        if attributeName is None:
            attribute = self.__currentAttribute
        else:
            attribute = attributeName

        if rowIndex is None:
            rowI = self._currentRowIndex
        else:
            rowI = rowIndex

        if isinstance(attribute, self._string_types) and isinstance(rowI, int) and (rowI >= 0):
            try:
                ind = -2
                # if row index is out of range - add the rows -
                for ii in range(rowI + 1 - len(self.data)):
                    self.data.append(self.__emptyRow())
                # self.data[rowI][attribute]=value
                ll = len(self.data[rowI])
                ind = self._attributeNameList.index(attribute)

                # extend the list if needed -
                if (ind >= ll):
                    self.data[rowI].extend([None for ii in range(ind - (ll - 1))])

                self.data[rowI][ind] = value
                return True
            except (IndexError):
                if self.__verbose:
                    logger.exception("DataCategory(setvalue) index error category %s attribute %s row index %d col %d rowlen %d value %r\n" %
                                     (self._name, attribute, rowI, ind, len(self.data[rowI]), value))
                    logger.debug("DataCategory(setvalue) attribute %r length attribute list %d \n" % (attribute, len(self._attributeNameList)))
                    for ii, a in enumerate(self._attributeNameList):
                        logger.debug("DataCategory(setvalue) %d attributeName %r\n" % (ii, a))

                raise IndexError
            except (ValueError):
                if self.__verbose:
                    logger.exception("DataCategory(setvalue) value error category %s attribute %s row index %d value %r\n" %
                                     (self._name, attribute, rowI, value))
                raise ValueError
        else:
            raise ValueError

    def __emptyRow(self):
        return [None for ii in range(len(self._attributeNameList))]

    def replaceValue(self, oldValue, newValue, attributeName):
        try:
            numReplace = 0
            if attributeName not in self._attributeNameList:
                return numReplace
            ind = self._attributeNameList.index(attributeName)
            for row in self.data:
                if row[ind] == oldValue:
                    row[ind] = newValue
                    numReplace += 1
            return numReplace
        except Exception as e:
            raise e

    def replaceSubstring(self, oldValue, newValue, attributeName):
        try:
            numReplace = 0
            if attributeName not in self._attributeNameList:
                return numReplace
            ind = self._attributeNameList.index(attributeName)
            for row in self.data:
                val = row[ind]
                row[ind] = val.replace(oldValue, newValue)
                if val != row[ind]:
                    numReplace += 1
            return numReplace
        except Exception as e:
            raise e

    def selectIndices(self, attributeValue, attributeName):
        try:
            rL = []
            if attributeName not in self._attributeNameList:
                return rL
            ind = self._attributeNameList.index(attributeName)
            for ii, row in enumerate(self.data):
                if attributeValue == row[ind]:
                    rL.append(ii)
            return rL
        except Exception as e:
            raise e

    def selectIndicesFromList(self, attributeValueList, attributeNameList):
        rL = []
        try:
            indList = []
            for at in attributeNameList:
                indList.append(self._attributeNameList.index(at))
            indValList = list(zip(indList, attributeValueList))
            #
            numList = len(indValList)
            for ii, row in enumerate(self.data):
                nMatch = 0
                for ind, tVal in indValList:
                    if tVal == row[ind]:
                        nMatch += 1
                if nMatch == numList:
                    rL.append(ii)
        except Exception as e:
            if self.__verbose:
                logger.exception("Selection/index failure for values %r" % attributeValueList)
            raise e

        return rL

    def selectValuesWhere(self, attributeName, attributeValueWhere, attributeNameWhere):
        rL = []
        try:
            ind = self._attributeNameList.index(attributeName)
            indWhere = self._attributeNameList.index(attributeNameWhere)
            for ii, row in enumerate(self.data):
                if attributeValueWhere == row[indWhere]:
                    rL.append(row[ind])
        except Exception as e:
            if self.__verbose:
                logger.exception("Selection failure")
            raise e
        return rL

    def selectValueListWhere(self, attributeNameList, attributeValueWhere, attributeNameWhere):
        """ Return a  list of lists containing the values of input attributeNameList
            satisfiying the attribute value where condition.
        """
        rL = []
        try:
            indList = []
            for at in attributeNameList:
                indList.append(self._attributeNameList.index(at))
            indWhere = self._attributeNameList.index(attributeNameWhere)
            for ii, row in enumerate(self.data):
                if attributeValueWhere == row[indWhere]:
                    rL.append([row[jj] for jj in indList])
        except Exception as e:
            if self.__verbose:
                logger.exception("Selection failure")
            raise e
        return rL

    def invokeAttributeMethod(self, attributeName, type, method, db):
        self._currentRowIndex = 0
        self.__currentAttribute = attributeName
        self.appendAttribute(attributeName)
        currentRowIndex = self._currentRowIndex
        #
        ind = self._attributeNameList.index(attributeName)
        if len(self.data) == 0:
            row = [None for ii in range(len(self._attributeNameList) * 2)]
            row[ind] = None
            self.data.append(row)

        for row in self.data:
            ll = len(row)
            if (ind >= ll):
                row.extend([None for ii in range(2 * ind - ll)])
                row[ind] = None
            exec(method.getInline(), globals(), locals())
            self._currentRowIndex += 1
            currentRowIndex = self._currentRowIndex

    def invokeCategoryMethod(self, type, method, db):
        self._currentRowIndex = 0
        exec(method.getInline(), globals(), locals())

    def printIt(self, fh=sys.stdout):
        fh.write("--------------------------------------------\n")
        fh.write("  Category: %s attribute list length: %d\n" %
                 (self._name, len(self._attributeNameList)))
        for at in self._attributeNameList:
            fh.write("  Category: %s attribute: %s\n" % (self._name, at))

        fh.write("  Row value list length: %d\n" % len(self.data))
        #
        for row in self.data[:2]:
            #
            if len(row) == len(self._attributeNameList):
                for ii, v in enumerate(row):
                    fh.write("        %30s: %s ...\n" % (self._attributeNameList[ii], str(v)[:30]))
            else:
                fh.write("+WARNING - %s data length %d attribute name length %s mismatched\n" %
                         (self._name, len(row), len(self._attributeNameList)))

    def dumpIt(self, fh=sys.stdout):
        fh.write("--------------------------------------------\n")
        fh.write("  Category: %s attribute list length: %d\n" %
                 (self._name, len(self._attributeNameList)))
        for at in self._attributeNameList:
            fh.write("  Category: %s attribute: %s\n" % (self._name, at))

        fh.write("  Value list length: %d\n" % len(self.data))
        for row in self.data:
            for ii, v in enumerate(row):
                fh.write("        %30s: %s\n" % (self._attributeNameList[ii], v))
##
##
