// File: ./src/wrapmmciflib.cpp
// Date: 2018-01-10
//
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py = pybind11;
using namespace pybind11::literals;

void wraprcsb_types(py::module &);
void wrapCifDataInfo(py::module &);
void wrapDictDataInfo(py::module &);
void wrapISTable(py::module &);
void wrapTableFile(py::module &);
void wrapCifFileUtil(py::module &);
void wrapCifFileReadDef(py::module &);
void wrapCifFile(py::module &);
void wrapDicFile(py::module &);

PYBIND11_MODULE(mmciflib, m) {
wraprcsb_types(m);
wrapCifDataInfo(m);
wrapDictDataInfo(m);
wrapISTable(m);
wrapTableFile(m);
wrapCifFileUtil(m);
wrapCifFileReadDef(m);
wrapCifFile(m);
wrapDicFile(m);
}
