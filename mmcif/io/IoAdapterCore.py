##
# File: IoAdapterCore.py
# Date: 20-Jan-2013  John Westbrook
#
# Updates:
# 20-Jan-2013 jdw Type convert to string or '?'
#  7-May-2014 jdw Make output line length 2048
# 30-Jul-2014 jdw Expose maximum line length as an optional writeFile() parameter.
#  5-Feb-2015 jdw disable maximum line length parameter -
#  6-Dec-2015 jdw add detailed timers
#  6-Dec-2015 jdw add additional filters for category write order -
# 28-Jul-2016 rps readFile(), __readData() methods updated to accept optional "logtag" parameter
# 15-Feb-2017 ep  Correct variable name in exception in __readDataSelect()
#  8-Jan-2018 jdw adapt to new python bindings -  change logging framework -- py2->3
#
##
"""
Adapter between PDBx IO classes and the Pybind11/Python wrappers

"""
from __future__ import absolute_import
from six.moves import range
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"


import sys
import time
import os
from future.utils import raise_from

import logging
logger = logging.getLogger(__name__)

HERE = os.path.abspath(os.path.dirname(__file__))


from mmcif.io.IoAdapterBase import IoAdapterBase

from mmcif.api.PdbxContainers import *
from mmcif.api.DataCategory import DataCategory
from mmcif.io.PdbxExceptions import PdbxError, SyntaxError

try:
    from mmcif.core.mmciflib import ParseCifSimple, CifFile, ParseCifSelective, type, CifFileReadDef
except Exception as e:
    sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
    from build.lib.mmciflib import ParseCifSimple, CifFile, ParseCifSelective, type, CifFileReadDef


