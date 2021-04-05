##
# File:    IoAdapterBase.py
# Author:  J. Westbrook
# Date:    1-Aug-2017
# Version: 0.001 Initial version
#
# Updates:
#   13-Jan-2018 jdw move _getCategoryNameList() PdbxContainerBase class
#    6-Aug-2018 jdw add _setContainerProperties() to assign default container properties
#   10-Aug-2018 jdw add _uncompress() method (suppress xz as lzma is not support in py27)
#   11-Nov-2018 jdw add method to _chooseTemporaryPath()
##
"""
Base class presenting essential PDBx/mmCIF IO methods.

"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"

import bz2
import datetime
import gzip
import io
import logging

# import lzma
import os
import shutil
import tempfile
import time
import zipfile

from mmcif.io.PdbxExceptions import PdbxError

logger = logging.getLogger(__name__)


class IoAdapterBase(object):
    """Base class presenting essential mmCIF I/O methods."""

    def __init__(self, *args, **kwargs):
        """General options controlling I/O method operations:

        Args:
            raiseExceptions (bool, optional): Flag to indicate that API errors should generate exceptions (True) or catch and log errors (default=False)
            maxInputLineLength (int, optional):  Default maximum input line length (default=4096)
            useCharRefs (bool, optional): Replace non-ascii characters with XML Character References (default=True)
            readEncodingErrors (str, optional): treatment of encoding errors at read time (default='ignore')
            timing (bool, optional):  log timing details for parsing and processing steps (default=False)
            verbose (bool,optional):  log verbose output from wrapped libraries

        """
        _ = args
        self._raiseExceptions = kwargs.get("raiseExceptions", False)
        self._maxInputLineLength = kwargs.get("maxInputLineLength", 4096)
        self._useCharRefs = kwargs.get("useCharRefs", True)
        self.__logFilePath = None
        self._debug = kwargs.get("debug", False)
        self._timing = kwargs.get("timing", False)
        self._verbose = kwargs.get("verbose", True)
        self._readEncodingErrors = kwargs.get("readEncodingErrors", "ignore")

    def readFile(self, *args, **kwargs):
        """Read file method. (abstract)

         Args:
            inputFilePath (string):  Input file path/uri
                   kw:  optional key-value arguments

        Returns:
            list of DataContainer Objects:  list of data or definition container objects
        """
        raise NotImplementedError("To be implemented in subclass")

    def writeFile(self, outputFilePath, containerList, **kwargs):
        """Write file method - (abstract)

        Args:
            outputFilePath (string):  output file path
            containerList (list of DataContainer objects):  list of data or definition containers objects for output

        Returns:
            bool: Completion status
        """
        raise NotImplementedError("To be implemented in subclass")

    def getReadDiags(self):
        """Return any diagnostics from the last read operation. (abstract)"""
        raise NotImplementedError("To be implemented in subclass")

    def _setContainerProperties(self, containerList, **kwargs):
        try:
            for container in containerList:
                for kw in kwargs:
                    container.setProp(kw, kwargs[kw])
        except Exception:
            return False

    def _getTimeStamp(self):
        utcnow = datetime.datetime.utcnow()
        ts = utcnow.strftime("%Y-%m-%d:%H:%M:%S")
        return ts

    def _getCategoryNameList(self, container, lastInOrder=None, selectOrder=None):
        """Return an ordered list of categories in the input container subject to
        input category name lists.

        Args:
           container (DataContainer object):  Input DataContainer object
           lastInOrder (list):  names of categories to be shifted to the end of the container.
           selectOrder (list):  preferred order of category names

        Returns:
           catNameList: list:  augmented category list or full list (default)
        """
        catNameList = []
        if lastInOrder:
            objNameList = container.getObjNameList()
            lastList = []
            for nm in objNameList:
                if nm in lastInOrder:
                    lastList.append(nm)
                    continue
                catNameList.append(nm)
            catNameList.extend(lastList)
        elif selectOrder:
            for nm in selectOrder:
                if container.exists(nm):
                    catNameList.append(nm)
        else:
            catNameList = container.getObjNameList()

        return catNameList

    def _setLogFilePath(self, filePath):
        """Set the log file path."""
        self.__logFilePath = filePath

    def _getLogFilePath(self):
        """Return current log file path."""
        return self.__logFilePath

    def _appendToLog(self, stList):
        """Append input string list to the current log file -"""
        if not self.__logFilePath:
            return False
        try:
            with open(self.__logFilePath, "a") as ofh:
                ofh.write("%s\n" % "\n".join(stList))
            return True
        except Exception as e:
            logger.debug("Failing with %s", str(e))
        return True

    def _logError(self, msg):
        """Convenience method to log error messages and optionally raise general exceptions (PdbxError)."""
        self._appendToLog([msg])
        if self._raiseExceptions:
            raise PdbxError(msg)
        else:
            logger.error(msg)

    def _readLogRecords(self):
        """Return the contents of the current log file as list of strings."""
        diagL = []
        try:
            with open(self.__logFilePath, "r") as ifh:
                for line in ifh:
                    diagL.append(line[:-1])
        except Exception as e:
            msg = "No logfile found %s (%s)" % (self.__logFilePath, str(e))
            diagL.append(msg)
            logger.debug(msg)

        return diagL

    def __getDiscriminator(self):
        """Internal method returning a string which can discriminate among default file names -"""
        return str(int(time.time() * 10000))

    def _chooseTemporaryPath(self, filePath, outDirPath=None):
        """Select a path for temporary files in the priority order
        outDirpath, directory containing the input filePath, current working directory,
        dynamically created temporary directory.

        These choices harmonize various legacy api behaviors.
        """
        if outDirPath:
            return outDirPath
        #
        for oPath in [os.path.dirname(filePath), ".", tempfile.gettempdir()]:
            if os.access(oPath, os.W_OK):
                return oPath

    def _getDefaultFileName(self, filePath, fileType="cif-parser", fileExt="log", outDirPath=None, verify=True):
        """Return default file path for the target input file subject to input attributes and the output path."""
        returnFilePath = None
        try:
            _, fn = os.path.split(filePath)
            bn, _ = os.path.splitext(fn)
            #
            ft = fileType if fileType else "temp"
            fex = fileExt if fileExt else "tmp"
            #
            sf = "_" + ft + "_P" + self.__getDiscriminator() + "." + fex
            #
            # pth = outDirPath if outDirPath else '.'
            pth = self._chooseTemporaryPath(filePath, outDirPath=outDirPath)
            #
            if verify:
                # test if pth is actually writable ?  Throw exception otherwise -
                #
                testfile = tempfile.TemporaryFile(dir=pth)
                testfile.close()
                #
            returnFilePath = os.path.join(pth, bn + sf)
        except Exception as e:
            if self._raiseExceptions:
                raise e
            else:
                logger.error("Failed creating default filename for %s type %s with %s", filePath, fileType, str(e))

        return returnFilePath

    def _fileExists(self, filePath):
        """Verify that input file path exists and is readable."""
        try:
            if not os.access(filePath, os.R_OK):
                msg = "Missing file %r" % filePath
                self._appendToLog([msg])
                logger.error(msg)
                #
                if self._raiseExceptions:
                    raise PdbxError(msg)
                return False
            else:
                logger.debug("Reading from file path %s", filePath)
                return True
        except Exception as e:
            msg = "File check error for %r with %s " % (filePath, str(e))
            self._appendToLog([msg])
            if self._raiseExceptions:
                raise PdbxError(msg)
            else:
                logger.error(msg)
        return False

    def _cleanupFile(self, test, filePath):
        """Remove the input file path subject to the input test condition."""
        try:
            if test:
                os.remove(filePath)
        except Exception:
            pass

    def _toAscii(self, inputFilePath, outputFilePath, chunkSize=5000, encodingErrors="ignore", readEncodingErrors="ignore"):
        """Encode input file to Ascii and write this to the target output file.   Handle encoding
        errors according to the input settting ('ignore', 'escape', 'xmlcharrefreplace').
        """
        try:
            startTime = time.time()
            chunk = []
            with io.open(inputFilePath, "r", encoding="utf-8", errors=readEncodingErrors) as ifh, io.open(outputFilePath, "w", encoding="ascii") as ofh:
                for line in ifh:
                    # chunk.append(line.encode('ascii', 'xmlcharrefreplace').decode('ascii'))
                    chunk.append(line.encode("ascii", encodingErrors).decode("ascii"))
                    if len(chunk) == chunkSize:
                        ofh.writelines(chunk)
                        chunk = []
                ofh.writelines(chunk)
            if self._timing:
                stepTime1 = time.time()
                logger.info("Timing text file %s encoded to as ascii in %.4f seconds", inputFilePath, stepTime1 - startTime)
            return True
        except Exception as e:
            msg = "Failing text ascii encoding for %s with %s" % (inputFilePath, str(e))
            self._appendToLog([msg])
            logger.error(msg)
            if self._raiseExceptions:
                raise PdbxError(msg)
        #
        return False

    def _uncompress(self, inputFilePath, outputDir):
        """Uncompress the input file if the path name has a recognized compression type file extension.file

        Return the file name of the uncompressed file (in outDir) or the original input file path.

        """
        try:
            startTime = time.time()
            _, fn = os.path.split(inputFilePath)
            bn, _ = os.path.splitext(fn)
            outputFilePath = os.path.join(outputDir, bn)
            if inputFilePath.endswith(".gz"):
                with gzip.open(inputFilePath, mode="rb") as inpF:
                    with io.open(outputFilePath, "wb") as outF:
                        shutil.copyfileobj(inpF, outF)
            elif inputFilePath.endswith(".bz2"):
                with bz2.open(inputFilePath, mode="rb") as inpF:
                    with io.open(outputFilePath, "wb") as outF:
                        shutil.copyfileobj(inpF, outF)
            # elif inputFilePath.endswith(".xz"):
            #    with lzma.open(inputFilePath, mode="rb") as inpF:
            #        with io.open(outputFilePath, "wb") as outF:
            #            shutil.copyfileobj(inpF, outF)
            elif inputFilePath.endswith(".zip"):
                with zipfile.ZipFile(inputFilePath, mode="rb") as inpF:
                    with io.open(outputFilePath, "wb") as outF:
                        shutil.copyfileobj(inpF, outF)
            else:
                outputFilePath = inputFilePath
            if self._timing:
                stepTime1 = time.time()
                logger.info("Timing text file %s uncompressed in %.4f seconds", inputFilePath, stepTime1 - startTime)
            #
        except Exception as e:
            msg = "Failing uncompress for file %s with %s" % (inputFilePath, str(e))
            self._appendToLog([msg])
            logger.exception(msg)
            if self._raiseExceptions:
                raise PdbxError(msg)

        logger.debug("Returning file path %r", outputFilePath)
        return outputFilePath
