##
# File: config.py
# Date: 06-Jul-2026
#
# Configuration settings, primarily for BinaryCifWriter.py encoding behavior.
#
##

_UNSET = object()


def _set_float_item_names(itemConfigs):
    """Populate each FloatEncodingConfig.name from its dictionary key."""
    for itemName, itemConfig in itemConfigs.items():
        itemConfig.name = itemName
    return itemConfigs


class FloatEncodingConfig:
    """Describes how a single float data item should be encoded.

    All items tracked via FloatEncodingConfig are assumed to be floats.

    Attributes:
        name (str): full item name, e.g. "_atom_site.Cartn_x"
        factor (int or None): FixedPoint scaling factor.
            - Not provided (default) -> 1000. (This is what _UNSET is for.)
            - Provided as None -> no fixed factor; the caller is expected to
              auto-detect a safe factor from the column's data (used below
              for a handful of high-volume items that need this today).
            - Provided as an int -> always use that fixed factor.
        encoderList (list or None): the encoder chain for this item, e.g.
            ["FixedPoint", "Delta", "IntegerPacking", "ByteArray"]. Include
            the literal string "FixedPoint" wherever the FixedPoint step
            belongs in the chain; get_float_encoder_list() will substitute in
            the actual factor. Defaults to None (no pre-determined chain).
    """

    def __init__(self, factor=_UNSET, encoderList=None, name=None):
        self.name = name
        self.factor = 1000 if factor is _UNSET else factor
        self.encoderList = encoderList

    def get_float_encoder_list(self):
        """Return this item's encoder list, with any "FixedPoint" entry
        replaced by the tuple ("FixedPoint", self.factor).

        Returns:
            list or None: the resolved encoder list, or None if this item
            has no pre-determined encoderList.
        """
        if self.encoderList is None:
            return None
        procEncoderList = []
        for enc in self.encoderList:
            if enc == "FixedPoint":
                if self.factor is None:
                    raise ValueError(f"Forced float data item {self.name} with encoder list {self.encoderList} must have a factor defined for 'FixedPoint' encoding ({self.factor})")
                procEncoderList.append(("FixedPoint", self.factor))
            else:
                procEncoderList.append(enc)
        return procEncoderList

    def __repr__(self):
        return "FloatEncodingConfig(name=%r, factor=%r, encoderList=%r)" % (
            self.name,
            self.factor,
            self.encoderList,
        )


class BinaryCifEncodingConfig:
    """Container for all BinaryCifWriter float-encoding configuration."""

    # -----------------------------------------------------------------------
    # Global float-encoding switches
    # -----------------------------------------------------------------------

    # True:  use the configured RunLength encoding chains for selected
    #        high-volume float items.
    # False: treat those items as general floats and use automatic factor
    #        detection and general FixedPoint chain selection.
    USE_RUN_LENGTH_FLOAT_HINTS = True

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
    FORCED_FLOAT_ITEMS = _set_float_item_names({

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
        return cls.FORCED_FLOAT_ITEMS.get(itemName)

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


BCIF_CONFIG = BinaryCifEncodingConfig()