class IoAdapterCore(IoAdapterBase):

    """ Adapter between PDBx IO classes (C++ Pybind11 wrappers) and Python persistence classes.
    """

    def __init__(self, *args, **kwargs):
        super(IoAdapterCore, self).__init__(*args, **kwargs)

    def readFile(self, filePath, enforceAscii=True, selectList=None, logFilePath=None, outDirPath=None, cleanUp=True):
        """ Import the input Pdbx data file.
        """
        asciiFilePath = None
        try:
            #
            lPath = logFilePath
            if not lPath:
                lPath = self._getDefaultFileName(filePath, fileType='cif-parser-log', outDirPath=outDirPath)
            #
            self._setLogFilePath(lPath)
            #
            if not self._fileExists(filePath):
                return []
            #
            inputFilePath = filePath
            if enforceAscii:
                asciiFilePath = self._getDefaultFileName(filePath, fileType='cif-parser-ascii', fileExt='cif', outDirPath=outDirPath)
                encodingErrors = 'xmlcharrefreplace' if self._useCharRefs else 'ignore'
                logger.debug("Filtering input file to %s using encoding errors as %s" % (asciiFilePath, encodingErrors))
                ok = self._toAscii(filePath, asciiFilePath, chunkSize=5000, encodingErrors=encodingErrors)
                if ok:
                    inputFilePath = asciiFilePath
            #
            readDef = None
            if selectList and len(selectList) > 0:
                readDef = self.__getSelectionDef(selectList)
            #
            containerL, diagL = self.__readData(inputFilePath, readDef=readDef, cleanUp=cleanUp, logFilePath=lPath, maxLineLength=self._maxInputLineLength)
            #
            self._cleanupFile(asciiFilePath and cleanUp, asciiFilePath)
            #
            return containerL
        except (PdbxError, SyntaxError) as ex:
            self._cleanupFile(asciiFilePath and cleanUp, asciiFilePath)
            if self._raiseExceptions:
                raise_from(ex, None)
                # raise ex from None
        except Exception as e:
            self._cleanupFile(asciiFilePath and cleanUp, asciiFilePath)
            msg = "Failing read for %s with %s" % (filePath, str(e))
            self._logError(msg)

        return []

    def getReadDiags(self):
        return self._readLogRecords()

    def __getSelectionDef(self, selectList):
        try:
            readDef = CifFileReadDef()
            readDef.SetCategoryList(selectList, type.A)
            return readDef
        except Exception as e:
            msg = "Failing read selection with %s" % str(e)
            self._logError(msg)
        return None

    def __processReadLogFile(self, pdbxFilePath):
        diagL = self._readLogRecords()
        #
        if diagL:
            numErrors = 0
            numSyntaxErrors = 0
            numWarnings = 0
            for diag in diagL:
                if 'ERROR' in diag:
                    numErrors += 1
                if 'WARN' in diag:
                    numWarnings += 1
                if 'syntax' in diag.lower():
                    numSyntaxErrors += 1
            #
            logger.debug("%s syntax errors %d  warnings %d all errors %d" % (pdbxFilePath, numSyntaxErrors, numWarnings, numErrors))
            #
            if numSyntaxErrors and self._raiseExceptions:
                raise SyntaxError("%s syntax errors %d  all errors %d" % (pdbxFilePath, numSyntaxErrors, numErrors))
            elif numErrors and self._raiseExceptions:
                raise PdbxError("%s error count is %d" % (pdbxFilePath, numErrors))
            elif numErrors:
                logger.error("%s syntax errors %d  all errors %d" % (pdbxFilePath, numSyntaxErrors, numErrors))
            if numWarnings:
                logger.warn("%s warnings %d" % (pdbxFilePath, numWarnings))

        return diagL

    def __processContent(self, cifFileObj):
        containerList = []
        containerNameList = []
        try:
            # ----- Repackage the data content  ----
            #
            containerList = []
            containerNameList = []
            containerNameList = list(cifFileObj.GetBlockNames(containerNameList))
            for containerName in containerNameList:
                #
                aContainer = DataContainer(containerName)
                #
                block = cifFileObj.GetBlock(containerName)
                tableNameList = []
                tableNameList = list(block.GetTableNames(tableNameList))

                for tableName in tableNameList:
                    table = block.GetTable(tableName)
                    attributeNameList = list(table.GetColumnNames())
                    numRows = table.GetNumRows()
                    rowList = []
                    for iRow in range(0, numRows):
                        row = table.GetRow(iRow)
                        # row = table.GetRow(iRow).decode('unicode_escape').encode('utf-8')
                        # row = [p.encode('ascii', 'xmlcharrefreplace') for p in table.GetRow(iRow)]
                        rowList.append(list(row))
                    aCategory = DataCategory(tableName, attributeNameList, rowList, copyInputData=False)
                    aContainer.append(aCategory)
                containerList.append(aContainer)
        except Exception as e:
            msg = "Failing packaging with %s" % str(e)
            self._logError(msg)

        return containerList

    def __readData(self, pdbxFilePath, readDef=None, maxLineLength=1024, logFilePath=None, cleanUp=False):
        """ Internal method to read input file and return data as a list of DataContainer objects.
            readDef optionally contains a selection of data categories to be returned.    Diagnostics
            will be written to logFilePath (persisted if cleanuUp=False).

        """
        #
        startTime = time.clock()
        containerList = []
        diagL = []
        try:
            if readDef:
                cifFileObj = ParseCifSelective(
                    pdbxFilePath,
                    readDef,
                    verbose=self._verbose,
                    intCaseSense=0,
                    maxLineLength=maxLineLength,
                    nullValue="?",
                    parseLogFileName=logFilePath)
            else:
                cifFileObj = ParseCifSimple(pdbxFilePath, verbose=self._verbose, intCaseSense=0, maxLineLength=maxLineLength, nullValue="?", parseLogFileName=logFilePath)
            #
            # ---  Process/Handle read errors   ----
            #
            diagL = self.__processReadLogFile(pdbxFilePath)
            logger.debug("Diagnostic count %d values %r" % (len(diagL), diagL))
            #
            if self._timing:
                stepTime1 = time.clock()
                logger.info("Timing parsed %r in %.4f seconds" % (pdbxFilePath, stepTime1 - startTime))
            #
            containerList = self.__processContent(cifFileObj)
            #
            self._cleanupFile(cleanUp, logFilePath)
            if self._timing:
                stepTime2 = time.clock()
                logger.info("Timing api load in %.4f seconds read time %.4f seconds\n" %
                            (stepTime2 - stepTime1, stepTime2 - startTime))
            #
            return containerList, diagL
        except (PdbxError, SyntaxError) as ex:
            self._cleanupFile(cleanUp, logFilePath)
            if self._raiseExceptions:
                raise_from(ex, None)
        except Exception as e:
            self._cleanupFile(cleanUp, logFilePath)
            msg = "Failing read for %s with %s" % (pdbxFilePath, str(e))
            self._logError(msg)

        return containerList, diagL

    def writeFile(self, pdbxFilePath, containerList=[], maxLineLength=900, enforceAscii=True,
                  lastInOrder=['pdbx_nonpoly_scheme', 'pdbx_poly_seq_scheme', 'atom_site', 'atom_site_anisotrop'], selectOrder=None, **kwargs):
        """ Export the input containerlist to PDBx format file in the path 'pdbxFilePath'.
        """
        try:
            if len(kwargs):
                logger.warn("Unsupported keyword arguments %s" % kwargs.keys())
            startTime = time.clock()
            logger.debug("write container length %d\n" % len(containerList))
            # cF = CifFile()
            # (verbose: bool, caseSense: Char::eCompareType, maxLineLength: int, nullValue: str)
            cF = CifFile(True, self._verbose, 0, maxLineLength, '?')
            for container in containerList:
                containerName = container.getName()
                logger.debug("writing container %s\n" % containerName)
                cF.AddBlock(containerName)
                block = cF.GetBlock(containerName)
                #
                # objNameList = container.getObjNameList()
                # logger.debug("write category length %d\n" % len(objNameList))
                #
                # Reorder/Filter - container object list-
                objNameList = container.filterObjectNameList(lastInOrder=lastInOrder, selectOrder=selectOrder)
                logger.debug("write category names  %r\n" % objNameList)
                #
                for objName in objNameList:
                    name, attributeNameList, rowList = container.getObj(objName).get()
                    table = block.AddTable(name)
                    for attributeName in attributeNameList:
                        table.AddColumn(attributeName)
                    try:
                        rLen = len(attributeNameList)
                        for ii, row in enumerate(rowList):
                            table.AddRow()
                            table.FillRow(ii, [str(row[jj]) if row[jj] is not None else '?' for jj in range(0, rLen)])
                    except Exception as e:
                        logger.error("Exception for %s preparing data for writing %s" % (pdbxFilePath, str(e)))
                    #
                    block.WriteTable(table)
            #
            if self._timing:
                stepTime1 = time.clock()
                logger.info("Timing %d container(s) api loaded in %.4f seconds" % (len(containerList), stepTime1 - startTime))
            if (self._debug):
                self.__dumpBlocks(cF)
            cF.Write(str(pdbxFilePath))
            if self._timing:
                stepTime2 = time.clock()
                logger.info("Timing %d container(s) written in %.4f seconds total time %.4f" %
                            (len(containerList), stepTime2 - stepTime1, stepTime2 - startTime))
            return True

        except Exception as e:
            msg = "Write failing for file %s with %s" % (pdbxFilePath, str(e))
            self._logError(msg)
        return False

    def __dumpBlocks(self, cf):
        try:
            logger.info("cif file %r" % cf)
            blockNameList = []
            blockNameList = cf.GetBlockNames(blockNameList)
            #
            logger.info(" block name list %r" % repr(blockNameList))
            for blockName in blockNameList:
                #
                block = cf.GetBlock(blockName)
                tableNameList = []
                tableNameList = list(block.GetTableNames(tableNameList))
                logger.info("tables name list %r" % repr(tableNameList))
                for tableName in tableNameList:
                    logger.info("table name %r" % tableName)
                    ok = block.IsTablePresent(tableName)
                    logger.info("table present %r" % ok)
                    table = block.GetTable(tableName)

                    attributeNameList = list(table.GetColumnNames())
                    logger.info("Attribute name list %r" % repr(attributeNameList))
                    numRows = table.GetNumRows()
                    logger.info("row length %r" % numRows)
                    for iRow in range(0, numRows):
                        row = table.GetRow(iRow)
                        logger.info("Attribute name list %r" % row)
        except Exception as e:
            logger.exception("dump failing with %s\n" % str(e))


if __name__ == '__main__':
    pass
