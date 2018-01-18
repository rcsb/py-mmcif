// File: ./src/wrapDictDataInfo.cpp
// Date: 2018-01-10
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include <vector>
#include "DataInfo.h"
#include "DictObjCont.h"
#include "DictDataInfo.h"
namespace py = pybind11;
using namespace pybind11::literals;

#ifndef BINDER_PYBIND11_TYPE_CASTER
    #define BINDER_PYBIND11_TYPE_CASTER
    PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
    PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
    PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void wrapDictDataInfo(py::module &m) {
   m.doc() = "Wrapper for header file DictDataInfo.h";

   {
    py::class_<DictDataInfo, std::shared_ptr<DictDataInfo>> cls(m, "DictDataInfo", "Wrapper for class DictDataInfo");
   
     cls.def(py::init<const DictObjCont &>(), py::arg("dictObjCont"));
     cls.def("GetVersion", [](DictDataInfo &o , std::string & version) {
        o.GetVersion(version);
       return version;
     },"GetVersion with arguments version",py::return_value_policy::reference_internal , py::arg("version"));
     cls.def("GetItemsNames", &DictDataInfo::GetItemsNames,"",py::return_value_policy::reference_internal);
     cls.def("IsCatDefined", (bool (DictDataInfo::*)(const std::string &) const ) &DictDataInfo::IsCatDefined,"IsCatDefined with arguments const std::string &",py::arg("catName"));
     cls.def("IsItemDefined", (bool (DictDataInfo::*)(const std::string &)) &DictDataInfo::IsItemDefined,"IsItemDefined with arguments const std::string &",py::arg("itemName"));
     cls.def("GetCatKeys", &DictDataInfo::GetCatKeys,"",py::return_value_policy::reference_internal,py::arg("catName"));
     cls.def("GetCatAttribute", &DictDataInfo::GetCatAttribute,"",py::return_value_policy::reference_internal,py::arg("catName"), py::arg("refCatName"), py::arg("refAttrName"));
     cls.def("GetItemAttribute", &DictDataInfo::GetItemAttribute,"",py::return_value_policy::reference_internal,py::arg("itemName"), py::arg("refCatName"), py::arg("refAttrName"));
   }

}