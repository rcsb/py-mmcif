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
import logging
logger = logging.getLogger(__name__)

from mmcif.io.IoAdapterBase import IoAdapterBase
from mmcif.io.PdbxReader import PdbxReader
from mmcif.io.PdbxWriter import PdbxWriter

class IoAdapterPy(IoAdapterBase):
    """ Python implementation of IoAdapterBase class providing read and write
        methods for PDBx/mmCIF data files -

    """

    def __init__(self, *args, **kwargs):
        super(IoAdapterPy, self).__init__(*args, **kwargs)

    def readFile(self, inputFile, enforceAscii=False):
        """  Read PDBx/mmCIF file and return list of data or definition containers.

             The Py2 Py3 behavior -

        """
        containerList = []
        if enforceAscii:
            encoding = 'ascii'
        else:
            encoding = 'utf-8'
        try:
            if sys.version_info[0] > 2:
                with open(inputFile, 'r', encoding=encoding) as ifh:
                    pRd = PdbxReader(ifh)
                    pRd.read(containerList)
            else:
                if enforceAscii:
                    with io.open(inputFile, 'r', encoding=encoding) as ifh:
                        pRd = PdbxReader(ifh)
                        pRd.read(containerList)
                else:
                    with open(inputFile, 'r') as ifh:
                        pRd = PdbxReader(ifh)
                        pRd.read(containerList)
        except Exception as e:
            if self._raiseExceptions:
                raise e
            else:
                logger.error("Failing read for %s with %s" % (inputFile, str(e)))
        return containerList

    def writeFile(self, outputFile, containerList, maxLineLength=900, columnAlignFlag=True, useStopTokens=False, formattingStep=None, enforceAscii=True, cnvCharRefs=False):
        """ Write input list of data or definition containers to the specified output file path.
        """
        try:
            if enforceAscii:
                encoding = 'ascii'
            else:
                encoding = 'utf-8'
            #
            if sys.version_info[0] > 2:
                with open(outputFile, "w", encoding=encoding) as ofh:
                    self.__writeFile(ofh, containerList, maxLineLength=maxLineLength, columnAlignFlag=columnAlignFlag, useStopTokens=useStopTokens,
                                     formattingStep=formattingStep, enforceAscii=enforceAscii, cnvCharRefs=cnvCharRefs)
            else:
                if enforceAscii:
                    with io.open(outputFile, 'w', encoding=encoding) as ofh:
                        self.__writeFile(ofh, containerList, maxLineLength=maxLineLength, columnAlignFlag=columnAlignFlag, useStopTokens=useStopTokens,
                                         formattingStep=formattingStep, enforceAscii=enforceAscii, cnvCharRefs=cnvCharRefs)
                else:
                    with open(outputFile, "wb") as ofh:
                        self.__writeFile(ofh, containerList, maxLineLength=maxLineLength, columnAlignFlag=columnAlignFlag, useStopTokens=useStopTokens,
                                         formattingStep=formattingStep, enforceAscii=enforceAscii, cnvCharRefs=cnvCharRefs)
            return True
        except Exception as e:
            logger.exception("Failing write with %s" % str(e))
            if self._raiseExceptions:
                raise e
            else:
                logger.error("Failing write for %s with %s" % (outputFile, str(e)))

        return False

    def __writeFile(self, ofh, containerList, maxLineLength=900, columnAlignFlag=True, useStopTokens=False, formattingStep=None, enforceAscii=False, cnvCharRefs=False):
        pdbxW = PdbxWriter(ofh)
        pdbxW.setUseStopTokens(flag=useStopTokens)
        pdbxW.setMaxLineLength(numChars=maxLineLength)
        pdbxW.setAlignmentFlag(flag=columnAlignFlag)
        pdbxW.setRowPartition(numParts=formattingStep)
        pdbxW.setConvertCharRefs(flag=cnvCharRefs)
        pdbxW.setSetEnforceAscii(enforceAscii)
        pdbxW.write(containerList)
