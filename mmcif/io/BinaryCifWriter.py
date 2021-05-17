##
# File: BinaryCifWrite.py
# Date: 15-May-2021  jdw
#
#  Write methods and encoders for binary CIF serialization.
#
#  Updates:
#
##

import logging
import struct
import msgpack

from mmcif.api.DataCategoryTyped import DataCategoryTyped
from mmcif.io.BinaryCifReader import BinaryCifDecoders

logger = logging.getLogger(__name__)


class BinaryCifWriter(object):
    """Writer methods for the binary CIF format."""

    def __init__(self, dictionaryApi, storeStringsAsBytes=False, defaultStringEncoding="utf-8", applyTypes=True, useStringTypes=False, useFloat64=False):
        """Create an instance of the binary CIF writer class.

        Args:
            dictionaryApi (object): DictionaryApi object instance
            storeStringsAsBytes (bool, optional): strings are stored as lists of bytes. Defaults to False.
            defaultStringEncoding (str, optional): default encoding for string data. Defaults to "utf-8".
            applyTypes (bool, optional): apply explicit data typing before encoding. Defaults to True.
            useStringTypes (bool, optional): assume all types are string. Defaults to False.
            useFloat64 (bool, optional): store floats with 64 bit precision. Defaults to False.
        """
        self.__version = "0.01"
        self.__storeStringsAsBytes = storeStringsAsBytes
        self.__defaultStringEncoding = defaultStringEncoding
        self.__applyTypes = applyTypes
        self.__useStringTypes = useStringTypes
        self.__useFloat64 = useFloat64
        self.__dApi = dictionaryApi

    def serialize(self, filePath, containerList):
        """Serialize the input container list in binary CIF and store these data in the input file path.

        Args:
            filePath (str): output file path
            containerList (list): list of DataContainer objects
        """
        try:
            blocks = []
            for container in containerList:
                name = container.getName()
                block = {self.__toBytes("header"): self.__toBytes(name), self.__toBytes("categories"): []}
                categories = block[self.__toBytes("categories")]
                blocks.append(block)
                for catName in container.getObjNameList():
                    cObj = container.getObj(catName)
                    if self.__applyTypes:
                        cObj = DataCategoryTyped(cObj, dictionaryApi=self.__dApi, copyInputData=False)
                    #
                    rowCount = cObj.getRowCount()
                    #
                    cols = []
                    for ii, atName in enumerate(cObj.getAttributeList()):
                        colDataList = cObj.getColumn(ii)
                        dataType = self.__getAttributeType(cObj, atName) if not self.__useStringTypes else "string"
                        logger.debug("catName %r atName %r dataType %r", catName, atName, dataType)
                        colMaskDict, encodedColDataList, encodingDictL = self.__encodeColumnData(colDataList, dataType)
                        cols.append(
                            {
                                self.__toBytes("name"): self.__toBytes(atName),
                                self.__toBytes("mask"): colMaskDict,
                                self.__toBytes("data"): {self.__toBytes("data"): encodedColDataList, self.__toBytes("encoding"): encodingDictL},
                            }
                        )
                    categories.append({self.__toBytes("name"): self.__toBytes("_" + catName), self.__toBytes("columns"): cols, self.__toBytes("rowCount"): rowCount})
            #
            data = {
                self.__toBytes("version"): self.__toBytes(self.__version),
                self.__toBytes("encoder"): self.__toBytes("python-mmcif library"),
                self.__toBytes("dataBlocks"): blocks,
            }
            with open(filePath, "wb") as ofh:
                msgpack.pack(data, ofh)
            return True
        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return False

    def __encodeColumnData(self, colDataList, dataType):
        colMaskDict = {}
        enc = BinaryCifEncoders(defaultStringEncoding=self.__defaultStringEncoding, storeStringsAsBytes=self.__storeStringsAsBytes, useFloat64=self.__useFloat64)
        #
        maskEncoderList = ["Delta", "RunLength", "ByteArray"]
        typeEncoderD = {"string": "StringArrayMasked", "integer": "IntArrayMasked", "float": "FloatArrayMasked"}
        colMaskList = enc.getMask(colDataList)
        dataEncType = typeEncoderD[dataType]
        colDataEncoded, colDataEncodingDictL = enc.encodeWithMask(colDataList, colMaskList, dataEncType)
        if colMaskList:
            maskEncoded, maskEncodingDictL = enc.encode(colMaskList, maskEncoderList, "integer")
            colMaskDict = {self.__toBytes("data"): maskEncoded, self.__toBytes("encoding"): maskEncodingDictL}
        return colMaskDict, colDataEncoded, colDataEncodingDictL

    def __toBytes(self, strVal):
        """Optional conversion of the input string to bytes according to the class setting (storeStringsAsBytes).

        Args:
            strVal (string): input string

        Returns:
            string or bytes: optionally converted string.
        """
        try:
            return strVal.encode(self.__defaultStringEncoding) if self.__storeStringsAsBytes else strVal
        except (UnicodeDecodeError, AttributeError):
            logger.exception("Bad type for %r", strVal)
        return strVal

    def __getAttributeType(self, dObj, atName):
        """Get attribute data type (string, integer, or float) and optionality

        Args:
            atName (str): attribute name

        Returns:
            (string): data type (string, integer or float)
        """
        cifDataType = self.__dApi.getTypeCode(dObj.getName(), atName)
        cifPrimitiveType = self.__dApi.getTypePrimitive(dObj.getName(), atName)
        dataType = "integer" if "int" in cifDataType else "float" if cifPrimitiveType == "numb" else "string"
        return dataType


