#include <CifFile.h>
#include <CifParentChild.h>
#include <GenString.h>
#include <ISTable.h>
#include <ITTable.h>
#include <ParentChild.h>
#include <Serializer.h>
#include <TableFile.h>
#include <__string>
#include <initializer_list>
#include <ios>
#include <iterator>
#include <memory>
#include <ostream>
#include <sstream> // __str__
#include <string>
#include <string_view>
#include <vector>

#include <pybind11/pybind11.h>
#include "pybind11/stl.h"


#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

// ParentChild file:ParentChild.h line:25
struct PyCallBack_ParentChild : public ParentChild {
	using ParentChild::ParentChild;

	void GetParentCifItems(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > & a0, const class std::__1::basic_string<char> & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const ParentChild *>(this), "GetParentCifItems");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"ParentChild::GetParentCifItems\"");
	}
};

// CifParentChild file:CifParentChild.h line:37
struct PyCallBack_CifParentChild : public CifParentChild {
	using CifParentChild::CifParentChild;

	void GetParentCifItems(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > & a0, const class std::__1::basic_string<char> & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifParentChild *>(this), "GetParentCifItems");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return CifParentChild::GetParentCifItems(a0, a1);
	}
};

void bind_TableFile(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // TableFile file:TableFile.h line:366
		pybind11::class_<TableFile, std::shared_ptr<TableFile>> cl(M(""), "TableFile", "*  \n\n*\n*  \n\n Public class that represents a file composed of blocks with tables.\n*\n*  This class represents an ordered container of data blocks. Data blocks can\n*  come from DDL, dictionary or CIF files, where each data block is a\n*  container of tables. This class provides methods for construction and\n*  destruction, data blocks manipulation (addition, retrieval, renaming.).\n*  The class does in-memory management of data blocks, as well as\n*  serialization and de-serialization to and from a file. The class supports\n*  the following file modes: read-only, create, update and virtual. In\n*  read-only mode, blocks and tables can only be read (from an existing table\n*  file that has been previously serialized to a file) and cannot be\n*  modified. Create mode is used to create a table file from scratch and\n*  add/update blocks and tables in it and serialize it to a file. Update mode\n*  is used to update an existing table file (that has been previously\n*  serialized to a file). Virtual mode only provides in-memory management of\n*  data blocks and is used when object persistency is not needed. Hence, all\n*  modes except virtual mode provide association between in-memory data\n*  blocks and persistent data blocks stored in a file.");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](){ return new TableFile(); }), "doc");
		cl.def(pybind11::init<const enum Char::eCompareType>(), pybind11::arg("caseSense"));

		cl.def(pybind11::init([](const enum eFileMode  &a0, const class std::__1::basic_string<char> & a1){ return new TableFile(a0, a1); }), "doc");
		cl.def(pybind11::init<const enum eFileMode, const class std::__1::basic_string<char> &, const enum Char::eCompareType>(), pybind11::arg("fileMode"), pybind11::arg("fileName"), pybind11::arg("caseSense"));

		pybind11::enum_<TableFile::eStatusInd>(cl, "eStatusInd", "")
			.value("eCLEAR_STATUS", TableFile::eStatusInd::eCLEAR_STATUS)
			.value("eDUPLICATE_BLOCKS", TableFile::eStatusInd::eDUPLICATE_BLOCKS)
			.value("eUNNAMED_BLOCKS", TableFile::eStatusInd::eUNNAMED_BLOCKS)
			.export_values();

		cl.def("GetFileName", (std::string (TableFile::*)()) &TableFile::GetFileName, "*  Retrieves the name of the file that persistently holds data blocks\n*  and their tables.\n*\n*  \n\n None\n*\n*  \n\n String that contains the file name.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: TableFile::GetFileName() --> std::string");
		cl.def("GetFileMode", (enum eFileMode (TableFile::*)()) &TableFile::GetFileMode, "*  Retrieves table file mode.\n*\n*  \n\n None\n*\n*  \n\n READ_MODE - if read-only mode\n*  \n\n CREATE_MODE - if create mode\n*  \n\n UPDATE_MODE - if update mode\n*  \n\n VIRTUAL_MODE - if virtual mode\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: TableFile::GetFileMode() --> enum eFileMode");
		cl.def("GetCaseSensitivity", (enum Char::eCompareType (TableFile::*)()) &TableFile::GetCaseSensitivity, "*  Retrieves case sensitivity of table names in blocks.\n*\n*  \n\n None\n*\n*  \n\n eCASE_SENSITIVE - if case sensitive\n*  \n\n eCASE_INSENSITIVE - if case in-sensitive\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: TableFile::GetCaseSensitivity() --> enum Char::eCompareType");
		cl.def("GetStatusInd", (unsigned int (TableFile::*)()) &TableFile::GetStatusInd, "*  Retrieves table file status in form of one or more flags.\n*\n*  \n\n None\n*\n*  \n\n One or more of these flags: \n*    eCLEAR_STATUS - no flag value indicates that there are no flags set \n*    eDUPLICATE_BLOCKS - flag that indicates existence of blocks with\n*    the same name, which are internally stored with different names \n*    eUNNAMED_BLOCKS - flag that indicates existence of blocks with\n*    empty names\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: TableFile::GetStatusInd() --> unsigned int");
		cl.def("GetNumBlocks", (unsigned int (TableFile::*)()) &TableFile::GetNumBlocks, "*  Retrieves the number of data blocks in the table file.\n*\n*  \n\n None\n*\n*  \n\n The number of data blocks in the table file.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: TableFile::GetNumBlocks() --> unsigned int");
		cl.def("GetBlockNames", (void (TableFile::*)(class std::vector<std::string, class std::allocator<std::string > > &)) &TableFile::GetBlockNames, "*  Retrieves data block names.\n*\n*  \n\n - retrieved data block names\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: TableFile::GetBlockNames(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &) --> void", pybind11::arg("blockNames"));
		cl.def("GetFirstBlockName", (std::string (TableFile::*)()) &TableFile::GetFirstBlockName, "*  Retrieves the name of the first data block.\n*\n*  \n\n None\n*\n*  \n\n String that contains the name of the first data block.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: TableFile::GetFirstBlockName() --> std::string");
		cl.def("IsBlockPresent", (bool (TableFile::*)(const std::string &)) &TableFile::IsBlockPresent, "*  Checks for data block existence.\n*\n*  \n\n - the name of the data block\n*\n*  \n\n true - if data block exists\n*  \n\n false - if data block does not exist\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: TableFile::IsBlockPresent(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("blockName"));
		cl.def("AddBlock", (std::string (TableFile::*)(const std::string &)) &TableFile::AddBlock, "*  Adds a block to the table file. If a block with the specified name\n*  already exists, table file stores it under different internal name,\n*  that is obtained by appending a \"#\" symbol and the current block\n*  count. After writing blocks, with these kinds of block names,\n*  to an ASCII file, \"#\" symbol becomes a comment and the text after\n*  it is ignored. This enables the preservation of all duplicate blocks\n*  in the written file.\n*\n*  \n\n - the name of the data block\n*\n*  \n\n String that contains the internally assigned data block name.\n*    This value is different from  if data block with\n*    the name  already exists when this method is invoked.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: TableFile::AddBlock(const class std::__1::basic_string<char> &) --> std::string", pybind11::arg("blockName"));
		cl.def("GetBlock", (class Block & (TableFile::*)(const std::string &)) &TableFile::GetBlock, "*  Retrieves a reference to the data block in the table file.\n*\n*  \n\n - the name of the data block\n*\n*  \n\n Reference to the data block in the table file.\n*\n*  \n\n Data block with name  must be present\n*\n*  \n\n None\n*\n*  \n\n NotFoundException - if data block with name \n    does not exist\n\nC++: TableFile::GetBlock(const class std::__1::basic_string<char> &) --> class Block &", pybind11::return_value_policy::automatic, pybind11::arg("blockName"));
		cl.def("RenameBlock", (std::string (TableFile::*)(const std::string &, const std::string &)) &TableFile::RenameBlock, "*  Changes the data block name.\n*\n*  \n\n - the name of the data block which is to\n*    be renamed\n*  \n\n - the new data block name\n*\n*  \n\n String that contains the internally assigned data block name.\n*    This value is different from  if data block with\n*    the name  already exists when this method is invoked.\n*\n*  \n\n Table file must have at least one data block.\n*  \n\n Data block with name  must be present\n*\n*  \n\n None\n*\n*  \n\n EmptyContainerException - if table file has no data blocks\n*  \n\n NotFoundException - if data block with name \n    does not exist\n\nC++: TableFile::RenameBlock(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> std::string", pybind11::arg("oldBlockName"), pybind11::arg("newBlockName"));
		cl.def("RenameFirstBlock", (std::string (TableFile::*)(const std::string &)) &TableFile::RenameFirstBlock, "*  Changes the name of the first data block in table file.\n*\n*  \n\n - the new data block name\n*\n*  \n\n String that contains the internally assigned data block name.\n*    This value is different from  if data block with\n*    the name  already exists when this method is invoked.\n*\n*  \n\n Table file must have at least one data block.\n*\n*  \n\n None\n*\n*  \n\n EmptyContainerException - if table file has no data blocks\n\nC++: TableFile::RenameFirstBlock(const class std::__1::basic_string<char> &) --> std::string", pybind11::arg("newBlockName"));
		cl.def("Flush", (void (TableFile::*)()) &TableFile::Flush, "*  Writes only the new or modified tables in data blocks to the\n*  associated persistent storage file (specified at table file\n*  construction time).\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n Table file must be in create or update mode\n*\n*  \n\n None\n*\n*  \n\n FileModeException - if table file is not in create or\n*    update mode\n\nC++: TableFile::Flush() --> void");
		cl.def("Serialize", (void (TableFile::*)(const std::string &)) &TableFile::Serialize, "*  Writes all the data blocks and their tables in the specified file.\n*  The inteded purpose of this method is to write to a file different\n*  than the one specified at construction time.\n*\n*  \n\n - relative or absolute name of the file\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: TableFile::Serialize(const class std::__1::basic_string<char> &) --> void", pybind11::arg("fileName"));
		cl.def("Close", (void (TableFile::*)()) &TableFile::Close, "*  Flushes the table file (if in create or update mode) and closes\n*  the associated persistent storage file.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: TableFile::Close() --> void");
		cl.def("assign", (class TableFile & (TableFile::*)(const class TableFile &)) &TableFile::operator=, "C++: TableFile::operator=(const class TableFile &) --> class TableFile &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	{ // ParentChild file:ParentChild.h line:25
		pybind11::class_<ParentChild, std::shared_ptr<ParentChild>, PyCallBack_ParentChild> cl(M(""), "ParentChild", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new PyCallBack_ParentChild(); } ) );
		cl.def("GetLinkGroupIdLabel", (void (ParentChild::*)(std::string &, const class std::vector<std::string, class std::allocator<std::string > > &, const class std::vector<std::string, class std::allocator<std::string > > &)) &ParentChild::GetLinkGroupIdLabel, "C++: ParentChild::GetLinkGroupIdLabel(class std::__1::basic_string<char> &, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &) --> void", pybind11::arg("linkGroupIdLabel"), pybind11::arg("parKeys"), pybind11::arg("childKeys"));
		cl.def("IsParKeyPresent", (bool (ParentChild::*)(const class std::vector<std::string, class std::allocator<std::string > > &, const std::string &)) &ParentChild::IsParKeyPresent, "C++: ParentChild::IsParKeyPresent(const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &, const class std::__1::basic_string<char> &) --> bool", pybind11::arg("parKey"), pybind11::arg("childCatName"));
		cl.def("IsInParentComboKeys", (bool (ParentChild::*)(const std::string &)) &ParentChild::IsInParentComboKeys, "C++: ParentChild::IsInParentComboKeys(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("itemName"));
		cl.def("assign", (class ParentChild & (ParentChild::*)(const class ParentChild &)) &ParentChild::operator=, "C++: ParentChild::operator=(const class ParentChild &) --> class ParentChild &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	{ // CifParentChild file:CifParentChild.h line:37
		pybind11::class_<CifParentChild, std::shared_ptr<CifParentChild>, PyCallBack_CifParentChild, ParentChild> cl(M(""), "CifParentChild", "");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init<class Block &>(), pybind11::arg("block"));

		cl.def(pybind11::init<class Block &, class ISTable *>(), pybind11::arg("block"), pybind11::arg("parChildTableP"));

		cl.def("WriteGroupTables", (void (CifParentChild::*)(class Block &)) &CifParentChild::WriteGroupTables, "C++: CifParentChild::WriteGroupTables(class Block &) --> void", pybind11::arg("block"));
		cl.def("assign", (class CifParentChild & (CifParentChild::*)(const class CifParentChild &)) &CifParentChild::operator=, "C++: CifParentChild::operator=(const class CifParentChild &) --> class CifParentChild &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	{ // CifFile file:CifFile.h line:47
		pybind11::class_<CifFile, std::shared_ptr<CifFile>, TableFile> cl(M(""), "CifFile", "*  \n\n*\n*  \n\n Public class that represents a CIF file, composed of blocks with\n*    tables.\n*\n*  This class represents a CIF file. In addition to inherited methods from\n*   class, this class provides methods for writing the data to\n*  a text file, along with methods for controlling how the data is written,\n*  and a method for verifying the CIF file against dictionary.");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](const enum eFileMode  &a0, const class std::__1::basic_string<char> & a1){ return new CifFile(a0, a1); }), "doc");
		cl.def(pybind11::init([](const enum eFileMode  &a0, const class std::__1::basic_string<char> & a1, const bool  &a2){ return new CifFile(a0, a1, a2); }), "doc");
		cl.def(pybind11::init([](const enum eFileMode  &a0, const class std::__1::basic_string<char> & a1, const bool  &a2, const enum Char::eCompareType  &a3){ return new CifFile(a0, a1, a2, a3); }), "doc");
		cl.def(pybind11::init([](const enum eFileMode  &a0, const class std::__1::basic_string<char> & a1, const bool  &a2, const enum Char::eCompareType  &a3, const unsigned int  &a4){ return new CifFile(a0, a1, a2, a3, a4); }), "doc");
		cl.def(pybind11::init<const enum eFileMode, const class std::__1::basic_string<char> &, const bool, const enum Char::eCompareType, const unsigned int, const class std::__1::basic_string<char> &>(), pybind11::arg("fileMode"), pybind11::arg("fileName"), pybind11::arg("verbose"), pybind11::arg("caseSense"), pybind11::arg("maxLineLength"), pybind11::arg("nullValue"));

		cl.def(pybind11::init([](){ return new CifFile(); }), "doc");
		cl.def(pybind11::init([](const bool  &a0){ return new CifFile(a0); }), "doc");
		cl.def(pybind11::init([](const bool  &a0, const enum Char::eCompareType  &a1){ return new CifFile(a0, a1); }), "doc");
		cl.def(pybind11::init([](const bool  &a0, const enum Char::eCompareType  &a1, const unsigned int  &a2){ return new CifFile(a0, a1, a2); }), "doc");
		cl.def(pybind11::init<const bool, const enum Char::eCompareType, const unsigned int, const class std::__1::basic_string<char> &>(), pybind11::arg("verbose"), pybind11::arg("caseSense"), pybind11::arg("maxLineLength"), pybind11::arg("nullValue"));

		cl.def(pybind11::init([](const bool  &a0, const bool  &a1){ return new CifFile(a0, a1); }), "doc");
		cl.def(pybind11::init([](const bool  &a0, const bool  &a1, const unsigned int  &a2){ return new CifFile(a0, a1, a2); }), "doc");
		cl.def(pybind11::init([](const bool  &a0, const bool  &a1, const unsigned int  &a2, const unsigned int  &a3){ return new CifFile(a0, a1, a2, a3); }), "doc");
		cl.def(pybind11::init<const bool, const bool, const unsigned int, const unsigned int, const class std::__1::basic_string<char> &>(), pybind11::arg("fake"), pybind11::arg("verbose"), pybind11::arg("intCaseSense"), pybind11::arg("maxLineLength"), pybind11::arg("nullValue"));

		pybind11::enum_<CifFile::eQuoting>(cl, "eQuoting", "")
			.value("eSINGLE", CifFile::eQuoting::eSINGLE)
			.value("eDOUBLE", CifFile::eQuoting::eDOUBLE)
			.export_values();

		cl.def_readwrite("_parsingDiags", &CifFile::_parsingDiags);
		cl.def_readwrite("_checkingDiags", &CifFile::_checkingDiags);
		cl.def("SetSrcFileName", (void (CifFile::*)(const std::string &)) &CifFile::SetSrcFileName, "*  Sets file name of a file that was the source of the object data.\n*\n*  \n\n - The name of the source data file.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::SetSrcFileName(const class std::__1::basic_string<char> &) --> void", pybind11::arg("srcFileName"));
		cl.def("GetSrcFileName", (const std::string & (CifFile::*)()) &CifFile::GetSrcFileName, "*  Retrieves source file name.\n*\n*  \n\n None\n*\n*  \n\n - source file name\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::GetSrcFileName() --> const std::string &", pybind11::return_value_policy::automatic);
		cl.def("GetVerbose", (bool (CifFile::*)()) &CifFile::GetVerbose, "*  Retrieves logging option.\n*\n*  \n\n None\n*\n*  \n\n true - if logging is turned on\n*  \n\n false - if logging is turned off\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::GetVerbose() --> bool");
		cl.def("SetSmartPrint", [](CifFile &o) -> void { return o.SetSmartPrint(); }, "");
		cl.def("SetSmartPrint", (void (CifFile::*)(bool)) &CifFile::SetSmartPrint, "*  Sets smart printing option. Smart printing is used to beautify the\n*  output of a written text file.\n*\n*  \n\n - smart printing. If false, smart printing is\n*    disabled. If true, smart printing is enabled. If not specified,\n*    smart printing is enabled.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::SetSmartPrint(bool) --> void", pybind11::arg("smartPrint"));
		cl.def("IsSmartPrint", (bool (CifFile::*)()) &CifFile::IsSmartPrint, "*  Retrieves smart printing option.\n*\n*  \n\n None\n*\n*  \n\n true - if smart printing is enabled\n*  \n\n false - if smart printing is disabled\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::IsSmartPrint() --> bool");
		cl.def("SetQuoting", (void (CifFile::*)(enum CifFile::eQuoting)) &CifFile::SetQuoting, "*  Sets quoting option. This option is used in order to\n*  select the type of quoting to be used in the written text file.\n*\n*  \n\n - type of quoting. If  single quotes are\n*    used. If  double quotes are used.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::SetQuoting(enum CifFile::eQuoting) --> void", pybind11::arg("quoting"));
		cl.def("GetQuoting", (unsigned int (CifFile::*)()) &CifFile::GetQuoting, "*  Retrieves quoting option.\n*\n*  \n\n None\n*\n*  \n\n eSINGLE - if single quotes are used\n*  \n\n eDOUBLE - if double quotes are used\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::GetQuoting() --> unsigned int");
		cl.def("SetLooping", [](CifFile &o, const class std::__1::basic_string<char> & a0) -> void { return o.SetLooping(a0); }, "", pybind11::arg("catName"));
		cl.def("SetLooping", (void (CifFile::*)(const std::string &, bool)) &CifFile::SetLooping, "*  This method is used in order to control how single row categories are\n*  written: in form of a \"loop_\" construct or as an item-value pair.\n*\n*  \n\n - category name\n*  \n\n - category looping option. If false and the\n*    category is a single row category, that category will not be\n*    written with \"loop_\" construct. Otherwise, if true, single row\n*    category will be written with \"loop_\" construct.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::SetLooping(const class std::__1::basic_string<char> &, bool) --> void", pybind11::arg("catName"), pybind11::arg("looping"));
		cl.def("GetLooping", (bool (CifFile::*)(const std::string &)) &CifFile::GetLooping, "*  Retrieves looping option of a category.\n*\n*  \n\n - category name\n*\n*  \n\n - category looping option, as described in SetLooping() method.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::GetLooping(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("catName"));
		cl.def("Write", [](CifFile &o, const class std::__1::basic_string<char> & a0) -> void { return o.Write(a0); }, "", pybind11::arg("cifFileName"));
		cl.def("Write", [](CifFile &o, const class std::__1::basic_string<char> & a0, const bool  &a1) -> void { return o.Write(a0, a1); }, "", pybind11::arg("cifFileName"), pybind11::arg("sortTables"));
		cl.def("Write", (void (CifFile::*)(const std::string &, const bool, const bool)) &CifFile::Write, "*  Writes the data out to a text file.\n*\n*  \n\n - relative or absolute name of the text file\n*    to which the data from  object is to be written to.\n*  \n\n - optional parameter that indicates whether\n*    written tables should be sorted (if true) or not sorted (if false).\n*    If  is not specified, tables are not sorted prior to\n*    writing them.\n*  \n\n - optional parameter that indicates\n*    whether empty tables (0 rows) are to be written (if true) or not\n*    written (if false). If  is not specified, empty\n*    tables are not written.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::Write(const class std::__1::basic_string<char> &, const bool, const bool) --> void", pybind11::arg("cifFileName"), pybind11::arg("sortTables"), pybind11::arg("writeEmptyTables"));
		cl.def("Write", [](CifFile &o, const class std::__1::basic_string<char> & a0, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > & a1) -> void { return o.Write(a0, a1); }, "", pybind11::arg("cifFileName"), pybind11::arg("tableOrder"));
		cl.def("Write", (void (CifFile::*)(const std::string &, const class std::vector<std::string, class std::allocator<std::string > > &, const bool)) &CifFile::Write, "*  Writes the data out to a text file.\n*\n*  \n\n - relative or absolute name of the text file\n*    to which the data from  object is to be written to.\n*  \n\n - vector of table names that indicates the\n*    order of written tables.\n*  \n\n - optional parameter that indicates\n*    whether empty tables (0 rows) are to be written (if true) or not\n*    written (if false). If  is not specified, empty\n*    tables are not written.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::Write(const class std::__1::basic_string<char> &, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &, const bool) --> void", pybind11::arg("cifFileName"), pybind11::arg("tableOrder"), pybind11::arg("writeEmptyTables"));
		cl.def("Write", [](CifFile &o, class std::__1::basic_ostream<char> & a0) -> void { return o.Write(a0); }, "", pybind11::arg("outStream"));
		cl.def("Write", [](CifFile &o, class std::__1::basic_ostream<char> & a0, const bool  &a1) -> void { return o.Write(a0, a1); }, "", pybind11::arg("outStream"), pybind11::arg("sortTables"));
		cl.def("Write", (void (CifFile::*)(std::ostream &, const bool, const bool)) &CifFile::Write, "*  Writes the data out to an output stream.\n*\n*  \n\n - a reference to the output stream\n*  \n\n - optional parameter that indicates whether\n*    written tables should be sorted (if true) or not sorted (if false).\n*    If  is not specified, tables are not sorted prior to\n*    writing them.\n*  \n\n - optional parameter that indicates\n*    whether empty tables (0 rows) are to be written (if true) or not\n*    written (if false). If  is not specified, empty\n*    tables are not written.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::Write(class std::__1::basic_ostream<char> &, const bool, const bool) --> void", pybind11::arg("outStream"), pybind11::arg("sortTables"), pybind11::arg("writeEmptyTables"));
		cl.def("WriteNmrStar", [](CifFile &o, const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1) -> void { return o.WriteNmrStar(a0, a1); }, "", pybind11::arg("nmrStarFileName"), pybind11::arg("globalBlockName"));
		cl.def("WriteNmrStar", [](CifFile &o, const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1, const bool  &a2) -> void { return o.WriteNmrStar(a0, a1, a2); }, "", pybind11::arg("nmrStarFileName"), pybind11::arg("globalBlockName"), pybind11::arg("sortTables"));
		cl.def("WriteNmrStar", (void (CifFile::*)(const std::string &, const std::string &, const bool, const bool)) &CifFile::WriteNmrStar, "*  Writes the data out to a text file in NMR-STAR format.\n*\n*  \n\n - relative or absolute name of the text file\n*    to which the data from  object is to be written to.\n*  \n\n - the name of the global NMR-STAR block.\n*  \n\n - optional parameter that indicates whether\n*    written tables should be sorted (if true) or not sorted (if false).\n*    If  is not specified, tables are not sorted prior to\n*    writing them.\n*  \n\n - optional parameter that indicates\n*    whether empty tables (0 rows) are to be written (if true) or not\n*    written (if false). If  is not specified, empty\n*    tables are not written.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::WriteNmrStar(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const bool, const bool) --> void", pybind11::arg("nmrStarFileName"), pybind11::arg("globalBlockName"), pybind11::arg("sortTables"), pybind11::arg("writeEmptyTables"));
		cl.def("DataChecking", [](CifFile &o, class CifFile & a0, const class std::__1::basic_string<char> & a1) -> int { return o.DataChecking(a0, a1); }, "", pybind11::arg("dicRef"), pybind11::arg("diagFileName"));
		cl.def("DataChecking", [](CifFile &o, class CifFile & a0, const class std::__1::basic_string<char> & a1, const bool  &a2) -> int { return o.DataChecking(a0, a1, a2); }, "", pybind11::arg("dicRef"), pybind11::arg("diagFileName"), pybind11::arg("extraDictChecks"));
		cl.def("DataChecking", (int (CifFile::*)(class CifFile &, const std::string &, const bool, const bool)) &CifFile::DataChecking, "*  Checks a CIF file (all blocks in it) against the dictionary.\n*\n*  \n\n - reference to a dictionary file. The check is\n*    done against the first block in the dictionary file.\n*  \n\n - relative or absolute name of the file,\n*    where diagnostic information is stored.\n*  \n\n - optional parameter that indicates whether\n*    to perform additional, non-standard, dictionary checks. If not\n*    specified, those checks are not performed.\n*  \n\n - optional parameter that indicates whether\n*    to perform additional, non-standard, CIF checks. If not specified,\n*    those checks are not performed.\n*\n*  \n\n 0 - if all checks passed\n*  \n\n different than 0 - if checks failed\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::DataChecking(class CifFile &, const class std::__1::basic_string<char> &, const bool, const bool) --> int", pybind11::arg("dicRef"), pybind11::arg("diagFileName"), pybind11::arg("extraDictChecks"), pybind11::arg("extraCifChecks"));
		cl.def("SetEnumCheck", [](CifFile &o) -> void { return o.SetEnumCheck(); }, "");
		cl.def("SetEnumCheck", (void (CifFile::*)(bool)) &CifFile::SetEnumCheck, "*  Sets enumerations checking option for case-insensitive types.\n*\n*  \n\n - case sensitivity of enumeration values check. If\n*    false, enumeration values of case-insensitive types will be checked\n*    as case-insensitive. If true, enumeration values of case-insensitive\n*    types will be checked as case-sensitive.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::SetEnumCheck(bool) --> void", pybind11::arg("caseSense"));
		cl.def("GetEnumCheck", (bool (CifFile::*)()) &CifFile::GetEnumCheck, "*  Retrieves enumerations checking option for case-insensitive types.\n*\n*  \n\n None\n*\n*  \n\n true - if case-sensitive enumeration check is enabled\n*  \n\n false - if case-insensitive enumeration check is enabled\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::GetEnumCheck() --> bool");
		cl.def("GetParsingDiags", (const std::string & (CifFile::*)()) &CifFile::GetParsingDiags, "*  Gets parsing diagnostics.\n*\n*  \n\n None\n*\n*  \n\n - reference to parsing diagnostics\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::GetParsingDiags() --> const std::string &", pybind11::return_value_policy::automatic);
		cl.def("FindCifNullRows", (void (CifFile::*)(class std::vector<unsigned int, class std::allocator<unsigned int> > &, const class ISTable &)) &CifFile::FindCifNullRows, "*  Finds indices of rows that contain all CIF null values. A CIF null\n*  value is defined as a \"?\" or \"\".\n*\n*  \n\n - vector of null rows indices.\n*  \n\n - table reference\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: CifFile::FindCifNullRows(class std::__1::vector<unsigned int, class std::__1::allocator<unsigned int> > &, const class ISTable &) --> void", pybind11::arg("nullRowsIndices"), pybind11::arg("isTable"));
		cl.def("GetAttributeValue", (void (CifFile::*)(std::string &, const std::string &, const std::string &, const std::string &)) &CifFile::GetAttributeValue, "C++: CifFile::GetAttributeValue(class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("attribVal"), pybind11::arg("blockId"), pybind11::arg("category"), pybind11::arg("attribute"));
		cl.def("GetAttributeValueIf", (void (CifFile::*)(std::string &, const std::string &, const std::string &, const std::string &, const std::string &, const std::string &)) &CifFile::GetAttributeValueIf, "C++: CifFile::GetAttributeValueIf(class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("attribVal"), pybind11::arg("blockId"), pybind11::arg("category"), pybind11::arg("attributeA"), pybind11::arg("attributeB"), pybind11::arg("valB"));
		cl.def("IsAttributeValueDefined", (bool (CifFile::*)(const std::string &, const std::string &, const std::string &)) &CifFile::IsAttributeValueDefined, "C++: CifFile::IsAttributeValueDefined(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> bool", pybind11::arg("blockId"), pybind11::arg("category"), pybind11::arg("attribute"));
		cl.def("SetAttributeValue", [](CifFile &o, const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1, const class std::__1::basic_string<char> & a2, const class std::__1::basic_string<char> & a3) -> void { return o.SetAttributeValue(a0, a1, a2, a3); }, "", pybind11::arg("blockId"), pybind11::arg("category"), pybind11::arg("attribute"), pybind11::arg("value"));
		cl.def("SetAttributeValue", (void (CifFile::*)(const std::string &, const std::string &, const std::string &, const std::string &, const bool)) &CifFile::SetAttributeValue, "C++: CifFile::SetAttributeValue(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const bool) --> void", pybind11::arg("blockId"), pybind11::arg("category"), pybind11::arg("attribute"), pybind11::arg("value"), pybind11::arg("create"));
		cl.def("SetAttributeValueIf", [](CifFile &o, const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1, const class std::__1::basic_string<char> & a2, const class std::__1::basic_string<char> & a3, const class std::__1::basic_string<char> & a4, const class std::__1::basic_string<char> & a5) -> void { return o.SetAttributeValueIf(a0, a1, a2, a3, a4, a5); }, "", pybind11::arg("blockId"), pybind11::arg("category"), pybind11::arg("attributeA"), pybind11::arg("valA"), pybind11::arg("attributeB"), pybind11::arg("valB"));
		cl.def("SetAttributeValueIf", (void (CifFile::*)(const std::string &, const std::string &, const std::string &, const std::string &, const std::string &, const std::string &, const bool)) &CifFile::SetAttributeValueIf, "C++: CifFile::SetAttributeValueIf(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const bool) --> void", pybind11::arg("blockId"), pybind11::arg("category"), pybind11::arg("attributeA"), pybind11::arg("valA"), pybind11::arg("attributeB"), pybind11::arg("valB"), pybind11::arg("create"));
		cl.def("SetAttributeValueIfNull", (void (CifFile::*)(const std::string &, const std::string &, const std::string &, const std::string &)) &CifFile::SetAttributeValueIfNull, "C++: CifFile::SetAttributeValueIfNull(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("blockId"), pybind11::arg("category"), pybind11::arg("attribute"), pybind11::arg("value"));
		cl.def("GetAttributeValues", (void (CifFile::*)(class std::vector<std::string, class std::allocator<std::string > > &, const std::string &, const std::string &, const std::string &)) &CifFile::GetAttributeValues, "C++: CifFile::GetAttributeValues(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("strings"), pybind11::arg("blockId"), pybind11::arg("category"), pybind11::arg("attribute"));
		cl.def("GetAttributeValuesIf", (void (CifFile::*)(class std::vector<std::string, class std::allocator<std::string > > &, const std::string &, const std::string &, const std::string &, const std::string &, const std::string &)) &CifFile::GetAttributeValuesIf, "C++: CifFile::GetAttributeValuesIf(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("strings"), pybind11::arg("blockId"), pybind11::arg("category"), pybind11::arg("attributeA"), pybind11::arg("attributeB"), pybind11::arg("valB"));
		cl.def("SetAttributeValues", (void (CifFile::*)(const std::string &, const std::string &, const std::string &, const class std::vector<std::string, class std::allocator<std::string > > &)) &CifFile::SetAttributeValues, "C++: CifFile::SetAttributeValues(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &) --> void", pybind11::arg("blockId"), pybind11::arg("category"), pybind11::arg("attribute"), pybind11::arg("values"));
		cl.def("assign", (class CifFile & (CifFile::*)(const class CifFile &)) &CifFile::operator=, "C++: CifFile::operator=(const class CifFile &) --> class CifFile &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
}
