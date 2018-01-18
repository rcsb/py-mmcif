// File: ./src/wrapDicFile.cpp
// Date: 2018-01-10
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include <iostream>
#include "GenString.h"
#include "ISTable.h"
#include "CifFile.h"
#include "DicFile.h"
namespace py = pybind11;
using namespace pybind11::literals;

#ifndef BINDER_PYBIND11_TYPE_CASTER
    #define BINDER_PYBIND11_TYPE_CASTER
    PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
    PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
    PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void wrapDicFile(py::module &m) {
   m.doc() = "Wrapper for header file DicFile.h";

   {
    py::class_<DicFile, std::shared_ptr<DicFile>, CifFile> cls(m, "DicFile", "Wrapper for class DicFile");
   
     cls.def(py::init<const eFileMode, const std::string &, const bool, const Char::eCompareType, const unsigned int, const std::string &>(), py::arg("fileMode"), py::arg("objFileName"), py::arg("verbose"), py::arg("caseSense"), py::arg("maxLineLength"), py::arg("nullValue"));
     cls.def(py::init([](const eFileMode fileMode,const std::string & objFileName){ return new DicFile(fileMode,objFileName); }), "Generated constructor");
     cls.def(py::init([](const eFileMode fileMode,const std::string & objFileName,const bool verbose){ return new DicFile(fileMode,objFileName,verbose); }), "Generated constructor");
     cls.def(py::init([](const eFileMode fileMode,const std::string & objFileName,const bool verbose,const Char::eCompareType caseSense){ return new DicFile(fileMode,objFileName,verbose,caseSense); }), "Generated constructor");
     cls.def(py::init([](const eFileMode fileMode,const std::string & objFileName,const bool verbose,const Char::eCompareType caseSense,const unsigned int maxLineLength){ return new DicFile(fileMode,objFileName,verbose,caseSense,maxLineLength); }), "Generated constructor");
     cls.def(py::init<const bool, const Char::eCompareType, const unsigned int, const std::string &>(), py::arg("verbose"), py::arg("caseSense"), py::arg("maxLineLength"), py::arg("nullValue"));
     cls.def(py::init([](){ return new DicFile(); }), "Generated constructor");
     cls.def(py::init([](const bool verbose){ return new DicFile(verbose); }), "Generated constructor");
     cls.def(py::init([](const bool verbose,const Char::eCompareType caseSense){ return new DicFile(verbose,caseSense); }), "Generated constructor");
     cls.def(py::init([](const bool verbose,const Char::eCompareType caseSense,const unsigned int maxLineLength){ return new DicFile(verbose,caseSense,maxLineLength); }), "Generated constructor");
     cls.def("WriteItemAliases", (void (DicFile::*)(const std::string &)) &DicFile::WriteItemAliases,"WriteItemAliases with arguments const std::string &",py::arg("fileName"));
     cls.def("GetFormatTable", &DicFile::GetFormatTable,"",py::return_value_policy::reference_internal);
     cls.def("WriteFormatted", (int (DicFile::*)(const std::string &, ISTable *)) &DicFile::WriteFormatted,"WriteFormatted with arguments const std::string &, ISTable *",py::arg("cifFileName"), py::arg("formatP"));
     cls.def("WriteFormatted", [](DicFile &o, const std::string & cifFileName) -> int { return o.WriteFormatted(cifFileName); },"doc");
     cls.def("WriteFormatted", (int (DicFile::*)(const std::string &, TableFile *, ISTable *)) &DicFile::WriteFormatted,"WriteFormatted with arguments const std::string &, TableFile *, ISTable *",py::arg("cifFileName"), py::arg("ddl"), py::arg("formatP"));
     cls.def("WriteFormatted", [](DicFile &o, const std::string & cifFileName,TableFile * ddl) -> int { return o.WriteFormatted(cifFileName,ddl); },"doc");
     cls.def("Compress", &DicFile::Compress,"",py::arg("ddl"));
     cls.def("GetRefFile", &DicFile::GetRefFile,"",py::return_value_policy::reference_internal);
   }

}