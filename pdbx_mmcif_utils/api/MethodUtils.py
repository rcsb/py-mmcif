##
# File:      MethodUtils.py
# Orignal:   Aug 12, 2013   Jdw
#
# Updates:
#   01-Aug-2017   jdw migrate portions to public repo
##
"""
Utility classes for applying dictionary methods on PDBx/mmCIF data files.
"""
from __future__ import absolute_import

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"




import sys

# from pdbx_mmcif_utils.api.PdbxContainers import *
from pdbx_mmcif_utils.api.DataCategory import DataCategory
from pdbx_mmcif_utils.api.DictionaryApi import DictionaryApi


class MethodUtils(object):

    def __init__(self, dictContainerList, verbose=False, log=sys.stderr):
        #
        self.__verbose = verbose
        self.__lfh = log
        #
        # list of dictionary data & definition containers
        self.__dictContainerList = dictContainerList
        self.__dApi = DictionaryApi(containerList=self.__dictContainerList, consolidate=True, verbose=self.__verbose, log=self.__lfh)
        #
        # Target data container list
        self.__dataContainerList = []
        #

    def setDataContainerList(self, dataContainerList):
        self.__dataContainerList = dataContainerList

    def getDataContainerList(self):
        return self.__dataContainerList

    def getDictionary(self):
        return self.__dApi

    def getMethods(self):
        return self.__dApi.getMethods()

    def getMethod(self, id):
        return self.__dApi.getMethod(id)

    def invokeMethods(self, fh=sys.stdout):
        mI = self.__dApi.getMethodIndex()
        lenD = len(mI)
        i = 0
        for k, mRefL in mI.items():
            for mRef in mRefL:
                i += 1
                id = mRef.getId()
                type = mRef.getType()
                categoryName = mRef.getCategoryName()
                attributeName = mRef.getAttributeName()
                if (self.__verbose):
                    fh.write("\n")
                    fh.write("++++++++++++++++++--------------------\n")
                    fh.write("Invoking dictionary method on file object: %s (%d/%d)\n" % (k, i, lenD))
                    fh.write(" + Method id: %s\n" % id)
                    fh.write(" + Type:      %s\n" % type)
                    fh.write(" + Category:  %s\n" % categoryName)
                    fh.write(" + Attribute: %s\n" % attributeName)
                #
                if type == "datablock":
                    if (self.__verbose):
                        fh.write("Invoke datablock method %s\n" % id)
                    # self.invokeDataBlockMethod(type,self.__dApi.getMethod(id))
                    # continue
                #
                for db in self.__dataContainerList:
                    if type == "category":
                        if not db.exists(categoryName):
                            dc = DataCategory(categoryName)
                            db.append(dc)
                        dObj = db.getObj(categoryName)
                        dObj.invokeCategoryMethod(type, self.__dApi.getMethod(id), db)
                    elif type == "attribute":
                        if not db.exists(categoryName):
                            dc = DataCategory(categoryName)
                            db.append(dc)
                        dObj = db.getObj(categoryName)
                        dObj.invokeAttributeMethod(attributeName, type, self.__dApi.getMethod(id), db)
                    elif type == "datablock":
                        fh.write("Invoke datablock method %s\n" % id)
                        db.invokeDataBlockMethod(type, self.__dApi.getMethod(id), db)
                    else:
                        pass

    def dumpMethods(self, fh=sys.stdout):
        self.__dApi.dumpMethods(fh)

    def dumpDictionary(self, fh=sys.stdout):
        lenD = len(self.__dictContainerList)
        fh.write("\n--------------------------------------------\n")
        fh.write("\n-----------DUMP DICTIONARY------------------\n")
        fh.write("Dictionary object list length is: %d\n" % lenD)
        i = 1
        for dObj in self.__dictContainerList:
            if len(dObj.getName()) > 0:
                fh.write("\n")
                fh.write("++++++++++++++++++--------------------\n")
                fh.write("Dumping dictionary object named: %s (%d/%d)\n" %
                         (dObj.getName(), i, lenD))
                dObj.printIt(fh)
            i += 1
    #

    def dumpDataFile(self, fh=sys.stdout):
        lenD = len(self.__dataContainerList)
        fh.write("\n--------------------------------------------\n")
        fh.write("\n-----------DUMP DATAFILE--------------------\n")
        fh.write("Data object list length is: %d\n" % lenD)
        i = 1
        for dObj in self.__dataContainerList:
            fh.write("\n")
            fh.write("++++++++++++++++++--------------------\n")
            fh.write("Dumping data file object named: %s (%d/%d)\n" %
                     (dObj.getName(), i, lenD))
            dObj.printIt(fh)
            i += 1
