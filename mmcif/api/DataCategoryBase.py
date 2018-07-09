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

import copy
import logging

from mmcif.api import __STRING_TYPES__

from six.moves import UserList, range, zip

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


logger = logging.getLogger(__name__)


class DataCategoryBase(UserList):

    """ Base object definition for a data category -

        This class subclasses UserList and implements many list-like features for
        row data managed by this class.

    """

    def __init__(self, name, attributeNameList=None, rowList=None, raiseExceptions=True, copyInputData=True):
        self._name = name
        if copyInputData:
            self._attributeNameList = copy.deepcopy(attributeNameList) if attributeNameList is not None else []
            self.data = copy.deepcopy(rowList) if rowList is not None else []
        else:
            self._attributeNameList = attributeNameList if attributeNameList is not None else []
            self.data = rowList if rowList is not None else []
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
        #
        # try:
        #    basestring
        # except NameError:
        #    basestring = str
        # self._string_types = basestring
        # self._isPy3 = sys.version_info[0] == 3
        # if self._isPy3:
        #    self._string_types = str
        # else:
        #    try:
        #        self._string_types = basestring
        #    except Exception as e:
        #        logger.exception("Unable to assign string type %s" % str(e))
        self._string_types = __STRING_TYPES__
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
            pass
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
        """ Return a list of
        """
        try:
            idx = self.getAttributeIndex(attributeName)
            rL = [row[idx] for row in self.data]
            return rL
        except Exception as e:
            raise e

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

             If there are fewer labels than data elements in a row, then placeholder labels
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
        except Exception:
            raise IndexError

    def cmpAttributeNames(self, dcObj):
        """ Compare the attributeNameList in current data category (dca) and input data category .

            Return: (current attributes not in dcObj), (attributes common to both), (attributes in dcObj not in current data category)
        """
        sa = set(self.getAttributeList())
        sb = set(dcObj.getAttributeList())
        return tuple(sa - sb), tuple(sa & sb), tuple(sb - sa)

    def cmpAttributeValues(self, dcObj):
        """ Compare the values by attribute for current data category (dca) and input data category.
            The comparison is performed independently for the values of corresponding attributes.
            Length differences are treated inequality out of hand.

            Return: [(attributeName, values equal flag (bool)), (attributeName, values equal flag (bool), ...]


            Note on slower alternative
            >>> import collections
            >>> compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        """
        try:
            rL = []
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
            raise e

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
