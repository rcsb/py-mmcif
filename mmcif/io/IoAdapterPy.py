##
# File:    IoAdapterPy.py
# Author:  J. Westbrook
# Date:    16-Jan-2013
# Version: 0.001 Initial version
#
# Updates:
# 30-Jul-2014 jdw Expose column aligmment and  maximum line length as optional writeFile() parameters.
# 22-Jun-2015 jdw add additional formatting control on write method.
# 15-Aug-2016 rps readFile() updated to accept optional "logtag" parameter for consistency with IoAdapterCore API
# 01-Aug-2017 jdw migrate portions to public repo
# 12-Jan-2018 jdw start to unify api features -
##
"""
Python implementation of IoAdapterBase class providing read and write
        methods for PDBx/mmCIF data files -

"""
from __future__ import absolute_import


__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"

import io
import sys
from future.utils import raise_from

import logging
logger = logging.getLogger(__name__)

from mmcif.io.IoAdapterBase import IoAdapterBase
from mmcif.io.PdbxReader import PdbxReader
from mmcif.io.PdbxWriter import PdbxWriter
from mmcif.io.PdbxExceptions import PdbxError, SyntaxError


class IoAdapterPy(IoAdapterBase):
    """ Python implementation of IoAdapterBase class providing read and write
        methods for PDBx/mmCIF data files -

    """

    def __init__(self, *args, **kwargs):
        super(IoAdapterPy, self).__init__(*args, **kwargs)

    def readFile(self, inputFilePath, enforceAscii=False, selectList=None, excludeFlag=False, logFilePath=None, outDirPath=None, cleanUp=False, **kwargs):
        """  Read PDBx/mmCIF file and return list of data or definition containers.

        """
        if len(kwargs):
                logger.warn("Unsupported keyword arguments %s" % kwargs.keys())
        filePath = str(inputFilePath)
        containerList = []
        if enforceAscii:
            encoding = 'ascii'
        else:
            encoding = 'utf-8'
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

            if sys.version_info[0] > 2:
                with open(filePath, 'r', encoding=encoding) as ifh:
                    pRd = PdbxReader(ifh)
                    pRd.read(containerList, selectList, excludeFlag=excludeFlag)
            else:
                if enforceAscii:
                    with io.open(filePath, 'r', encoding=encoding) as ifh:
                        pRd = PdbxReader(ifh)
                        pRd.read(containerList, selectList, excludeFlag=excludeFlag)
                else:
                    with open(filePath, 'r') as ifh:
                        pRd = PdbxReader(ifh)
                        pRd.read(containerList, selectList, excludeFlag=excludeFlag)

            self._cleanupFile(lPath and cleanUp, lPath)

        except (PdbxError, SyntaxError) as ex:
            msg = "File %r with %s" % (filePath, str(ex))
            self._appendToLog([msg])
            self._cleanupFile(lPath and cleanUp, lPath)
            if self._raiseExceptions:
                raise_from(ex, None)
                # raise ex from None
        except Exception as e:
            msg = "File %r with %s" % (filePath, str(e))
            self._appendToLog([msg])
            self._cleanupFile(lPath and cleanUp, lPath)
            if self._raiseExceptions:
                raise e
            else:
                logger.error("Failing read for %s with %s" % (filePath, str(e)))
        return containerList

    def getReadDiags(self):
        """ Return diagnostics from last readFile operation. This will NOT be an exhustive list but
        rather the particular failure that raised a parsing exception.
        """
        return self._readLogRecords()

    def writeFile(self, outputFilePath, containerList, maxLineLength=900, enforceAscii=True,
                  lastInOrder=['pdbx_nonpoly_scheme', 'pdbx_poly_seq_scheme', 'atom_site', 'atom_site_anisotrop'], selectOrder=None,
                  columnAlignFlag=True, useStopTokens=False, formattingStep=None, **kwargs):
        """ Write input list of data or definition containers to the specified output file path.
        """
        if len(kwargs):
                logger.warn("Unsupported keyword arguments %s" % kwargs.keys())
        try:
            if enforceAscii:
                encoding = 'ascii'
            else:
                encoding = 'utf-8'
            #
            if sys.version_info[0] > 2:
                with open(outputFilePath, "w", encoding=encoding) as ofh:
                    self.__writeFile(ofh, containerList, maxLineLength=maxLineLength, columnAlignFlag=columnAlignFlag,
                                     lastInOrder=lastInOrder, selectOrder=selectOrder, useStopTokens=useStopTokens,
                                     formattingStep=formattingStep, enforceAscii=enforceAscii, cnvCharRefs=self._useCharRefs)
            else:
                if enforceAscii:
                    with io.open(outputFilePath, 'w', encoding=encoding) as ofh:
                        self.__writeFile(ofh, containerList, maxLineLength=maxLineLength, columnAlignFlag=columnAlignFlag,
                                         lastInOrder=lastInOrder, selectOrder=selectOrder, useStopTokens=useStopTokens,
                                         formattingStep=formattingStep, enforceAscii=enforceAscii, cnvCharRefs=self._useCharRefs)
                else:
                    with open(outputFilePath, "wb") as ofh:
                        self.__writeFile(ofh, containerList, maxLineLength=maxLineLength, columnAlignFlag=columnAlignFlag,
                                         lastInOrder=lastInOrder, selectOrder=selectOrder, useStopTokens=useStopTokens,
                                         formattingStep=formattingStep, enforceAscii=enforceAscii, cnvCharRefs=self._useCharRefs)
            return True
        except Exception as ex:
            if self._raiseExceptions:
                raise_from(ex, None)
            else:
                logger.error("Failing write for %s with %s" % (outputFilePath, str(ex)))

        return False

    def __writeFile(self, ofh, containerList, maxLineLength=900, columnAlignFlag=True,
                    lastInOrder=None, selectOrder=None, useStopTokens=False,
                    formattingStep=None, enforceAscii=False, cnvCharRefs=False):

        #
        pdbxW = PdbxWriter(ofh)
        pdbxW.setUseStopTokens(flag=useStopTokens)
        pdbxW.setMaxLineLength(numChars=maxLineLength)
        pdbxW.setAlignmentFlag(flag=columnAlignFlag)
        pdbxW.setRowPartition(numParts=formattingStep)
        pdbxW.setConvertCharRefs(flag=cnvCharRefs)
        pdbxW.setSetEnforceAscii(enforceAscii)
        pdbxW.write(containerList, lastInOrder=lastInOrder, selectOrder=selectOrder)
