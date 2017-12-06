#include <CifFileReadDef.h>
#include <GenString.h>
#include <__string>
#include <initializer_list>
#include <iterator>
#include <memory>
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

void bind_CifFileReadDef(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	// type file:CifFileReadDef.h line:29
	pybind11::enum_<type>(M(""), "type", "")
		.value("A", type::A)
		.value("D", type::D)
		.export_values();

;

	{ // CifFileReadDef file:CifFileReadDef.h line:38
		pybind11::class_<CifFileReadDef, std::shared_ptr<CifFileReadDef>> cl(M(""), "CifFileReadDef", "* \n\n*\n* \n\n Private class that represents a CIF parser controller.");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > >  const &a0, class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > >  const &a1){ return new CifFileReadDef(a0, a1); }), "doc");
		cl.def(pybind11::init([](class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > >  const &a0, class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > >  const &a1, enum type  const &a2){ return new CifFileReadDef(a0, a1, a2); }), "doc");
		cl.def(pybind11::init<class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > >, class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > >, enum type, enum type>(), pybind11::arg("dblist"), pybind11::arg("clist"), pybind11::arg("dbtype"), pybind11::arg("ctype"));

		cl.def( pybind11::init( [](){ return new CifFileReadDef(); } ) );
		cl.def("SetDataBlockList", [](CifFileReadDef &o, class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > >  const &a0) -> void { return o.SetDataBlockList(a0); }, "", pybind11::arg("dblist"));
		cl.def("SetDataBlockList", (void (CifFileReadDef::*)(class std::vector<std::string, class std::allocator<std::string > >, enum type)) &CifFileReadDef::SetDataBlockList, "C++: CifFileReadDef::SetDataBlockList(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > >, enum type) --> void", pybind11::arg("dblist"), pybind11::arg("dbtype"));
		cl.def("SetCategoryList", [](CifFileReadDef &o, class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > >  const &a0) -> void { return o.SetCategoryList(a0); }, "", pybind11::arg("clist"));
		cl.def("SetCategoryList", (void (CifFileReadDef::*)(class std::vector<std::string, class std::allocator<std::string > >, enum type)) &CifFileReadDef::SetCategoryList, "C++: CifFileReadDef::SetCategoryList(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > >, enum type) --> void", pybind11::arg("clist"), pybind11::arg("ctype"));
		cl.def("SetDataBlockListType", [](CifFileReadDef &o) -> void { return o.SetDataBlockListType(); }, "");
		cl.def("SetDataBlockListType", (void (CifFileReadDef::*)(enum type)) &CifFileReadDef::SetDataBlockListType, "C++: CifFileReadDef::SetDataBlockListType(enum type) --> void", pybind11::arg("dbtype"));
		cl.def("SetCategoryListType", [](CifFileReadDef &o) -> void { return o.SetCategoryListType(); }, "");
		cl.def("SetCategoryListType", (void (CifFileReadDef::*)(enum type)) &CifFileReadDef::SetCategoryListType, "C++: CifFileReadDef::SetCategoryListType(enum type) --> void", pybind11::arg("ctype"));
		cl.def("AreAllCatsRead", (int (CifFileReadDef::*)()) &CifFileReadDef::AreAllCatsRead, "C++: CifFileReadDef::AreAllCatsRead() --> int");
		cl.def("IncreaseNumReadCats", (void (CifFileReadDef::*)()) &CifFileReadDef::IncreaseNumReadCats, "C++: CifFileReadDef::IncreaseNumReadCats() --> void");
		cl.def("Category_OK", (int (CifFileReadDef::*)(const std::string &)) &CifFileReadDef::Category_OK, "C++: CifFileReadDef::Category_OK(const class std::__1::basic_string<char> &) --> int", pybind11::arg("categoryName"));
		cl.def("Datablock_OK", (int (CifFileReadDef::*)(const std::string &)) &CifFileReadDef::Datablock_OK, "C++: CifFileReadDef::Datablock_OK(const class std::__1::basic_string<char> &) --> int", pybind11::arg("datablockName"));
	}
	{ // Char file:GenString.h line:23
		pybind11::class_<Char, std::shared_ptr<Char>> cl(M(""), "Char", "* \n\n*\n* \n\n Generic character class that contains character related methods.\n*\n* This class is a static class that contains generic character related utility\n* methods.");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Char(); } ) );
		pybind11::enum_<Char::eCompareType>(cl, "eCompareType", "")
			.value("eCASE_SENSITIVE", Char::eCompareType::eCASE_SENSITIVE)
			.value("eCASE_INSENSITIVE", Char::eCompareType::eCASE_INSENSITIVE)
			.value("eWS_INSENSITIVE", Char::eCompareType::eWS_INSENSITIVE)
			.value("eAS_INTEGER", Char::eCompareType::eAS_INTEGER)
			.export_values();

		cl.def_static("ToLower", (char (*)(const char)) &Char::ToLower, "C++: Char::ToLower(const char) --> char", pybind11::arg("c"));
		cl.def_static("ToUpper", (char (*)(const char)) &Char::ToUpper, "C++: Char::ToUpper(const char) --> char", pybind11::arg("c"));
		cl.def_static("IsCiLess", (bool (*)(const char, const char)) &Char::IsCiLess, "C++: Char::IsCiLess(const char, const char) --> bool", pybind11::arg("c1"), pybind11::arg("c2"));
		cl.def_static("IsWhiteSpace", (bool (*)(const char)) &Char::IsWhiteSpace, "C++: Char::IsWhiteSpace(const char) --> bool", pybind11::arg("c"));
		cl.def_static("IsDigit", (bool (*)(const char)) &Char::IsDigit, "C++: Char::IsDigit(const char) --> bool", pybind11::arg("c"));
		cl.def_static("IsCarriageReturn", (bool (*)(const char)) &Char::IsCarriageReturn, "C++: Char::IsCarriageReturn(const char) --> bool", pybind11::arg("c"));
		cl.def_static("IsPrintable", (bool (*)(const char)) &Char::IsPrintable, "C++: Char::IsPrintable(const char) --> bool", pybind11::arg("c"));
		cl.def_static("AsciiCodeInHex", (void (*)(const char, std::string &)) &Char::AsciiCodeInHex, "C++: Char::AsciiCodeInHex(const char, class std::__1::basic_string<char> &) --> void", pybind11::arg("c"), pybind11::arg("asciiHexString"));
	}
	{ // CharLess file:GenString.h line:56
		pybind11::class_<CharLess, std::shared_ptr<CharLess>> cl(M(""), "CharLess", "* \n\n*\n* \n\n Public class that encapsulates character comparison.\n*\n* This class encapsulates character comparison. It supports the following\n* compare types: case-sensitive and case-insensitive.");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](){ return new CharLess(); }), "doc");
		cl.def(pybind11::init<enum Char::eCompareType>(), pybind11::arg("compareType"));

		cl.def("assign", (class CharLess & (CharLess::*)(const class CharLess &)) &CharLess::operator=, "C++: CharLess::operator=(const class CharLess &) --> class CharLess &", pybind11::return_value_policy::automatic, pybind11::arg("in"));
		cl.def("__call__", (bool (CharLess::*)(const char, const char) const) &CharLess::operator(), "C++: CharLess::operator()(const char, const char) const --> bool", pybind11::arg("c1"), pybind11::arg("c2"));
	}
}
