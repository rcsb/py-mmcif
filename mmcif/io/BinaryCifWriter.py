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

from mmcif.api.DataCategoryTyped import DataCategoryTyped, DataCategoryHints
from mmcif.api.PdbxContainers import CifName
from mmcif.io.BinaryCifReader import BinaryCifDecoders

logger = logging.getLogger(__name__)


class BinaryCifWriter(object):
    """Writer methods for the binary CIF format."""

    def __init__(
        self,
        dictionaryApi,
        storeStringsAsBytes=False,
        defaultStringEncoding="utf-8",
        applyTypes=True,
        useStringTypes=False,
        useFloat64=False,
        copyInputData=False,
        ignoreCastErrors=False,
        **kwargs
    ):
        """Create an instance of the binary CIF writer class.

        Args:
            dictionaryApi (object): DictionaryApi object instance
            storeStringsAsBytes (bool, optional): strings are stored as lists of bytes. Defaults to False.
            defaultStringEncoding (str, optional): default encoding for string data. Defaults to "utf-8".
            applyTypes (bool, optional): apply explicit data typing before encoding. Defaults to True.
            useStringTypes (bool, optional): assume all types are string. Defaults to False.
            useFloat64 (bool, optional): store floats with 64 bit precision. Defaults to False.
            copyInputData (bool, optional): make a new copy input data. Defaults to False.
            ignoreCastErrors (bool, optional): suppress errors when casting attribute types with dictionaryApi. Defaults to False.
            applyMolStarTypes: (bool, optional): If applyTypes is used, will use specific molstar hints. Defaults to True.
        """
        self.__version = "0.3.0"
        self.__storeStringsAsBytes = storeStringsAsBytes
        self.__defaultStringEncoding = defaultStringEncoding
        self.__applyTypes = applyTypes
        self.__useStringTypes = useStringTypes
        self.__useFloat64 = useFloat64
        self.__dApi = dictionaryApi
        self.__copyInputData = copyInputData
        self.__ignoreCastErrors = ignoreCastErrors
        self.__applyMolStarTypes = kwargs.get("applyMolStarTypes", True)
        self.__dch = DataCategoryHints()

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
                        cObj = DataCategoryTyped(cObj, dictionaryApi=self.__dApi, copyInputData=self.__copyInputData,
                                                 ignoreCastErrors=self.__ignoreCastErrors, applyMolStarTypes=self.__applyMolStarTypes)
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
        colMaskDict = None  # Use None when no mask and not {} - per Mol* implementation
        enc = BinaryCifEncoders(defaultStringEncoding=self.__defaultStringEncoding, storeStringsAsBytes=self.__storeStringsAsBytes, useFloat64=self.__useFloat64)
        #
        maskEncoderList = ["Delta", "RunLength", "IntegerPacking", "ByteArray"]
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
        # cifPrimitiveType = self.__dApi.getTypePrimitive(dObj.getName(), atName)
        if cifDataType is None:
            dataType = "string"
            if not self.__ignoreCastErrors:
                logger.warning("Undefined type for category %s attribute %s - Will treat as string", dObj.getName(), atName)
        else:
            dataType = self.__dch.getPdbxItemType(cifDataType)
            # dataType = "integer" if "int" in cifDataType else "float" if cifPrimitiveType == "numb" else "string"

        # Only if applying types, do we allow Mol* hints
        if self.__applyTypes and self.__applyMolStarTypes:
            nm = CifName().itemName(dObj.getName(), atName)
            if self.__dch.inMolStarIntHints(nm):
                dataType = "integer"

        return dataType


