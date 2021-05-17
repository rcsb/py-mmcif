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
#    4-Oct-2018   jdw add optional method parameter returnCount=0 to selectValuesWhere() and selectValueListWhere()
#   11-Nov-2018   jdw update consistent handling of raiseExceptions flag.
#    5-May-2019   jdw add selectValuesWhereConditions() and countValuesWhereConditions()
#    7-Aug-2019   jdw don't raise exception for *OrDefault() methods.
##
"""

A collection of container classes supporting the PDBx/mmCIF storage model.

"""

from __future__ import absolute_import

import logging
import sys

from six.moves import range
from six.moves import zip

from mmcif.api.DataCategoryBase import DataCategoryBase

__docformat__ = "google en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


logger = logging.getLogger(__name__)


class DataCategory(DataCategoryBase):
    """Methods for creating, accessing, and formatting PDBx/mmCif data categories."""

    def __init__(self, name, attributeNameList=None, rowList=None, raiseExceptions=True, copyInputData=True):
        """Summary

        Args:
            name (str): Category name
            attributeNameList (None, optional):  Initial attribute names
            rowList (None, optional): Initial category data organized in rows corresponding to the attribute name list
            raiseExceptions (bool, optional): Flag to control if expections are raised or handled internally
            copyInputData (bool, optional):  Copy rather than reference input data
        """
        super(DataCategory, self).__init__(name, attributeNameList, rowList, raiseExceptions=raiseExceptions, copyInputData=copyInputData)
        #
        self.__verbose = False
        self._currentRowIndex = 0
        self.__currentAttribute = None
        #

    def setVerboseMode(self, boolVal):
        self.__verbose = boolVal

    def getCurrentAttribute(self):
        return self.__currentAttribute

    def getRowIndex(self):
        return self._currentRowIndex

    def getFullRow(self, index):
        """Return a full row based on the length of the the attribute list or a row initialized with missing values"""
        try:
            if len(self.data[index]) < self._numAttributes:
                for _ in range(self._numAttributes - len(self.data[index])):
                    self.data[index].append("?")
            return self.data[index]
        except Exception as e:
            logger.debug("Returning an empty row at %d (%s)", index, str(e))
        return ["?" for ii in range(self._numAttributes)]

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
            logger.info("Appending existing attribute %s", attributeName)
        else:
            self._attributeNameList.append(attributeName)
            self._catalog[attributeNameLC] = attributeName
            # add a placeholder to any existing rows for the new attribute.
            if self.data:
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

        if isinstance(attribute, self._stringTypes) and isinstance(rowI, int):
            try:
                return self.data[rowI][self._attributeNameList.index(attribute)]
            except IndexError:
                if self._raiseExceptions:
                    raise IndexError
        if self._raiseExceptions:
            raise IndexError(attribute)
        else:
            return None

    def getValueOrDefault(self, attributeName=None, rowIndex=None, defaultValue=""):
        """Within the current category return the value of input attribute in the input rowIndex [0-based].

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

        if isinstance(attribute, self._stringTypes) and isinstance(rowI, int):
            try:
                tV = self.data[rowI][self._attributeNameList.index(attribute)]
                if (tV is None) or (tV in [".", "?"]):
                    return defaultValue
                else:
                    return tV
            except Exception as e:
                logger.debug("Failing attributeName %s rowIndex %r defaultValue %r with %s", attributeName, rowIndex, defaultValue, str(e))
                # if self._raiseExceptions:
                #     raise e
                # Returning default -- no exception
        else:
            if self._raiseExceptions:
                raise ValueError
        #
        return defaultValue

    def getFirstValueOrDefault(self, attributeNameList, rowIndex=0, defaultValue=""):
        """Return the value from the first non-null attribute found in the input attribute list
        from the row (rowIndex) in the current category object.
        """
        try:
            for at in attributeNameList:
                if self.hasAttribute(at):
                    tV = self.getValue(at, rowIndex)
                    if (tV is None) or (tV in ["", ".", "?"]):
                        continue
                    else:
                        return tV
        except Exception as e:
            logger.debug("Failing with %s", str(e))
            # if self._raiseExceptions:
            #    raise e
        return defaultValue

    def setValue(self, value, attributeName=None, rowIndex=None):
        """Set the value of an existing attribute.  rowIndex values >=0, where
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

        if isinstance(attribute, self._stringTypes) and isinstance(rowI, int) and (rowI >= 0):
            try:
                ind = -2
                # if row index is out of range - add the rows -
                for ii in range(rowI + 1 - len(self.data)):
                    self.data.append(self.__emptyRow())
                # self.data[rowI][attribute]=value
                ll = len(self.data[rowI])
                ind = self._attributeNameList.index(attribute)

                # extend the list if needed -
                if ind >= ll:
                    self.data[rowI].extend([None for ii in range(ind - (ll - 1))])

                self.data[rowI][ind] = value
                return True
            except IndexError:
                if self.__verbose:
                    logger.exception(
                        "DataCategory(setvalue) index error category %s attribute %s row index %d col %d rowlen %d value %r",
                        self._name,
                        attribute,
                        rowI,
                        ind,
                        len(self.data[rowI]),
                        value,
                    )
                    logger.debug("DataCategory(setvalue) attribute %r length attribute list %d", attribute, len(self._attributeNameList))
                    for ii, aV in enumerate(self._attributeNameList):
                        logger.debug("DataCategory(setvalue) %d attributeName %r", ii, aV)
                if self._raiseExceptions:
                    raise IndexError
            except ValueError:
                if self.__verbose:
                    logger.exception("DataCategory(setvalue) value error category %s attribute %s row index %d value %r", self._name, attribute, rowI, value)
                if self._raiseExceptions:
                    raise ValueError
        else:
            if self._raiseExceptions:
                raise ValueError
        return False

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
            if self._raiseExceptions:
                raise e
        return numReplace

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
            if self._raiseExceptions:
                raise e
        return numReplace

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
            if self._raiseExceptions:
                raise e
        return rL

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
                logger.exception("Selection/index failure for values %r", attributeValueList)
            if self._raiseExceptions:
                raise e

        return rL

    def selectValuesWhere(self, attributeName, attributeValueWhere, attributeNameWhere, returnCount=0):
        rL = []
        try:
            iCount = 0
            ind = self._attributeNameList.index(attributeName)
            indWhere = self._attributeNameList.index(attributeNameWhere)
            for row in self.data:
                if attributeValueWhere == row[indWhere]:
                    rL.append(row[ind])
                    iCount += 1
                    if returnCount and (iCount >= returnCount):
                        break
        except Exception as e:
            if self.__verbose:
                logger.exception("Selection failure")
            if self._raiseExceptions:
                raise e
        return rL

    def selectValueListWhere(self, attributeNameList, attributeValueWhere, attributeNameWhere, returnCount=0):
        """Return a  list of lists containing the values of input attributeNameList
        satisfying the attribute value where condition.
        """
        rL = []
        try:
            iCount = 0
            indList = []
            for at in attributeNameList:
                indList.append(self._attributeNameList.index(at))
            indWhere = self._attributeNameList.index(attributeNameWhere)
            for row in self.data:
                if attributeValueWhere == row[indWhere]:
                    rL.append([row[jj] for jj in indList])
                    iCount += 1
                    if returnCount and (iCount >= returnCount):
                        break
        except Exception as e:
            if self.__verbose:
                logger.exception("Selection failure")
            if self._raiseExceptions:
                raise e
        return rL

    def selectValuesWhereConditions(self, attributeName, conditionsD, returnCount=0):
        rL = []
        try:
            iCount = 0
            ind = self._attributeNameList.index(attributeName)
            idxD = {k: self._attributeNameList.index(k) for k, v in conditionsD.items()}
            #
            #
            for row in self.data:
                ok = True
                for k, v in conditionsD.items():
                    ok = (v == row[idxD[k]]) and ok
                if ok:
                    rL.append(row[ind])
                    iCount += 1
                    if returnCount and (iCount >= returnCount):
                        break
        except Exception as e:
            if self.__verbose:
                logger.exception("Selection failure")
            if self._raiseExceptions:
                raise e
        return rL

    def countValuesWhereConditions(self, conditionsD):
        """Count row instances subject to input equivalence conditions

        Args:
            conditionsD (dict): {'atName': value, ....}

        Raises:
            e: any failure

        Returns:
            int: count of instances satisfying input conditions
        """
        try:
            iCount = 0
            idxD = {k: self._attributeNameList.index(k) for k, v in conditionsD.items()}
            #
            for row in self.data:
                ok = True
                for k, v in conditionsD.items():
                    ok = (v == row[idxD[k]]) and ok
                if ok:
                    iCount += 1

        except Exception as e:
            if self.__verbose:
                logger.exception("Selection failure")
            if self._raiseExceptions:
                raise e
        return iCount

    def countValuesWhereOpConditions(self, conditionTupleList):
        """Count row instances subject to input condition list

        Args:
            conditionTupleList (list): (attributeName, op, value) where (op = 'eq', 'gt(int)', 'lt(int)', 'in', 'ne', 'not in')

        Raises:
            e: any failure

        Returns:
            int: count of instances satisfying input conditions
        """
        try:
            iCount = 0
            idxD = {atName: self._attributeNameList.index(atName) for (atName, op, value) in conditionTupleList}
            #
            for row in self.data:
                ok = True
                for (atName, op, v) in conditionTupleList:
                    if op == "eq":
                        ok = (v == row[idxD[atName]]) and ok
                    elif op == "ne":
                        ok = (v != row[idxD[atName]]) and ok
                    elif op == "lt(int)":
                        ok = (int(row[idxD[atName]]) < v) and ok
                    elif op == "gt(int)":
                        ok = (int(row[idxD[atName]]) > v) and ok
                    elif op == "in":
                        ok = (row[idxD[atName]] in v) and ok
                    elif op == "not in":
                        ok = (row[idxD[atName]] not in v) and ok
                if ok:
                    iCount += 1

        except Exception as e:
            if self.__verbose:
                logger.exception("Selection failure")
            if self._raiseExceptions:
                raise e
        return iCount

    #
    def getCombinationCounts(self, attributeList):
        """Count the value occurrences of the input attributeList in the category.

        Args:
            attributeList (list): target list of attribute names

        Returns:

            cD[(attribute value, ... )] = count

        """
        cD = {}
        try:
            idxL = [self._attributeNameList.index(atName) for atName in attributeList]
            #
            for row in self.data:
                ky = tuple([row[jj] for jj in idxL])
                cD[ky] = cD[ky] + 1 if ky in cD else 1
        except Exception as e:
            if self.__verbose:
                logger.exception("Selection failure")
            if self._raiseExceptions:
                raise e
        return cD

    def getCombinationCountsWithConditions(self, attributeList, conditionTupleList):
        """Count the value occurrences of the input attributeList in the category.

        Args:
            attributeList (list): target list of attribute names
            conditionTupleList (list): (attributeName, op, value) where (op = 'eq', 'gt(int)', 'lt(int)', 'in', 'ne', 'not in')

        Returns:

            cD[(attribute value, ... )] = count
        """
        cD = {}
        try:
            idxL = [self._attributeNameList.index(atName) for atName in attributeList]
            idxD = {atName: self._attributeNameList.index(atName) for (atName, op, value) in conditionTupleList}
            #
            for row in self.data:
                ok = True
                for (atName, op, v) in conditionTupleList:
                    if op == "eq":
                        ok = (v == row[idxD[atName]]) and ok
                    elif op == "ne":
                        ok = (v != row[idxD[atName]]) and ok
                    elif op == "lt(int)":
                        ok = (int(row[idxD[atName]]) < v) and ok
                    elif op == "gt(int)":
                        ok = (int(row[idxD[atName]]) > v) and ok
                    elif op == "in":
                        ok = (row[idxD[atName]] in v) and ok
                    elif op == "not in":
                        ok = (row[idxD[atName]] not in v) and ok
                if ok:
                    ky = tuple([row[jj] for jj in idxL])
                    cD[ky] = cD[ky] + 1 if ky in cD else 1
        except Exception as e:
            if self.__verbose:
                logger.exception("Selection failure")
            if self._raiseExceptions:
                raise e
        return cD

    def invokeAttributeMethod(self, attributeName, mType, method, db):
        _ = mType
        _ = db
        self._currentRowIndex = 0
        self.__currentAttribute = attributeName
        self.appendAttribute(attributeName)
        currentRowIndex = self._currentRowIndex  # pylint: disable=possibly-unused-variable
        #
        ind = self._attributeNameList.index(attributeName)
        if not self.data:
            row = [None for ii in range(len(self._attributeNameList) * 2)]
            row[ind] = None
            self.data.append(row)

        for row in self.data:
            ll = len(row)
            if ind >= ll:
                row.extend([None for ii in range(2 * ind - ll)])
                row[ind] = None
            exec(method.getInline(), globals(), locals())  # pylint: disable=exec-used
            self._currentRowIndex += 1
            currentRowIndex = self._currentRowIndex

    def invokeCategoryMethod(self, mType, method, db):
        _ = mType
        _ = db
        self._currentRowIndex = 0
        exec(method.getInline(), globals(), locals())  # pylint: disable=exec-used

    def printIt(self, fh=sys.stdout):
        fh.write("--------------------------------------------\n")
        fh.write("  Category: %s attribute list length: %d\n" % (self._name, len(self._attributeNameList)))
        for at in self._attributeNameList:
            fh.write("  Category: %s attribute: %s\n" % (self._name, at))

        fh.write("  Row value list length: %d\n" % len(self.data))
        #
        for row in self.data[:2]:
            #
            if len(row) == len(self._attributeNameList):
                for ii, v in enumerate(row):
                    fh.write("       %30s: %s ...\n" % (self._attributeNameList[ii], str(v)[:30]))
            else:
                fh.write("+WARNING - %s data length %d attribute name length %s mismatched\n" % (self._name, len(row), len(self._attributeNameList)))

    def dumpIt(self, fh=sys.stdout):
        fh.write("--------------------------------------------\n")
        fh.write("  Category: %s attribute list length: %d\n" % (self._name, len(self._attributeNameList)))
        for at in self._attributeNameList:
            fh.write("  Category: %s attribute: %s\n" % (self._name, at))

        fh.write("  Value list length: %d\n" % len(self.data))
        for jj, row in enumerate(self.data):
            for ii, v in enumerate(row):
                fh.write("%4d        %30s: %s\n" % (jj, self._attributeNameList[ii], v))


##
##
