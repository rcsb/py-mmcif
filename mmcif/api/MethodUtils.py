##
# File:      MethodUtils.py
# Orignal:   Aug 12, 2013   Jdw
#
# Updates:
#   01-Aug-2017   jdw migrate portions to public repo
##
"""
Utility classes for applying inline dictionary methods on PDBx/mmCIF data files.
"""
from __future__ import absolute_import

import logging
import sys

# from mmcif.api.PdbxContainers import *
from mmcif.api.DataCategory import DataCategory
from mmcif.api.DictionaryApi import DictionaryApi

__docformat__ = "google en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


logger = logging.getLogger(__name__)


class MethodUtils(object):
    def __init__(self, dictContainerList, verbose=False):
        #
        self.__verbose = verbose
        # list of dictionary data & definition containers
        self.__dictContainerList = dictContainerList
        self.__dApi = DictionaryApi(containerList=self.__dictContainerList, consolidate=True, verbose=self.__verbose)
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
        return self.__dApi.getMethodIndex()

    def getMethod(self, mId):
        return self.__dApi.getMethod(mId)

    def invokeMethods(self, fh=sys.stdout):
        _ = fh
        mI = self.__dApi.getMethodIndex()
        lenD = len(mI)
        i = 0
        for k, mRefL in mI.items():
            for mRef in mRefL:
                i += 1
                mId = mRef.getId()
                mType = mRef.getType()
                categoryName = mRef.getCategoryName()
                attributeName = mRef.getAttributeName()
                #
                logger.debug("\n")
                logger.debug("++++++++++++++++++--------------------\n")
                logger.debug("Invoking dictionary method on file object: %s (%d/%d)", k, i, lenD)
                logger.debug(" + Method id: %s", mId)
                logger.debug(" + Type:      %s", mType)
                logger.debug(" + Category:  %s", categoryName)
                logger.debug(" + Attribute: %s", attributeName)
                #
                if mType == "datablock":
                    logger.debug("Invoke datablock method %s", mId)
                    # self.invokeDataBlockMethod(type,self.__dApi.getMethod(id))
                    # continue
                #
                for db in self.__dataContainerList:
                    if mType == "category":
                        if not db.exists(categoryName):
                            dc = DataCategory(categoryName)
                            db.append(dc)
                        dObj = db.getObj(categoryName)
                        dObj.invokeCategoryMethod(mType, self.__dApi.getMethod(mId), db)
                    elif mType == "attribute":
                        if not db.exists(categoryName):
                            dc = DataCategory(categoryName)
                            db.append(dc)
                        dObj = db.getObj(categoryName)
                        # logger.debug("invoke -  %r %r %r %r" % (attributeName, type, self.__dApi.getMethod(id), db))
                        dObj.invokeAttributeMethod(attributeName, mType, self.__dApi.getMethod(mId), db)
                    elif mType == "datablock":
                        logger.debug("Invoke datablock method %s", mId)
                        db.invokeDataBlockMethod(mType, self.__dApi.getMethod(mId), db)
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
            if dObj.getName():
                fh.write("\n")
                fh.write("++++++++++++++++++--------------------\n")
                fh.write("Dumping dictionary object named: %s (%d/%d)\n" % (dObj.getName(), i, lenD))
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
            fh.write("Dumping data file object named: %s (%d/%d)\n" % (dObj.getName(), i, lenD))
            dObj.printIt(fh)
            i += 1
