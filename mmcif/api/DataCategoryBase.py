##
#
# File:     DataCategoryBase.py
# Original: 02-Feb-2009   jdw
#
# Update:
#   14-Nov-2012   jdw refactoring
#   19-Nov-2012   jdw subclass UserList -
#                     _rowList becomes data
#   27-Nov-2012   jdw revise method removeAttribute()
#    7-Jan-2013   jdw add getAttributeIndexDict()
#   29-Jun-2013   jdw add removeRow()
#   24-Jun-2015   jdw add getRowAttributeDict(self, index) and getRowItemDict(self, index)
#   01-Aug-2017   jdw migrate portions to public repo
#   11-Nov-2018   jdw update consistent handling of raiseExceptions flag.
#   28-Jan-2019   jdw add row dictionary initialization, append, and extend methods
#    7-Feb-2019   jdw adjust initialization error checking to allow empty list
#   11-Mar-2019   jdw add getAttributeUniqueValueList()
##
"""

A collection of container classes supporting the PDBx/mmCIF storage model.

"""
from __future__ import absolute_import

import copy
import logging

# from mmcif.api import __STRING_TYPES__
from past.builtins import basestring
from six.moves import UserList, range, zip

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


logger = logging.getLogger(__name__)


# pylint: disable=arguments-differ
class DataCategoryBase(UserList):

    """Base object definition for a data category -

    This class subclasses UserList and implements many list-like features for
    row data managed by this class.

    """

    def __init__(self, name, attributeNameList=None, rowList=None, raiseExceptions=True, copyInputData=True):
        self._name = name
        if copyInputData:
            self._attributeNameList = copy.deepcopy(attributeNameList) if attributeNameList is not None else []
            # self.data = copy.deepcopy(rowList) if rowList is not None else []
        else:
            self._attributeNameList = attributeNameList if attributeNameList is not None else []
            # self.data = rowList if rowList is not None else []
        #
        # -------
        if rowList is None or (isinstance(rowList, list) and not rowList):
            self.data = []
        elif isinstance(rowList, list) and rowList:
            if isinstance(rowList[0], (list, tuple)):
                if copyInputData:
                    self.data = copy.deepcopy(rowList) if rowList is not None else []
                else:
                    self.data = rowList if rowList is not None else []

            elif isinstance(rowList[0], dict):
                rL = []
                for rowD in rowList:
                    rL.append([rowD[k] if k in rowD else None for k in self._attributeNameList])
                if copyInputData:
                    self.data = copy.deepcopy(rL)
                else:
                    self.data = rL

            else:
                if raiseExceptions:
                    raise ValueError
                else:
                    logger.error("Initialization failure")
        else:
            if raiseExceptions:
                raise ValueError
            else:
                logger.error("Initialization failure")

        # -------
        #
        self._itemNameList = []
        self.__mappingType = "DATA"
        self._raiseExceptions = raiseExceptions
        self._copyInputData = copyInputData
        #
        super(DataCategoryBase, self).__init__(self.data)
        #
        # Derived class data -
        #
        self._catalog = {}
        self._numAttributes = 0
        #
        self._stringTypes = basestring
        self.__setup()

    def __setup(self):
        self._numAttributes = len(self._attributeNameList)
        self._catalog = {}
        for attributeName in self._attributeNameList:
            attributeNameLC = attributeName.lower()
            self._catalog[attributeNameLC] = attributeName
        self.__updateItemLabels()

    # Add append/extend methods to accept row lists and dictionaries -
    #

    def append(self, row):
        if isinstance(row, (list, tuple)):
            self.data.append(row)
            return True
        elif isinstance(row, dict):
            try:
                # -
                self.data.append([row[k] if k in row else None for k in self._attributeNameList])
                return False
            except Exception as e:
                if self._raiseExceptions:
                    raise e
                else:
                    logger.error("Row processing failing with %s", str(e))
        else:
            if self._raiseExceptions:
                raise ValueError
            else:
                logger.error("Unsupported row type")
        return False

    def extend(self, rowList):
        if isinstance(rowList, list) and rowList:
            if isinstance(rowList[0], (list, tuple)):
                if self._copyInputData:
                    self.data.extend(copy.deepcopy(rowList))
                else:
                    self.data.extend(rowList)
                return True
            elif isinstance(rowList[0], dict):
                rL = []
                for rowD in rowList:
                    #  -
                    rL.append([rowD[k] if k in rowD else None for k in self._attributeNameList])
                if self._copyInputData:
                    self.data.extend(copy.deepcopy(rL))
                else:
                    self.data.extend(rL)
                return True
            else:
                if self._raiseExceptions:
                    raise ValueError
                else:
                    logger.error("unexpected row data type")
        else:
            logger.error("unexpected input data type")
        return False

    #
    # Setters/appenders
    #

    def setName(self, name):
        self._name = name

    def setRowList(self, rowList):
        if self._copyInputData:
            self.data = copy.deepcopy(rowList)
        else:
            self.data = rowList

    def setAttributeNameList(self, attributeNameList):
        if self._copyInputData:
            self._attributeNameList = copy.deepcopy(attributeNameList)
        else:
            self._attributeNameList = attributeNameList
        self.__setup()

    def appendAttribute(self, attributeName):
        attributeNameLC = attributeName.lower()
        if attributeNameLC in self._catalog:
            i = self._attributeNameList.index(self._catalog[attributeNameLC])
            self._attributeNameList[i] = attributeName
            self._catalog[attributeNameLC] = attributeName
        else:
            self._attributeNameList.append(attributeName)
            self._catalog[attributeNameLC] = attributeName
            #
        self._numAttributes = len(self._attributeNameList)
        return self._numAttributes

    def renameAttributes(self, mapDict):
        """Rename attributes according to mapping information in the input mapping dictionary {oldName: newName}"""
        atL = []
        for atName in self._attributeNameList:
            atL.append(mapDict[atName] if atName in mapDict else atName)
        self._attributeNameList = atL
        self.__setup()
        return True

    ##
    # Getters
    ##
    def get(self):
        return (self._name, self._attributeNameList, self.data)

    def getName(self):
        return self._name

    def getAttributeList(self):
        return self._attributeNameList

    def getAttributeCount(self):
        return len(self._attributeNameList)

    def getAttributeIndex(self, attributeName):
        try:
            return self._attributeNameList.index(attributeName)
        except Exception as e:
            logger.debug("Fails for %s with %s", attributeName, str(e))

        return -1

    def getAttributeIndexDict(self):
        rD = {}
        for ii, attributeName in enumerate(self._attributeNameList):
            rD[attributeName] = ii
        return rD

    def getIndex(self, attributeName):
        return self.getAttributeIndex(attributeName)

    def hasAttribute(self, attributeName):
        return attributeName in self._attributeNameList

    def getItemNameList(self):
        return self.__updateItemLabels()

    def getRowList(self):
        return self.data

    def getRowCount(self):
        return len(self.data)

    def getRow(self, index):
        try:
            return self.data[index]
        except Exception as e:
            if self._raiseExceptions:
                raise e
        return []

    def getRowAttributeDict(self, index):
        rD = {}
        try:
            for ii, v in enumerate(self.data[index]):
                rD[self._attributeNameList[ii]] = v
            return rD
        except Exception as e:
            if self._raiseExceptions:
                raise e

        return rD

    def getRowItemDict(self, index):
        rD = {}
        try:
            self.__updateItemLabels()
            for ii, v in enumerate(self.data[index]):
                rD[self._itemNameList[ii]] = v
            return rD
        except Exception as e:
            if self._raiseExceptions:
                raise e

        return rD

    def getAttributeValueList(self, attributeName):
        """Return a list of attribute values."""
        rL = []
        try:
            idx = self.getAttributeIndex(attributeName)
            rL = [row[idx] for row in self.data]
            return rL
        except Exception as e:
            if self._raiseExceptions:
                raise e
        return rL

    def getAttributeUniqueValueList(self, attributeName):
        """Return a sorted list of unique attribute values."""
        rL = []
        try:
            rD = {}
            idx = self.getAttributeIndex(attributeName)
            rD = {row[idx]: True for row in self.data}
            return sorted(rD.keys())
        except Exception as e:
            if self._raiseExceptions:
                raise e
        return rL

    def removeRow(self, index):
        try:
            del self.data[index]
            return True
        except Exception as e:
            if self._raiseExceptions:
                raise e

        return False

    def removeRows(self, indexList):
        try:
            iL = sorted(indexList, reverse=True)
            for i in iL:
                del self.data[i]
            return True
        except Exception as e:
            if self._raiseExceptions:
                raise e

        return False

    def removeAttribute(self, attributeName):
        """Remove the attribute from the attribute list along with any
        corresponding row data.
        """
        idx = self.getAttributeIndex(attributeName)
        if idx != -1:
            try:
                del self._attributeNameList[idx]
                for row in self.data:
                    try:
                        del row[idx]
                    except Exception:
                        pass
                self.__setup()
                return True
            except Exception:
                return False

    ##
    ##
    ##
    def __updateItemLabels(self):
        """Internal method to create mmCIF style item names for the current attribute
        list.
        """
        self._itemNameList = []
        for atName in self._attributeNameList:
            self._itemNameList.append("_" + str(self._name) + "." + atName)
        #
        return self._itemNameList

    def __alignLabels(self, row):
        """Internal method which aligns the list of input attributes with row data.

        If there are fewer labels than data elements in a row, then placeholder labels
        are created (e.g. "unlabeled_#")

        """
        if len(row) > len(self._attributeNameList):
            for i in range(len(self._attributeNameList), len(row) - 1):
                self._attributeNameList.insert(i, "unlabeled_" + str(i))
            if self.__mappingType == "ITEM":
                self.__updateItemLabels()

    def setMapping(self, mType):
        """Controls the manner in which this class returns data when accessed by
        index or in the context of an iterator:

        DATA      = list of row data elements as these were input. [default]

        ATTRIBUTE = row returned as a dictionary with attribute key

        ITEM      = row returned as a dictionary with item key

        """
        if mType in ["DATA", "ATTRIBUTE", "ITEM"]:
            self.__mappingType = mType
            return True
        else:
            return False

    def __str__(self):
        ans = "name:%r\nattrbuteList: %r\nData: %r\n" % (self._name, self._attributeNameList, list(self.data))
        return ans

    def __repr__(self):
        return self.__class__.__name__ + "(" + str(self) + ")"

    def __iter__(self):
        for dD in self.data:
            yield self.__applyMapping(dD)

    def __getitem__(self, idx):
        return self.__applyMapping(self.data[idx])

    def __setitem__(self, idx, value):
        dL = self.__extractMapping(value)
        self.data[idx] = dL

    def __applyMapping(self, dD):
        if self.__mappingType == "DATA":
            return dD
        elif self.__mappingType == "ATTRIBUTE":
            self.__alignLabels(dD)
            return dict(list(zip(self._attributeNameList, dD)))
        elif self.__mappingType == "ITEM":
            self.__alignLabels(dD)
            self.__updateItemLabels()
            return dict(list(zip(self._itemNameList, dD)))

    def __extractMapping(self, dD):
        try:
            if self.__mappingType == "DATA":
                return dD
            elif self.__mappingType == "ATTRIBUTE":
                rL = []
                for k, v in dD.items():
                    rL.insert(self._attributeNameList.index(k), v)
                return rL
            elif self.__mappingType == "ITEM":
                rL = []
                for k, v in dD.items():
                    rL.insert(self._itemNameList.index(k), v)
                return rL
        except Exception:
            if self._raiseExceptions:
                raise IndexError
        return None

    def cmpAttributeNames(self, dcObj):
        """Compare the attributeNameList in current data category (dca) and input data category .

        Return: (current attributes not in dcObj), (attributes common to both), (attributes in dcObj not in current data category)
        """
        sa = set(self.getAttributeList())
        sb = set(dcObj.getAttributeList())
        return tuple(sa - sb), tuple(sa & sb), tuple(sb - sa)

    def cmpAttributeValues(self, dcObj):
        """Compare the values by attribute for current data category (dca) and input data category.
        The comparison is performed independently for the values of corresponding attributes.
        Length differences are treated inequality out of hand.

        Return: [(attributeName, values equal flag (bool)), (attributeName, values equal flag (bool), ...]


        Note on slower alternative
        >>> import collections
        >>> compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        """
        rL = []
        try:
            sa = set(self.getAttributeList())
            sb = set(dcObj.getAttributeList())
            atComList = list(sa & sb)
            #
            lenEq = self.getRowCount() == dcObj.getRowCount()
            for at in atComList:
                if lenEq:
                    same = sorted(self.getAttributeValueList(at)) == sorted(dcObj.getAttributeValueList(at))
                else:
                    same = False
                rL.append((at, same))
            return rL
        except Exception as e:
            if self._raiseExceptions:
                raise e
        return rL

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        # return hash(tuple(sorted(self.__dict__.items())))
        return hash((self._name, tuple(self._attributeNameList), tuple(tuple(x) for x in self.data)))

    #
