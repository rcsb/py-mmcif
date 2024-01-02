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
#  5-Dec-2023 dwp Add support for binary mmCIF (BCIF) reading and writing;
#                 Set cleanup default to True (delete temporary files and logs after reading)
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
from mmcif.io.BinaryCifReader import BinaryCifReader
from mmcif.io.BinaryCifWriter import BinaryCifWriter

try:
    from urllib.parse import urlsplit
except Exception:
    from urlparse import urlsplit


__docformat__ = "google en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


logger = logging.getLogger(__name__)


class IoAdapterPy(IoAdapterBase):
    """Python implementation of IoAdapterBase class providing essential read and write methods for mmCIF and BCIF data files -"""

    # pylint: disable=arguments-differ
    def readFile(
        self,
        inputFilePath,
        enforceAscii=False,
        selectList=None,
        excludeFlag=False,
        logFilePath=None,
        outDirPath=None,
        cleanUp=True,
        fmt="mmcif",
        timeout=None,
        storeStringsAsBytes=False,
        defaultStringEncoding="utf-8",
        **kwargs
    ):
        """Parse the data blocks in the input mmCIF or BCIF format data file into list of data or definition containers. The data category
           content within each data block is stored a collection of DataCategory objects within each container.

        Args:
            inputFilePath (string): Input file path
            enforceAscii (bool, optional): Flag to require ASCII encoding when reading in 'mmcif' file. See encoding error options. Defaults to False.
            selectList (List, optional):  List of data category names to be extracted or excluded from the input file (default: select/extract)
            excludeFlag (bool, optional): Flag to indicate selectList should be treated as an exclusion list
            logFilePath (string, optional): Log file path (if not provided this will be derived from the input file.)
            outDirPath (string, optional): Path for translated/re-encoded files and default logfiles.
            cleanUp (bool, optional): Flag to automatically remove logs and temporary files on exit.
            fmt (string, optional): Format of input file (either "mmcif" or "bcif"). Defaults to "mmcif".
            timeout (float, optional): Timeout in seconds for fetching data from remote urls

            # BCIF-specific args:
            storeStringsAsBytes (bool, optional): Strings are stored as lists of bytes (for BCIF files only). Defaults to False.
            defaultStringEncoding (str, optional): Default encoding for string data (for BCIF files only). Defaults to "utf-8".

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
            fmt = fmt.lower()
            #
            if sys.version_info[0] > 2:  # Check if using Python version higher than 2
                if fmt == "mmcif":
                    if self.__isLocal(filePath):
                        filePath = self._uncompress(filePath, oPath)
                        with open(filePath, "r", encoding=encoding, errors=self._readEncodingErrors) as ifh:
                            pRd = PdbxReader(ifh)
                            pRd.read(containerList, selectList, excludeFlag=excludeFlag)
                    else:  # handle files from the internet...
                        if filePath.endswith(".gz"):
                            customHeader = {"Accept-Encoding": "gzip"}
                            with closing(requests.get(filePath, headers=customHeader, timeout=timeout)) as ifh:
                                if self._raiseExceptions:
                                    ifh.raise_for_status()
                                gzit = gzip.GzipFile(fileobj=io.BytesIO(ifh.content))
                                it = (line.decode(encoding, "ignore") for line in gzit)
                                pRd = PdbxReader(it)
                                pRd.read(containerList, selectList, excludeFlag=excludeFlag)
                        else:
                            with closing(requests.get(filePath, timeout=timeout)) as ifh:
                                if self._raiseExceptions:
                                    ifh.raise_for_status()
                                it = (line.decode(encoding, "ignore") + "\n" for line in ifh.iter_lines())
                                pRd = PdbxReader(it)
                                pRd.read(containerList, selectList, excludeFlag=excludeFlag)
                elif fmt == "bcif":
                    # local vs. remote and gzip business is already done in BinaryCifReader
                    bcifRd = BinaryCifReader(storeStringsAsBytes=storeStringsAsBytes, defaultStringEncoding=defaultStringEncoding)
                    containerList = bcifRd.deserialize(filePath)
                else:
                    logger.error("Unsupported fmt %r. Currently only supports 'mmcif' or 'bcif'.", fmt)
            else:
                logger.warning("Support for Python 2 will be deprecated soon. Please use Python 3.")
                if fmt == "bcif":
                    logger.error("Support for BCIF reading only available in Python 3.")
                elif fmt == "mmcif":
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
                            with closing(requests.get(filePath, headers=customHeader, timeout=timeout)) as ifh:
                                if self._raiseExceptions:
                                    ifh.raise_for_status()
                                gzit = gzip.GzipFile(fileobj=io.BytesIO(ifh.content))
                                it = (line.decode(encoding, "ignore") for line in gzit)
                                pRd = PdbxReader(it)
                                pRd.read(containerList, selectList, excludeFlag=excludeFlag)
                        else:
                            with closing(requests.get(filePath, timeout=timeout)) as ifh:
                                if self._raiseExceptions:
                                    ifh.raise_for_status()
                                it = (line.decode(encoding, "ignore") + "\n" for line in ifh.iter_lines())
                                pRd = PdbxReader(it)
                                pRd.read(containerList, selectList, excludeFlag=excludeFlag)
                else:
                    logger.error("Unsupported fmt %r for Python2 installation of mmcif.io.IoAdapterPy. Currently only 'mmcif' is supported. Upgrade to Python3 for 'bcif' support", fmt)

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
        fmt="mmcif",
        storeStringsAsBytes=False,
        defaultStringEncoding="utf-8",
        applyTypes=True,
        dictionaryApi=None,
        useStringTypes=False,
        useFloat64=False,
        copyInputData=False,
        ignoreCastErrors=False,
        **kwargs
    ):
        """Write input list of data containers to the specified output file path in mmCIF or BCIF format.

        Args:
            outputFilePath (string): output file path
            containerList (list DataContainer objects, optional)
            maxLineLength (int, optional): Maximum length of output line (content is wrapped beyond this length)
            enforceAscii (bool, optional): Enforce ASCII encoding when writing out 'mmcif' file. Defaults to True.
            lastInOrder (list of category names, optional): Move data categories in this list to end of each data block
            selectOrder (list of category names, optional): Write only data categories on this list.
            columnAlignFlag (bool, optional): Format the output in aligned columns (default=True) (Native Python Only)
            useStopTokens (bool, optional): Include terminating 'stop_' tokens at the end of mmCIF categories (loop_'s) (Native Python only)
            formattingStep (int, optional): The number row samples within each category used to estimate maximum column width for data alignment (Native Python only)
            fmt (string, optional): Format of output file (either "mmcif" or "bcif"). Defaults to "mmcif".

            # BCIF-specific args:
            storeStringsAsBytes (bool, optional): Strings are stored as lists of bytes (for BCIF files only). Defaults to False.
            defaultStringEncoding (str, optional): Default encoding for string data (for BCIF files only). Defaults to "utf-8".
            applyTypes (bool, optional): apply explicit data typing before encoding (for BCIF files only; requires dictionaryApi to be passed too). Defaults to True.
            dictionaryApi (object, optional): DictionaryApi object instance (needed for BCIF files, only when applyTypes is True). Defaults to None.
            useStringTypes (bool, optional): assume all types are string (for BCIF files only). Defaults to False.
            useFloat64 (bool, optional): store floats with 64 bit precision (for BCIF files only). Defaults to False.
            copyInputData (bool, optional): make a new copy input data (for BCIF files only). Defaults to False.
            ignoreCastErrors (bool, optional): suppress errors when casting attribute types with dictionaryApi. Defaults to False.

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
            fmt = fmt.lower()
            #
            if sys.version_info[0] > 2:  # Check if using Python version higher than 2
                if fmt == "mmcif":
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
                elif fmt == "bcif":
                    bcifW = BinaryCifWriter(
                        dictionaryApi=dictionaryApi,
                        storeStringsAsBytes=storeStringsAsBytes,
                        defaultStringEncoding=defaultStringEncoding,
                        applyTypes=applyTypes,
                        useStringTypes=useStringTypes,
                        useFloat64=useFloat64,
                        copyInputData=copyInputData,
                        ignoreCastErrors=ignoreCastErrors,
                    )
                    bcifW.serialize(outputFilePath, containerList)
                else:
                    logger.error("Unsupported fmt %r. Currently only supports 'mmcif' or 'bcif'.", fmt)
                    return False
            else:
                logger.warning("Support for Python 2 will be deprecated soon. Please use Python 3.")
                if fmt == "bcif":
                    logger.error("Support for BCIF writing only available in Python 3.")
                    return False
                elif fmt == "mmcif":
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
                else:
                    logger.error("Unsupported fmt %r for Python2 installation of mmcif.io.IoAdapterPy. Currently only 'mmcif' is supported. Upgrade to Python3 for 'bcif' support", fmt)
                    return False
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
