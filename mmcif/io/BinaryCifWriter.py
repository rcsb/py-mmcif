##
# File: BinaryCifWriter.py
# Date: 15-May-2021  jdw
#
# Write methods and encoders for BinaryCIF serialization.
#
#  Updates:
#   10-Jul-2026 ha
#   - dictionaryApi type resolution replaced with auto-detection via
#     bcif_type_detector.classify_column().
#   - dictionaryApi parameter is now optional (defaults to None).
#     If None, auto-detection is used for all columns.
#     If supplied, it is used only as a fallback for all-sentinel/empty columns.
#   - DataCategoryTyped pre-casting is skipped when dictionaryApi is None.
#   - __encodeColumnData() casts raw string values to int/float before encoding.
#   - __getAttributeType() uses classify_column() as primary type resolver.
#   - _FORCE_STRING_ATTRS overrides auto-detection for char-typed attributes
#     that look numeric (e.g. _audit_conform.dict_version = "5.281").
#
#   15-Jul-2026 ym
#   - Added FixedPoint float encoding with IntegerPacking, RunLength, and Delta
#     chains.
#   - Added configurable item-specific float encoding and automatic selection
#     of the smallest general FixedPoint chain.
#   - Moved BinaryCIF float-encoding configuration to mmcif.io.config.
#   - Added optional StringArray fallback for high-precision floats, disabled
#     by default.
##

import logging
import struct
import msgpack
import math
import warnings

from mmcif.api.DataCategoryTyped import DataCategoryTyped, DataCategoryHints
from mmcif.api.PdbxContainers import CifName
from mmcif.io.BinaryCifReader import BinaryCifDecoders
from mmcif.io.config import BCIF_CONFIG, canonical_item_name, get_forced_type

from mmcif.io.bcif_type_detector import classify_column

logger = logging.getLogger(__name__)


