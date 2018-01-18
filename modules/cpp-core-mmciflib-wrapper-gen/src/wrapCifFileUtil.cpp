// File: ./src/wrapCifFileUtil.cpp
// Date: 2018-01-10
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include "CifFileReadDef.h"
#include "DicFile.h"
#include "CifFile.h"
#include "CifFileUtil.h"
namespace py = pybind11;
using namespace pybind11::literals;

#ifndef BINDER_PYBIND11_TYPE_CASTER
    #define BINDER_PYBIND11_TYPE_CASTER
    PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
    PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
    PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void wrapCifFileUtil(py::module &m) {
   m.doc() = "Wrapper for header file CifFileUtil.h";

     m.def("GetDictFile", [](DicFile * ddlFileP, const std::string & dictFileName, const std::string & dictSdbFileName, const bool verbose, const eFileMode fileMode) {
       auto _retVal =  GetDictFile(ddlFileP, dictFileName, dictSdbFileName, verbose, fileMode);
       return std::make_tuple(_retVal, ddlFileP);
     },"GetDictFile with arguments ddlFileP, dictFileName, dictSdbFileName, verbose, fileMode",py::return_value_policy::reference_internal , py::arg("ddlFileP"), py::arg("dictFileName"), py::arg("dictSdbFileName"), py::arg("verbose"), py::arg("fileMode"));
     m.def("CheckDict", [](DicFile * dictFileP, DicFile * ddlFileP, const string & dictFileName, const bool extraDictChecks) {
        CheckDict(dictFileP, ddlFileP, dictFileName, extraDictChecks);
       return std::make_tuple(dictFileP, ddlFileP);
     },"CheckDict with arguments dictFileP, ddlFileP, dictFileName, extraDictChecks",py::return_value_policy::reference_internal , py::arg("dictFileP"), py::arg("ddlFileP"), py::arg("dictFileName"), py::arg("extraDictChecks"));
     m.def("CheckCif", [](CifFile * cifFileP, DicFile * dictFileP, const string & cifFileName, const bool extraCifChecks) {
        CheckCif(cifFileP, dictFileP, cifFileName, extraCifChecks);
       return std::make_tuple(cifFileP, dictFileP);
     },"CheckCif with arguments cifFileP, dictFileP, cifFileName, extraCifChecks",py::return_value_policy::reference_internal , py::arg("cifFileP"), py::arg("dictFileP"), py::arg("cifFileName"), py::arg("extraCifChecks"));
     m.def("ParseDict", [](const std::string & dictFileName, DicFile * ddlFileP, const bool verbose) {
       auto _retVal =  ParseDict(dictFileName, ddlFileP, verbose);
       return std::make_tuple(_retVal, ddlFileP);
     },"ParseDict with arguments dictFileName, ddlFileP, verbose",py::return_value_policy::reference_internal , py::arg("dictFileName"), py::arg("ddlFileP"), py::arg("verbose"));
     m.def("ParseCif",  &ParseCif, "", py::arg("fileName"), py::arg("verbose"), py::arg("caseSense"), py::arg("maxLineLength"), py::arg("nullValue"), py::arg("parseLogFileName"));
     m.def("ParseCifString",  &ParseCifString, "", py::arg("cifString"), py::arg("verbose"), py::arg("caseSense"), py::arg("maxLineLength"), py::arg("nullValue"));
     m.def("ParseCifSimple",  &ParseCifSimple, "", py::arg("fileName"), py::arg("verbose"), py::arg("intCaseSense"), py::arg("maxLineLength"), py::arg("nullValue"), py::arg("parseLogFileName"));
     m.def("ParseCifSelective",  &ParseCifSelective, "", py::arg("fileName"), py::arg("readDef"), py::arg("verbose"), py::arg("intCaseSense"), py::arg("maxLineLength"), py::arg("nullValue"), py::arg("parseLogFileName"));
     m.def("DataCorrection", [](CifFile & cifFile, DicFile & dicRef) {
        DataCorrection(cifFile, dicRef);
       return std::make_tuple(cifFile, dicRef);
     },"DataCorrection with arguments cifFile, dicRef",py::return_value_policy::reference_internal , py::arg("cifFile"), py::arg("dicRef"));
}