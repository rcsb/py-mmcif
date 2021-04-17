##
# File:    IoAdapterPy.py
# Author:  J. Westbrook
# Date:    16-Jan-2013
# Version: 0.001 Initial version
#
# Updates:
# 30-Jul-2014 jdw Expose column alignment and  maximum line length as optional writeFile() parameters.
# 22-Jun-2015 jdw add additional formatting control on write method.
# 15-Aug-2016 rps readFile() updated to accept optional "logtag" parameter for consistency with IoAdapterCore API
# 01-Aug-2017 jdw migrate portions to public repo
# 12-Jan-2018 jdw start to unify api features -
#  6-Aug-2018 jdw set default container properties (locator and load_date)
# 25-Aug-2018 jdw use the input locator rather than uncompressed locator name
#  5-Apr-2021 jdw allow access to data/dictionary artifacts over HTTP(S)
##
"""
Python implementation of IoAdapterBase class providing read and write
        methods for PDBx/mmCIF data files -

"""
from __future__ import absolute_import

import gzip
import io
import logging
import sys
import uuid
from contextlib import closing

import requests
from future.utils import raise_from
from mmcif.io.IoAdapterBase import IoAdapterBase
from mmcif.io.PdbxExceptions import PdbxError
from mmcif.io.PdbxExceptions import PdbxSyntaxError
from mmcif.io.PdbxReader import PdbxReader
from mmcif.io.PdbxWriter import PdbxWriter

try:
    from urllib.parse import urlsplit
except Exception:
    from urlparse import urlsplit


__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


logger = logging.getLogger(__name__)


