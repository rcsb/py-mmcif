##
#
# File:     PdbxContainers.py
# Original: 02-Feb-2009   jdw
#
# Update:
#   23-Mar-2011   jdw Added method to rename attributes in category containers.
#   05-Apr-2011   jdw Change cif writer to select double quoting as preferred
#                     quoting style where possible.
#   16-Jan-2012   jdw Create base class for DataCategory class
#   22-Mar-2012   jdw when append attributes to existing categories update
#                     existing rows with placeholder null values.
#    2-Sep-2012   jdw add option to avoid embedded quoting that might
#                     confuse simple parsers.
#    4-Nov-2012   jdw extend static methods in CifName class
#   14-Nov-2012   jdw refactoring
#   28-Jun-2013   jdw expose remove method
#   01-Aug-2017   jdw migrate portions to public repo
#   14-Jan-2018   jdw add method filterObjectNameList(lastInOrder=None, selectOrder=None)
#    4-Apr-2018   jdw adding internal __eq__ and __hash__ methods
#    6-Aug-2018   jdw add setters/getters for container properties
#    5-Feb-2019   jdw add merge method and logging
##
"""

A collection of container classes supporting the PDBx/mmCIF storage model.

A base container class is defined which supports common features of
data and definition containers.   PDBx data files are organized in
sections called data blocks which are mapped to data containers.
PDBx dictionaries contain definition sections and data sections
which are mapped to definition and data containers respectively.

Data in both PDBx data files and dictionaries are organized in
data categories. In the PDBx syntax individual items or data
identified by labels of the form '_categoryName.attributeName'.
The terms category and attribute in PDBx jargon are analogous
table and column in relational data model, or class and attribute
in an object oriented data model.

The DataCategory class provides base storage container for instance
data and definition meta data.

"""
from __future__ import absolute_import

import logging
import sys

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"

logger = logging.getLogger(__name__)


class CifName(object):
    """Class of utilities for CIF-style data names -"""

    def __init__(self):
        pass

    @staticmethod
    def categoryPart(name):
        tname = ""
        try:
            if name.startswith("_"):
                tname = name[1:]
            else:
                tname = name

            i = tname.find(".")
            if i == -1:
                return tname
            else:
                return tname[:i]
        except Exception:
            return tname

    @staticmethod
    def attributePart(name):
        try:
            i = name.find(".")
            if i == -1:
                return None
            else:
                return name[i + 1 :]
        except Exception:
            return None

    @staticmethod
    def itemName(categoryName, attributeName):
        try:
            return "_" + str(categoryName) + "." + str(attributeName)
        except Exception:
            return None


