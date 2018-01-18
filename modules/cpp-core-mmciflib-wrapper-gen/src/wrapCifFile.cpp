// File: ./src/wrapCifFile.cpp
// Date: 2018-01-10
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include <vector>
#include <map>
#include <iostream>
#include <sstream>
#include "GenString.h"
#include "CifString.h"
#include "TableFile.h"
#include "CifParentChild.h"
#include "CifFile.h"
namespace py = pybind11;
using namespace pybind11::literals;

#ifndef BINDER_PYBIND11_TYPE_CASTER
    #define BINDER_PYBIND11_TYPE_CASTER
    PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
    PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
    PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void wrapCifFile(py::module &m) {
   m.doc() = "Wrapper for header file CifFile.h";

   {
    py::class_<CifFile, std::shared_ptr<CifFile>, TableFile> cls(m, "CifFile", "Wrapper for class CifFile");
   
      py::enum_<CifFile::eQuoting>(cls, "eQuoting")
        .value("eSINGLE", CifFile::eQuoting::eSINGLE)
        .value("eDOUBLE", CifFile::eQuoting::eDOUBLE)
        .export_values();
   
     cls.def(py::init<const eFileMode, const std::string &, const bool, const Char::eCompareType, const unsigned int, const std::string &>(), py::arg("fileMode"), py::arg("fileName"), py::arg("verbose"), py::arg("caseSense"), py::arg("maxLineLength"), py::arg("nullValue"));
     cls.def(py::init([](const eFileMode fileMode,const std::string & fileName){ return new CifFile(fileMode,fileName); }), "Generated constructor");
     cls.def(py::init([](const eFileMode fileMode,const std::string & fileName,const bool verbose){ return new CifFile(fileMode,fileName,verbose); }), "Generated constructor");
     cls.def(py::init([](const eFileMode fileMode,const std::string & fileName,const bool verbose,const Char::eCompareType caseSense){ return new CifFile(fileMode,fileName,verbose,caseSense); }), "Generated constructor");
     cls.def(py::init([](const eFileMode fileMode,const std::string & fileName,const bool verbose,const Char::eCompareType caseSense,const unsigned int maxLineLength){ return new CifFile(fileMode,fileName,verbose,caseSense,maxLineLength); }), "Generated constructor");
     cls.def(py::init<const bool, const Char::eCompareType, const unsigned int, const std::string &>(), py::arg("verbose"), py::arg("caseSense"), py::arg("maxLineLength"), py::arg("nullValue"));
     cls.def(py::init([](){ return new CifFile(); }), "Generated constructor");
     cls.def(py::init([](const bool verbose){ return new CifFile(verbose); }), "Generated constructor");
     cls.def(py::init([](const bool verbose,const Char::eCompareType caseSense){ return new CifFile(verbose,caseSense); }), "Generated constructor");
     cls.def(py::init([](const bool verbose,const Char::eCompareType caseSense,const unsigned int maxLineLength){ return new CifFile(verbose,caseSense,maxLineLength); }), "Generated constructor");
     cls.def(py::init<const bool, const bool, const unsigned int, const unsigned int, const std::string &>(), py::arg("fake"), py::arg("verbose"), py::arg("intCaseSense"), py::arg("maxLineLength"), py::arg("nullValue"));
     cls.def(py::init([](const bool fake,const bool verbose){ return new CifFile(fake,verbose); }), "Generated constructor");
     cls.def(py::init([](const bool fake,const bool verbose,const unsigned int intCaseSense){ return new CifFile(fake,verbose,intCaseSense); }), "Generated constructor");
     cls.def(py::init([](const bool fake,const bool verbose,const unsigned int intCaseSense,const unsigned int maxLineLength){ return new CifFile(fake,verbose,intCaseSense,maxLineLength); }), "Generated constructor");
     cls.def("SetSrcFileName", &CifFile::SetSrcFileName,"",py::arg("srcFileName"));
     cls.def("GetSrcFileName", &CifFile::GetSrcFileName,"",py::return_value_policy::reference_internal);
     cls.def("GetVerbose", (bool (CifFile::*)()) &CifFile::GetVerbose,"GetVerbose with arguments ");
     cls.def("SetSmartPrint", (void (CifFile::*)(bool)) &CifFile::SetSmartPrint,"SetSmartPrint with arguments bool",py::arg("smartPrint"));
     cls.def("SetSmartPrint", [](CifFile &o ) -> void { return o.SetSmartPrint(); },"doc");
     cls.def("IsSmartPrint", (bool (CifFile::*)()) &CifFile::IsSmartPrint,"IsSmartPrint with arguments ");
     cls.def("SetQuoting", &CifFile::SetQuoting,"",py::arg("quoting"));
     cls.def("GetQuoting", &CifFile::GetQuoting,"");
     cls.def("SetLooping", (void (CifFile::*)(const std::string &, bool)) &CifFile::SetLooping,"SetLooping with arguments const std::string &, bool",py::arg("catName"), py::arg("looping"));
     cls.def("SetLooping", [](CifFile &o, const std::string & catName) -> void { return o.SetLooping(catName); },"doc");
     cls.def("GetLooping", (bool (CifFile::*)(const std::string &)) &CifFile::GetLooping,"GetLooping with arguments const std::string &",py::arg("catName"));
     cls.def("Write", (void (CifFile::*)(const std::string &, const bool, const bool)) &CifFile::Write,"Write with arguments const std::string &, const bool, const bool",py::arg("cifFileName"), py::arg("sortTables"), py::arg("writeEmptyTables"));
     cls.def("Write", [](CifFile &o, const std::string & cifFileName) -> void { return o.Write(cifFileName); },"doc");
     cls.def("Write", [](CifFile &o, const std::string & cifFileName,const bool sortTables) -> void { return o.Write(cifFileName,sortTables); },"doc");
     cls.def("Write", (void (CifFile::*)(const std::string &, const std::vector<std::string> &, const bool)) &CifFile::Write,"Write with arguments const std::string &, const std::vector<std::string> &, const bool",py::arg("cifFileName"), py::arg("tableOrder"), py::arg("writeEmptyTables"));
     cls.def("Write", [](CifFile &o, const std::string & cifFileName,const std::vector<std::string> & tableOrder) -> void { return o.Write(cifFileName,tableOrder); },"doc");
     cls.def("WriteNmrStar", (void (CifFile::*)(const std::string &, const std::string &, const bool, const bool)) &CifFile::WriteNmrStar,"WriteNmrStar with arguments const std::string &, const std::string &, const bool, const bool",py::arg("nmrStarFileName"), py::arg("globalBlockName"), py::arg("sortTables"), py::arg("writeEmptyTables"));
     cls.def("WriteNmrStar", [](CifFile &o, const std::string & nmrStarFileName,const std::string & globalBlockName) -> void { return o.WriteNmrStar(nmrStarFileName,globalBlockName); },"doc");
     cls.def("WriteNmrStar", [](CifFile &o, const std::string & nmrStarFileName,const std::string & globalBlockName,const bool sortTables) -> void { return o.WriteNmrStar(nmrStarFileName,globalBlockName,sortTables); },"doc");
     cls.def("DataChecking", [](CifFile &o , CifFile & dicRef, const std::string & diagFileName, const bool extraDictChecks, const bool extraCifChecks) {
       int _retVal =  o.DataChecking(dicRef, diagFileName, extraDictChecks, extraCifChecks);
       return std::make_tuple(_retVal, dicRef);
     },"DataChecking with arguments dicRef, diagFileName, extraDictChecks, extraCifChecks",py::return_value_policy::reference_internal , py::arg("dicRef"), py::arg("diagFileName"), py::arg("extraDictChecks"), py::arg("extraCifChecks"));
     cls.def("SetEnumCheck", (void (CifFile::*)(bool)) &CifFile::SetEnumCheck,"SetEnumCheck with arguments bool",py::arg("caseSense"));
     cls.def("SetEnumCheck", [](CifFile &o ) -> void { return o.SetEnumCheck(); },"doc");
     cls.def("GetEnumCheck", (bool (CifFile::*)()) &CifFile::GetEnumCheck,"GetEnumCheck with arguments ");
     cls.def("GetParsingDiags", &CifFile::GetParsingDiags,"",py::return_value_policy::reference_internal);
     cls.def("FindCifNullRows", [](CifFile &o , std::vector<unsigned int> & nullRowsIndices, const ISTable & isTable) {
        o.FindCifNullRows(nullRowsIndices, isTable);
       return nullRowsIndices;
     },"FindCifNullRows with arguments nullRowsIndices, isTable",py::return_value_policy::reference_internal , py::arg("nullRowsIndices"), py::arg("isTable"));
     cls.def("GetAttributeValue", [](CifFile &o , std::string & attribVal, const std::string & blockId, const std::string & category, const std::string & attribute) {
        o.GetAttributeValue(attribVal, blockId, category, attribute);
       return attribVal;
     },"GetAttributeValue with arguments attribVal, blockId, category, attribute",py::return_value_policy::reference_internal , py::arg("attribVal"), py::arg("blockId"), py::arg("category"), py::arg("attribute"));
     cls.def("GetAttributeValueIf", [](CifFile &o , std::string & attribVal, const std::string & blockId, const std::string & category, const std::string & attributeA, const std::string & attributeB, const std::string & valB) {
        o.GetAttributeValueIf(attribVal, blockId, category, attributeA, attributeB, valB);
       return attribVal;
     },"GetAttributeValueIf with arguments attribVal, blockId, category, attributeA, attributeB, valB",py::return_value_policy::reference_internal , py::arg("attribVal"), py::arg("blockId"), py::arg("category"), py::arg("attributeA"), py::arg("attributeB"), py::arg("valB"));
     cls.def("IsAttributeValueDefined", (bool (CifFile::*)(const std::string &, const std::string &, const std::string &)) &CifFile::IsAttributeValueDefined,"IsAttributeValueDefined with arguments const std::string &, const std::string &, const std::string &",py::arg("blockId"), py::arg("category"), py::arg("attribute"));
     cls.def("SetAttributeValue", (void (CifFile::*)(const std::string &, const std::string &, const std::string &, const std::string &, const bool)) &CifFile::SetAttributeValue,"SetAttributeValue with arguments const std::string &, const std::string &, const std::string &, const std::string &, const bool",py::arg("blockId"), py::arg("category"), py::arg("attribute"), py::arg("value"), py::arg("create"));
     cls.def("SetAttributeValue", [](CifFile &o, const std::string & blockId,const std::string & category,const std::string & attribute,const std::string & value) -> void { return o.SetAttributeValue(blockId,category,attribute,value); },"doc");
     cls.def("SetAttributeValueIf", (void (CifFile::*)(const std::string &, const std::string &, const std::string &, const std::string &, const std::string &, const std::string &, const bool)) &CifFile::SetAttributeValueIf,"SetAttributeValueIf with arguments const std::string &, const std::string &, const std::string &, const std::string &, const std::string &, const std::string &, const bool",py::arg("blockId"), py::arg("category"), py::arg("attributeA"), py::arg("valA"), py::arg("attributeB"), py::arg("valB"), py::arg("create"));
     cls.def("SetAttributeValueIf", [](CifFile &o, const std::string & blockId,const std::string & category,const std::string & attributeA,const std::string & valA,const std::string & attributeB,const std::string & valB) -> void { return o.SetAttributeValueIf(blockId,category,attributeA,valA,attributeB,valB); },"doc");
     cls.def("SetAttributeValueIfNull", &CifFile::SetAttributeValueIfNull,"",py::arg("blockId"), py::arg("category"), py::arg("attribute"), py::arg("value"));
     cls.def("GetAttributeValues", [](CifFile &o , std::vector<std::string> & strings, const std::string & blockId, const std::string & category, const std::string & attribute) {
        o.GetAttributeValues(strings, blockId, category, attribute);
       return strings;
     },"GetAttributeValues with arguments strings, blockId, category, attribute",py::return_value_policy::reference_internal , py::arg("strings"), py::arg("blockId"), py::arg("category"), py::arg("attribute"));
     cls.def("GetAttributeValuesIf", [](CifFile &o , std::vector<std::string> & strings, const std::string & blockId, const std::string & category, const std::string & attributeA, const std::string & attributeB, const std::string & valB) {
        o.GetAttributeValuesIf(strings, blockId, category, attributeA, attributeB, valB);
       return strings;
     },"GetAttributeValuesIf with arguments strings, blockId, category, attributeA, attributeB, valB",py::return_value_policy::reference_internal , py::arg("strings"), py::arg("blockId"), py::arg("category"), py::arg("attributeA"), py::arg("attributeB"), py::arg("valB"));
     cls.def("SetAttributeValues", &CifFile::SetAttributeValues,"",py::arg("blockId"), py::arg("category"), py::arg("attribute"), py::arg("values"));
   }

}