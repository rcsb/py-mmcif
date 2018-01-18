// File: ./src/wrapTableFile.cpp
// Date: 2018-01-10
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <set>
#include "rcsb_types.h"
#include "mapped_ptr_vector.h"
#include "mapped_ptr_vector.C"
#include "GenString.h"
#include "ISTable.h"
#include "Serializer.h"
#include "TableFile.h"
namespace py = pybind11;
using namespace pybind11::literals;

#ifndef BINDER_PYBIND11_TYPE_CASTER
    #define BINDER_PYBIND11_TYPE_CASTER
    PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
    PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
    PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void wrapTableFile(py::module &m) {
   m.doc() = "Wrapper for header file TableFile.h";

   {
    py::class_<Block, std::shared_ptr<Block>> cls(m, "Block", "Wrapper for class Block");
   
     cls.def(py::init<const string &, Serializer *, const eFileMode, const Char::eCompareType>(), py::arg("name"), py::arg("serP"), py::arg("fileMode"), py::arg("caseSense"));
     cls.def(py::init([](const string & name,Serializer * serP){ return new Block(name,serP); }), "Generated constructor");
     cls.def(py::init([](const string & name,Serializer * serP,const eFileMode fileMode){ return new Block(name,serP,fileMode); }), "Generated constructor");
     cls.def("__eq__", (vector<pair<string, ISTable::eTableDiff> > (Block::*)(Block &)) &Block::operator==,"operator== with arguments Block &",py::arg("inBlock"));
     cls.def("SetName", &Block::SetName,"",py::arg("name"));
     cls.def("GetName", &Block::GetName,"",py::return_value_policy::reference_internal);
     cls.def("AddTable", (ISTable & (Block::*)(const std::string &, const Char::eCompareType)) &Block::AddTable,"AddTable with arguments const std::string &, const Char::eCompareType",py::return_value_policy::reference_internal,py::arg("name"), py::arg("colCaseSense"));
     cls.def("AddTable", [](Block &o ) -> ISTable & { return o.AddTable(); },"doc",py::return_value_policy::reference_internal);
     cls.def("AddTable", [](Block &o, const std::string & name) -> ISTable & { return o.AddTable(name); },"doc",py::return_value_policy::reference_internal);
     cls.def("RenameTable", &Block::RenameTable,"",py::arg("oldName"), py::arg("newName"));
     cls.def("GetTableNames", [](Block &o , vector<string> & tableNames) {
        o.GetTableNames(tableNames);
       return tableNames;
     },"GetTableNames with arguments tableNames",py::return_value_policy::reference_internal , py::arg("tableNames"));
     cls.def("IsTablePresent", (bool (Block::*)(const string &)) &Block::IsTablePresent,"IsTablePresent with arguments const string &",py::arg("tableName"));
     cls.def("GetTable", &Block::GetTable,"",py::return_value_policy::reference_internal,py::arg("tableName"));
     cls.def("GetTablePtr", &Block::GetTablePtr,"",py::return_value_policy::reference_internal,py::arg("tableName"));
     cls.def("DeleteTable", &Block::DeleteTable,"",py::arg("tableName"));
     cls.def("WriteTable", [](Block &o , ISTable & isTable) {
        o.WriteTable(isTable);
       return isTable;
     },"WriteTable with arguments isTable",py::return_value_policy::reference_internal , py::arg("isTable"));
     cls.def("WriteTable", (void (Block::*)(ISTable *)) &Block::WriteTable,"WriteTable with arguments ISTable *",py::arg("isTableP"));
     cls.def("Print", &Block::Print,"");
     cls.def("_AddTable", (void (Block::*)(const string &, const int, ISTable *)) &Block::_AddTable,"_AddTable with arguments const string &, const int, ISTable *",py::arg("name"), py::arg("indexInFile"), py::arg("isTableP"));
     cls.def("_AddTable", [](Block &o, const string & name) -> void { return o._AddTable(name); },"doc");
     cls.def("_AddTable", [](Block &o, const string & name,const int indexInFile) -> void { return o._AddTable(name,indexInFile); },"doc");
   }

   {
    py::class_<TableFile, std::shared_ptr<TableFile>> cls(m, "TableFile", "Wrapper for class TableFile");
   
      py::enum_<TableFile::eStatusInd>(cls, "eStatusInd")
        .value("eCLEAR_STATUS", TableFile::eStatusInd::eCLEAR_STATUS)
        .value("eDUPLICATE_BLOCKS", TableFile::eStatusInd::eDUPLICATE_BLOCKS)
        .value("eUNNAMED_BLOCKS", TableFile::eStatusInd::eUNNAMED_BLOCKS)
        .export_values();
   
     cls.def(py::init<const Char::eCompareType>(), py::arg("caseSense"));
     cls.def(py::init([](){ return new TableFile(); }), "Generated constructor");
     cls.def(py::init<const eFileMode, const string &, const Char::eCompareType>(), py::arg("fileMode"), py::arg("fileName"), py::arg("caseSense"));
     cls.def(py::init([](const eFileMode fileMode,const string & fileName){ return new TableFile(fileMode,fileName); }), "Generated constructor");
     cls.def("GetFileName", &TableFile::GetFileName,"");
     cls.def("GetFileMode", &TableFile::GetFileMode,"");
     cls.def("GetCaseSensitivity", &TableFile::GetCaseSensitivity,"");
     cls.def("GetStatusInd", &TableFile::GetStatusInd,"");
     cls.def("GetNumBlocks", &TableFile::GetNumBlocks,"");
     cls.def("GetBlockNames", [](TableFile &o , vector<string> & blockNames) {
        o.GetBlockNames(blockNames);
       return blockNames;
     },"GetBlockNames with arguments blockNames",py::return_value_policy::reference_internal , py::arg("blockNames"));
     cls.def("GetFirstBlockName", &TableFile::GetFirstBlockName,"");
     cls.def("IsBlockPresent", (bool (TableFile::*)(const string &)) &TableFile::IsBlockPresent,"IsBlockPresent with arguments const string &",py::arg("blockName"));
     cls.def("AddBlock", &TableFile::AddBlock,"",py::arg("blockName"));
     cls.def("GetBlock", (Block & (TableFile::*)(const string &)) &TableFile::GetBlock,"GetBlock with arguments const string &",py::return_value_policy::reference_internal,py::arg("blockName"));
     cls.def("RenameBlock", &TableFile::RenameBlock,"",py::arg("oldBlockName"), py::arg("newBlockName"));
     cls.def("RenameFirstBlock", &TableFile::RenameFirstBlock,"",py::arg("newBlockName"));
     cls.def("Flush", &TableFile::Flush,"");
     cls.def("Serialize", &TableFile::Serialize,"",py::arg("fileName"));
     cls.def("Close", &TableFile::Close,"");
   }

}