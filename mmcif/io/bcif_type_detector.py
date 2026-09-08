"""
bcif_type_detector.py
---------------------
Single-pass column type detection for BinaryCIF encoding.

Exports
-------
ColumnProfile   : dataclass holding all classification results for one column
classify_column : scan a column list once and return a populated ColumnProfile

This module has no dependency on the BinaryCIF writer or dictionaryApi.
It consumes immutable policy from mmcif.io.config and can otherwise be used
independently.

The three-way col_type result ("int" | "float" | "str") is a direct
replacement for the dictionaryApi.getTypeCode() → getPdbxItemType() chain
used in BinaryCifWriter.py. The writer currently consumes only col_type;
the additional profile fields are retained for callers and future encoding
pipeline selection.
"""

import re
from dataclasses import dataclass
from typing import Any, Optional

from mmcif.io.config import MISSING_VALUE_TOKENS, TYPE_DETECTION_CONFIG, TypeDetectionConfig

# ---------------------------------------------------------------------------
# Module-level compiled regex — built once, shared across all calls
# ---------------------------------------------------------------------------

_FLOAT = re.compile(r"^-?\d+\.\d*$|^-?\d*\.\d+$")



# ---------------------------------------------------------------------------
# ColumnProfile dataclass
# ---------------------------------------------------------------------------

@dataclass
class ColumnProfile:
    """
    All classification results for a single column.

    Fields used directly by BinaryCifWriter.py
    ------------------------------------------
    col_type       : "int" | "float" | "str"  — replaces dictionaryApi type lookup

    Fields available for encoding optimisation
    ------------------------------------------
    int_width      : narrowest safe integer type ("uint8"|"int8"|"uint16"|"int16"|"int32")
    float_prec     : float precision needed ("f32" | "f64")
    col_min        : minimum numeric value seen (None for str columns)
    col_max        : maximum numeric value seen (None for str columns)
    max_decimals   : maximum decimal places seen (0 for int/str columns)
    is_sequential  : True if integers form a consecutive 1-step sequence
    has_long_runs  : True if any adjacent run of identical values is >= 4 long
    unique_ratio   : len(unique values) / total non-sentinel values
    value_count    : number of non-sentinel values
    sentinel_count : number of sentinel ("." or "?") values
    """
    col_type:       str   = "str"
    int_width:      str   = "int32"
    float_prec:     str   = "f32"
    col_min:        Any   = None
    col_max:        Any   = None
    max_decimals:   int   = 0
    is_sequential:  bool  = False
    has_long_runs:  bool  = False
    unique_ratio:   float = 1.0
    value_count:    int   = 0
    sentinel_count: int   = 0


# ---------------------------------------------------------------------------
# classify_column — the single public entry point
# ---------------------------------------------------------------------------