class TypedArray:
    """A typed array to include a data type with an array of data"""

    __slots = ["dtype", "data"]

    def __init__(self, data, dtype=None):
        self.data = data
        self.dtype = dtype

    def __repr__(self):
        return "<typed_array type %s data %s>" % (self.dtype, self.data)


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

    def __getDataType(self, colTypedDataList):
        """Returns type of data array - or 'integer_32' """
        if colTypedDataList.dtype:
            return colTypedDataList.dtype
        else:
            return "integer_32"

    def encode(self, colDataList, encodingTypeList, dataType):
        """Encode the data using the input list of encoding types returning encoded data and encoding instructions.

        Args:
            colDataList (list or TypedArray): input data to be encoded
            encodingTypeList (list): list of encoding types (ByteArray, Delta, or RunLength)
            dataType (string):  column input data type (string, integer, float)

        Returns:
            (list, list ): encoded data column, list of encoding instructions
        """
        encodingDictL = []

        legacy = False
        if type(colDataList) is list:
            colDataList = TypedArray(colDataList)
            legacy = True

        encDict = None
        for encType in encodingTypeList:
            if encType == "ByteArray":
                colDataList, encDict = self.byteArrayEncoderTyped(colDataList, dataType)
            elif encType == "Delta":
                colDataList, encDict = self.deltaEncoderTyped(colDataList)
            elif encType == "RunLength":
                colDataList, encDict = self.runLengthEncoderTyped(colDataList)
            elif encType == "IntegerPacking":
                colDataList, encDict = self.integerPackingEncoderTyped(colDataList)
            else:
                logger.info("unsupported encoding %r", encType)
            if encDict is not None:
                encodingDictL.append(encDict)
        if legacy:
            return colDataList.data, encodingDictL
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
        raise TypeError("Cannot determine integer packing type")

    def byteArrayEncoder(self, colDataList, dataType):
        """Encode integer or float list in a packed byte array.

        Args:
            data (list): list of integer or float data
            dataType (str): data type (integer|float)

        Returns:
            bytes: byte encoded packed data
        """
        colDataListTyped = TypedArray(colDataList)

        cList, encDict = self.byteArrayEncoderTyped(colDataListTyped, dataType)
        return cList.data, encDict

    def byteArrayEncoderTyped(self, colTypedDataList, dataType):
        """Encode integer or float list in a packed byte array.

        Args:
            data (TypedArray): list of integer or float data
            dataType (str): data type (integer|float)

        Returns:
            TypedArray: byte encoded packed data
        """
        if dataType == "float":
            byteArrayType = self.__bCifTypeCodeD["float_64"] if self.__useFloat64 else self.__bCifTypeCodeD["float_32"]
        else:
            byteArrayType = self.__getIntegerPackingType(colTypedDataList.data)
        encodingD = {self.__toBytes("kind"): self.__toBytes("ByteArray"), self.__toBytes("type"): byteArrayType}
        fmt = BinaryCifDecoders.bCifTypeD[BinaryCifDecoders.bCifCodeTypeD[byteArrayType]]["struct_format_code"]
        # Data are encoded little-endian '<'
        encodedData = struct.pack("<" + fmt * len(colTypedDataList.data), *colTypedDataList.data)
        encodedTypedData = TypedArray(encodedData)
        return encodedTypedData, encodingD

    def deltaEncoder(self, colDataList, minLen=40):
        """Encode an integer list as a list of consecutive differences.

        Args:
            colDataList (list): list of integer data
            minLen (int, optional): minimum list length to apply encoder. Defaults to 40.

        Returns:
            list: delta encoded integer list
        """
        colDataListTyped = TypedArray(colDataList)

        cList, encDict = self.deltaEncoderTyped(colDataListTyped, minLen)
        return cList.data, encDict

    def deltaEncoderTyped(self, colTypedDataList, minLen=40):
        """Encode an integer list as a list of consecutive differences.

        Args:
            colTypedDataList (list): list of integer data
            minLen (int, optional): minimum list length to apply encoder. Defaults to 40.

        Returns:
            TypedArray: delta encoded integer list (integer_8, integer_16, integer_32)
        """

        if colTypedDataList.dtype and colTypedDataList.dtype not in ["integer_8", "integer_16", "integer_32"]:
            raise TypeError("Only signed integer types can be encoded with delta encoder: %s" % colTypedDataList.dtype)

        if len(colTypedDataList.data) <= minLen:
            return colTypedDataList, None

        byteArrayType = self.__getDataType(colTypedDataList)
        encodingD = {self.__toBytes("kind"): self.__toBytes("Delta"), self.__toBytes("origin"): colTypedDataList.data[0], self.__toBytes("srcType"): self.__bCifTypeCodeD[byteArrayType]}
        encodedColDataList = [0] + [colTypedDataList.data[i] - colTypedDataList.data[i - 1] for i in range(1, len(colTypedDataList.data))]
        encodedTypedColDataList = TypedArray(encodedColDataList, byteArrayType)
        return encodedTypedColDataList, encodingD

    def runLengthEncoder(self, colDataList, minLen=40):
        """Encode an integer array as pairs of (value, number of repeats)

        Args:
            colDataList (list): list of integer data
            minLen (int, optional): minimum list length to apply encoder. Defaults to 40.

        Returns:
            list: runlength encoded integer list
        """
        colDataListTyped = TypedArray(colDataList)

        cList, encDict = self.runLengthEncoderTyped(colDataListTyped, minLen)
        return cList.data, encDict

    def runLengthEncoderTyped(self, colTypedDataList, minLen=40):
        """Encode an integer array as pairs of (value, number of repeats)

        Args:
            colTypedDataList (TypedArray): list of integer data (signed and unsigned 8/16/32 bit types)
            minLen (int, optional): minimum list length to apply encoder. Defaults to 40.

        Returns:
            TypedArray: runlength encoded integer list (integer_32)
        """

        if len(colTypedDataList.data) <= minLen:
            return colTypedDataList, None

        byteArrayType = "integer_32"
        encodingD = {self.__toBytes("kind"): self.__toBytes("RunLength"), self.__toBytes("srcType"): self.__bCifTypeCodeD[byteArrayType],
                     self.__toBytes("srcSize"): len(colTypedDataList.data)}
        encodedColDataList = []
        val = None
        repeat = 1
        for colVal in colTypedDataList.data:
            if colVal != val:
                if val is not None:
                    encodedColDataList.extend((val, repeat))
                val = colVal
                repeat = 1
            else:
                repeat += 1
        encodedColDataList.extend((val, repeat))
        # Check for any gains and possibly retreat
        if len(encodedColDataList) > len(colTypedDataList.data):
            return colTypedDataList, None
        else:
            encodedTypedColDataList = TypedArray(encodedColDataList, byteArrayType)
            return encodedTypedColDataList, encodingD

    def stringArrayMaskedEncoder(self, colDataList, colMaskList):
        """Encode the input data column (string) along with the incompleteness mask.

        Args:
            colDataList (list): input data column (string)
            colMaskList (list): incompleteness mask

        Returns:
            (list, list): encoded data column, list of encoding instructions
        """
        integerEncoderList = ["Delta", "RunLength", "IntegerPacking", "ByteArray"]
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
        integerEncoderList = ["Delta", "RunLength", "IntegerPacking", "ByteArray"]

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

    # Support for IntegerPacking
    def _determine_packing(self, colDataList):
        """Determines what the optimal IntegerPacking will be for a set of data.
        IntegerPacking allows for values above maximum by duplicating MaxV, so it is not simply based on the maximum value.

        Return information on data length and bytes per element.

        """

        def packing_size_signed(colDataList, upper_limit):
            """For signed data, determine packing with upper_limit, allowing repeats of max_val"""
            lower_limit = -upper_limit - 1
            size = 0
            for colVal in colDataList:
                if colVal >= 0:
                    size += int(colVal / upper_limit)
                else:
                    size += int(colVal / lower_limit)
            return size + len(colDataList)

        def packing_size_unsigned(colDataList, upper_limit):
            """For unsigned data, determine packing with upper_limit, allowing repeats of max_val"""
            size = 0
            for colVal in colDataList:
                size += int(colVal / upper_limit)
            return size + len(colDataList)

        try:
            minV = min(colDataList)
            is_signed = True if minV < 0 else False

            size8 = packing_size_signed(colDataList, 0x7F) if is_signed else packing_size_unsigned(colDataList, 0xFF)
            size16 = packing_size_signed(colDataList, 0x7FFF) if is_signed else packing_size_unsigned(colDataList, 0xFFFF)
            dlen = len(colDataList)

            # Determine optimal packing
            if dlen * 4 < size16 * 2:
                size = dlen
                nbytes = 4

            elif size16 * 2 < size8:
                size = size16
                nbytes = 2

            else:
                size = size8
                nbytes = 1

            return {"size": size, "bytes": nbytes, "isSigned": is_signed}

        except Exception as e:
            logger.exception("Failing with %s", str(e))
        raise TypeError("Cannot determine integer packing type")

    def integerPackingEncoder(self, colDataList):
        """Encode a 32-bit integer array as 8-bit or 16-bit encoding

        Args:
            colDataList (list): list of integer data

        Returns:
            list: packed encoded 8-bit/16-bit integer list
        """
        colDataListTyped = TypedArray(colDataList)

        cList, encDict = self.integerPackingEncoderTyped(colDataListTyped)
        return cList.data, encDict

    def integerPackingEncoderTyped(self, colTypedDataList):
        """Encode a 32-bit integer array as 8-bit or 16-bit encoding

        Args:
            colTypedDataList (TypedArray): list of integer data (integer_32 required)

        Returns:
            TypedArray: packed encoded 8-bit/16-bit integer list
        """
        if colTypedDataList.dtype and colTypedDataList.dtype not in ["integer_32"]:
            raise TypeError("Only integer-32 can be encoded with delta encoder: %s" % colTypedDataList.dtype)

        packing = self._determine_packing(colTypedDataList.data)
        nbytes = packing["bytes"]
        isSigned = packing["isSigned"]

        if nbytes == 4:
            # We will not be packing
            return colTypedDataList, None

        encodingD = {self.__toBytes("kind"): self.__toBytes("IntegerPacking"), self.__toBytes("byteCount"): nbytes,
                     self.__toBytes("srcSize"): len(colTypedDataList.data), self.__toBytes("isUnsigned"): not isSigned}
        encodedColDataList = []

        if isSigned:
            upper_limit = 0x7F if nbytes == 1 else 0x7FFF
        else:
            upper_limit = 0xFF if nbytes == 1 else 0xFFFF

        lower_limit = -upper_limit - 1

        # Pack data
        for colVal in colTypedDataList.data:
            if colVal >= 0:
                while colVal >= upper_limit:
                    encodedColDataList.append(upper_limit)
                    colVal -= upper_limit
            else:
                while colVal <= lower_limit:
                    encodedColDataList.append(lower_limit)
                    colVal -= lower_limit

            encodedColDataList.append(colVal)

        byteArrayType = None  # Should never happen, but keep pylint happy. 4 bytes handled above
        if nbytes == 1:
            byteArrayType = "integer_8" if isSigned else "unsigned_integer_8"
        elif nbytes == 2:
            byteArrayType = "integer_16" if isSigned else "unsigned_integer_16"

        encodedTypedColDataList = TypedArray(encodedColDataList, byteArrayType)

        return encodedTypedColDataList, encodingD
