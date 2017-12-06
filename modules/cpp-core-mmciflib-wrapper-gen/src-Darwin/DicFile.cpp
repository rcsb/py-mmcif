#include <CifFile.h>
#include <CifFileUtil.h>
#include <DicFile.h>
#include <GenString.h>
#include <ISTable.h>
#include <ITTable.h>
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

#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void bind_DicFile(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // DicFile file:DicFile.h line:36
		pybind11::class_<DicFile, std::shared_ptr<DicFile>, CifFile> cl(M(""), "DicFile", "*  \n\n*\n*  \n\n Public class that represents a dictionary file, composed of\n*    blocks with tables.\n*\n*  This class represents a dictionary file. In addition to inherited methods\n*  from  class, this class provides a method for writing the\n*  content of \"item_aliases\" table to a text file.");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](const enum eFileMode  &a0, const class std::__1::basic_string<char> & a1){ return new DicFile(a0, a1); }), "doc");
		cl.def(pybind11::init([](const enum eFileMode  &a0, const class std::__1::basic_string<char> & a1, const bool  &a2){ return new DicFile(a0, a1, a2); }), "doc");
		cl.def(pybind11::init([](const enum eFileMode  &a0, const class std::__1::basic_string<char> & a1, const bool  &a2, const enum Char::eCompareType  &a3){ return new DicFile(a0, a1, a2, a3); }), "doc");
		cl.def(pybind11::init([](const enum eFileMode  &a0, const class std::__1::basic_string<char> & a1, const bool  &a2, const enum Char::eCompareType  &a3, const unsigned int  &a4){ return new DicFile(a0, a1, a2, a3, a4); }), "doc");
		cl.def(pybind11::init<const enum eFileMode, const class std::__1::basic_string<char> &, const bool, const enum Char::eCompareType, const unsigned int, const class std::__1::basic_string<char> &>(), pybind11::arg("fileMode"), pybind11::arg("objFileName"), pybind11::arg("verbose"), pybind11::arg("caseSense"), pybind11::arg("maxLineLength"), pybind11::arg("nullValue"));

		cl.def(pybind11::init([](){ return new DicFile(); }), "doc");
		cl.def(pybind11::init([](const bool  &a0){ return new DicFile(a0); }), "doc");
		cl.def(pybind11::init([](const bool  &a0, const enum Char::eCompareType  &a1){ return new DicFile(a0, a1); }), "doc");
		cl.def(pybind11::init([](const bool  &a0, const enum Char::eCompareType  &a1, const unsigned int  &a2){ return new DicFile(a0, a1, a2); }), "doc");
		cl.def(pybind11::init<const bool, const enum Char::eCompareType, const unsigned int, const class std::__1::basic_string<char> &>(), pybind11::arg("verbose"), pybind11::arg("caseSense"), pybind11::arg("maxLineLength"), pybind11::arg("nullValue"));

		cl.def("Write", [](DicFile &o, class std::__1::basic_ostream<char> & a0, class std::__1::vector<unsigned int, class std::__1::allocator<unsigned int> > & a1) -> void { return o.Write(a0, a1); }, "", pybind11::arg("cifo"), pybind11::arg("tables"));
		cl.def("Write", [](DicFile &o, class std::__1::basic_ostream<char> & a0, class std::__1::vector<unsigned int, class std::__1::allocator<unsigned int> > & a1, const bool  &a2) -> void { return o.Write(a0, a1, a2); }, "", pybind11::arg("cifo"), pybind11::arg("tables"), pybind11::arg("writeEmptyTables"));
		cl.def("Write", [](DicFile &o, class std::__1::basic_ostream<char> & a0, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > & a1) -> void { return o.Write(a0, a1); }, "", pybind11::arg("cifo"), pybind11::arg("catOrder"));
		cl.def("Write", [](DicFile &o, class std::__1::basic_ostream<char> & a0, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > & a1, const bool  &a2) -> void { return o.Write(a0, a1, a2); }, "", pybind11::arg("cifo"), pybind11::arg("catOrder"), pybind11::arg("writeEmptyTables"));
		cl.def("Write", [](DicFile &o, class std::__1::basic_ostream<char> & a0) -> void { return o.Write(a0); }, "", pybind11::arg("outStream"));
		cl.def("Write", [](DicFile &o, class std::__1::basic_ostream<char> & a0, const bool  &a1) -> void { return o.Write(a0, a1); }, "", pybind11::arg("outStream"), pybind11::arg("sortTables"));
		cl.def("Write", [](DicFile &o, class std::__1::basic_ostream<char> & a0, const bool  &a1, const bool  &a2) -> void { return o.Write(a0, a1, a2); }, "", pybind11::arg("outStream"), pybind11::arg("sortTables"), pybind11::arg("writeEmptyTables"));
		cl.def("Write", [](DicFile &o, const class std::__1::basic_string<char> & a0, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > & a1) -> void { return o.Write(a0, a1); }, "", pybind11::arg("cifFileName"), pybind11::arg("tableOrder"));
		cl.def("Write", [](DicFile &o, const class std::__1::basic_string<char> & a0, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > & a1, const bool  &a2) -> void { return o.Write(a0, a1, a2); }, "", pybind11::arg("cifFileName"), pybind11::arg("tableOrder"), pybind11::arg("writeEmptyTables"));
		cl.def("Write", [](DicFile &o, const class std::__1::basic_string<char> & a0) -> void { return o.Write(a0); }, "", pybind11::arg("cifFileName"));
		cl.def("Write", [](DicFile &o, const class std::__1::basic_string<char> & a0, const bool  &a1) -> void { return o.Write(a0, a1); }, "", pybind11::arg("cifFileName"), pybind11::arg("sortTables"));
		cl.def("Write", [](DicFile &o, const class std::__1::basic_string<char> & a0, const bool  &a1, const bool  &a2) -> void { return o.Write(a0, a1, a2); }, "", pybind11::arg("cifFileName"), pybind11::arg("sortTables"), pybind11::arg("writeEmptyTables"));
		cl.def("WriteItemAliases", (void (DicFile::*)(const std::string &)) &DicFile::WriteItemAliases, "*  Writes the content of \"item_aliases\" table to a text file.\n*\n*  \n\n - relative or absolute name of the text file\n*    to which the content of \"item_aliases\" table is to be written to.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: DicFile::WriteItemAliases(const class std::__1::basic_string<char> &) --> void", pybind11::arg("fileName"));
		cl.def("GetFormatTable", (class ISTable * (DicFile::*)()) &DicFile::GetFormatTable, "*  Method, not currently part of users public API, and will soon be\n*  re-examined.\n\nC++: DicFile::GetFormatTable() --> class ISTable *", pybind11::return_value_policy::automatic);
		cl.def("WriteFormatted", [](DicFile &o, const class std::__1::basic_string<char> & a0) -> int { return o.WriteFormatted(a0); }, "", pybind11::arg("cifFileName"));
		cl.def("WriteFormatted", (int (DicFile::*)(const std::string &, class ISTable *)) &DicFile::WriteFormatted, "*  Method, not currently part of users public API, and will soon be\n*  re-examined.\n\nC++: DicFile::WriteFormatted(const class std::__1::basic_string<char> &, class ISTable *) --> int", pybind11::arg("cifFileName"), pybind11::arg("formatP"));
		cl.def("WriteFormatted", [](DicFile &o, const class std::__1::basic_string<char> & a0, class TableFile * a1) -> int { return o.WriteFormatted(a0, a1); }, "", pybind11::arg("cifFileName"), pybind11::arg("ddl"));
		cl.def("WriteFormatted", (int (DicFile::*)(const std::string &, class TableFile *, class ISTable *)) &DicFile::WriteFormatted, "*  Method, not currently part of users public API, and will soon be\n*  re-examined.\n\nC++: DicFile::WriteFormatted(const class std::__1::basic_string<char> &, class TableFile *, class ISTable *) --> int", pybind11::arg("cifFileName"), pybind11::arg("ddl"), pybind11::arg("formatP"));
		cl.def("Compress", (void (DicFile::*)(class CifFile *)) &DicFile::Compress, "*  Method, not currently part of users public API, and will soon be\n*  re-examined.\n\nC++: DicFile::Compress(class CifFile *) --> void", pybind11::arg("ddl"));
		cl.def("GetRefFile", (class CifFile * (DicFile::*)()) &DicFile::GetRefFile, "C++: DicFile::GetRefFile() --> class CifFile *", pybind11::return_value_policy::automatic);
		cl.def("assign", (class DicFile & (DicFile::*)(const class DicFile &)) &DicFile::operator=, "C++: DicFile::operator=(const class DicFile &) --> class DicFile &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	// GetDictFile(class DicFile *, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const bool, const enum eFileMode) file:CifFileUtil.h line:18
	M("").def("GetDictFile", [](class DicFile * a0, const class std::__1::basic_string<char> & a1) -> DicFile * { return GetDictFile(a0, a1); }, "", pybind11::return_value_policy::automatic, pybind11::arg("ddlFileP"), pybind11::arg("dictFileName"));
	M("").def("GetDictFile", [](class DicFile * a0, const class std::__1::basic_string<char> & a1, const class std::__1::basic_string<char> & a2) -> DicFile * { return GetDictFile(a0, a1, a2); }, "", pybind11::return_value_policy::automatic, pybind11::arg("ddlFileP"), pybind11::arg("dictFileName"), pybind11::arg("dictSdbFileName"));
	M("").def("GetDictFile", [](class DicFile * a0, const class std::__1::basic_string<char> & a1, const class std::__1::basic_string<char> & a2, const bool  &a3) -> DicFile * { return GetDictFile(a0, a1, a2, a3); }, "", pybind11::return_value_policy::automatic, pybind11::arg("ddlFileP"), pybind11::arg("dictFileName"), pybind11::arg("dictSdbFileName"), pybind11::arg("verbose"));
	M("").def("GetDictFile", (class DicFile * (*)(class DicFile *, const std::string &, const std::string &, const bool, const enum eFileMode)) &GetDictFile, "C++: GetDictFile(class DicFile *, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const bool, const enum eFileMode) --> class DicFile *", pybind11::return_value_policy::automatic, pybind11::arg("ddlFileP"), pybind11::arg("dictFileName"), pybind11::arg("dictSdbFileName"), pybind11::arg("verbose"), pybind11::arg("fileMode"));

	// CheckDict(class DicFile *, class DicFile *, const class std::__1::basic_string<char> &, const bool) file:CifFileUtil.h line:21
	M("").def("CheckDict", [](class DicFile * a0, class DicFile * a1, const class std::__1::basic_string<char> & a2) -> void { return CheckDict(a0, a1, a2); }, "", pybind11::arg("dictFileP"), pybind11::arg("ddlFileP"), pybind11::arg("dictFileName"));
	M("").def("CheckDict", (void (*)(class DicFile *, class DicFile *, const std::string &, const bool)) &CheckDict, "C++: CheckDict(class DicFile *, class DicFile *, const class std::__1::basic_string<char> &, const bool) --> void", pybind11::arg("dictFileP"), pybind11::arg("ddlFileP"), pybind11::arg("dictFileName"), pybind11::arg("extraDictChecks"));

	// CheckCif(class CifFile *, class DicFile *, const class std::__1::basic_string<char> &, const bool) file:CifFileUtil.h line:23
	M("").def("CheckCif", [](class CifFile * a0, class DicFile * a1, const class std::__1::basic_string<char> & a2) -> void { return CheckCif(a0, a1, a2); }, "", pybind11::arg("cifFileP"), pybind11::arg("dictFileP"), pybind11::arg("cifFileName"));
	M("").def("CheckCif", (void (*)(class CifFile *, class DicFile *, const std::string &, const bool)) &CheckCif, "C++: CheckCif(class CifFile *, class DicFile *, const class std::__1::basic_string<char> &, const bool) --> void", pybind11::arg("cifFileP"), pybind11::arg("dictFileP"), pybind11::arg("cifFileName"), pybind11::arg("extraCifChecks"));

	// ParseDict(const class std::__1::basic_string<char> &, class DicFile *, const bool) file:CifFileUtil.h line:26
	M("").def("ParseDict", [](const class std::__1::basic_string<char> & a0) -> DicFile * { return ParseDict(a0); }, "", pybind11::return_value_policy::automatic, pybind11::arg("dictFileName"));
	M("").def("ParseDict", [](const class std::__1::basic_string<char> & a0, class DicFile * a1) -> DicFile * { return ParseDict(a0, a1); }, "", pybind11::return_value_policy::automatic, pybind11::arg("dictFileName"), pybind11::arg("ddlFileP"));
	M("").def("ParseDict", (class DicFile * (*)(const std::string &, class DicFile *, const bool)) &ParseDict, "C++: ParseDict(const class std::__1::basic_string<char> &, class DicFile *, const bool) --> class DicFile *", pybind11::return_value_policy::automatic, pybind11::arg("dictFileName"), pybind11::arg("ddlFileP"), pybind11::arg("verbose"));

	// ParseCif(const class std::__1::basic_string<char> &, const bool, const enum Char::eCompareType, const unsigned int, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) file:CifFileUtil.h line:28
	M("").def("ParseCif", [](const class std::__1::basic_string<char> & a0) -> CifFile * { return ParseCif(a0); }, "", pybind11::return_value_policy::automatic, pybind11::arg("fileName"));
	M("").def("ParseCif", [](const class std::__1::basic_string<char> & a0, const bool  &a1) -> CifFile * { return ParseCif(a0, a1); }, "", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("verbose"));
	M("").def("ParseCif", [](const class std::__1::basic_string<char> & a0, const bool  &a1, const enum Char::eCompareType  &a2) -> CifFile * { return ParseCif(a0, a1, a2); }, "", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("verbose"), pybind11::arg("caseSense"));
	M("").def("ParseCif", [](const class std::__1::basic_string<char> & a0, const bool  &a1, const enum Char::eCompareType  &a2, const unsigned int  &a3) -> CifFile * { return ParseCif(a0, a1, a2, a3); }, "", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("verbose"), pybind11::arg("caseSense"), pybind11::arg("maxLineLength"));
	M("").def("ParseCif", [](const class std::__1::basic_string<char> & a0, const bool  &a1, const enum Char::eCompareType  &a2, const unsigned int  &a3, const class std::__1::basic_string<char> & a4) -> CifFile * { return ParseCif(a0, a1, a2, a3, a4); }, "", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("verbose"), pybind11::arg("caseSense"), pybind11::arg("maxLineLength"), pybind11::arg("nullValue"));
	M("").def("ParseCif", (class CifFile * (*)(const std::string &, const bool, const enum Char::eCompareType, const unsigned int, const std::string &, const std::string &)) &ParseCif, "C++: ParseCif(const class std::__1::basic_string<char> &, const bool, const enum Char::eCompareType, const unsigned int, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> class CifFile *", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("verbose"), pybind11::arg("caseSense"), pybind11::arg("maxLineLength"), pybind11::arg("nullValue"), pybind11::arg("parseLogFileName"));

	// ParseCifString(const class std::__1::basic_string<char> &, const bool, const enum Char::eCompareType, const unsigned int, const class std::__1::basic_string<char> &) file:CifFileUtil.h line:33
	M("").def("ParseCifString", [](const class std::__1::basic_string<char> & a0) -> CifFile * { return ParseCifString(a0); }, "", pybind11::return_value_policy::automatic, pybind11::arg("cifString"));
	M("").def("ParseCifString", [](const class std::__1::basic_string<char> & a0, const bool  &a1) -> CifFile * { return ParseCifString(a0, a1); }, "", pybind11::return_value_policy::automatic, pybind11::arg("cifString"), pybind11::arg("verbose"));
	M("").def("ParseCifString", [](const class std::__1::basic_string<char> & a0, const bool  &a1, const enum Char::eCompareType  &a2) -> CifFile * { return ParseCifString(a0, a1, a2); }, "", pybind11::return_value_policy::automatic, pybind11::arg("cifString"), pybind11::arg("verbose"), pybind11::arg("caseSense"));
	M("").def("ParseCifString", [](const class std::__1::basic_string<char> & a0, const bool  &a1, const enum Char::eCompareType  &a2, const unsigned int  &a3) -> CifFile * { return ParseCifString(a0, a1, a2, a3); }, "", pybind11::return_value_policy::automatic, pybind11::arg("cifString"), pybind11::arg("verbose"), pybind11::arg("caseSense"), pybind11::arg("maxLineLength"));
	M("").def("ParseCifString", (class CifFile * (*)(const std::string &, const bool, const enum Char::eCompareType, const unsigned int, const std::string &)) &ParseCifString, "C++: ParseCifString(const class std::__1::basic_string<char> &, const bool, const enum Char::eCompareType, const unsigned int, const class std::__1::basic_string<char> &) --> class CifFile *", pybind11::return_value_policy::automatic, pybind11::arg("cifString"), pybind11::arg("verbose"), pybind11::arg("caseSense"), pybind11::arg("maxLineLength"), pybind11::arg("nullValue"));

	// ParseCifSimple(const class std::__1::basic_string<char> &, const bool, const unsigned int, const unsigned int, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) file:CifFileUtil.h line:38
	M("").def("ParseCifSimple", [](const class std::__1::basic_string<char> & a0) -> CifFile * { return ParseCifSimple(a0); }, "", pybind11::return_value_policy::automatic, pybind11::arg("fileName"));
	M("").def("ParseCifSimple", [](const class std::__1::basic_string<char> & a0, const bool  &a1) -> CifFile * { return ParseCifSimple(a0, a1); }, "", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("verbose"));
	M("").def("ParseCifSimple", [](const class std::__1::basic_string<char> & a0, const bool  &a1, const unsigned int  &a2) -> CifFile * { return ParseCifSimple(a0, a1, a2); }, "", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("verbose"), pybind11::arg("intCaseSense"));
	M("").def("ParseCifSimple", [](const class std::__1::basic_string<char> & a0, const bool  &a1, const unsigned int  &a2, const unsigned int  &a3) -> CifFile * { return ParseCifSimple(a0, a1, a2, a3); }, "", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("verbose"), pybind11::arg("intCaseSense"), pybind11::arg("maxLineLength"));
	M("").def("ParseCifSimple", [](const class std::__1::basic_string<char> & a0, const bool  &a1, const unsigned int  &a2, const unsigned int  &a3, const class std::__1::basic_string<char> & a4) -> CifFile * { return ParseCifSimple(a0, a1, a2, a3, a4); }, "", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("verbose"), pybind11::arg("intCaseSense"), pybind11::arg("maxLineLength"), pybind11::arg("nullValue"));
	M("").def("ParseCifSimple", (class CifFile * (*)(const std::string &, const bool, const unsigned int, const unsigned int, const std::string &, const std::string &)) &ParseCifSimple, "C++: ParseCifSimple(const class std::__1::basic_string<char> &, const bool, const unsigned int, const unsigned int, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> class CifFile *", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("verbose"), pybind11::arg("intCaseSense"), pybind11::arg("maxLineLength"), pybind11::arg("nullValue"), pybind11::arg("parseLogFileName"));

}
