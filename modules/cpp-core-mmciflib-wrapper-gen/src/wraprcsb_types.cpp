// File: ./src/wraprcsb_types.cpp
// Date: 2018-01-10
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "rcsb_types.h"
namespace py = pybind11;
using namespace pybind11::literals;

#ifndef BINDER_PYBIND11_TYPE_CASTER
    #define BINDER_PYBIND11_TYPE_CASTER
    PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
    PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
    PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void wraprcsb_types(py::module &m) {
   m.doc() = "Wrapper for header file rcsb_types.h";

   py::enum_<eTypeCode>(m, "eTypeCode")
     .value("eTYPE_CODE_NONE", eTypeCode::eTYPE_CODE_NONE)
     .value("eTYPE_CODE_INT", eTypeCode::eTYPE_CODE_INT)
     .value("eTYPE_CODE_FLOAT", eTypeCode::eTYPE_CODE_FLOAT)
     .value("eTYPE_CODE_STRING", eTypeCode::eTYPE_CODE_STRING)
     .value("eTYPE_CODE_TEXT", eTypeCode::eTYPE_CODE_TEXT)
     .value("eTYPE_CODE_DATETIME", eTypeCode::eTYPE_CODE_DATETIME)
     .value("eTYPE_CODE_BIGINT", eTypeCode::eTYPE_CODE_BIGINT)
     .export_values();

}