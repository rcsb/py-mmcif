// File: ./src/wrapISTable.cpp
// Date: 2018-01-10
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <float.h>
#include <string>
#include <vector>
#include <map>
#include "mapped_vector.h"
#include "mapped_vector.C"
#include "GenString.h"
#include "ITTable.h"
#include "Serializer.h"
#include "ISTable.h"
namespace py = pybind11;
using namespace pybind11::literals;

#ifndef BINDER_PYBIND11_TYPE_CASTER
    #define BINDER_PYBIND11_TYPE_CASTER
    PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
    PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
    PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void wrapISTable(py::module &m) {
   m.doc() = "Wrapper for header file ISTable.h";

   {
    py::class_<ISTable, std::shared_ptr<ISTable>> cls(m, "ISTable", "Wrapper for class ISTable");
   
      py::enum_<ISTable::eTableDiff>(cls, "eTableDiff")
        .value("eNONE", ISTable::eTableDiff::eNONE)
        .value("eCASE_SENSE", ISTable::eTableDiff::eCASE_SENSE)
        .value("eMORE_COLS", ISTable::eTableDiff::eMORE_COLS)
        .value("eLESS_COLS", ISTable::eTableDiff::eLESS_COLS)
        .value("eCOL_NAMES", ISTable::eTableDiff::eCOL_NAMES)
        .value("eMORE_ROWS", ISTable::eTableDiff::eMORE_ROWS)
        .value("eLESS_ROWS", ISTable::eTableDiff::eLESS_ROWS)
        .value("eCELLS", ISTable::eTableDiff::eCELLS)
        .value("eMISSING", ISTable::eTableDiff::eMISSING)
        .value("eEXTRA", ISTable::eTableDiff::eEXTRA)
        .export_values();
   
      py::enum_<ISTable::eSearchType>(cls, "eSearchType")
        .value("eEQUAL", ISTable::eSearchType::eEQUAL)
        .value("eLESS_THAN", ISTable::eSearchType::eLESS_THAN)
        .value("eLESS_THAN_OR_EQUAL", ISTable::eSearchType::eLESS_THAN_OR_EQUAL)
        .value("eGREATER_THAN", ISTable::eSearchType::eGREATER_THAN)
        .value("eGREATER_THAN_OR_EQUAL", ISTable::eSearchType::eGREATER_THAN_OR_EQUAL)
        .export_values();
   
      py::enum_<ISTable::eSearchDir>(cls, "eSearchDir")
        .value("eFORWARD", ISTable::eSearchDir::eFORWARD)
        .value("eBACKWARD", ISTable::eSearchDir::eBACKWARD)
        .export_values();
   
     cls.def(py::init<const Char::eCompareType>(), py::arg("colCaseSense"));
     cls.def(py::init([](){ return new ISTable(); }), "Generated constructor");
     cls.def(py::init<ITTable::eOrientation, const Char::eCompareType>(), py::arg("orient"), py::arg("colCaseSense"));
     cls.def(py::init([](ITTable::eOrientation orient){ return new ISTable(orient); }), "Generated constructor");
     cls.def(py::init<const std::string &, const Char::eCompareType>(), py::arg("name"), py::arg("colCaseSense"));
     cls.def(py::init([](const std::string & name){ return new ISTable(name); }), "Generated constructor");
     cls.def(py::init<const std::string &, ITTable::eOrientation, const Char::eCompareType>(), py::arg("name"), py::arg("orient"), py::arg("colCaseSense"));
     cls.def(py::init([](const std::string & name,ITTable::eOrientation orient){ return new ISTable(name,orient); }), "Generated constructor");
     cls.def(py::init<ISTable const &>(), py::arg("inTable"));
     cls.def("assign", (ISTable & (ISTable::*)(const ISTable &)) &ISTable::operator=,"operator= with arguments const ISTable &",py::return_value_policy::reference_internal,py::arg("inTable"));
     cls.def("__eq__", (ISTable::eTableDiff (ISTable::*)(ISTable &)) &ISTable::operator==,"operator== with arguments ISTable &",py::arg("inTable"));
     cls.def("GetName", &ISTable::GetName,"",py::return_value_policy::reference_internal);
     cls.def("SetName", &ISTable::SetName,"",py::arg("name"));
     cls.def("GetNumColumns", &ISTable::GetNumColumns,"");
     cls.def("GetColumnNames", &ISTable::GetColumnNames,"",py::return_value_policy::reference_internal);
     cls.def("IsColumnPresent", (bool (ISTable::*)(const std::string &)) &ISTable::IsColumnPresent,"IsColumnPresent with arguments const std::string &",py::arg("colName"));
     cls.def("AddColumn", (void (ISTable::*)(const std::string &, const std::vector<std::string> &)) &ISTable::AddColumn,"AddColumn with arguments const std::string &, const std::vector<std::string> &",py::arg("colName"), py::arg("col"));
     cls.def("AddColumn", [](ISTable &o, const std::string & colName) -> void { return o.AddColumn(colName); },"doc");
     cls.def("InsertColumn", (void (ISTable::*)(const std::string &, const std::string &, const std::vector<std::string> &)) &ISTable::InsertColumn,"InsertColumn with arguments const std::string &, const std::string &, const std::vector<std::string> &",py::arg("colName"), py::arg("afColName"), py::arg("col"));
     cls.def("InsertColumn", [](ISTable &o, const std::string & colName,const std::string & afColName) -> void { return o.InsertColumn(colName,afColName); },"doc");
     cls.def("FillColumn", &ISTable::FillColumn,"",py::arg("colName"), py::arg("col"));
     cls.def("GetColumn", [](ISTable &o , std::vector<std::string> & col, const std::string & colName) {
        o.GetColumn(col, colName);
       return col;
     },"GetColumn with arguments col, colName",py::return_value_policy::reference_internal , py::arg("col"), py::arg("colName"));
     cls.def("GetColumn", [](ISTable &o , std::vector<std::string> & col, const std::string & colName, const unsigned int fromRowIndex, unsigned int toRowIndex) {
        o.GetColumn(col, colName, fromRowIndex, toRowIndex);
       return col;
     },"GetColumn with arguments col, colName, fromRowIndex, toRowIndex",py::return_value_policy::reference_internal , py::arg("col"), py::arg("colName"), py::arg("fromRowIndex"), py::arg("toRowIndex"));
     cls.def("GetColumn", [](ISTable &o , std::vector<std::string> & col, const std::string & colName, const std::vector<unsigned int> & rowIndex) {
        o.GetColumn(col, colName, rowIndex);
       return col;
     },"GetColumn with arguments col, colName, rowIndex",py::return_value_policy::reference_internal , py::arg("col"), py::arg("colName"), py::arg("rowIndex"));
     cls.def("GetColumn", [](ISTable &o , std::vector<std::string> & col, const std::string & colName, const std::string & indexName) {
        o.GetColumn(col, colName, indexName);
       return col;
     },"GetColumn with arguments col, colName, indexName",py::return_value_policy::reference_internal , py::arg("col"), py::arg("colName"), py::arg("indexName"));
     cls.def("RenameColumn", &ISTable::RenameColumn,"",py::arg("oldColName"), py::arg("newColName"));
     cls.def("ClearColumn", &ISTable::ClearColumn,"",py::arg("colName"));
     cls.def("DeleteColumn", &ISTable::DeleteColumn,"",py::arg("colName"));
     cls.def("GetNumRows", &ISTable::GetNumRows,"");
     cls.def("AddRow", (unsigned int (ISTable::*)(const std::vector<std::string> &)) &ISTable::AddRow,"AddRow with arguments const std::vector<std::string> &",py::arg("row"));
     cls.def("AddRow", [](ISTable &o ) -> unsigned int { return o.AddRow(); },"doc");
     cls.def("InsertRow", (unsigned int (ISTable::*)(const unsigned int, const std::vector<std::string> &)) &ISTable::InsertRow,"InsertRow with arguments const unsigned int, const std::vector<std::string> &",py::arg("atRowIndex"), py::arg("row"));
     cls.def("InsertRow", [](ISTable &o, const unsigned int atRowIndex) -> unsigned int { return o.InsertRow(atRowIndex); },"doc");
     cls.def("FillRow", &ISTable::FillRow,"",py::arg("rowIndex"), py::arg("row"));
     cls.def("GetRow", [](ISTable &o , std::vector<std::string> & row, const unsigned int rowIndex, const std::string & fromColName, const std::string & toColName) {
        o.GetRow(row, rowIndex, fromColName, toColName);
       return row;
     },"GetRow with arguments row, rowIndex, fromColName, toColName",py::return_value_policy::reference_internal , py::arg("row"), py::arg("rowIndex"), py::arg("fromColName"), py::arg("toColName"));
     cls.def("GetRow", (const std::vector<std::string> & (ISTable::*)(const unsigned int)) &ISTable::GetRow,"GetRow with arguments const unsigned int",py::return_value_policy::reference_internal,py::arg("rowIndex"));
     cls.def("ClearRow", &ISTable::ClearRow,"",py::arg("rowIndex"));
     cls.def("DeleteRow", &ISTable::DeleteRow,"",py::arg("rowIndex"));
     cls.def("DeleteRows", &ISTable::DeleteRows,"",py::arg("rows"));
     cls.def("GetLastRowIndex", &ISTable::GetLastRowIndex,"");
     cls.def("UpdateCell", (void (ISTable::*)(const unsigned int, const std::string &, const std::string &)) &ISTable::UpdateCell,"UpdateCell with arguments const unsigned int, const std::string &, const std::string &",py::arg("rowIndex"), py::arg("colName"), py::arg("value"));
     cls.def("__call__", (const std::string & (ISTable::*)(const unsigned int, const std::string &) const ) &ISTable::operator(),"operator() with arguments const unsigned int, const std::string &",py::return_value_policy::reference_internal,py::arg("rowIndex"), py::arg("colName"));
     cls.def("SetFlags", (void (ISTable::*)(const std::string &, const unsigned char)) &ISTable::SetFlags,"SetFlags with arguments const std::string &, const unsigned char",py::arg("colName"), py::arg("flags"));
     cls.def("GetDataType", &ISTable::GetDataType,"",py::arg("colName"));
     cls.def("FindFirst", (unsigned int (ISTable::*)(const std::vector<std::string> &, const std::vector<std::string> &, const std::string &)) &ISTable::FindFirst,"FindFirst with arguments const std::vector<std::string> &, const std::vector<std::string> &, const std::string &",py::arg("targets"), py::arg("colNames"), py::arg("indexName"));
     cls.def("FindFirst", [](ISTable &o, const std::vector<std::string> & targets,const std::vector<std::string> & colNames) -> unsigned int { return o.FindFirst(targets,colNames); },"doc");
     cls.def("Search", [](ISTable &o , std::vector<unsigned int> & res, const std::string & target, const std::string & colName, const unsigned int fromRowIndex, const ISTable::eSearchDir searchDir, const ISTable::eSearchType searchType) {
        o.Search(res, target, colName, fromRowIndex, searchDir, searchType);
       return res;
     },"Search with arguments res, target, colName, fromRowIndex, searchDir, searchType",py::return_value_policy::reference_internal , py::arg("res"), py::arg("target"), py::arg("colName"), py::arg("fromRowIndex"), py::arg("searchDir"), py::arg("searchType"));
     cls.def("Search", [](ISTable &o , std::vector<unsigned int> & res, const std::vector<std::string> & targets, const std::vector<std::string> & colNames, const unsigned int fromRowIndex, const ISTable::eSearchDir searchDir, const ISTable::eSearchType searchType, const std::string & indexName) {
        o.Search(res, targets, colNames, fromRowIndex, searchDir, searchType, indexName);
       return res;
     },"Search with arguments res, targets, colNames, fromRowIndex, searchDir, searchType, indexName",py::return_value_policy::reference_internal , py::arg("res"), py::arg("targets"), py::arg("colNames"), py::arg("fromRowIndex"), py::arg("searchDir"), py::arg("searchType"), py::arg("indexName"));
     cls.def("FindDuplicateRows", [](ISTable &o , std::vector<std::pair<unsigned int, unsigned int> > & duplRows, const std::vector<std::string> & colNames, const bool keepDuplRows, const ISTable::eSearchDir searchDir) {
        o.FindDuplicateRows(duplRows, colNames, keepDuplRows, searchDir);
       return duplRows;
     },"FindDuplicateRows with arguments duplRows, colNames, keepDuplRows, searchDir",py::return_value_policy::reference_internal , py::arg("duplRows"), py::arg("colNames"), py::arg("keepDuplRows"), py::arg("searchDir"));
     cls.def("GetColCaseSense", &ISTable::GetColCaseSense,"");
     cls.def("SetModified", &ISTable::SetModified,"",py::arg("modified"));
     cls.def("GetModified", (bool (ISTable::*)()) &ISTable::GetModified,"GetModified with arguments ");
     cls.def("SetSerializer", &ISTable::SetSerializer,"",py::arg("ser"));
     cls.def("WriteObject", [](ISTable &o , Serializer * ser, int & size) {
       int _retVal =  o.WriteObject(ser, size);
       return std::make_tuple(_retVal, ser, size);
     },"WriteObject with arguments ser, size",py::return_value_policy::reference_internal , py::arg("ser"), py::arg("size"));
     cls.def("GetObject", &ISTable::GetObject,"",py::arg("index"), py::arg("ser"));
     cls.def("Read", &ISTable::Read,"",py::arg("indexInFile"));
     cls.def("Write", &ISTable::Write,"");
     cls.def("PrintDiff", [](ISTable &o , ISTable & inTable) {
       bool _retVal =  o.PrintDiff(inTable);
       return std::make_tuple(_retVal, inTable);
     },"PrintDiff with arguments inTable",py::return_value_policy::reference_internal , py::arg("inTable"));
     cls.def("IndexExists", (bool (ISTable::*)(const std::string &)) &ISTable::IndexExists,"IndexExists with arguments const std::string &",py::arg("indexName"));
     cls.def("CreateIndex", (void (ISTable::*)(const std::string &, const std::vector<std::string> &, const unsigned int)) &ISTable::CreateIndex,"CreateIndex with arguments const std::string &, const std::vector<std::string> &, const unsigned int",py::arg("indexName"), py::arg("colNames"), py::arg("unique"));
     cls.def("CreateIndex", [](ISTable &o, const std::string & indexName,const std::vector<std::string> & colNames) -> void { return o.CreateIndex(indexName,colNames); },"doc");
     cls.def("DeleteIndex", (void (ISTable::*)(const std::string &)) &ISTable::DeleteIndex,"DeleteIndex with arguments const std::string &",py::arg("indexName"));
     cls.def("GetNumIndices", &ISTable::GetNumIndices,"");
     cls.def("CreateKey", (void (ISTable::*)(const std::vector<std::string> &)) &ISTable::CreateKey,"CreateKey with arguments const std::vector<std::string> &",py::arg("colNames"));
     cls.def("DeleteKey", &ISTable::DeleteKey,"");
     cls.def("GetColumnsIndices", [](ISTable &o , std::vector<unsigned int> & colIndices, const std::vector<std::string> & colNames) {
        o.GetColumnsIndices(colIndices, colNames);
       return colIndices;
     },"GetColumnsIndices with arguments colIndices, colNames",py::return_value_policy::reference_internal , py::arg("colIndices"), py::arg("colNames"));
   }

}