class BinaryCifEncoders(object):
    """Column oriented Binary CIF encoders implementing
    StringArray, ByteArray, IntegerPacking, Delta, RunLength,
    and FixedPoint encoders from the BinaryCIF specification described in:

    Sehnal D, Bittrich S, Velankar S, Koca J, Svobodova R, Burley SK, Rose AS.
    BinaryCIF and CIFTools-Lightweight, efficient and extensible macromolecular data management.
    PLoS Comput Biol. 2020 Oct 19;16(10):e1008247.
    doi: 10.1371/journal.pcbi.1008247. PMID: 33075050; PMCID: PMC7595629.

    and in the specification at https://github.com/molstar/BinaryCIF/blob/master/encoding.md

    and from the I/HM Python implementation at https://github.com/ihmwg/python-ihm

    """

    def __init__(self, defaultStringEncoding="utf-8", storeStringsAsBytes=True, useFloat64=False):
        """Instantiate the binary CIF encoder class.

        Args:
            defaultStringEncoding (str, optional): default encoding for string data . Defaults to "utf-8".
            storeStringsAsBytes (bool, optional): strings are stored as bytes. Defaults to True.
            useFloat64 (bool, optional): store floats in 64 bit precision. Defaults to True.
        """
        self.__unknown = [".", "?"]
        self.__defaultStringEncoding = defaultStringEncoding
        self.__storeStringsAsBytes = storeStringsAsBytes
        self.__useFloat64 = useFloat64
        self.__bCifTypeCodeD = {v: k for k, v in BinaryCifDecoders.bCifCodeTypeD.items()}

    def encode(self, colDataList, encodingTypeList, dataType):
        """Encode the data using the input list of encoding types returning encoded data and encoding instructions.

        Args:
            colDataList (list): input data to be encoded
            encodingTypeList (list): list of encoding types (ByteArray, Delta, or RunLength)
            dataType (string):  column input data type (string, integer, float)

        Returns:
            (list, list ): encoded data column, list of encoding instructions
        """
        encodingDictL = []
        for encType in encodingTypeList:
            if encType == "ByteArray":
                colDataList, encDict = self.byteArrayEncoder(colDataList, dataType)
            elif encType == "Delta":
                colDataList, encDict = self.deltaEncoder(colDataList)
            elif encType == "RunLength":
                colDataList, encDict = self.runLengthEncoder(colDataList)
            else:
                logger.info("unsupported encoding %r", encType)
            if encDict is not None:
                encodingDictL.append(encDict)
        return colDataList, encodingDictL

    def encodeWithMask(self, colDataList, colMaskList, encodingType):
        """Encode the data using the input mask and encoding type returning encoded data and encoding instructions.

        Args:
            colDataList (string): input data column
            colMaskList (list): incompleteness mask for the input data column
            encodingType (string): encoding type to apply (StringArrayMask, IntArrayMasked, FloatArrayMasked)

        Returns:
            (list, list ): encoded data column, list of encoding instructions
        """
        encodedColDataList = []
        encodingDictL = []
        if encodingType == "StringArrayMasked":
            encodedColDataList, encodingDictL = self.stringArrayMaskedEncoder(colDataList, colMaskList)
        elif encodingType == "IntArrayMasked":
            encodedColDataList, encodingDictL = self.intArrayMaskedEncoder(colDataList, colMaskList)
        elif encodingType == "FloatArrayMasked":
            encodedColDataList, encodingDictL = self.floatArrayMaskedEncoder(colDataList, colMaskList)
        else:
            logger.info("unsupported masked encoding %r", encodingType)
        return encodedColDataList, encodingDictL

    def __getIntegerPackingType(self, colDataList):
        """Determine the integer packing type of the input integer data list"""
        try:
            minV = min(colDataList)
            maxV = max(colDataList)
            if minV >= 0:
                # Unsigned types
                for typeName in ["unsigned_integer_8", "unsigned_integer_16", "unsigned_integer_32"]:
                    byteArrayType = self.__bCifTypeCodeD[typeName]
                    upperLimit = BinaryCifDecoders.bCifTypeD[typeName]["max"]
                    if maxV <= upperLimit:
                        return byteArrayType
            else:
                # Signed types
                for typeName in ["integer_8", "integer_16", "integer_32"]:
                    byteArrayType = self.__bCifTypeCodeD[typeName]
                    upperLimit = BinaryCifDecoders.bCifTypeD[typeName]["max"]
                    lowerLimit = BinaryCifDecoders.bCifTypeD[typeName]["min"]
                    if minV >= lowerLimit and maxV <= upperLimit:
                        return byteArrayType
        except Exception as e:
            logger.exception("Failing with %s", str(e))
        raise TypeError("Cannot determine interger packing type")

    def byteArrayEncoder(self, colDataList, dataType):
        """Encode integer or float list in a packed byte array.

        Args:
            data (list): list of integer or float data
            dataType (str): data type (integer|float)

        Returns:
            bytes: byte encoded packed data
        """
        if dataType == "float":
            byteArrayType = self.__bCifTypeCodeD["float_64"] if self.__useFloat64 else self.__bCifTypeCodeD["float_32"]
        else:
            byteArrayType = self.__getIntegerPackingType(colDataList)
        encodingD = {self.__toBytes("kind"): self.__toBytes("ByteArray"), self.__toBytes("type"): byteArrayType}
        fmt = BinaryCifDecoders.bCifTypeD[BinaryCifDecoders.bCifCodeTypeD[byteArrayType]]["struct_format_code"]
        # Data are encoded little-endian '<'
        return struct.pack("<" + fmt * len(colDataList), *colDataList), encodingD

    def deltaEncoder(self, colDataList, minLen=40):
        """Encode an integer list as a list of consecutive differences.

        Args:
            colDataList (list): list of integer data
            minLen (int, optional): minimum list length to apply encoder. Defaults to 40.

        Returns:
            list: delta encoded integer list
        """
        if len(colDataList) <= minLen:
            return colDataList, None
        byteArrayType = self.__getIntegerPackingType(colDataList)
        encodingD = {self.__toBytes("kind"): self.__toBytes("Delta"), self.__toBytes("origin"): colDataList[0], self.__toBytes("srcType"): byteArrayType}
        encodedColDataList = [0] + [colDataList[i] - colDataList[i - 1] for i in range(1, len(colDataList))]
        return encodedColDataList, encodingD

    def runLengthEncoder(self, colDataList, minLen=40):
        """Encode an integer array as pairs of (value, number of repeats)

        Args:
            colDataList (list): list of integer data
            minLen (int, optional): minimum list length to apply encoder. Defaults to 40.

        Returns:
            list: runlength encoded integer list
        """

        if len(colDataList) <= minLen:
            return colDataList, None
        byteArrayType = self.__getIntegerPackingType(colDataList)
        encodingD = {self.__toBytes("kind"): self.__toBytes("RunLength"), self.__toBytes("srcType"): byteArrayType, self.__toBytes("srcSize"): len(colDataList)}
        encodedColDataList = []
        val = None
        repeat = 1
        for colVal in colDataList:
            if colVal != val:
                if val is not None:
                    encodedColDataList.extend((val, repeat))
                val = colVal
                repeat = 1
            else:
                repeat += 1
        encodedColDataList.extend((val, repeat))
        # Check for any gains and possibly retreat
        if len(encodedColDataList) > len(colDataList):
            return colDataList, None
        else:
            return encodedColDataList, encodingD

    def stringArrayMaskedEncoder(self, colDataList, colMaskList):
        """Encode the input data column (string) along with the incompleteness mask.

        Args:
            colDataList (list): input data column (string)
            colMaskList (list): incompleteness mask

        Returns:
            (list, list): encoded data column, list of encoding instructions
        """
        integerEncoderList = ["Delta", "RunLength", "ByteArray"]
        uniqStringIndex = {}  # keys are substrings, values indices
        uniqStringList = []
        indexList = []
        for i, strVal in enumerate(colDataList):
            if colMaskList is not None and colMaskList[i]:
                indexList.append(-1)
            else:
                tS = strVal
                tS = str(tS)
                if tS not in uniqStringIndex:
                    uniqStringIndex[tS] = len(uniqStringIndex)
                    uniqStringList.append(tS)
                indexList.append(uniqStringIndex[tS])
        offsetList = [0]
        runningLen = 0
        for tS in uniqStringList:
            runningLen += len(tS)
            offsetList.append(runningLen)

        encodedOffsetList, offsetEncodingDictL = self.encode(offsetList, integerEncoderList, "integer")
        encodedIndexList, indexEncodingDictL = self.encode(indexList, integerEncoderList, "integer")

        encodingDict = {
            self.__toBytes("kind"): self.__toBytes("StringArray"),
            self.__toBytes("dataEncoding"): indexEncodingDictL,
            self.__toBytes("stringData"): self.__toBytes("".join(uniqStringList)),
            self.__toBytes("offsetEncoding"): offsetEncodingDictL,
            self.__toBytes("offsets"): encodedOffsetList,
        }
        return encodedIndexList, [encodingDict]

    def intArrayMaskedEncoder(self, colDataList, colMaskList):
        """Encode the input data column (integer) along with the incompleteness mask.

        Args:
            colDataList (list): input data column (string)
            colMaskList (list): incompleteness mask

        Returns:
            (list, list): encoded data column, list of encoding instructions
        """
        integerEncoderList = ["Delta", "RunLength", "ByteArray"]

        if colMaskList:
            maskedColDataList = [-1 if m else d for m, d in zip(colMaskList, colDataList)]
        else:
            maskedColDataList = colDataList
        encodedColDataList, encodingDictL = self.encode(maskedColDataList, integerEncoderList, "integer")
        return encodedColDataList, encodingDictL

    def floatArrayMaskedEncoder(self, colDataList, colMaskList):
        """Encode the input data column (float) along with the incompleteness mask.

        Args:
            colDataList (list): input data column (string)
            colMaskList (list): incompleteness mask

        Returns:
            (list, list): encoded data column, list of encoding instructions
        """
        floatEncoderList = ["ByteArray"]

        if colMaskList:
            maskedColDataList = [0.0 if m else d for m, d in zip(colMaskList, colDataList)]
        else:
            maskedColDataList = colDataList
        encodedColDataList, encodingDictL = self.encode(maskedColDataList, floatEncoderList, "float")
        return encodedColDataList, encodingDictL

    def getMask(self, colDataList):
        """Create an incompleteness mask list identifying missing/omitted values in the input data column.
        The mask is assigned: 0 = Value is present, 1 = '.' (value not specified), and 2 = '?' (value unknown).

        Args:
            colDataList (list): input data column

        Returns:
            list or None: mask list or None if the column contains no missing values
        """
        mask = None
        for ii, colVal in enumerate(colDataList):
            if colVal is not None and colVal not in self.__unknown:
                continue
            if not mask:
                mask = [0] * len(colDataList)
            mask[ii] = 2 if colVal is None or colVal == "?" else 1
        return mask

    def __toBytes(self, strVal):
        """Optional conversion of the input string to bytes according to the class setting (storeStringsAsBytes).

        Args:
            strVal (string): input string

        Returns:
            string or bytes: optionally converted string.
        """
        try:
            return strVal.encode(self.__defaultStringEncoding) if self.__storeStringsAsBytes else strVal
        except (UnicodeDecodeError, AttributeError):
            logger.exception("Bad type for %r", strVal)
        return strVal
