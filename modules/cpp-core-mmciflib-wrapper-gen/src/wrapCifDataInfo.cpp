// File: ./src/wrapCifDataInfo.cpp
// Date: 2018-01-10
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include <vector>
#include "DataInfo.h"
#include "DicFile.h"
#include "CifDataInfo.h"
namespace py = pybind11;
using namespace pybind11::literals;

#ifndef BINDER_PYBIND11_TYPE_CASTER
    #define BINDER_PYBIND11_TYPE_CASTER
    PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
    PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
    PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void wrapCifDataInfo(py::module &m) {
   m.doc() = "Wrapper for header file CifDataInfo.h";

   {
    py::class_<CifDataInfo, std::shared_ptr<CifDataInfo>> cls(m, "CifDataInfo", "Wrapper for class CifDataInfo");
   
     cls.def(py::init<DicFile &>(), py::arg("dictFile"));
     cls.def("GetVersion", [](CifDataInfo &o , std::string & version) {
        o.GetVersion(version);
       return version;
     },"GetVersion with arguments version",py::return_value_policy::reference_internal , py::arg("version"));
     cls.def("GetCatNames", &CifDataInfo::GetCatNames,"",py::return_value_policy::reference_internal);
     cls.def("GetItemsNames", &CifDataInfo::GetItemsNames,"",py::return_value_policy::reference_internal);
     cls.def("IsCatDefined", (bool (CifDataInfo::*)(const std::string &) const ) &CifDataInfo::IsCatDefined,"IsCatDefined with arguments const std::string &",py::arg("catName"));
     cls.def("IsItemDefined", (bool (CifDataInfo::*)(const std::string &)) &CifDataInfo::IsItemDefined,"IsItemDefined with arguments const std::string &",py::arg("itemName"));
     cls.def("GetCatKeys", &CifDataInfo::GetCatKeys,"",py::return_value_policy::reference_internal,py::arg("catName"));
     cls.def("GetCatAttribute", &CifDataInfo::GetCatAttribute,"",py::return_value_policy::reference_internal,py::arg("catName"), py::arg("refCatName"), py::arg("refAttrName"));
     cls.def("GetItemAttribute", &CifDataInfo::GetItemAttribute,"",py::return_value_policy::reference_internal,py::arg("itemName"), py::arg("refCatName"), py::arg("refAttrName"));
   }

}