##
# File: config.py
# Date: 06-Jul-2026
#
# BinaryCIF domain policy and reusable encoding configuration.
#
##

from dataclasses import dataclass
from types import MappingProxyType
from typing import Optional, Tuple


MISSING_VALUE_TOKENS = frozenset({".", "?"})

FORCED_STRING_ITEMS = frozenset({
    "_audit_conform.dict_version",
    "_audit_conform.dict_location",
    "_audit_conform.dict_name",
    "_atom_site.group_PDB",
    "_atom_site.type_symbol",
    "_atom_site.label_atom_id",
    "_atom_site.label_comp_id",
    "_atom_site.label_asym_id",
    "_atom_site.auth_comp_id",
    "_atom_site.auth_asym_id",
    "_atom_site.auth_atom_id",
})

FORCED_INTEGER_ITEMS = frozenset({
    "_atom_site.id",
    "_atom_site.auth_seq_id",
    "_atom_site_anisotrop.id",
    "_atom_site.label_seq_id",
    "_atom_site.pdbx_PDB_model_num",
    "_pdbx_struct_mod_residue.auth_seq_id",
    "_struct_conf.beg_auth_seq_id",
    "_struct_conf.end_auth_seq_id",
    "_struct_conn.ptnr1_auth_seq_id",
    "_struct_conn.ptnr2_auth_seq_id",
    "_struct_sheet_range.beg_auth_seq_id",
    "_struct_sheet_range.end_auth_seq_id",
})

SUPPORTED_ENCODERS = frozenset({"FixedPoint", "Delta", "RunLength", "IntegerPacking", "ByteArray"})
DEFAULT_INTEGER_CHAIN = ("Delta", "RunLength", "IntegerPacking", "ByteArray")
MASK_ENCODING_CHAIN = ("RunLength", "ByteArray")
FLOAT_BYTE_ARRAY_FALLBACK_CHAIN = ("ByteArray",)
DEFAULT_FIXED_POINT_INTEGER_CHAIN = ("Delta", "RunLength", "IntegerPacking", "ByteArray")
FIXED_POINT_CANDIDATE_INTEGER_CHAINS = (
    ("IntegerPacking", "ByteArray"),
    ("RunLength", "IntegerPacking", "ByteArray"),
    ("Delta", "IntegerPacking", "ByteArray"),
    ("Delta", "RunLength", "IntegerPacking", "ByteArray"),
)


@dataclass(frozen=True)
class TypeDetectionConfig:
    """Immutable schema-less type-detection policy."""

    force_small_float_as_string: bool = True
    min_rows_to_classify_as_float: int = 3

    def __post_init__(self):
        if not isinstance(self.min_rows_to_classify_as_float, int) or isinstance(self.min_rows_to_classify_as_float, bool):
            raise TypeError("min_rows_to_classify_as_float must be an integer")
        if self.min_rows_to_classify_as_float < 1:
            raise ValueError("min_rows_to_classify_as_float must be positive")


# If True, a column that would otherwise classify as "float" is forced to
# "str" when it has fewer than MIN_ROWS_TO_CLASSIFY_AS_FLOAT present
# non-sentinel values.
#
# Keep enabled temporarily while policy is moved without changing behavior.
FORCE_SMALL_FLOAT_AS_STRING = True
MIN_ROWS_TO_CLASSIFY_AS_FLOAT = 3
TYPE_DETECTION_CONFIG = TypeDetectionConfig(
    force_small_float_as_string=FORCE_SMALL_FLOAT_AS_STRING,
    min_rows_to_classify_as_float=MIN_ROWS_TO_CLASSIFY_AS_FLOAT,
)


@dataclass(frozen=True, init=False)
class FloatEncodingConfig:
    """FixedPoint factor and immutable post-FixedPoint integer chain."""

    factor: Optional[int]
    integer_chain: Tuple[str, ...]

    def __init__(self, factor=1000, encoderList=None, integer_chain=None):
        chain = integer_chain if integer_chain is not None else encoderList
        chain = tuple(chain or ())
        if chain and chain[0] == "FixedPoint":
            chain = chain[1:]
        object.__setattr__(self, "factor", factor)
        object.__setattr__(self, "integer_chain", chain)

    @property
    def encoderList(self):
        """Compatibility alias for the immutable post-FixedPoint chain."""
        return self.integer_chain

    def get_float_encoder_list(self):
        """Return the full fixed-factor chain used by the current writer."""
        if self.factor is None:
            return None
        return (("FixedPoint", self.factor),) + self.integer_chain