def classify_column(
    values: list,
    force_small_float_as_string: Optional[bool] = None,
    type_detection_config: Optional[TypeDetectionConfig] = None,
) -> ColumnProfile:
    """
    Scan a column once and return a fully populated ColumnProfile.

    Design
    ------
    Single pass per column, two things tracked concurrently:

      Type Probe
        Runs until the type is conclusively decided.
        Short-circuits (sets type_decided=True) as soon as a non-numeric value
        is encountered, but does NOT break — the loop continues for Phase B.

      Statistics
        Always completes the full loop regardless of Phase A outcome.
        Maintains: unique value set, adjacent run-length tracking.
        These are needed for encoding decisions even on pure string columns.

    Detection order within each value (cheapest-first):
      isinstance check  →  char-level isdigit fast path  →  compiled regex

    Parameters
    ----------
    values : list
        Raw column values as returned by DataCategory.getColumn().
        May contain strings, ints, floats, None, ".", "?".

    force_small_float_as_string : bool, optional
        Compatibility override for the configured small-float switch.
    type_detection_config : TypeDetectionConfig, optional
        Immutable policy for this call. Defaults to TYPE_DETECTION_CONFIG.
        When the effective switch is True, a column that would classify as
        "float" but has fewer than the configured number of present
        non-sentinel values is forced to "str".

    Returns
    -------
    ColumnProfile
        Fully populated.  col_type is always set to "int", "float", or "str".
    """
    type_detection_config = type_detection_config or TYPE_DETECTION_CONFIG
    force_small = (
        type_detection_config.force_small_float_as_string
        if force_small_float_as_string is None
        else force_small_float_as_string
    )
    p = ColumnProfile()

    # type-probe state
    all_int      = True
    all_float    = True
    type_decided = False     # flips to True once we know the column is str

    # numeric accumulation
    is_sequential = True
    col_min       = None
    col_max       = None
    max_dec       = 0
    prev          = None     # previous integer value for sequential check

    # statistics (always accumulated)
    unique        = set()
    run_val       = None
    run_len       = 1
    long_run_seen = False
    total         = 0
    sentinels     = 0

    for v in values:

        # --- sentinel gate (cheapest check) ---
        if v is None or v in MISSING_VALUE_TOKENS:
            sentinels += 1
            continue

        total += 1
        s = str(v).strip()
        unique.add(s)

        # --- run-length tracking (always runs) ---
        if s == run_val:
            run_len += 1
            if run_len >= 4:
                long_run_seen = True
        else:
            run_val = s
            run_len = 1

        # --- Type Probe: type detection (skip once type is decided) ---
        if type_decided:
            continue

        # bool must be checked before int — bool is a subclass of int in Python
        # Defensive check; If a CIF file contains "True" or "False" as values, treat it as string instead of bool.
        if isinstance(v, bool):
            all_int = all_float = False
            type_decided = True
            continue

        if isinstance(v, int):
            n = v
            all_float = False

        elif isinstance(v, float):
            all_int = False
            dec = len(s.split(".")[1]) if "." in s else 0
            max_dec = max(max_dec, dec)
            col_min = v if col_min is None else min(col_min, v)
            col_max = v if col_max is None else max(col_max, v)
            prev = None   # floats break sequential integer assumption
            continue

        elif isinstance(v, str):
            # char-level fast path before paying for regex
            candidate = s[1:] if s and s[0] == "-" else s
            if candidate.isdigit():
                if len(candidate)>1 and candidate[0] == "0":
                    # leading zero disqualifies integer type — treat as string
                    all_int = all_float = False
                    type_decided = True
                    continue
                #--------------------------------------
                n = int(s)
                all_float = False
            elif _FLOAT.match(s):
                all_int = False
                f = float(s)
                dec = len(s.split(".")[1]) if "." in s else 0
                max_dec = max(max_dec, dec)
                col_min = f if col_min is None else min(col_min, f)
                col_max = f if col_max is None else max(col_max, f)
                prev = None
                continue
            else:
                # non-numeric: type decided, but loop continues for Statistics
                all_int = all_float = False
                type_decided = True
                continue
        else:
            # unknown type — treat conservatively as string
            all_int = all_float = False
            type_decided = True
            continue

        # --- integer bookkeeping (reached only for confirmed int values) ---
        col_min = n if col_min is None else min(col_min, n)
        col_max = n if col_max is None else max(col_max, n)
        if prev is not None and n != prev + 1:
            is_sequential = False
        prev = n

    # ---------------------------------------------------------------------------
    # Finalise profile
    # ---------------------------------------------------------------------------

    p.value_count    = total
    p.sentinel_count = sentinels
    p.col_min        = col_min
    p.col_max        = col_max
    p.max_decimals   = max_dec
    p.is_sequential  = is_sequential and total > 1
    p.has_long_runs  = long_run_seen
    p.unique_ratio   = len(unique) / total if total else 1.0

    if total == 0:
        # Every value was a sentinel (e.g. pdbx_formal_charge all "?").
        # No present values to type from. Default to int: cheapest encoding
        # (IntArrayMasked fills masked with 0 → Delta+RunLength collapses),
        # and decode is identical regardless of declared type since every
        # value is masked.
        p.col_type = "int"

    elif all_int:
        p.col_type = "int"
        lo, hi = col_min, col_max
        if   lo >= 0    and hi <= 255:   p.int_width = "uint8"
        elif lo >= -128 and hi <= 127:   p.int_width = "int8"
        elif lo >= 0    and hi <= 65535: p.int_width = "uint16"
        elif lo >= -32768 and hi <= 32767: p.int_width = "int16"
        else:                            p.int_width = "int32"

    elif all_float:
        # Apply the configurable small-float override only when enabled.
        if force_small and total < type_detection_config.min_rows_to_classify_as_float:
            p.col_type = "str"
        else:
            p.col_type   = "float"
            p.float_prec = "f32" if max_dec <= 6 else "f64"

    else:
        p.col_type = "str"

    return p
