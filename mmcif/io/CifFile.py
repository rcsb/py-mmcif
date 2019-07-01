##
# File: CifFile.py
# Date: 28-Oct-2018 jdw
#
# Older deprecated API
#
#
##
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


import logging
import warnings

from mmcif.core.mmciflib import ParseCifSimple  # pylint: disable=no-name-in-module,import-error

warnings.filterwarnings("ignore", category=DeprecationWarning)
logger = logging.getLogger(__name__)


class CifFile(object):
    """
    CifFile

    New method prototype --

    CifFile* ParseCifSimple(const std::string& fileName,
                            const bool verbose = false,
                            const unsigned int intCaseSense = 0,
                            const unsigned int maxLineLength = CifFile::STD_CIF_LINE_LENGTH,
                            const std::string& nullValue = CifString::UnknownValue,
                            const std::string& parseLogFileName = std::string());

    """

    def __init__(self, fileName, parseLogFileName=None):
        self.__fileName = fileName

        if parseLogFileName is None:
            self.__cifFile = ParseCifSimple(self.__fileName, False, 0, 255, "?", "")
        else:
            self.__cifFile = ParseCifSimple(self.__fileName, False, 0, 255, "?", parseLogFileName)

    def getCifFile(self):
        return self.__cifFile

    @classmethod
    def getFileExt(cls):
        return "cif"

    def write(self, fileName):
        self.__cifFile.Write(fileName)

    @classmethod
    def read(cls, fileName):
        return cls(fileName)
