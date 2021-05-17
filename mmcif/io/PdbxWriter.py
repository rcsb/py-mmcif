##
# File:  PdbxWriter.py
# Date:  2011-10-09 Jdw  Adapted from PdbxParser.py
#
# Updates:
#    5-Apr-2011 jdw  Using the double quote format preference
#   23-Oct-2012 jdw  update path details and reorganize.
#   17-Dec-2012 jdw  Add quoting preference option
#   25-Jul-2014 jdw  expose methods setAlignmentFlag() and setMaxLineLength()
#   23-Jun-2015 jdw  correct misnamed parameter in formatting method
#   28-Dec-2017 jdw  port to
#   13-Jan-2018 jdw  add selection attributes lastInOrder=None, selectOrder=None
#    8-Mar-2018 jdw  make step calc integer division
#    2-Feb-2019 jdw  adjust formatting removing spurious comments and newlines
###
"""
Utilities for writing mmCIF format data and dictionary containers.

"""

__docformat__ = "google en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"

import logging
import sys

from mmcif.api.DataCategoryFormatted import DataCategoryFormatted
from mmcif.io.PdbxExceptions import PdbxError

logger = logging.getLogger(__name__)


class PdbxWriter(object):

    """Write mmCIF data files or dictionaries using the input container or container list."""

    def __init__(self, ofh=sys.stdout):
        self.__ofh = ofh
        self.__containerList = []
        self.__maximumLineLength = 2048
        self.__spacing = 2
        self.__indentDefinition = 3
        self.__indentSpace = " " * self.__indentDefinition
        self.__doDefinitionIndent = False
        # Maximum number of rows checked for value length and format
        self.__rowPartition = None
        # Defaults to double quoting preference -
        self.__preferDoubleQuotes = True
        self.__useAlignedColumns = True
        self.__useStopTokens = False
        self.__cnvCharRefs = False
        #
        self.__enforceAscii = False
        self.__isPy3 = sys.version_info[0] == 3
        # if self.__isPy3:
        #     self.__string_types = str
        # else:
        #    self.__string_types = basestring

    def setSetEnforceAscii(self, boolVal):
        self.__enforceAscii = boolVal

    def setConvertCharRefs(self, flag):
        self.__cnvCharRefs = flag

    def setUseStopTokens(self, flag):
        self.__useStopTokens = flag

    def setMaxLineLength(self, numChars):
        self.__maximumLineLength = numChars

    def setAlignmentFlag(self, flag=True):
        self.__useAlignedColumns = flag

    def setPreferSingleQuotes(self):
        self.__preferDoubleQuotes = False

    def setPreferDoubleQuotes(self):
        self.__preferDoubleQuotes = True

    def setRowPartition(self, numParts):
        """Maximum number of partitions used to format value length for column alignment"""
        self.__rowPartition = numParts

    def write(self, containerList, lastInOrder=None, selectOrder=None):
        self.__containerList = containerList
        for container in self.__containerList:
            self.writeContainer(container, lastInOrder=lastInOrder, selectOrder=selectOrder)

    def writeContainer(self, container, lastInOrder=None, selectOrder=None):
        indS = " " * self.__indentDefinition
        if container.getType() == "definition":
            self.__write("save_%s" % container.getName())
            # self.__write("save_%s\n" % container.getName())
            self.__doDefinitionIndent = True
            # self.__write(indS + "#\n")
        elif container.getType() == "data":
            if container.getGlobal():
                self.__write("global_\n")
                self.__doDefinitionIndent = False
                self.__write("\n")
            else:
                self.__write("data_%s\n" % container.getName())
                self.__doDefinitionIndent = False
                # self.__write("#\n")

        nmL = container.filterObjectNameList(lastInOrder=lastInOrder, selectOrder=selectOrder)
        for nm in nmL:
            obj = container.getObj(nm)
            objL = obj.getRowList()

            # Skip empty objects
            if not objL:
                continue

            # Item - value formattting
            elif len(objL) == 1:
                self.__writeItemValueFormat(obj)

            # Table formatting -
            elif objL and obj.getAttributeList():
                if self.__useAlignedColumns:
                    self.__writeTableFormat(obj)
                else:
                    self.__writeTable(obj)
            else:
                raise PdbxError("")

            if self.__doDefinitionIndent:
                self.__write(indS + "#")
            else:
                self.__write("#")

        # Add a trailing saveframe reserved word
        if container.getType() == "definition":
            self.__write("\nsave_\n")
        self.__write("#\n")

    def __write(self, st):
        try:
            if self.__cnvCharRefs:
                self.__ofh.write(st.encode("ascii", "xmlcharrefreplace").decode("ascii"))
            elif not self.__isPy3:
                if self.__enforceAscii:
                    self.__ofh.write(st.decode("ascii"))
                else:
                    self.__ofh.write(st)
                    # self.__ofh.write(st.encode('utf-8').decode('utf-8'))
            else:
                self.__ofh.write(st)
        except Exception as e:
            logger.exception("write fails with %s for %r", str(e), st)

    def __writeItemValueFormat(self, categoryObj):
        # indS = " " * self.__INDENT_DEFINITION
        myCategory = DataCategoryFormatted(categoryObj, preferDoubleQuotes=self.__preferDoubleQuotes)
        # Compute the maximum item name length within this category -
        attributeNameLengthMax = 0
        for attributeName in myCategory.getAttributeList():
            attributeNameLengthMax = max(attributeNameLengthMax, len(attributeName))
        itemNameLengthMax = self.__spacing + len(myCategory.getName()) + attributeNameLengthMax + 2
        #
        lineList = []
        # lineList.append(indS+"#\n")
        lineList.append("\n")
        for attributeName, _ in myCategory.getAttributeListWithOrder():
            if self.__doDefinitionIndent:
                #        - add indent --
                lineList.append(self.__indentSpace)

            itemName = "_%s.%s" % (myCategory.getName(), attributeName)
            lineList.append(itemName.ljust(itemNameLengthMax))

            lineList.append(myCategory.getValueFormatted(attributeName, 0))
            lineList.append("\n")

        self.__write("".join(lineList))

    def __writeTableFormat(self, categoryObj):
        # indS = " " * self.__INDENT_DEFINITION
        myCategory = DataCategoryFormatted(categoryObj, preferDoubleQuotes=self.__preferDoubleQuotes)
        # Write the declaration of the loop_
        #
        lineList = []
        # lineList.append(indS + '#\n')
        lineList.append("\n")
        if self.__doDefinitionIndent:
            lineList.append(self.__indentSpace)
        lineList.append("loop_")
        for attributeName in myCategory.getAttributeList():
            lineList.append("\n")
            if self.__doDefinitionIndent:
                lineList.append(self.__indentSpace)
            itemName = "_%s.%s" % (myCategory.getName(), attributeName)
            lineList.append(itemName)
        self.__write("".join(lineList))

        #
        # Write the data in tabular format -
        #
        # print myCategory.getName()
        # print myCategory.getAttributeList()

        #    For speed make the following evaluation on a portion of the table
        if self.__rowPartition is not None:
            numSteps = max(1, myCategory.getRowCount() // self.__rowPartition)
        else:
            numSteps = 1

        formatTypeList, _ = myCategory.getFormatTypeList(steps=numSteps)
        maxLengthList = myCategory.getAttributeValueMaxLengthList(steps=numSteps)
        spacing = " " * self.__spacing
        #

        # print formatTypeList
        # print dataTypeList
        # print maxLengthList
        #
        for iRow in range(myCategory.getRowCount()):
            lineList = []
            lineList.append("\n")
            if self.__doDefinitionIndent:
                lineList.append(self.__indentSpace + "  ")

            for iAt in range(myCategory.getAttributeCount()):
                formatType = formatTypeList[iAt]
                maxLength = maxLengthList[iAt]

                if formatType == "FT_UNQUOTED_STRING" or formatType == "FT_NULL_VALUE":
                    val = myCategory.getValueFormattedByIndex(iAt, iRow)
                    lineList.append(val.ljust(maxLength))

                elif formatType == "FT_NUMBER":
                    val = myCategory.getValueFormattedByIndex(iAt, iRow)
                    lineList.append(val.rjust(maxLength))

                elif formatType == "FT_QUOTED_STRING":
                    val = myCategory.getValueFormattedByIndex(iAt, iRow)
                    # don't pad the last item in row condition
                    if iAt == myCategory.getAttributeCount() - 1:
                        lineList.append(val.ljust(len(val)))
                    else:
                        lineList.append(val.ljust(maxLength + 2))

                elif formatType == "FT_MULTI_LINE_STRING":
                    val = myCategory.getValueFormattedByIndex(iAt, iRow)
                    lineList.append(val)

                lineList.append(spacing)

            self.__write("".join(lineList))
        self.__write("\n")
        if self.__useStopTokens:
            self.__write("stop_\n")

    def __writeTable(self, categoryObj, numSteps=5):
        indS = " " * self.__indentDefinition
        myCategory = DataCategoryFormatted(categoryObj, preferDoubleQuotes=self.__preferDoubleQuotes)
        # Write the declaration of the loop_
        #
        lineList = []
        lineList.append(indS + "#\n")
        if self.__doDefinitionIndent:
            lineList.append(self.__indentSpace)
        lineList.append("loop_")
        for attributeName in myCategory.getAttributeList():
            lineList.append("\n")
            if self.__doDefinitionIndent:
                lineList.append(self.__indentSpace)
            itemName = "_%s.%s" % (myCategory.getName(), attributeName)
            lineList.append(itemName)
        self.__write("".join(lineList))

        #
        formatTypeList, _ = myCategory.getFormatTypeList(steps=numSteps)
        spacing = " " * self.__spacing
        #
        for iRow in range(myCategory.getRowCount()):
            lineList = []
            lineList.append("\n")
            if self.__doDefinitionIndent:
                lineList.append(self.__indentSpace + "  ")

            for iAt in range(myCategory.getAttributeCount()):
                formatType = formatTypeList[iAt]

                if formatType == "FT_UNQUOTED_STRING" or formatType == "FT_NULL_VALUE":
                    val = myCategory.getValueFormattedByIndex(iAt, iRow)
                    lineList.append(val)

                elif formatType == "FT_NUMBER":
                    val = myCategory.getValueFormattedByIndex(iAt, iRow)
                    lineList.append(val)

                elif formatType == "FT_QUOTED_STRING":
                    val = myCategory.getValueFormattedByIndex(iAt, iRow)
                    lineList.append(val)

                elif formatType == "FT_MULTI_LINE_STRING":
                    val = myCategory.getValueFormattedByIndex(iAt, iRow)
                    lineList.append(val)

                lineList.append(spacing)

            self.__write("".join(lineList))
        self.__write("\n")
        if self.__useStopTokens:
            self.__write("stop_\n")
