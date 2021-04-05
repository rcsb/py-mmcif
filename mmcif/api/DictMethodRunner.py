##
# File:    DictMethodRunner.py
# Author:  J. Westbrook
# Date:    18-Aug-2018
# Version: 0.001 Initial version
#
# Updates:
# 12-Nov-2018 jdw Run block methods after category and attribute methods.
#  5-Jun-2019 jdw Refactor and generalize and remove dependencies on rcsb.db package
# 17-Jul-2019 jdw Propagate kwargs to __getModuleInstance()
#
##
"""
Manage the invocation of dictionary methods implemented in helper classes.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import sys
from operator import itemgetter

# from mmcif.api.DictionaryApi import DictionaryApi

logger = logging.getLogger(__name__)


class DictMethodRunner(object):
    """Manage the invocation of dictionary methods implemented as class methods."""

    def __init__(self, dictionaryApi, modulePathMap=None, **kwargs):
        """Manage invocation of dictionary methods referenced in external modules.

        Arguments:
            dictionaryApi {object} -- instance of DictionaryApi() for dictionary with target method definitions

        Keyword Arguments:
            modulePathMap {dict str} -- mapping between dictionary module path and execution path (default: {None})
            cacheModuleFlag {bool} -- flag to cache module instances (defaullt: True)
            implentationSource {str} -- method implementation (default: 'reference')
            methodCodes (list str) -- filter methods by codes {default: ['calculation']}
        """
        self.__dApi = dictionaryApi
        self.__modulePathMap = modulePathMap if modulePathMap else {}
        self.__cacheModuleFlag = kwargs.get("cacheModuleFlag", True)
        methodCodes = kwargs.get("methodCodes", ["calculation"])
        implementationSource = kwargs.get("implementationCodes", "reference")
        #
        self.__kwargs = kwargs
        #
        # Preserve and reuse the module instances if caching is enabled
        self.__moduleCache = {}
        #
        self.__methodD = self.__getMethodInfo(implementationSource=implementationSource, methodCodes=methodCodes)
        logger.debug("Method index %r", self.__methodD.items())

    def __getMethodInfo(self, implementationSource="reference", methodCodes=None):
        """Get method implementation with the input implementation source."""
        catName = atName = mId = mType = methDef = None
        methodCodes = methodCodes if methodCodes else ["calculation"]
        methodD = {}
        try:
            methodIndex = self.__dApi.getMethodIndex()
            for _, mrL in methodIndex.items():
                for mr in mrL:
                    mId = mr.getId()
                    catName = mr.getCategoryName()
                    atName = mr.getAttributeName()
                    mType = mr.getType()
                    if (catName, atName) not in methodD:
                        methodD[(catName, atName)] = []
                    methDef = self.__dApi.getMethod(mId)
                    logger.debug("Category %s attribute %s mId %r type %r methDef %r", catName, atName, mId, mType, methDef)
                    mSource = methDef.getImplementationSource()
                    mCode = methDef.getCode()
                    if mSource == implementationSource and mCode in methodCodes:
                        mPriority = methDef.getPriority()
                        mLang = methDef.getLanguage()
                        mImplement = methDef.getImplementation()
                        dD = {"METHOD_LANGUAGE": mLang, "METHOD_IMPLEMENT": mImplement, "METHOD_TYPE": mType, "METHOD_CODE": mCode, "METHOD_PRIORITY": mPriority}
                        methodD[(catName, atName)].append(dD)
                #
        except Exception as e:
            logger.exception("Failing for category %r attribute %r mId %r type %r methDef %r with %s", catName, atName, mId, mType, methDef, str(e))

        ##
        logger.debug("Method dictionary %r", methodD)
        return methodD

    def __invokeAttributeMethod(self, methodPath, dataContainer, catName, atName, **kwargs):
        """Invoke the input attribute method"""
        ok = False
        try:
            modulePath, methodName = self.__methodPathSplit(methodPath)
            mObj = self.__getModuleInstance(modulePath, **kwargs)
            theMeth = getattr(mObj, methodName, None)
            ok = theMeth(dataContainer, catName, atName, **kwargs)
        except Exception as e:
            logger.exception("Failed invoking attribute %s %s method %r with %s", catName, atName, methodPath, str(e))
        return ok

    def __invokeCategoryMethod(self, methodPath, dataContainer, catName, **kwargs):
        """Invoke the input category method"""
        ok = False
        try:
            modulePath, methodName = self.__methodPathSplit(methodPath)
            mObj = self.__getModuleInstance(modulePath, **kwargs)
            theMeth = getattr(mObj, methodName, None)
            ok = theMeth(dataContainer, catName, **kwargs)
        except Exception as e:
            logger.exception("Failed invoking category %s method %r with %s", catName, methodPath, str(e))
        return ok

    def __invokeDatablockMethod(self, methodPath, dataContainer, blockName, **kwargs):
        """Invoke the input data block method"""
        ok = False
        try:
            modulePath, methodName = self.__methodPathSplit(methodPath)
            mObj = self.__getModuleInstance(modulePath, **kwargs)
            theMeth = getattr(mObj, methodName, None)
            ok = theMeth(dataContainer, blockName, **kwargs)
        except Exception as e:
            logger.exception("Failed invoking block %s method %r with %s", blockName, methodPath, str(e))
        return ok

    def apply(self, dataContainer):
        """Apply category, attribute and block level dictionary methods on the input data container."""
        kwargs = self.__kwargs
        mTupL = self.__getCategoryMethods()
        logger.debug("Category methods %r", mTupL)
        for catName, _, methodPath, _ in mTupL:
            self.__invokeCategoryMethod(methodPath, dataContainer, catName, **kwargs)

        mTupL = self.__getAttributeMethods()
        logger.debug("Attribute methods %r", mTupL)
        for catName, atName, methodPath, _ in mTupL:
            self.__invokeAttributeMethod(methodPath, dataContainer, catName, atName, **kwargs)

        mTupL = self.__getDatablockMethods()
        logger.debug("Datablock methods %r", mTupL)
        for _, _, methodPath, _ in mTupL:
            self.__invokeDatablockMethod(methodPath, dataContainer, dataContainer.getName(), **kwargs)

        return True

    def __getDatablockMethods(self):
        mL = []
        try:
            for (dictName, _), mDL in self.__methodD.items():
                for mD in mDL:
                    if mD["METHOD_TYPE"].lower() == "datablock":
                        methodPath = mD["METHOD_IMPLEMENT"]
                        mL.append((dictName, None, methodPath, mD["METHOD_PRIORITY"]))
            mL = sorted(mL, key=itemgetter(3))
            return mL
        except Exception as e:
            logger.exception("Failing dictName %s with %s", dictName, str(e))
        return mL

    def __getCategoryMethods(self):
        mL = []
        try:
            for (catName, _), mDL in self.__methodD.items():
                for mD in mDL:
                    if mD["METHOD_TYPE"].lower() == "category":
                        methodPath = mD["METHOD_IMPLEMENT"]
                        mL.append((catName, None, methodPath, mD["METHOD_PRIORITY"]))
            mL = sorted(mL, key=itemgetter(3))
            return mL
        except Exception as e:
            logger.exception("Failing catName %r with %s", catName, str(e))
        return mL

    def __getAttributeMethods(self):
        mL = []
        try:
            for (catName, atName), mDL in self.__methodD.items():
                for mD in mDL:
                    if mD["METHOD_TYPE"].lower() == "attribute":
                        methodPath = mD["METHOD_IMPLEMENT"]
                        mL.append((catName, atName, methodPath, mD["METHOD_PRIORITY"]))
            mL = sorted(mL, key=itemgetter(3))
            return mL
        except Exception as e:
            logger.exception("Failing catName %s atName %s with %s", catName, atName, str(e))
        return mL

    def __methodPathSplit(self, methodPath):
        """Extract module path and the method name from the input path.  Optional
           remap the module path.

        Arguments:
            methodPath {str} -- implementation path from dictionary method definition

        Returns:
            {tuple str} -- module path, method name
        """
        try:
            # Strip off any leading path of the module from the method path.
            mpL = str(methodPath).split(".")
            methodName = mpL[-1]
            tp = ".".join(mpL[:-1])
            modulePath = self.__modulePathMap[tp] if tp in self.__modulePathMap else tp
            return modulePath, methodName
        except Exception as e:
            logger.error("Failing for method path %r with %s", methodPath, str(e))
        return None, None

    def __getModuleInstance(self, modulePath, **kwargs):
        #
        if self.__cacheModuleFlag and modulePath in self.__moduleCache:
            return self.__moduleCache[modulePath]
        #
        mObj = None
        try:
            aMod = __import__(modulePath, globals(), locals(), [""])
            sys.modules[modulePath] = aMod
            #
            # Strip off any leading path to the module before we instaniate the module object.
            mpL = str(modulePath).split(".")
            moduleName = mpL[-1]
            #
            mObj = getattr(aMod, moduleName)(**kwargs)
            self.__moduleCache[modulePath] = mObj

        except Exception as e:
            logger.error("Failing to instance helper %r with %s", modulePath, str(e))
        return mObj