class IoAdapterPy(IoAdapterBase):
    """Python implementation of IoAdapterBase class providing essential read and write methods for mmCIF data files -"""

    # def __init__(self, *args, **kwargs):
    #     super(IoAdapterPy, self).__init__(*args, **kwargs)
    # pylint: disable=arguments-differ
    def readFile(self, inputFilePath, enforceAscii=False, selectList=None, excludeFlag=False, logFilePath=None, outDirPath=None, cleanUp=False, **kwargs):
        """Parse the data blocks in the input mmCIF format data file into list of data or definition containers.  The data category content within
            each data block is stored a collection of DataCategory objects within each container.

        Args:
            inputFilePath (string): Input file path
            enforceAscii (bool, optional): Flag to requiring ASCII encoding. See encoding error options.
            selectList (List, optional):  List of data category names to be extracted or excluded from the input file (default: select/extract)
            excludeFlag (bool, optional): Flag to indicate selectList should be treated as an exclusion list
            logFilePath (string, optional): Log file path (if not provided this will be derived from the input file.)
            outDirPath (string, optional): Path for translated/re-encoded files and default logfiles.
            cleanUp (bool, optional): Flag to automatically remove logs and temporary files on exit.
            **kwargs: Placeholder for missing keyword arguments.

        Returns:
            List of DataContainers: Contents of input file parsed into a list of DataContainer objects.

        """
        if kwargs:
            logger.warning("Unsupported keyword arguments %s", kwargs.keys())
        filePath = str(inputFilePath)
        # oPath = outDirPath if outDirPath else '.'
        oPath = self._chooseTemporaryPath(inputFilePath, outDirPath=outDirPath)
        containerList = []
        if enforceAscii:
            encoding = "ascii"
        else:
            encoding = "utf-8"
        try:
            #
            lPath = logFilePath
            if not lPath:
                lPath = self._getDefaultFileName(filePath, fileType="cif-parser-log", outDirPath=oPath)
            #
            self._setLogFilePath(lPath)
            # ---
            if self.__isLocal(filePath) and not self._fileExists(filePath):
                return []
            #
            if sys.version_info[0] > 2:
                if self.__isLocal(filePath):
                    filePath = self._uncompress(filePath, oPath)
                    with open(filePath, "r", encoding=encoding, errors=self._readEncodingErrors) as ifh:
                        pRd = PdbxReader(ifh)
                        pRd.read(containerList, selectList, excludeFlag=excludeFlag)
                else:
                    if filePath.endswith(".gz"):
                        customHeader = {"Accept-Encoding": "gzip"}
                        with closing(requests.get(filePath, headers=customHeader)) as ifh:
                            gzit = gzip.GzipFile(fileobj=io.BytesIO(ifh.content))
                            it = (line.decode(encoding) for line in gzit)
                            pRd = PdbxReader(it)
                            pRd.read(containerList, selectList, excludeFlag=excludeFlag)
                    else:
                        with closing(requests.get(filePath)) as ifh:
                            it = (line.decode(encoding) + "\n" for line in ifh.iter_lines())
                            pRd = PdbxReader(it)
                            pRd.read(containerList, selectList, excludeFlag=excludeFlag)
            else:
                if self.__isLocal(filePath):
                    filePath = self._uncompress(filePath, oPath)
                    if enforceAscii:
                        with io.open(filePath, "r", encoding=encoding, errors=self._readEncodingErrors) as ifh:
                            pRd = PdbxReader(ifh)
                            pRd.read(containerList, selectList, excludeFlag=excludeFlag)
                    else:
                        with open(filePath, "r") as ifh:
                            pRd = PdbxReader(ifh)
                            pRd.read(containerList, selectList, excludeFlag=excludeFlag)
                else:
                    if filePath.endswith(".gz"):
                        customHeader = {"Accept-Encoding": "gzip"}
                        with closing(requests.get(filePath, headers=customHeader)) as ifh:
                            gzit = gzip.GzipFile(fileobj=io.BytesIO(ifh.content))
                            it = (line.decode(encoding) for line in gzit)
                            pRd = PdbxReader(it)
                            pRd.read(containerList, selectList, excludeFlag=excludeFlag)
                    else:
                        with closing(requests.get(filePath)) as ifh:
                            it = (line.decode(encoding) + "\n" for line in ifh.iter_lines())
                            pRd = PdbxReader(it)
                            pRd.read(containerList, selectList, excludeFlag=excludeFlag)
            if cleanUp:
                self._cleanupFile(lPath, lPath)
                self._cleanupFile(filePath != str(inputFilePath), filePath)
            self._setContainerProperties(containerList, locator=str(inputFilePath), load_date=self._getTimeStamp(), uid=uuid.uuid4().hex)
        except (PdbxError, PdbxSyntaxError) as ex:
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
                logger.error("Failing read for %s with %s", filePath, str(e))
        return containerList

    def getReadDiags(self):
        """Return diagnostics from last readFile operation. This will NOT be an exhaustive list but
        rather the particular failure that raised a parsing exception.
        """
        return self._readLogRecords()

    def writeFile(
        self,
        outputFilePath,
        containerList,
        maxLineLength=900,
        enforceAscii=True,
        lastInOrder=None,
        selectOrder=None,
        columnAlignFlag=True,
        useStopTokens=False,
        formattingStep=None,
        **kwargs
    ):
        """Write input list of data containers to the specified output file path in mmCIF format.

        Args:
            outputFilePath (string): output file path
            containerList (list DataContainer objects, optional)
            maxLineLength (int, optional): Maximum length of output line (content is wrapped beyond this length)
            enforceAscii (bool, optional): Filter output (not implemented - content must be ascii compatible on input)
            lastInOrder (list of category names, optional): Move data categories in this list to end of each data block
            selectOrder (list of category names, optional): Write only data categories on this list.

            columnAlignFlag (bool, optional): Format the output in aligned columns (default=True) (Native Python Only)
            useStopTokens (bool, optional): Include terminating 'stop_' tokens at the end of mmCIF categories (loop_'s) (Native Python only)
            formattingStep (int, optional): The number row samples within each category used to estimate maximum column width for data alignment (Native Python only)
            **kwargs: Placeholder for unsupported key value pairs

        Returns:
            bool: Completion status


        """
        lastInOrder = lastInOrder if lastInOrder else ["pdbx_nonpoly_scheme", "pdbx_poly_seq_scheme", "atom_site", "atom_site_anisotrop"]
        if kwargs:
            logger.warning("Unsupported keyword arguments %s", kwargs.keys())
        try:
            if enforceAscii:
                encoding = "ascii"
            else:
                encoding = "utf-8"
            #
            if sys.version_info[0] > 2:
                with open(outputFilePath, "w", encoding=encoding) as ofh:
                    self.__writeFile(
                        ofh,
                        containerList,
                        maxLineLength=maxLineLength,
                        columnAlignFlag=columnAlignFlag,
                        lastInOrder=lastInOrder,
                        selectOrder=selectOrder,
                        useStopTokens=useStopTokens,
                        formattingStep=formattingStep,
                        enforceAscii=enforceAscii,
                        cnvCharRefs=self._useCharRefs,
                    )
            else:
                if enforceAscii:
                    with io.open(outputFilePath, "w", encoding=encoding) as ofh:
                        self.__writeFile(
                            ofh,
                            containerList,
                            maxLineLength=maxLineLength,
                            columnAlignFlag=columnAlignFlag,
                            lastInOrder=lastInOrder,
                            selectOrder=selectOrder,
                            useStopTokens=useStopTokens,
                            formattingStep=formattingStep,
                            enforceAscii=enforceAscii,
                            cnvCharRefs=self._useCharRefs,
                        )
                else:
                    with open(outputFilePath, "wb") as ofh:
                        self.__writeFile(
                            ofh,
                            containerList,
                            maxLineLength=maxLineLength,
                            columnAlignFlag=columnAlignFlag,
                            lastInOrder=lastInOrder,
                            selectOrder=selectOrder,
                            useStopTokens=useStopTokens,
                            formattingStep=formattingStep,
                            enforceAscii=enforceAscii,
                            cnvCharRefs=self._useCharRefs,
                        )
            return True
        except Exception as ex:
            if self._raiseExceptions:
                raise_from(ex, None)
            else:
                logger.exception("Failing write for %s with %s", outputFilePath, str(ex))
                logger.error("Failing write for %s with %s", outputFilePath, str(ex))

        return False

    def __writeFile(
        self,
        ofh,
        containerList,
        maxLineLength=900,
        columnAlignFlag=True,
        lastInOrder=None,
        selectOrder=None,
        useStopTokens=False,
        formattingStep=None,
        enforceAscii=False,
        cnvCharRefs=False,
    ):
        """Internal method mapping arguments to PDBxWriter API."""
        #
        pdbxW = PdbxWriter(ofh)
        pdbxW.setUseStopTokens(flag=useStopTokens)
        pdbxW.setMaxLineLength(numChars=maxLineLength)
        pdbxW.setAlignmentFlag(flag=columnAlignFlag)
        pdbxW.setRowPartition(numParts=formattingStep)
        pdbxW.setConvertCharRefs(flag=cnvCharRefs)
        pdbxW.setSetEnforceAscii(enforceAscii)
        pdbxW.write(containerList, lastInOrder=lastInOrder, selectOrder=selectOrder)

    def __isLocal(self, locator):
        try:
            locSp = urlsplit(locator)
            return locSp.scheme in ["", "file"]
        except Exception as e:
            logger.exception("For locator %r failing with %s", locator, str(e))
        return None
