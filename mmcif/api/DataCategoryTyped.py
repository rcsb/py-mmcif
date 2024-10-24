##
#
# File:     DataCategoryTyped.py
# Original: 15-May-2021   jdw
#
# Update:
##
"""

A subclass of DataCategory including explicit typing.

"""
from __future__ import absolute_import

import logging

from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import CifName


__docformat__ = "google en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


logger = logging.getLogger(__name__)


class DataCategoryHints:
    """A class which will support hints for data types"""
    #
    __molstar_forced_ints = {
        "_atom_site.id": "integer",
        "_atom_site.auth_seq_id": "integer",
        "_atom_site_anisotrop.id": "integer",
        "_pdbx_struct_mod_residue.auth_seq_id": "integer",
        "_struct_conf.beg_auth_seq_id": "integer",
        "_struct_conf.end_auth_seq_id": "integer",
        "_struct_conn.ptnr1_auth_seq_id": "integer",
        "_struct_conn.ptnr2_auth_seq_id": "integer",
        "_struct_sheet_range.beg_auth_seq_id": "integer",
        "_struct_sheet_range.end_auth_seq_id": "integer",
    }
    #
    __pdbx_item_type_list_map = {
        # Strings
        "code": "string",  # char
        "line": "string",  # char
        "text": "string",  # char
        "boolean": "string",  # char
        "ucode": "string",  # uchar
        "uline": "string",  # uchar
        "name": "string",  # uchar
        "idname": "string",  # uchar
        "any": "string",  # char
        "yyyy-mm-dd": "string",  # char
        "yyyy-mm-dd:hh:mm-flex": "string",  # char
        "uchar3": "string",  # uchar
        "uchar5": "string",  # uchar
        "uchar1": "string",  # uchar
        "symop": "string",  # char
        "atcode": "string",  # char
        "yyyy-mm-dd:hh:mm": "string",  # char
        "fax": "string",  # uchar
        "phone": "string",  # uchar
        "email": "string",  # uchar
        "code30": "string",  # char
        "binary": "string",  # char
        "operation_expression": "string",  # char
        "ec-type": "string",  # char
        "seq-one-letter-code": "string",  # char
        "ucode-alphanum-csv": "string",  # uchar
        "point_symmetry": "string",  # char
        "asym_id": "string",  # char
        "id_list": "string",  # char
        "id_list_spc": "string",  # char
        "3x4_matrices": "string",  # char
        "3x4_matrix": "string",  # char
        "pdbx_related_db_id": "string",  # char
        "pdbx_PDB_obsoleted_db_id": "string",  # char
        "emd_id": "string",  # char
        "pdb_id": "string",  # char
        "pdb_id_u": "string",  # uchar
        "point_group": "string",  # char
        "point_group_helical": "string",  # char
        "author": "string",  # char
        "orcid_id": "string",  # char
        "symmetry_operation": "string",  # char
        "sequence_dep": "string",  # char
        "date_dep": "string",  # char
        "citation_doi": "string",  # char
        "exp_data_doi": "string",  # char
        "deposition_email": "string",  # uchar
        "entity_id_list": "string",  # uchar
        "int_list": "string",  # uchar
        "uniprot_ptm_id": "string",  # char
        "int-range": "string",  # numb
        "float-range": "string",  # numb
        # Integers
        "int": "integer",  # numb,
        "positive_int": "integer",  # numb,
        # Floats
        "float": "float",  # numb,
    }

    def __init__(self, **kwargs):
        pass

    def inMolStarIntHints(self, name):
        """Returns True if field name is in Mol* enforced-integer list; False otherwise

        Args:
            name: field name

        Returns:
            (bool): True if field name is in Mol* enforced-integer list; False otherwise
        """
        return name in self.__molstar_forced_ints

    def getPdbxItemType(self, typeCode):
        """Returns the item type corresponding to a given _item_type.code from PDBx dictionary

        Args:
            typeCode: field type code

        Returns:
            (str): item type corresponding to given type codes; else, if not present, "string"
        """
        return self.__pdbx_item_type_list_map.get(typeCode, "string")