class BinaryCifEncodingConfig:
    """Container for all BinaryCifWriter float-encoding configuration."""

    # -----------------------------------------------------------------------
    # Global float-encoding switches
    # -----------------------------------------------------------------------

    # True:  when no safe FixedPoint factor is found (general/undetected
    #        items only) and a column contains values with 5 or more decimal
    #        places, encode it as StringArrayMasked.
    # False: those high-precision fallback columns use float ByteArray
    #        instead.
    # NOTE: If set to True, the 'testSerialize' test will need to be updated.
    USE_STRING_FLOAT_FALLBACK = False
    STRING_FALLBACK_MIN_DECIMAL_PLACES = 5

    # True:  for general float items with a safe FixedPoint factor, compare all
    #        four supported integer encoding chains and use the smallest output.
    # False: use FixedPoint -> Delta -> RunLength -> IntegerPacking ->
    #        ByteArray directly without comparing alternative chains.
    COMPARE_ALL_FIXED_POINT_CHAINS = True

    # Used only for items that are NOT in FORCED_FLOAT_ITEMS (general
    # floats), or for a forced item whose factor is explicitly
    # set to None (auto-detect), when scanning the column to find the
    # smallest safe factor.
    MAX_FIXED_POINT_DECIMAL_PLACES = 4
    FIXED_POINT_TOLERANCE = 1.0e-6

    # -----------------------------------------------------------------------
    # Forced float data items
    # -----------------------------------------------------------------------
    #
    # Keys are full mmCIF item names, i.e. "_category.attribute".
    # Values are FloatEncodingConfig(factor, encoderList) instances. Every item
    # here is assumed to be a float.
    FLOAT_ITEM_CONFIGS = MappingProxyType({

        # ---- Cartesian coordinates: factor 1000, FixedPoint -> Delta -> IntegerPacking -> ByteArray ----
        # PDB / standard model coordinates
        "_atom_site.Cartn_x": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_atom_site.Cartn_y": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_atom_site.Cartn_z": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),

        # PDBx/mmCIF chemical component coordinates
        "_chem_comp_atom.model_Cartn_x": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_chem_comp_atom.model_Cartn_y": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_chem_comp_atom.model_Cartn_z": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_chem_comp_atom.pdbx_model_Cartn_x_ideal": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_chem_comp_atom.pdbx_model_Cartn_y_ideal": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_chem_comp_atom.pdbx_model_Cartn_z_ideal": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),

        # PDBx/mmCIF phasing-site coordinates
        "_phasing_MIR_der_site.Cartn_x": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_phasing_MIR_der_site.Cartn_y": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_phasing_MIR_der_site.Cartn_z": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_pdbx_phasing_MAD_set_site.Cartn_x": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_pdbx_phasing_MAD_set_site.Cartn_y": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_pdbx_phasing_MAD_set_site.Cartn_z": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),

        # PDBx/mmCIF solvent atom-site mapping coordinates
        "_pdbx_solvent_atom_site_mapping.Cartn_x": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_pdbx_solvent_atom_site_mapping.Cartn_y": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_pdbx_solvent_atom_site_mapping.Cartn_z": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_pdbx_solvent_atom_site_mapping.pre_Cartn_x": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_pdbx_solvent_atom_site_mapping.pre_Cartn_y": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_pdbx_solvent_atom_site_mapping.pre_Cartn_z": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),

        # ModelCIF / CSM template coordinates
        "_ma_template_coord.Cartn_x": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ma_template_coord.Cartn_y": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ma_template_coord.Cartn_z": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),

        # IHM coordinates
        "_ihm_starting_model_coord.Cartn_x": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ihm_starting_model_coord.Cartn_y": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ihm_starting_model_coord.Cartn_z": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ihm_sphere_obj_site.Cartn_x": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ihm_sphere_obj_site.Cartn_y": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ihm_sphere_obj_site.Cartn_z": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ihm_gaussian_obj_site.mean_Cartn_x": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ihm_gaussian_obj_site.mean_Cartn_y": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ihm_gaussian_obj_site.mean_Cartn_z": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ihm_gaussian_obj_ensemble.mean_Cartn_x": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ihm_gaussian_obj_ensemble.mean_Cartn_y": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ihm_gaussian_obj_ensemble.mean_Cartn_z": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ihm_pseudo_site.Cartn_x": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ihm_pseudo_site.Cartn_y": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_ihm_pseudo_site.Cartn_z": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),

        # FLR / FPS coordinates
        "_flr_FPS_mean_probe_position.mpp_xcoord": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_flr_FPS_mean_probe_position.mpp_ycoord": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_flr_FPS_mean_probe_position.mpp_zcoord": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_flr_FPS_MPP_atom_position.xcoord": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_flr_FPS_MPP_atom_position.ycoord": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_flr_FPS_MPP_atom_position.zcoord": FloatEncodingConfig(1000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),

        # ---- Anisotropic displacement U matrix: factor 10000, FixedPoint -> Delta -> IntegerPacking -> ByteArray ----
        "_atom_site_anisotrop.U[1][1]": FloatEncodingConfig(10000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_atom_site_anisotrop.U[1][2]": FloatEncodingConfig(10000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_atom_site_anisotrop.U[1][3]": FloatEncodingConfig(10000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_atom_site_anisotrop.U[2][2]": FloatEncodingConfig(10000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_atom_site_anisotrop.U[2][3]": FloatEncodingConfig(10000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),
        "_atom_site_anisotrop.U[3][3]": FloatEncodingConfig(10000, ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]),

        # ---- IHM sphere object radius: factor 1000, no Delta/RunLength ----
        "_ihm_sphere_obj_site.object_radius": FloatEncodingConfig(1000, ["FixedPoint", "IntegerPacking", "ByteArray"]),

        # ---- High-volume float items: factor auto-detected from data, RunLength chain ----
        # NOTE: Setting factor=None means the caller is expected to auto-detect a safe factor from the column's data,
        #       and prepend the "FixedPoint" step to the encoder list with that factor.
        "_atom_site.occupancy": FloatEncodingConfig(None, ["RunLength", "IntegerPacking", "ByteArray"]),

        "_atom_site.B_iso_or_equiv": FloatEncodingConfig(None, ["RunLength", "IntegerPacking", "ByteArray"]),
        "_ihm_sphere_obj_site.rmsf": FloatEncodingConfig(None, ["RunLength", "IntegerPacking", "ByteArray"]),

        "_ihm_starting_model_coord.B_iso_or_equiv": FloatEncodingConfig(None, ["RunLength", "IntegerPacking", "ByteArray"]),
    })

    # -----------------------------------------------------------------------
    # Accessors
    # -----------------------------------------------------------------------

    @classmethod
    def get_float_item_config(cls, itemName):
        """Return the FloatEncodingConfig for itemName, or None if it isn't a forced type.

        Args:
            itemName (str): full item name, e.g. "_atom_site.Cartn_x"

        Returns:
            FloatEncodingConfig or None
        """
        return cls.FLOAT_ITEM_CONFIGS.get(itemName)

    @classmethod
    def get_float_encoder_list(cls, itemName):
        """Return the resolved encoder list for itemName, if it is a forced type.

        Any "FixedPoint" entry in the item's encoderList is replaced with the
        tuple ("FixedPoint", factor), using that item's own factor.

        Args:
            itemName (str): full item name, e.g. "_atom_site.Cartn_x"

        Returns:
            list or None: the resolved encoder list, or None if itemName is
            not in FORCED_FLOAT_ITEMS, or if it has no pre-determined
            encoderList.
        """
        itemConfig = cls.get_float_item_config(itemName)
        if itemConfig is None:
            return None
        return itemConfig.get_float_encoder_list()