class ContainerBase(object):
    """Container base class for data and definition objects."""

    def __init__(self, name):
        # The enclosing scope of the data container (e.g. data_/save_)
        self.__name = name
        # List of category names within this container -
        self.__objNameList = []
        # dictionary of DataCategory objects keyed by category name.
        self.__objCatalog = {}
        # dictionary for properties of the container
        self.__propCatalog = {}
        self.__type = None

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.__name == other.getName()
            and self.__objNameList == other.getObjNameList()
            and self.__objCatalog == other.getObjCatalog()
            and self.__type == other.getType()
            and self.__propCatalog == other.getPropCatalog()
        )

    def __hash__(self):
        return hash((self.__name, tuple(self.__objNameList), self.__type, tuple(self.__objCatalog.items()), tuple(self.__propCatalog.items())))

    def getObjCatalog(self):
        return self.__objCatalog

    def getPropCatalog(self):
        return self.__propCatalog

    def setProp(self, propName, value):
        try:
            self.__propCatalog[propName] = value
            return True
        except Exception:
            return False

    def getProp(self, propName):
        try:
            return self.__propCatalog[propName]
        except Exception:
            return None

    def getType(self):
        return self.__type

    def setType(self, cType):
        self.__type = cType

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def exists(self, name):
        if name in self.__objCatalog:
            return True
        else:
            return False

    def getObj(self, name):
        if name in self.__objCatalog:
            return self.__objCatalog[name]
        else:
            return None

    def getObjNameList(self):
        return self.__objNameList

    def append(self, obj):
        """Add the input object to the current object catalog. An existing object
        of the same name will be overwritten.
        """
        if obj.getName() is not None:
            if obj.getName() not in self.__objCatalog:
                # self.__objNameList is keeping track of object order here --
                self.__objNameList.append(obj.getName())
            self.__objCatalog[obj.getName()] = obj

    def replace(self, obj):
        """Replace an existing object with the input object"""
        if (obj.getName() is not None) and (obj.getName() in self.__objCatalog):
            self.__objCatalog[obj.getName()] = obj

    def printIt(self, fh=sys.stdout, pType="brief"):
        fh.write("+ %s container: %30s contains %4d categories\n" % (self.getType(), self.getName(), len(self.__objNameList)))
        for nm in self.__objNameList:
            fh.write("--------------------------------------------\n")
            fh.write("Data category: %s\n" % nm)
            if pType == "brief":
                self.__objCatalog[nm].printIt(fh)
            else:
                self.__objCatalog[nm].dumpIt(fh)

    def rename(self, curName, newName):
        """Change the name of an object in place -"""
        try:
            i = self.__objNameList.index(curName)
            self.__objNameList[i] = newName
            self.__objCatalog[newName] = self.__objCatalog[curName]
            self.__objCatalog[newName].setName(newName)
            return True
        except Exception:
            return False

    def remove(self, curName):
        """Revmove object by name.  Return True on success or False otherwise."""
        try:
            if curName in self.__objCatalog:
                del self.__objCatalog[curName]
                i = self.__objNameList.index(curName)
                del self.__objNameList[i]
                return True
            else:
                return False
        except Exception:
            pass

        return False

    def merge(self, container):
        """Merge the contents of the input container with the contents of the current container."""
        try:
            objNameList = container.getObjNameList()
            for objName in objNameList:
                self.append(container.getObj(objName))
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            return False
        return True

    def filterObjectNameList(self, lastInOrder=None, selectOrder=None):
        """Return an ordered list of categories in the input container subject to
        input -

           lastInOrder: list:  categories to be shifted to the end of the container.
           selectOrder: list:  ordered selection of container categories

        returns:
           filNameList: list:  augmented category list or full list (default)
        """
        filNameList = []
        if lastInOrder:
            objNameList = self.__objNameList
            lastList = []
            for nm in objNameList:
                if nm in lastInOrder:
                    lastList.append(nm)
                    continue
                filNameList.append(nm)
            filNameList.extend(lastList)
        elif selectOrder:
            for nm in selectOrder:
                if self.exists(nm):
                    filNameList.append(nm)
        else:
            filNameList = self.__objNameList

        return filNameList

    def toJSON(self):
        return self.__objCatalog


class DefinitionContainer(ContainerBase):
    def __init__(self, name):
        super(DefinitionContainer, self).__init__(name)
        self.setType("definition")
        self.__globalFlag = False

    def isCategory(self):
        if self.exists("category"):
            return True
        return False

    def isAttribute(self):
        if self.exists("item"):
            return True
        return False

    def getGlobal(self):
        return self.__globalFlag

    def printIt(self, fh=sys.stdout, pType="brief"):
        fh.write("Definition container: %30s contains %4d categories\n" % (self.getName(), len(self.getObjNameList())))
        if self.isCategory():
            fh.write("Definition type: category\n")
        elif self.isAttribute():
            fh.write("Definition type: item\n")
        else:
            fh.write("Definition type: undefined\n")

        for nm in self.getObjNameList():
            fh.write("--------------------------------------------\n")
            fh.write("Definition category: %s\n" % nm)
            if pType == "brief":
                self.getObj(nm).printIt(fh)
            else:
                self.getObj(nm).dumpId(fh)


class DataContainer(ContainerBase):
    """Container class for DataCategory objects."""

    def __init__(self, name):
        super(DataContainer, self).__init__(name)
        self.setType("data")
        self.__globalFlag = False

    def invokeDataBlockMethod(self, mType, method, db):
        _ = mType
        _ = db
        # self.__currentRow = 1
        exec(method.getInline(), globals(), locals())  # pylint: disable=exec-used

    def setGlobal(self):
        self.__globalFlag = True

    def getGlobal(self):
        return self.__globalFlag


class SaveFrameContainer(ContainerBase):
    def __init__(self, name):
        super(SaveFrameContainer, self).__init__(name)
        self.setType("definition")