class DataCategoryTyped(DataCategory):
    """A subclass of DataCategory with methods to apply explicit data typing."""

    def __init__(
        self,
        dataCategoryObj,
        dictionaryApi=None,
        raiseExceptions=True,
        copyInputData=True,
        ignoreCastErrors=False,
        useCifUnknowns=True,
        missingValueString=None,
        missingValueInteger=None,
        missingValueFloat=None,
        **kwargs
    ):
        """A subclass of DataCategory with methods to apply explicit data typing.

        Args:
            dataCategoryObj (object): DataCategory object instance
            dictionaryApi (object, optional): instance of DictionaryApi class. Defaults to None.
            raiseExceptions (bool, optional): raise exceptions. Defaults to True.
            copyInputData (bool, optional): make a new copy input data. Defaults to True.
            ignoreCastErrors (bool, optional): ignore data processing cast errors. Defaults to False.
            useCifUnknowns (bool, optional): use CIF style missing values ('.' and '?'). Defaults to True.
            missingValueString (str, optional): missing string value . Defaults to None.
            missingValueInteger (integer, optional): missing integer value. Defaults to None.
            missingValueFloat (float, optional): missing float value. Defaults to None.
            applyMolStarTypes (bool, optional): use Mol* forced integer types.  Defaults to True.
        """
        self.__dcObj = dataCategoryObj
        super(DataCategoryTyped, self).__init__(
            self.__dcObj.getName(),
            self.__dcObj.getAttributeList(),
            self.__dcObj.data,
            raiseExceptions=raiseExceptions,
            copyInputData=copyInputData,
        )
        #
        self.__dApi = dictionaryApi
        self.__attributeTypeD = {}
        self.__castD = {"integer": int, "float": float, "string": str}
        self.__applyMolStarTypes = kwargs.get("applyMolStarTypes", True)
        self.__dch = DataCategoryHints()

        self.__typesSet = self.applyTypes(
            ignoreCastErrors=ignoreCastErrors,
            useCifUnknowns=useCifUnknowns,
            missingValueString=missingValueString,
            missingValueInteger=missingValueInteger,
            missingValueFloat=missingValueFloat,
        )

    def applyTypes(self, ignoreCastErrors=False, useCifUnknowns=True, missingValueString=None, missingValueInteger=None, missingValueFloat=None):
        """Cast data types (string, integer, float) in the current object based on dictionary type details.
        Missing values ('.' or '?') are set to None.

        Raises:
            e: any exception

        Returns:
            bool: True for success or False otherwise
        """
        ok = False
        try:
            for ii, atName in enumerate(self.getAttributeList()):
                # colValL = self.getColumn(ii)
                dataType, isMandatory = self.__getAttributeInfo(atName)
                if not dataType:
                    if not ignoreCastErrors:
                        logger.warning("Undefined type for category %s attribute %s - Will treat as string", self.getName(), atName)
                    dataType = "string"  # Treat undefined attributes as strings
                missingValue = missingValueInteger if dataType == "integer" else missingValueFloat if dataType in ["integer", "float"] else missingValueString
                missingValue = missingValue if not useCifUnknowns else "." if isMandatory else "?"
                for row in self.data:
                    try:
                        row[ii] = self.__castD[dataType](row[ii]) if row[ii] is not None and row[ii] not in [".", "?"] else missingValue
                    except Exception as e:
                        if not ignoreCastErrors:
                            logger.error("Cast error %s %s (%s) %r %r", self.getName(), atName, dataType, row[ii], str(e))
                        row[ii] = missingValue
                #
                logger.debug("%s %s %r", self.getName(), atName, [row[ii] for row in self.data])
                self.__attributeTypeD[atName] = dataType
                ok = True
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            if self._raiseExceptions:
                raise e
        return ok

    def getAttributeInfo(self, atName):
        """Get attribute data type (string, integer, or float) and optionality

        Args:
            atName (str): attribute name

        Returns:
             (string, bool): data type (string, integer or float) and mandatory code
        """
        try:
            dataType, mandatoryCode = self.__getAttributeInfo(atName)
            return dataType, mandatoryCode
        except Exception:
            return None, None

    def applyStringTypes(self):
        """Cast data types to strings in the current object.  Missing values are set to '?' and '.' for
        optional and mandatory attributes, respectively.

        Raises:
            e: any exception

        Returns:
            bool: True for success or False otherwise
        """
        ok = False
        try:
            for ii, atName in enumerate(self.getAttributeList()):
                _, isMandatory = self.__getAttributeInfo(atName)
                dataType = "string"
                for row in self.data:
                    if row[ii] is None or row[ii] in [".", "?"]:
                        row[ii] = "." if isMandatory else "?"
                    else:
                        row[ii] = self.__castD[dataType](row[ii])
                #
                self.__attributeTypeD[atName] = dataType
                ok = True
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            if self._raiseExceptions:
                raise e
        return ok

    def cmpAttributeValues(self, dcObj, ignoreOrder=True, **kwargs):
        """Compare the values by attribute for current typed data category (dca) and input data category.
        The comparison is performed for values of the attributes common to both objects. Length differences
        are treated inequality out of hand.

        Args:
            dcObj (object): DataCategory object
            ignoreOrder (bool, optional): ignore attribute order. Defaults to True.
            floatRelTolerance (float, optional): relative tolerance for float comparisons. Defaults to 1e-05.
            floatAbsTolerance (float, optional): absolute tolerance for float comparisons. Defaults to 1e-04.

        Raises:
            e: any exception

        Returns:
            list: [(attributeName, values equal/close flag (bool)), (attributeName, values equal/close flag (bool), ...]

        """
        rL = []
        floatRelTolerance = kwargs.get("floatRelTolerance", 1.0e-05)
        floatAbsTolerance = kwargs.get("floatAbsTolerance", 1.0e-04)
        try:
            sa = set(self.getAttributeList())
            sb = set(dcObj.getAttributeList())
            atNameComList = list(sa & sb)
            #
            lenEq = self.getRowCount() == dcObj.getRowCount()
            if not lenEq:
                return [(atName, False) for atName in atNameComList]
            #
            for atName in atNameComList:
                dataType, _ = self.__getAttributeInfo(atName)
                if dataType in ["string", "integer"]:
                    if ignoreOrder:
                        same = sorted(self.getAttributeValueList(atName)) == sorted(dcObj.getAttributeValueList(atName))
                    else:
                        same = self.getAttributeValueList(atName) == dcObj.getAttributeValueList(atName)
                elif dataType in ["float"]:
                    aVL = self.getAttributeValueList(atName)
                    bVL = dcObj.getAttributeValueList(atName)
                    if ignoreOrder:
                        for aV, bV in zip(sorted(aVL), sorted(bVL)):
                            same = self.__isClose(aV, bV, relTol=floatRelTolerance, absTol=floatAbsTolerance)
                            if not same:
                                break
                    else:
                        for aV, bV in zip(aVL, bVL):
                            same = self.__isClose(aV, bV, relTol=floatRelTolerance, absTol=floatAbsTolerance)
                            if not same:
                                logger.info("%s %s (rel=%r) (abs=%r) %r (%r)", self.getName(), atName, aV * floatRelTolerance, floatAbsTolerance, aV, abs(aV - bV))
                                break
                rL.append((atName, same))
            #
            return rL
        except Exception as e:
            if self._raiseExceptions:
                raise e
        return rL

    def __getAttributeInfo(self, atName):
        """Get attribute data type (string, integer, or float) and optionality

        Args:
            atName (str): attribute name

        Returns:
            (string, bool): data type (string, integer or float) and mandatory code
        """
        logger.debug("Working on cat %r, atName %r", self.getName(), atName)
        cifDataType = self.__dApi.getTypeCode(self.getName(), atName)
        # cifPrimitiveType = self.__dApi.getTypePrimitive(self.getName(), atName)
        isMandatory = self.__dApi.getMandatoryCode(self.getName(), atName) in ["yes", "implicit", "implicit-ordinal"]
        if cifDataType is None:
            dataType = None
        else:
            dataType = self.__dch.getPdbxItemType(cifDataType)
            # dataType = "integer" if "int" in cifDataType else "float" if cifPrimitiveType == "numb" else "string"

        # Allow for forced Mol* integer types
        if self.__applyMolStarTypes:
            nm = CifName().itemName(self.getName(), atName)
            if self.__dch.inMolStarIntHints(nm):
                dataType = "integer"

        return dataType, isMandatory

    def __isClose(self, aV, bV, relTol=1e-09, absTol=1e-06):
        if aV is None and bV is None:
            return True
        elif aV is not None and bV is not None and aV == bV:
            return True
        elif isinstance(aV, (float)) and isinstance(bV, (float)):
            return abs(aV - bV) <= max(relTol * max(abs(aV), abs(bV)), absTol)
        else:
            raise ValueError
