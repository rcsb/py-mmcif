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

import copy
import io

import logging
logger = logging.getLogger(__name__)

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    from mmcif.core.mmciflib import ParseCifSimple, CifFile, ParseCifSelective, type, CifFileReadDef
except Exception as e:
    sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
    from build.lib.mmciflib import ParseCifSimple, CifFile, ParseCifSelective, type, CifFileReadDef

from mmcif.io.IoAdapterBase import IoAdapterBase

from mmcif.api.PdbxContainers import *
from mmcif.api.DataCategory import DataCategory


class IoAdapterCore(IoAdapterBase):

    """ Adapter between PDBx IO classes (C++ Pybind11 wrappers) and Python persistence classes.
    """

    def __init__(self, *args, **kwargs):
        super(IoAdapterCore, self).__init__(*args, **kwargs)

        self.__verbose = True
        self.__debug = True
        self.__timing = False
        self.__lfh = sys.stderr
        #
        #
        self.__lastInOrder = ['pdbx_nonpoly_scheme', 'pdbx_poly_seq_scheme', 'atom_site', 'atom_site_anisotrop']
        #

    def readFile(self, pdbxFilePath, selectList=None, logFilePath=None, logtag="", enforceAscii=True):
        """ Import the input Pdbx data file.
        """
        try:
            if (not os.access(pdbxFilePath, os.R_OK)):
                if (self.__verbose):
                    logger.info("+ERROR- IoAdapterCore.read() Missing file %s\n" % pdbxFilePath)
                return []
            else:
                if (self.__debug):
                    logger.info("+IoAdapterCore.read() reading from file path %s\n" % pdbxFilePath)

            if selectList is not None and len(selectList) > 0:
                return self.__readDataSelect(pdbxFilePath, selectList, logFilePath=logFilePath)
            else:
                return self.__readData(pdbxFilePath, logtag=logtag)

        except Exception as e:
            if (self.__verbose):
                logger.exception("+ERROR- IoAdapterCore.read() Could not read file %s with %s\n" % (pdbxFilePath, str(e)))

            return []

    def __readDataSelect(self, pdbxFilePath, selectList, maxLineLength=1024, logFilePath=None):
        """ Read the selected  data/definition containers in the input PDBxfile.

        """
        #
        # Set read filters  -
        #
        startTime = time.clock()
        containerList = []
        try:
            readDef = CifFileReadDef()
            readDef.SetCategoryList(selectList, type.A)
        except:
            if (self.__verbose):
                logger.exception("+ERROR - IoAdapterCore.__readDataSelect() selection failed for %s select list %r\n" % (pdbxFilePath, selectList))
        #
        try:
            sFilePath = str(pdbxFilePath)
            if (not os.access(sFilePath, os.R_OK)):
                logger.info("+ERROR- IoAdapterCore.__readDataSelect() Missing file %r\n" % sFilePath)
                return containerList
            #
            #
            if logFilePath is None:
                sf = '-' + str(int(time.time() * 10000)) + '-cif-parser.log'
                logFilePath = sFilePath + sf
            # myReader = ParseCifSelective(sFilePath, readDef, parseLogFileName=logFilePath)
            myReader = ParseCifSelective(sFilePath, readDef, False, 0, maxLineLength, "?", logFilePath)
            containerNameList = []
            containerNameList = list(myReader.GetBlockNames(containerNameList))
            if self.__timing:
                stepTime1 = time.clock()
                logger.info("+IoAdapterCore.__readDataSelect() containerNameList %r read in %.4f seconds\n" % (repr(containerNameList), stepTime1 - startTime))
            #
            for containerName in containerNameList:
                #
                aContainer = DataContainer(containerName)
                #
                block = myReader.GetBlock(containerName)
                tableNameList = list(block.GetTableNames())

                for tableName in tableNameList:
                    table = block.GetTable(tableName)
                    attributeNameList = list(table.GetColumnNames())
                    if self.__debug:
                        logger.info("+IoAdapterCore.__readDataSelect() Attribute name list %r\n" % repr(attributeNameList))
                    numRows = table.GetNumRows()
                    rowList = []
                    for iRow in range(0, numRows):
                        row = table.GetRow(iRow)
                        rowList.append(list(row))
                    aCategory = DataCategory(tableName, attributeNameList, rowList)
                    aContainer.append(aCategory)
                    #
                    if self.__debug:
                        logger.info("+IoAdapterCore.__readDataSelect() read %s length %d %d\n" % (tableName, numRows, len(rowList)))
                containerList.append(aContainer)
            #
            if self.__timing:
                stepTime2 = time.clock()
                logger.info("Api load in %.4f seconds read time %.4f seconds\n" %
                            (stepTime2 - stepTime1, stepTime2 - startTime))
            return containerList
        except Exception as e:
            if (self.__verbose):
                logger.exception("Failing for %s with %s\n" % (pdbxFilePath, str(e)))
            return containerList

    def __readData(self, pdbxFilePath, maxLineLength=1024, logFilePath=None, logtag=""):
        """ Read all data/definition containers in the input PDBxfile.
        """
        # read file contents -
        #
        startTime = time.clock()
        containerList = []
        containerNameList = []
        try:
            sFilePath = str(pdbxFilePath)
            if (not os.access(sFilePath, os.R_OK)):
                logger.info("Missing input file %r" % sFilePath)
                return containerList
            #
            #
            if logFilePath is None:
                if(len(logtag) > 0):
                    logtag = '-' + logtag
                sf = '-' + str(int(time.time() * 10000)) + logtag + '-cif-parser.log'
                logFilePath = sFilePath + sf
            myReader = ParseCifSimple(sFilePath, verbose=self.__verbose, intCaseSense=0, maxLineLength=maxLineLength, nullValue="?", parseLogFileName=logFilePath)
            tt = []
            tt = myReader.GetBlockNames(tt)
            # print (dir(tt))
            containerNameList = list(myReader.GetBlockNames(containerNameList))
            if self.__timing:
                stepTime1 = time.clock()
                logger.info("%r containers read in %.4f seconds" % (len(containerNameList), stepTime1 - startTime))
            #
            for containerName in containerNameList:
                #
                aContainer = DataContainer(containerName)
                #
                block = myReader.GetBlock(containerName)
                tableNameList = []
                tableNameList = list(block.GetTableNames(tableNameList))

                for tableName in tableNameList:
                    table = block.GetTable(tableName)
                    attributeNameList = list(table.GetColumnNames())
                    numRows = table.GetNumRows()
                    rowList = []
                    for iRow in range(0, numRows):
                        row = table.GetRow(iRow)
                        rowList.append(list(row))
                    aCategory = DataCategory(tableName, attributeNameList, rowList)
                    aContainer.append(aCategory)
                containerList.append(aContainer)
            #
            if self.__timing:
                stepTime2 = time.clock()
                logger.info("Api load in %.4f seconds read time %.4f seconds\n" %
                            (stepTime2 - stepTime1, stepTime2 - startTime))
            return containerList
        except Exception as e:
            if (self.__verbose):
                logger.exception("Failing for %s with %s\n" % (pdbxFilePath, str(e)))
            return containerList

    def writeFile(self, pdbxFilePath, containerList=[], maxLineLength=900,
                  lastInWriteOrder=['pdbx_nonpoly_scheme', 'pdbx_poly_seq_scheme', 'atom_site', 'atom_site_anisotrop']):
        """ Export the input containerlist to PDBx format file in the path 'pdbxFilePath'.
        """
        try:
            startTime = time.clock()
            if self.__debug:
                logger.info("+IoAdapterCore.write() container length %d\n" % len(containerList))
            cF = CifFile()
            # cF=CifFile(maxLineLength=maxLineLength)
            for container in containerList:
                containerName = container.getName()
                if self.__debug:
                    logger.info("+IoAdapterCore.write() write container %s\n" % containerName)
                cF.AddBlock(containerName)
                block = cF.GetBlock(containerName)
                objNameList = container.getObjNameList()
                if self.__debug:
                    logger.info("+IoAdapterCore.write() category length %d\n" % len(objNameList))
                #
                # Reorder - output -
                if lastInWriteOrder is not None and len(lastInWriteOrder) > 0:
                    catNameList = []
                    lastList = []
                    for oN in objNameList:
                        if oN in lastInWriteOrder:
                            lastList.append(oN)
                            continue
                        catNameList.append(oN)
                    catNameList.extend(lastList)
                else:
                    catNameList = objNameList

                logger.info("category names  %r\n" % catNameList)
                #
                for objName in catNameList:
                    name, attributeNameList, rowList = container.getObj(objName).get()
                    logger.info("Adding table %s\n" % name)
                    table = block.AddTable(name)
                    for attributeName in attributeNameList:
                        logger.info("Adding column %s\n" % attributeName)
                        table.AddColumn(attributeName)
                    try:
                        rLen = len(attributeNameList)
                        for ii, row in enumerate(rowList):
                            logger.info("Adding row %d vals: %r\n" % (ii, row))
                            table.AddRow()
                            table.FillRow(ii, [str(row[jj]) if row[jj] is not None else '?' for jj in range(0, rLen)])
                    except Exception as e:
                        if (self.__verbose):
                            logger.info("Exception writing data structure %s" % str(e))
                            logger.info(" write failed for file %s" % pdbxFilePath)
                            logger.info(" table name %s len attributeNameList %d" % (objName, len(attributeNameList)))
                            logger.info(" len row index %d row no. %d" % (len(row), ii))
                            for ii, r in enumerate(row):
                                logger.info("col index %d  attr %r value %r" % (ii, attributeNameList[ii], r))
                            for ii, r in enumerate(attributeNameList):
                                logger.info("col index %d  attr %r" % (ii, r))
                    #
                    logger.info(" before writeTable : %r" % table)
                    block.WriteTable(table)
                    logger.info("after writeTable ")
            if self.__timing:
                stepTime1 = time.clock()
                logger.info(" %d container(s) api loaded in %.4f seconds\n" % (len(containerList), stepTime1 - startTime))
            logger.info(" before  dumpBlocks  %s" % pdbxFilePath)
            if (self.__debug):
                self.__dumpBlocks(cF)
            cF.Write(str(pdbxFilePath))
            if self.__timing:
                stepTime2 = time.clock()
                logger.info("%d container(s) written in %.4f seconds total time %.4f\n" %
                            (len(containerList), stepTime2 - stepTime1, stepTime2 - startTime))
            return True

        except Exception as e:
            if (self.__verbose):
                logger.info("Write failing for file %s with %s" % (pdbxFilePath, str(e)))
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
