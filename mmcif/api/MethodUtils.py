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

__docformat__ = "restructuredtext en"
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
                #
                logger.debug("\n")
                logger.debug("++++++++++++++++++--------------------\n")
                logger.debug("Invoking dictionary method on file object: %s (%d/%d)\n" % (k, i, lenD))
                logger.debug(" + Method id: %s\n" % id)
                logger.debug(" + Type:      %s\n" % type)
                logger.debug(" + Category:  %s\n" % categoryName)
                logger.debug(" + Attribute: %s\n" % attributeName)
                #
                if type == "datablock":
                    logger.debug("Invoke datablock method %s\n" % id)
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
                        # logger.debug("invoke -  %r %r %r %r" % (attributeName, type, self.__dApi.getMethod(id), db))
                        dObj.invokeAttributeMethod(attributeName, type, self.__dApi.getMethod(id), db)
                    elif type == "datablock":
                        logger.debug("Invoke datablock method %s\n" % id)
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
