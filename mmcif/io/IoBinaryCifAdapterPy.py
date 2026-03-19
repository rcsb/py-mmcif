"""
Python implementation of IoAdapterBase class providing read and write methods for Binary PDBx/mmCIF data files.
"""
import logging
from mmcif.io.IoAdapterBase import IoAdapterBase
from mmcif.io.PdbxExceptions import PdbxError, PdbxSyntaxError
from mmcif.io.BinaryCifReader import BinaryCifReader
from mmcif.io.BinaryCifWriter import BinaryCifWriter
from mmcif.io.PdbxWriter import PdbxWriter
from mmcif.api.DataCategoryTyped import DataCategoryTyped
from mmcif.api.DictionaryApi import DictionaryApi
from mmcif.api.PdbxContainers import DataContainer
import uuid

logger = logging.getLogger(__name__)


class IoBinaryCifAdapterPy(IoAdapterBase):
    """Python implementation of IoAdapterBase class providing essential read and write methods for binary mmCIF data files -"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #     super(IoBinaryCifAdapterPy, self).__init__(*args, **kwargs)
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
        # encoding variable is not used; removed
        try:
            lPath = logFilePath
            if not lPath:
                lPath = self._getDefaultFileName(filePath, fileType="bcif-parser-log", outDirPath=oPath)
            self._setLogFilePath(lPath)
            if self.__isLocal(filePath) and not self._fileExists(filePath):
                return []
            if self.__isLocal(filePath):
                filePath = self._uncompress(filePath, oPath)
                bRd = BinaryCifReader(storeStringsAsBytes=False)
                containerList = bRd.deserialize(filePath)
            # Remote file handling can be added here if needed
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
        """Write input list of data containers to the specified output file path in binary CIF format.

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
            # Legacy/broken code removed with Python 2.7 support
            logger.error("writeFile is not implemented in this stub.")
            return False
        except Exception as ex:
            if self._raiseExceptions:
                raise_from(ex, None)
            else:
                logger.exception("Failing write for %s with %s", outputFilePath, str(ex))
                logger.error("Failing write for %s with %s", outputFilePath, str(ex))

        return False

        if kwargs:
            logger.warning("Unsupported keyword arguments %s", kwargs.keys())
        filePath = str(inputFilePath)
        oPath = self._chooseTemporaryPath(inputFilePath, outDirPath=outDirPath)
        containerList = []
        try:
            lPath = logFilePath
            if not lPath:
                lPath = self._getDefaultFileName(filePath, fileType="bcif-parser-log", outDirPath=oPath)
            self._setLogFilePath(lPath)
            if self.__isLocal(filePath) and not self._fileExists(filePath):
                return []
            if self.__isLocal(filePath):
                filePath = self._uncompress(filePath, oPath)
                bRd = BinaryCifReader(storeStringsAsBytes=False)
                containerList = bRd.deserialize(filePath)
            # Remote file handling can be added here if needed
            if cleanUp:
                self._cleanupFile(lPath, lPath)
                self._cleanupFile(filePath != str(inputFilePath), filePath)
            self._setContainerProperties(containerList, locator=str(inputFilePath), load_date=self._getTimeStamp(), uid=uuid.uuid4().hex)
        except (PdbxError, PdbxSyntaxError) as ex:
            msg = "File %r with %s" % (filePath, str(ex))
            self._appendToLog([msg])
            self._cleanupFile(lPath and cleanUp, lPath)
            if self._raiseExceptions:
                raise ex
        except Exception as e:
            msg = "File %r with %s" % (filePath, str(e))
            self._appendToLog([msg])
            self._cleanupFile(lPath and cleanUp, lPath)
            if self._raiseExceptions:
                raise e
            else:
                logger.error("Failing read for %s with %s", filePath, str(e))
        return containerList