FLOAT_ITEM_CONFIGS = BinaryCifEncodingConfig.FLOAT_ITEM_CONFIGS


def canonical_item_name(category_name, attribute_name):
    """Return the canonical, case-sensitive _category.attribute name."""
    if category_name is None or attribute_name is None:
        return ""
    if category_name.startswith("_"):
        return "%s.%s" % (category_name, attribute_name)
    return "_%s.%s" % (category_name, attribute_name)


def get_forced_type(item_name):
    """Return a configured writer type for a canonical item name, if any."""
    if item_name in FORCED_STRING_ITEMS:
        return "string"
    if item_name in FORCED_INTEGER_ITEMS:
        return "integer"
    if item_name in FLOAT_ITEM_CONFIGS:
        return "float"
    return None


def validate_binary_cif_config():
    """Raise ValueError for contradictory or unsupported BinaryCIF policy."""
    errors = []
    if FORCED_STRING_ITEMS & FORCED_INTEGER_ITEMS:
        errors.append("items cannot be both forced string and forced integer")
    if FORCED_STRING_ITEMS & set(FLOAT_ITEM_CONFIGS):
        errors.append("forced string items cannot have float configurations")
    if FORCED_INTEGER_ITEMS & set(FLOAT_ITEM_CONFIGS):
        errors.append("forced integer items cannot have float configurations")

    reusable_chains = FIXED_POINT_CANDIDATE_INTEGER_CHAINS + (
        DEFAULT_FIXED_POINT_INTEGER_CHAIN,
        DEFAULT_INTEGER_CHAIN,
        FLOAT_BYTE_ARRAY_FALLBACK_CHAIN,
        MASK_ENCODING_CHAIN,
    )
    for chain in reusable_chains:
        unsupported = set(chain) - SUPPORTED_ENCODERS
        if unsupported:
            errors.append("unsupported encoders: %s" % sorted(unsupported))

    for item_name, item_config in FLOAT_ITEM_CONFIGS.items():
        if item_config.factor is not None and (
            not isinstance(item_config.factor, int)
            or isinstance(item_config.factor, bool)
            or item_config.factor <= 0
        ):
            errors.append("%s has an invalid FixedPoint factor" % item_name)
        unsupported = set(item_config.integer_chain) - SUPPORTED_ENCODERS
        if unsupported:
            errors.append("%s has unsupported encoders: %s" % (item_name, sorted(unsupported)))

    if errors:
        raise ValueError("; ".join(errors))
    return True


BCIF_CONFIG = BinaryCifEncodingConfig()

validate_binary_cif_config()
