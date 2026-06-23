##
# File: BinaryCifWriter.py
# Date: 15-May-2021  jdw
#
# Write methods and encoders for BinaryCIF serialization.
#
# Float encoding updates:
# - FixedPoint support with IntegerPacking, RunLength, and Delta chains.
# - Column-specific chains for known high-volume float attributes.
# - Automatic selection of the smallest general FixedPoint chain.
# - StringArray fallback for high-precision floats that cannot use FixedPoint.
##

import logging
import struct
import msgpack
import math
import warnings

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
                        # Pass category/item names so float columns can use coordinate-specific hints
                        colMaskDict, encodedColDataList, encodingDictL = self.__encodeColumnData(colDataList, dataType, catName, atName)
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

    # Accept category/item names so encoder selection can use column-specific hints
    def __encodeColumnData(self, colDataList, dataType, catName=None, atName=None):
        colMaskDict = None  # Use None when no mask and not {} - per Mol* implementation
        enc = BinaryCifEncoders(defaultStringEncoding=self.__defaultStringEncoding, storeStringsAsBytes=self.__storeStringsAsBytes, useFloat64=self.__useFloat64)
        #
        maskEncoderList = ["RunLength", "ByteArray"]
        typeEncoderD = {"string": "StringArrayMasked", "integer": "IntArrayMasked", "float": "FloatArrayMasked"}
        colMaskList = enc.getMask(colDataList)
        dataEncType = typeEncoderD[dataType]
        # Forward category/item names to the masked encoder
        colDataEncoded, colDataEncodingDictL = enc.encodeWithMask(colDataList, colMaskList, dataEncType, catName=catName, atName=atName)
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


    # Float encoding feature switches
    #
    # The five individual switches below only apply when the switch is
    # True. Disabling an individual hard-code does not force ByteArray; it sends
    # that column through the general automatic FixedPoint chain selection.


    # True: enable the new FixedPoint-based float encoding logic and all enabled
    #       specialized paths below.
    # False: bypass every float optimization below and encode all floats directly
    #        with the original float ByteArray behavior.
    USE_FIXED_POINT_FLOAT_ENCODING = True

    # True: known coordinate columns use factor 1000 followed by
    #       Delta -> IntegerPacking -> ByteArray.
    # False: coordinates skip this hard-coded chain and use the general automatic
    #        factor detection and four-chain comparison instead.
    USE_COORDINATE_CHAIN = True


    # True: the six _atom_site_anisotrop U columns use factor 10000 followed by
    #       Delta -> IntegerPacking -> ByteArray.
    # False: those columns skip this hard-code and use the general float path.
    USE_ANISOTROP_U_CHAIN = True


    # True: _ihm_sphere_obj_site.object_radius uses factor 1000 followed by
    #       IntegerPacking -> ByteArray, without Delta or RunLength.
    # False: object_radius skips this hard-code and uses the general float path.
    USE_OBJECT_RADIUS_CHAIN = True


    # True: occupancy, B_iso_or_equiv, rmsf, and starting-model B_iso_or_equiv
    #       use an automatically detected factor followed by
    #       RunLength -> IntegerPacking -> ByteArray.
    # False: those four attributes skip the RunLength hint and use the general
    #        automatic factor detection and four-chain comparison.
    USE_RUN_LENGTH_FLOAT_HINTS = True


    # True: when no safe FixedPoint factor is found and a column contains values
    #       with 5 or more decimal places, encode it as StringArrayMasked.
    # False: those high-precision fallback columns use float ByteArray instead.
    USE_STRING_FLOAT_FALLBACK = False

    COORDINATE_FIXED_POINT_FACTOR = 1000


    ANISOTROP_U_FIXED_POINT_FACTOR = 10000
    OBJECT_RADIUS_FIXED_POINT_FACTOR = 1000
    MAX_FIXED_POINT_DECIMAL_PLACES = 4
    STRING_FALLBACK_MIN_DECIMAL_PLACES = 5
    FIXED_POINT_TOLERANCE = 1.0e-6

    COORDINATE_ITEMS = {
        # PDB / standard model coordinates
        "_atom_site.Cartn_x",
        "_atom_site.Cartn_y",
        "_atom_site.Cartn_z",

        # PDBx/mmCIF chemical component coordinates
        "_chem_comp_atom.model_Cartn_x",
        "_chem_comp_atom.model_Cartn_y",
        "_chem_comp_atom.model_Cartn_z",
        "_chem_comp_atom.pdbx_model_Cartn_x_ideal",
        "_chem_comp_atom.pdbx_model_Cartn_y_ideal",
        "_chem_comp_atom.pdbx_model_Cartn_z_ideal",

        # PDBx/mmCIF phasing-site coordinates
        "_phasing_MIR_der_site.Cartn_x",
        "_phasing_MIR_der_site.Cartn_y",
        "_phasing_MIR_der_site.Cartn_z",
        "_pdbx_phasing_MAD_set_site.Cartn_x",
        "_pdbx_phasing_MAD_set_site.Cartn_y",
        "_pdbx_phasing_MAD_set_site.Cartn_z",

        # PDBx/mmCIF solvent atom-site mapping coordinates
        "_pdbx_solvent_atom_site_mapping.Cartn_x",
        "_pdbx_solvent_atom_site_mapping.Cartn_y",
        "_pdbx_solvent_atom_site_mapping.Cartn_z",
        "_pdbx_solvent_atom_site_mapping.pre_Cartn_x",
        "_pdbx_solvent_atom_site_mapping.pre_Cartn_y",
        "_pdbx_solvent_atom_site_mapping.pre_Cartn_z",

        # ModelCIF / CSM template coordinates
        "_ma_template_coord.Cartn_x",
        "_ma_template_coord.Cartn_y",
        "_ma_template_coord.Cartn_z",

        # IHM coordinates
        "_ihm_starting_model_coord.Cartn_x",
        "_ihm_starting_model_coord.Cartn_y",
        "_ihm_starting_model_coord.Cartn_z",
        "_ihm_sphere_obj_site.Cartn_x",
        "_ihm_sphere_obj_site.Cartn_y",
        "_ihm_sphere_obj_site.Cartn_z",
        "_ihm_gaussian_obj_site.mean_Cartn_x",
        "_ihm_gaussian_obj_site.mean_Cartn_y",
        "_ihm_gaussian_obj_site.mean_Cartn_z",
        "_ihm_gaussian_obj_ensemble.mean_Cartn_x",
        "_ihm_gaussian_obj_ensemble.mean_Cartn_y",
        "_ihm_gaussian_obj_ensemble.mean_Cartn_z",
        "_ihm_pseudo_site.Cartn_x",
        "_ihm_pseudo_site.Cartn_y",
        "_ihm_pseudo_site.Cartn_z",

        # FLR / FPS coordinates
        "_flr_FPS_mean_probe_position.mpp_xcoord",
        "_flr_FPS_mean_probe_position.mpp_ycoord",
        "_flr_FPS_mean_probe_position.mpp_zcoord",
        "_flr_FPS_MPP_atom_position.xcoord",
        "_flr_FPS_MPP_atom_position.ycoord",
        "_flr_FPS_MPP_atom_position.zcoord",
    }

    ANISOTROP_U_ITEMS = {
        "_atom_site_anisotrop.U[1][1]",
        "_atom_site_anisotrop.U[1][2]",
        "_atom_site_anisotrop.U[1][3]",
        "_atom_site_anisotrop.U[2][2]",
        "_atom_site_anisotrop.U[2][3]",
        "_atom_site_anisotrop.U[3][3]",
    }

    RUN_LENGTH_FLOAT_ITEMS = {
        "_atom_site.occupancy",
        "_atom_site.B_iso_or_equiv",
        "_ihm_sphere_obj_site.rmsf",
        "_ihm_starting_model_coord.B_iso_or_equiv",
    }

    OBJECT_RADIUS_ITEM = "_ihm_sphere_obj_site.object_radius"

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
        # Track data type changes as chained encoders transform the array
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

    # Accept category/item names for float-column encoding decisions
    def encodeWithMask(self, colDataList, colMaskList, encodingType, catName=None, atName=None):
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
        # Pass category/item names only to the float encoder
        elif encodingType == "FloatArrayMasked":
            encodedColDataList, encodingDictL = self.floatArrayMaskedEncoder(colDataList, colMaskList, catName=catName, atName=atName)
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

    # Check whether the current column is one of the Cartesian coordinate columns
    # Check whether the current column is one of the known Cartesian coordinate columns
    def __isCoordinateItem(self, catName, atName):
        """Return True for a coordinate item that uses the factor-1000 hint."""
        return self.__getItemName(catName, atName) in self.COORDINATE_ITEMS

    def __getItemName(self, catName, atName):
        """Return normalized _category.attribute item name."""
        if catName is None or atName is None:
            return ""

        cat = str(catName)
        if cat.startswith("_"):
            cat = cat[1:]

        return "_%s.%s" % (cat, atName)

    def __isAnisotropUItem(self, catName, atName):
        """Return True for an anisotropic displacement U matrix item."""
        return self.__getItemName(catName, atName) in self.ANISOTROP_U_ITEMS

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

            if decimalPlaces >= self.STRING_FALLBACK_MIN_DECIMAL_PLACES:
                return True

        return False

    def __encodeFloatStringFallback(self, colDataList, colMaskList):
        """Encode a float fallback column as StringArrayMasked."""
        if colMaskList:
            stringColDataList = ["0.0" if m else str(d) for m, d in zip(colMaskList, colDataList)]
        else:
            stringColDataList = [str(d) for d in colDataList]

        return self.stringArrayMaskedEncoder(stringColDataList, colMaskList)


    # scan the column for needed precision (for other than harcoded columns)
    def __getFloatFixedPointFactor(self, colDataList, catName=None, atName=None):
        """Return the smallest exact-enough FixedPoint factor for a float column."""
        if self.__isCoordinateItem(catName, atName):
            return self.COORDINATE_FIXED_POINT_FACTOR

        mantissaDigits = 0
        for val in colDataList:
            value = float(val)
            if not math.isfinite(value):
                return None

            foundDigits = None
            factor = 1
            for digits in range(self.MAX_FIXED_POINT_DECIMAL_PLACES + 1):
                scaledValue = factor * value
                if abs(round(scaledValue) - scaledValue) <= self.FIXED_POINT_TOLERANCE:
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

        best = None
        for encoderList in candidateEncoderLists:
            try:
                encodedColDataList, encodingDictL = self.encode(list(colDataList), encoderList, "float")
                encodedData = encodedColDataList.data if isinstance(encodedColDataList, TypedArray) else encodedColDataList
                size = len(encodedData)

                if best is None or size < best[0]:
                    best = (size, encodedColDataList, encodingDictL)
            except Exception as e:
                logger.debug("Skipping float encoder chain %r: %s", encoderList, str(e))

        if best is None:
            return None, None

        return best[1], best[2]





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
        """Run one FixedPoint chain, falling back to float ByteArray when unsafe."""
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

    def floatArrayMaskedEncoder(self, colDataList, colMaskList, catName=None, atName=None):
        """Encode a float column, preserving its incompleteness mask."""
        if colMaskList:
            maskedColDataList = [0.0 if m else d for m, d in zip(colMaskList, colDataList)]
        else:
            maskedColDataList = colDataList

        fallbackEncoderList = ["ByteArray"]
        if not self.USE_FIXED_POINT_FLOAT_ENCODING:
            return self.encode(maskedColDataList, fallbackEncoderList, "float")

        itemName = self.__getItemName(catName, atName)

        # Known coordinate columns: factor 1000 + Delta.
        if self.USE_COORDINATE_CHAIN and self.__isCoordinateItem(catName, atName):
            factor = self.COORDINATE_FIXED_POINT_FACTOR
            encoderList = [("FixedPoint", factor), "Delta", "IntegerPacking", "ByteArray"]
            return self.__encodeFixedPointChainOrFallback(maskedColDataList, factor, encoderList, itemName)

        # Anisotropic U columns: factor 10000 + Delta.
        if self.USE_ANISOTROP_U_CHAIN and self.__isAnisotropUItem(catName, atName):
            factor = self.ANISOTROP_U_FIXED_POINT_FACTOR
            encoderList = [("FixedPoint", factor), "Delta", "IntegerPacking", "ByteArray"]
            return self.__encodeFixedPointChainOrFallback(maskedColDataList, factor, encoderList, itemName)

        # IHM sphere radius: factor 1000 without Delta or RunLength.
        if self.USE_OBJECT_RADIUS_CHAIN and itemName == self.OBJECT_RADIUS_ITEM:
            factor = self.OBJECT_RADIUS_FIXED_POINT_FACTOR
            encoderList = [("FixedPoint", factor), "IntegerPacking", "ByteArray"]
            return self.__encodeFixedPointChainOrFallback(maskedColDataList, factor, encoderList, itemName)

        # Repeated high-volume float items: automatic factor + RunLength.
        if self.USE_RUN_LENGTH_FLOAT_HINTS and itemName in self.RUN_LENGTH_FLOAT_ITEMS:
            factor = self.__getFloatFixedPointFactor(maskedColDataList, catName=catName, atName=atName)
            if factor is None:
                if self.USE_STRING_FLOAT_FALLBACK and self.__shouldUseStringFallbackForFloat(maskedColDataList):
                    return self.__encodeFloatStringFallback(colDataList, colMaskList)
                return self.encode(maskedColDataList, fallbackEncoderList, "float")

            encoderList = [("FixedPoint", factor), "RunLength", "IntegerPacking", "ByteArray"]
            return self.__encodeFixedPointChainOrFallback(maskedColDataList, factor, encoderList, itemName)

        # General floats: detect a factor and choose the smallest of four chains.
        factor = self.__getFloatFixedPointFactor(maskedColDataList, catName=catName, atName=atName)
        if factor is None:
            if self.USE_STRING_FLOAT_FALLBACK and self.__shouldUseStringFallbackForFloat(maskedColDataList):
                return self.__encodeFloatStringFallback(colDataList, colMaskList)
            return self.encode(maskedColDataList, fallbackEncoderList, "float")

        fixedPointValues = [self.__roundLikeMolStar(float(v) * factor) for v in maskedColDataList]
        if not self.__fitsInt32(fixedPointValues):
            return self.encode(maskedColDataList, fallbackEncoderList, "float")

        encodedColDataList, encodingDictL = self.__encodeBestFixedPointChain(maskedColDataList, factor)
        if encodedColDataList is None:
            return self.encode(maskedColDataList, fallbackEncoderList, "float")

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