class BinaryCifWriter(object):
    """Writer methods for the binary CIF format."""

    def __init__(
        self,
        dictionaryApi=None,
        useAutoDetect=True,
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
            dictionaryApi (object, optional): DictionaryApi object instance.
                Required for dictionary-driven typing. In auto-detect mode it is
                optional and, when supplied, is used only as a fallback for
                empty/all-sentinel columns. Defaults to None.
            useAutoDetect (bool, optional): Infer column types from values instead
                of resolving every type through dictionaryApi. Defaults to True.
                Set False to preserve the original dictionary-driven behavior.
            storeStringsAsBytes (bool, optional): strings are stored as lists of bytes. Defaults to False.
            defaultStringEncoding (str, optional): default encoding for string data. Defaults to "utf-8".
            applyTypes (bool, optional): apply explicit data typing before encoding.
                Only has effect when dictionaryApi is also supplied (pre-casting
                requires the dictionary). Defaults to True.
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
        self.__useAutoDetect = useAutoDetect
        self.__copyInputData = copyInputData
        self.__ignoreCastErrors = ignoreCastErrors
        self.__applyMolStarTypes = kwargs.get("applyMolStarTypes", True)
        self.__dch = DataCategoryHints()

        if not self.__useAutoDetect and self.__dApi is None:
            raise ValueError("dictionaryApi is required when useAutoDetect is False")

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
                    # DataCategoryTyped pre-casting is only applied when a
                    # dictionaryApi is available — auto-detection works on raw
                    # string values and does not require pre-casting.
                    if not self.__useAutoDetect and self.__applyTypes:
                        cObj = DataCategoryTyped(cObj, dictionaryApi=self.__dApi, copyInputData=self.__copyInputData,
                                                 ignoreCastErrors=self.__ignoreCastErrors, applyMolStarTypes=self.__applyMolStarTypes)
                    #
                    rowCount = cObj.getRowCount()
                    #
                    cols = []
                    for ii, atName in enumerate(cObj.getAttributeList()):
                        colDataList = cObj.getColumn(ii)
                        itemName = canonical_item_name(catName, atName)
                        dataType = self.__getAttributeType(catName, atName, itemName, colDataList) if not self.__useStringTypes else "string"

                        logger.debug("itemName %r dataType %r", itemName, dataType)
                        colMaskDict, encodedColDataList, encodingDictL = self.__encodeColumnData(
                            colDataList, dataType, itemName
                        )
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

    # Accept the canonical item name so encoding policy is resolved only once.
    def __encodeColumnData(self, colDataList, dataType, itemName=""):
        colMaskDict = None  # Use None when no mask and not {} - per Mol* implementation
        enc = BinaryCifEncoders(defaultStringEncoding=self.__defaultStringEncoding, storeStringsAsBytes=self.__storeStringsAsBytes, useFloat64=self.__useFloat64)
        #
        maskEncoderList = ["RunLength", "ByteArray"]
        typeEncoderD = {"string": "StringArrayMasked", "integer": "IntArrayMasked", "float": "FloatArrayMasked"}
        colMaskList = enc.getMask(colDataList)

        # When no DataCategoryTyped pre-casting was applied (dApi is None),
        # column values arrive as raw strings. The integer and float encoders
        # call struct.pack which requires actual int/float Python objects.
        # Cast here using the dataType already determined by __getAttributeType.
        # Sentinel values (".", "?", None) are left untouched so getMask()
        # results remain valid.
        _SENTINELS = {".", "?"}
        if self.__useAutoDetect and dataType == "integer":
            colDataList = [
                v if (v is None or v in _SENTINELS)
                else (v if isinstance(v, int) else int(v))
                for v in colDataList
            ]
        elif self.__useAutoDetect and dataType == "float":
            colDataList = [
                v if (v is None or v in _SENTINELS)
                else (v if isinstance(v, float) else float(v))
                for v in colDataList
            ]

        dataEncType = typeEncoderD[dataType]
        # Forward category/item names to the masked encoder
        colDataEncoded, colDataEncodingDictL = enc.encodeWithMask(colDataList, colMaskList, dataEncType, itemName=itemName)
        if colMaskList:
            # Mol* indicates that masks should be encoded as if uint_8
            colMaskListTyped = TypedArray(colMaskList, "unsigned_integer_8")
            maskEncoded, maskEncodingDictL = enc.encode(colMaskListTyped, maskEncoderList, "integer")
            colMaskDict = {self.__toBytes("data"): maskEncoded.data, self.__toBytes("encoding"): maskEncodingDictL}
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


    def __getAttributeType(self, catName, atName, itemName, colDataList):
        """Resolve a column type without changing either legacy path.

        Dictionary mode reproduces the original BinaryCifWriter behavior.
        Auto-detect mode applies forced types first, then scans the values, and
        optionally uses dictionaryApi only for empty/all-sentinel columns.
        """
        if not self.__useAutoDetect:
            cifDataType = self.__dApi.getTypeCode(catName, atName)
            if cifDataType is None:
                dataType = "string"
                if not self.__ignoreCastErrors:
                    logger.warning(
                        "Undefined type for category %s attribute %s - Will treat as string",
                        catName,
                        atName,
                    )
            else:
                dataType = self.__dch.getPdbxItemType(cifDataType)

            # Mol* integer hints apply only to the dictionary-driven path.
            # Auto-detect mode resolves configured integer policy before
            # falling back to schema-less classification.
            if self.__applyTypes and self.__applyMolStarTypes:
                nm = CifName().itemName(catName, atName)
                if self.__dch.inMolStarIntHints(nm):
                    dataType = "integer"

        else:
            forcedType = get_forced_type(itemName)
            if forcedType is not None:
                logger.debug(
                    "Forced type override applied for %s.%s -> %s",
                    catName,
                    atName,
                    forcedType,
                )
                dataType = forcedType
            else:
                profile = classify_column(colDataList)
                typeMap = {"int": "integer", "float": "float", "str": "string"}
                dataType = typeMap[profile.col_type]

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
        # Chained encoders can change the array's data type. FixedPoint converts
        # float values to integer_32 values, so a later ByteArray step must encode
        # the current integer type rather than the original float input type.
        currentDataType = dataType
        for encType in encodingTypeList:
            encArg = None
            # Allow encoders with parameters, e.g. ("FixedPoint", factor)
            if isinstance(encType, tuple):
                encType, encArg = encType

            if encType == "ByteArray":
                colDataList, encDict = self.byteArrayEncoderTyped(colDataList, currentDataType)
            # FixedPoint converts float values into integer_32 values
            elif encType == "FixedPoint":
                colDataList, encDict = self.fixedPointEncoderTyped(colDataList, encArg)
                currentDataType = "integer"
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

    # Accept a canonical item name while retaining category/item compatibility.
    def encodeWithMask(self, colDataList, colMaskList, encodingType, catName=None, atName=None, itemName=None):
        """Encode the data using the input mask and encoding type returning encoded data and encoding instructions.

        Args:
            colDataList (list): input data column
            colMaskList (list): incompleteness mask for the input data column
            encodingType (string): encoding type to apply
                (StringArrayMasked, IntArrayMasked, FloatArrayMasked)
            catName (str, optional): category name retained for compatibility.
            atName (str, optional): attribute name retained for compatibility.
            itemName (str, optional): canonical item name used for configured
                float encoding decisions.

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
            if itemName is None:
                itemName = canonical_item_name(catName, atName)
            encodedColDataList, encodingDictL = self.floatArrayMaskedEncoder(colDataList, colMaskList, itemName=itemName)
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
        warnings.warn("byteArrayEncode should be replaced with typed encoder.  This will be removed in 2026.", DeprecationWarning)
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
            if colTypedDataList.dtype:
                byteArrayType = self.__bCifTypeCodeD[colTypedDataList.dtype]
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
        warnings.warn("deltaEncoder should be replaced with typed encoder.  This will be removed in 2026.", DeprecationWarning)
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
        warnings.warn("runLengthEncoder should be replaced with typed encoder.  This will be removed in 2026.", DeprecationWarning)

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

        srcType = self.__getDataType(colTypedDataList)

        encodingD = {self.__toBytes("kind"): self.__toBytes("RunLength"), self.__toBytes("srcType"): self.__bCifTypeCodeD[srcType],
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
            encodedTypedColDataList = TypedArray(encodedColDataList, "integer_32")
            return encodedTypedColDataList, encodingD

    # Convert scaled float values into integer_32 values for later integer encoders
    def fixedPointEncoderTyped(self, colTypedDataList, factor):
        """Encode a float array as a 32-bit integer array using FixedPoint.

        Args:
            colTypedDataList (TypedArray): list of float data (float_32 or float_64)
            factor (int): multiplier used to convert float values to integers

        Returns:
            TypedArray: fixed-point encoded integer list (integer_32)
            dict: binary CIF FixedPoint encoding instructions

        Raises:
            TypeError: if the input is not a float array or the scaled
                FixedPoint values cannot be represented as signed integer_32.
        """
        if colTypedDataList.dtype and colTypedDataList.dtype not in ["float_32", "float_64"]:
            raise TypeError("Only float arrays can be encoded with FixedPoint: %s" % colTypedDataList.dtype)

        srcType = colTypedDataList.dtype or ("float_64" if self.__useFloat64 else "float_32")
        encodedColDataList = [self.__roundLikeMolStar(float(v) * factor) for v in colTypedDataList.data]

        if not self.__fitsInt32(encodedColDataList):
            raise TypeError("FixedPoint output does not fit in integer_32")

        encodingD = {
            self.__toBytes("kind"): self.__toBytes("FixedPoint"),
            self.__toBytes("factor"): factor,
            self.__toBytes("srcType"): self.__bCifTypeCodeD[srcType],
        }
        return TypedArray(encodedColDataList, "integer_32"), encodingD

    # Match Mol* JavaScript rounding behavior during FixedPoint conversion
    def __roundLikeMolStar(self, value):
        """Round a float value using JavaScript Math.round-like behavior.

        Args:
            value (float): input float value

        Returns:
            int: rounded integer value
        """
        return int(math.floor(value + 0.5))

    # Ensure FixedPoint output can safely be stored as integer_32
    def __fitsInt32(self, data):
        """Check whether all input values fit in a signed 32-bit integer array.

        Args:
            data (list): list of integer values

        Returns:
            bool: True if all values fit in signed 32-bit integer range, otherwise False
        """
        return all(-2147483648 <= int(v) <= 2147483647 for v in data)

    def __shouldUseStringFallbackForFloat(self, colDataList):
        """Return True when the column requires high-precision float fallback."""
        for val in colDataList:
            if val is None:
                continue

            valueString = str(val).strip()
            if valueString in self.__unknown:
                continue

            if "e" in valueString.lower():
                decimalPlaces = 99
            elif "." in valueString:
                decimalPlaces = len(valueString.split(".", 1)[1].rstrip("0"))
            else:
                decimalPlaces = 0

            if decimalPlaces >= BCIF_CONFIG.STRING_FALLBACK_MIN_DECIMAL_PLACES:
                return True

        return False

    def __encodeFloatStringFallback(self, colDataList, colMaskList):
        """Encode a float fallback column as StringArrayMasked."""
        if colMaskList:
            stringColDataList = ["0.0" if m else str(d) for m, d in zip(colMaskList, colDataList)]
        else:
            stringColDataList = [str(d) for d in colDataList]

        return self.stringArrayMaskedEncoder(stringColDataList, colMaskList)

    # Scan the column for the precision needed by general float items.
    def __getFloatFixedPointFactor(self, colDataList):
        """Return the smallest exact-enough FixedPoint factor for a float column."""

        mantissaDigits = 0
        for val in colDataList:
            value = float(val)
            if not math.isfinite(value):
                return None

            foundDigits = None
            factor = 1
            for digits in range(BCIF_CONFIG.MAX_FIXED_POINT_DECIMAL_PLACES + 1):
                scaledValue = factor * value
                if abs(round(scaledValue) - scaledValue) <= BCIF_CONFIG.FIXED_POINT_TOLERANCE:
                    foundDigits = digits
                    break
                factor *= 10

            if foundDigits is None:
                return None

            mantissaDigits = max(mantissaDigits, foundDigits)

        return 10 ** mantissaDigits

    # Try each FixedPoint integer chain and keep the smallest byte output
    def __encodeBestFixedPointChain(self, colDataList, factor):
        """Try the four FixedPoint integer chains and return the smallest output."""
        candidateEncoderLists = [
            [("FixedPoint", factor), "IntegerPacking", "ByteArray"],
            [("FixedPoint", factor), "RunLength", "IntegerPacking", "ByteArray"],
            [("FixedPoint", factor), "Delta", "IntegerPacking", "ByteArray"],
            [("FixedPoint", factor), "Delta", "RunLength", "IntegerPacking", "ByteArray"],
        ]

        bestSize = None
        bestEncodedColDataList = None
        bestEncodingDictL = None
        for encoderList in candidateEncoderLists:
            try:
                encodedColDataList, encodingDictL = self.encode(list(colDataList), encoderList, "float")
                encodedData = encodedColDataList.data if isinstance(encodedColDataList, TypedArray) else encodedColDataList
                size = len(encodedData)

                if bestSize is None or size < bestSize:
                    bestSize = size
                    bestEncodedColDataList = encodedColDataList
                    bestEncodingDictL = encodingDictL
            except Exception as e:
                logger.debug("Skipping float encoder chain %r: %s", encoderList, str(e))

        if bestSize is None:
            return None, None

        return bestEncodedColDataList, bestEncodingDictL

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
            # Mol* and BinaryCif specification https://github.com/molstar/BinaryCIF/blob/master/encoding.md
            # indcates that masked (missing) data are encoded as 0
            maskedColDataList = [0 if m else d for m, d in zip(colMaskList, colDataList)]
        else:
            maskedColDataList = colDataList
        encodedColDataList, encodingDictL = self.encode(maskedColDataList, integerEncoderList, "integer")
        return encodedColDataList, encodingDictL

    # Encode float columns with FixedPoint chains instead of ByteArray-only when safe
    def __encodeFixedPointChainOrFallback(self, colDataList, factor, encoderList, itemName):
        """Run one FixedPoint chain, falling back to float ByteArray when FixedPoint is unsafe or the chain raises."""
        try:
            numericValues = [float(v) for v in colDataList]

            if not all(math.isfinite(v) for v in numericValues):
                return self.encode(colDataList, ["ByteArray"], "float")

            fixedPointValues = [
                self.__roundLikeMolStar(v * factor)
                for v in numericValues
            ]
            if not self.__fitsInt32(fixedPointValues):
                return self.encode(colDataList, ["ByteArray"], "float")

            return self.encode(colDataList, encoderList, "float")
        except Exception as e:
            logger.debug("Falling back from the fixed float chain for %s: %s", itemName, str(e))
            return self.encode(colDataList, ["ByteArray"], "float")

    def floatArrayMaskedEncoder(self, colDataList, colMaskList, catName=None, atName=None, itemName=None):
        """Encode a float column, preserving its incompleteness mask."""
        if colMaskList:
            maskedColDataList = [0.0 if m else d for m, d in zip(colMaskList, colDataList)]
        else:
            maskedColDataList = colDataList

        fallbackEncoderList = ["ByteArray"]
        if itemName is None:
            itemName = canonical_item_name(catName, atName)
        itemConfig = BCIF_CONFIG.get_float_item_config(itemName)

        # Forced float items with a fixed factor always use their configured
        # factor and encoder chain.
        if itemConfig is not None and itemConfig.factor is not None:
            factor = itemConfig.factor
            encoderList = BCIF_CONFIG.get_float_encoder_list(itemName)
            return self.__encodeFixedPointChainOrFallback(
                maskedColDataList,
                factor,
                encoderList,
                itemName,
            )

        # Configured auto-factor float items use their configured encoder chain.
        if itemConfig is not None and itemConfig.factor is None:
            factor = self.__getFloatFixedPointFactor(maskedColDataList)
            if factor is None:
                if (
                    BCIF_CONFIG.USE_STRING_FLOAT_FALLBACK
                    and self.__shouldUseStringFallbackForFloat(maskedColDataList)
                ):
                    return self.__encodeFloatStringFallback(colDataList, colMaskList)
                return self.encode(maskedColDataList, fallbackEncoderList, "float")

            encoderList = [
                ("FixedPoint", factor),
                *itemConfig.encoderList,
            ]
            return self.__encodeFixedPointChainOrFallback(
                maskedColDataList,
                factor,
                encoderList,
                itemName,
            )

        # General floats: auto-detect a safe FixedPoint factor.
        factor = self.__getFloatFixedPointFactor(maskedColDataList)
        if factor is None:  # no suitable FixedPoint factor was found; use a fallback encoding (string or bytearray)
            if (
                BCIF_CONFIG.USE_STRING_FLOAT_FALLBACK
                and self.__shouldUseStringFallbackForFloat(maskedColDataList)
            ):
                return self.__encodeFloatStringFallback(colDataList, colMaskList)
            # encode as byte array
            return self.encode(maskedColDataList, fallbackEncoderList, "float")

        if BCIF_CONFIG.COMPARE_ALL_FIXED_POINT_CHAINS:
            encodedColDataList, encodingDictL = self.__encodeBestFixedPointChain(
                maskedColDataList,
                factor,
            )
            if encodedColDataList is None:
                return self.encode(maskedColDataList, fallbackEncoderList, "float")
            return encodedColDataList, encodingDictL

        encoderList = [
            ("FixedPoint", factor),
            "Delta",
            "RunLength",
            "IntegerPacking",
            "ByteArray",
        ]
        return self.__encodeFixedPointChainOrFallback(
            maskedColDataList,
            factor,
            encoderList,
            itemName,
        )

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
        warnings.warn("integerPackingEncoder should be replaced with typed encoder.  This will be removed in 2026.", DeprecationWarning, 4)
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
            # no packing done, Int32 encoding will be used
            # We will not be packing - as already integer 32 on way in
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
