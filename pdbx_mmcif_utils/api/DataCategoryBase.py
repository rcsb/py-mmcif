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
##
"""

A collection of container classes supporting the PDBx/mmCIF storage model.

"""
from __future__ import absolute_import
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


from six.moves import range
from six.moves import zip


from six.moves import UserList

import logging
logger = logging.getLogger(__name__)


class DataCategoryBase(UserList):

    """ Base object definition for a data category -

        This class subclasses UserList and implements many list-like features for
        row data managed by this class.

    """

    def __init__(self, name, attributeNameList=None, rowList=None):
        self._name = name
        self._attributeNameList = attributeNameList if attributeNameList is not None else []
        self.data = rowList if rowList is not None else []
        self._itemNameList = []
        self.__mappingType = "DATA"
        #
        super(DataCategoryBase, self).__init__(self.data)
        #
        # Derived class data -
        #
        self._catalog = {}
        self._numAttributes = 0
        #
        self.__setup()

    def __setup(self):
        self._numAttributes = len(self._attributeNameList)
        self._catalog = {}
        for attributeName in self._attributeNameList:
            attributeNameLC = attributeName.lower()
            self._catalog[attributeNameLC] = attributeName
    #
    # Setters/appenders
    #

    def setName(self, name):
        self._name = name

    def setRowList(self, rowList):
        self.data = rowList

    def setAttributeNameList(self, attributeNameList):
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
        except:
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
        return (len(self.data))

    def getRow(self, index):
        try:
            return self.data[index]
        except:
            return []

    def getRowAttributeDict(self, index):
        rD = {}
        try:
            for ii, v in enumerate(self.data[index]):
                rD[self._attributeNameList[ii]] = v
            return rD
        except:
            return rD

    def getRowItemDict(self, index):
        rD = {}
        try:
            self.__updateItemLabels()
            for ii, v in enumerate(self.data[index]):
                rD[self._itemNameList[ii]] = v
            return rD
        except:
            logger.exception("Item access failure at index %r" % index)
            return rD

    def removeRow(self, index):
        try:
            del self.data[index]
            return True
        except:
            pass

        return False

    def removeAttribute(self, attributeName):
        """ Remove the attribute from the attribute list along with any
            corresponding row data.
        """
        idx = self.getAttributeIndex(attributeName)
        if idx != -1:
            try:
                del self._attributeNameList[idx]
                for row in self.data:
                    try:
                        del row[idx]
                    except:
                        pass
                self.__setup()
                return True
            except:
                return False

    ##
    ##
    ##
    def __updateItemLabels(self):
        """  Internal method to create mmCIF style item names for the current attribute
             list.
        """
        self._itemNameList = []
        for atName in self._attributeNameList:
            self._itemNameList.append("_" + str(self._name) + "." + atName)
        #
        return self._itemNameList

    def __alignLabels(self, row):
        """  Internal method which aligns the list of input attributes with row data.

             If there are fewer labels that data elements in a row, then placeholder labels
             are creeated (e.g. "unlabeled_#")

        """
        if len(row) > len(self._attributeNameList):
            for i in range(len(self._attributeNameList), len(row) - 1):
                self._attributeNameList.insert(i, "unlabeled_" + str(i))
            if self.__mappingType == "ITEM":
                self.__updateItemLabels()

    def setMapping(self, mType):
        """  Controls the manner in which this class returns data when accessed by
             index or in the context of an iterator:

             DATA      = list of row data elements as these were input. [default]

             ATTRIBUTE = row returned as a dictionary with attribute key

             ITEM      = row returned as a dictionary with item key

        """
        if mType in ['DATA', 'ATTRIBUTE', 'ITEM']:
            self.__mappingType = mType
            return True
        else:
            return False

    def __str__(self):
        ans = 'name:%r\nattrbuteList: %r\nData: %r\n' % (self._name, self._attributeNameList, list(self.data),)
        return ans

    def __repr__(self):
        return self.__class__.__name__ + '(' + str(self) + ')'

    def __iter__(self):
        for d in self.data:
            yield self.__applyMapping(d)

    def __getitem__(self, idx):
        return self.__applyMapping(self.data[idx])

    def __setitem__(self, idx, value):
        dL = self.__extractMapping(value)
        self.data[idx] = dL

    def __applyMapping(self, d):
        if self.__mappingType == "DATA":
            return d
        elif self.__mappingType == "ATTRIBUTE":
            self.__alignLabels(d)
            return dict(list(zip(self._attributeNameList, d)))
        elif self.__mappingType == "ITEM":
            self.__alignLabels(d)
            self.__updateItemLabels()
            return dict(list(zip(self._itemNameList, d)))

    def __extractMapping(self, d):
        try:
            if self.__mappingType == "DATA":
                return d
            elif self.__mappingType == "ATTRIBUTE":
                rL = []
                for k, v in d.items():
                    rL.insert(self._attributeNameList.index(k), v)
                return rL
            elif self.__mappingType == "ITEM":
                rL = []
                for k, v in d.items():
                    rL.insert(self._itemNameList.index(k), v)
                return rL
        except:
            raise IndexError
