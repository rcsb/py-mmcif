// File: ./src/wrapCifFileReadDef.cpp
// Date: 2018-01-10
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <string.h>
#include "CifFileReadDef.h"
namespace py = pybind11;
using namespace pybind11::literals;

#ifndef BINDER_PYBIND11_TYPE_CASTER
    #define BINDER_PYBIND11_TYPE_CASTER
    PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
    PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
    PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void wrapCifFileReadDef(py::module &m) {
   m.doc() = "Wrapper for header file CifFileReadDef.h";

   py::enum_<type>(m, "type")
     .value("A", type::A)
     .value("D", type::D)
     .export_values();

   {
    py::class_<CifFileReadDef, std::shared_ptr<CifFileReadDef>> cls(m, "CifFileReadDef", "Wrapper for class CifFileReadDef");
   
     cls.def(py::init<std::vector<std::string>, std::vector<std::string>, type, type>(), py::arg("dblist"), py::arg("clist"), py::arg("dbtype"), py::arg("ctype"));
     cls.def(py::init([](std::vector<std::string> dblist,std::vector<std::string> clist){ return new CifFileReadDef(dblist,clist); }), "Generated constructor");
     cls.def(py::init([](std::vector<std::string> dblist,std::vector<std::string> clist,type dbtype){ return new CifFileReadDef(dblist,clist,dbtype); }), "Generated constructor");
     cls.def(py::init([](){ return new CifFileReadDef(); }), "Default constructor for CifFileReadDef");
     cls.def("SetDataBlockList", (void (CifFileReadDef::*)(std::vector<std::string>, type)) &CifFileReadDef::SetDataBlockList,"SetDataBlockList with arguments std::vector<std::string>, type",py::arg("dblist"), py::arg("dbtype"));
     cls.def("SetDataBlockList", [](CifFileReadDef &o, std::vector<std::string> dblist) -> void { return o.SetDataBlockList(dblist); },"doc");
     cls.def("SetCategoryList", (void (CifFileReadDef::*)(std::vector<std::string>, type)) &CifFileReadDef::SetCategoryList,"SetCategoryList with arguments std::vector<std::string>, type",py::arg("clist"), py::arg("ctype"));
     cls.def("SetCategoryList", [](CifFileReadDef &o, std::vector<std::string> clist) -> void { return o.SetCategoryList(clist); },"doc");
     cls.def("SetDataBlockListType", (void (CifFileReadDef::*)(type)) &CifFileReadDef::SetDataBlockListType,"SetDataBlockListType with arguments type",py::arg("dbtype"));
     cls.def("SetDataBlockListType", [](CifFileReadDef &o ) -> void { return o.SetDataBlockListType(); },"doc");
     cls.def("SetCategoryListType", (void (CifFileReadDef::*)(type)) &CifFileReadDef::SetCategoryListType,"SetCategoryListType with arguments type",py::arg("ctype"));
     cls.def("SetCategoryListType", [](CifFileReadDef &o ) -> void { return o.SetCategoryListType(); },"doc");
     cls.def("AreAllCatsRead", &CifFileReadDef::AreAllCatsRead,"");
     cls.def("IncreaseNumReadCats", &CifFileReadDef::IncreaseNumReadCats,"");
     cls.def("Category_OK", &CifFileReadDef::Category_OK,"",py::arg("categoryName"));
     cls.def("Datablock_OK", &CifFileReadDef::Datablock_OK,"",py::arg("datablockName"));
   }

}