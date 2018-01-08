#include <GenString.h>
#include <__string>
#include <initializer_list>
#include <iterator>
#include <memory>
#include <sstream> // __str__
#include <string>
#include <string_view>

#include <pybind11/pybind11.h>
#include "pybind11/stl.h"


#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void bind_GenString(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // WhiteSpace file:GenString.h line:96
		pybind11::class_<WhiteSpace, std::shared_ptr<WhiteSpace>, std::unary_function<char,bool>> cl(M(""), "WhiteSpace", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new WhiteSpace(); } ) );
		cl.def("__call__", (bool (WhiteSpace::*)(const char) const) &WhiteSpace::operator(), "C++: WhiteSpace::operator()(const char) const --> bool", pybind11::arg("c"));
		cl.def("__call__", (bool (WhiteSpace::*)(const char, const char) const) &WhiteSpace::operator(), "C++: WhiteSpace::operator()(const char, const char) const --> bool", pybind11::arg("c1"), pybind11::arg("c2"));
	}
	{ // StringLess file:GenString.h line:112
		pybind11::class_<StringLess, std::shared_ptr<StringLess>> cl(M(""), "StringLess", "* \n\n*\n* \n\n Public class that encapsulates string comparison.\n*\n* This class encapsulates string comparison. It supports the following\n* compare types: case-sensitive, case-insensitive and as-integer.");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](){ return new StringLess(); }), "doc");
		cl.def(pybind11::init<enum Char::eCompareType>(), pybind11::arg("compareType"));

		cl.def(pybind11::init<StringLess const &>());
		cl.def("assign", (class StringLess & (StringLess::*)(const class StringLess &)) &StringLess::operator=, "C++: StringLess::operator=(const class StringLess &) --> class StringLess &", pybind11::return_value_policy::automatic, pybind11::arg("in"));
		cl.def("__call__", (bool (StringLess::*)(const std::string &, const std::string &) const) &StringLess::operator(), "C++: StringLess::operator()(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) const --> bool", pybind11::arg("s1"), pybind11::arg("s2"));
	}
	{ // StringEqualTo file:GenString.h line:136
		pybind11::class_<StringEqualTo, std::shared_ptr<StringEqualTo>, std::binary_function<std::string,std::string,bool>> cl(M(""), "StringEqualTo", "* \n\n*\n* \n\n Public class that encapsulates generic string equal_to functor.\n*\n* This class is equal_to functor for generic strings. It supports the\n* following compare types: case-sensitive, case-insensitive and as-integer.");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](){ return new StringEqualTo(); }), "doc");
		cl.def(pybind11::init<enum Char::eCompareType>(), pybind11::arg("compareType"));

		cl.def("assign", (class StringEqualTo & (StringEqualTo::*)(const class StringEqualTo &)) &StringEqualTo::operator=, "C++: StringEqualTo::operator=(const class StringEqualTo &) --> class StringEqualTo &", pybind11::return_value_policy::automatic, pybind11::arg("in"));
		cl.def("__call__", (bool (StringEqualTo::*)(const std::string &, const std::string &) const) &StringEqualTo::operator(), "C++: StringEqualTo::operator()(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) const --> bool", pybind11::arg("s1"), pybind11::arg("s2"));
		cl.def("GetCompareType", (enum Char::eCompareType (StringEqualTo::*)()) &StringEqualTo::GetCompareType, "C++: StringEqualTo::GetCompareType() --> enum Char::eCompareType");
	}
	{ // String file:GenString.h line:164
		pybind11::class_<String, std::shared_ptr<String>> cl(M(""), "String", "* \n\n*\n* \n\n Generic string class that contains string related utility methods.\n*\n* This class is a static class that contains generic string related utility\n* methods, such as: converting string to uppercase/lowercase, removing\n* whitespaces, converting strings to/from integers/real numbers, determining\n* if string a number, determining whether strings are equal, escaping and\n* unescaping.");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new String(); } ) );
		cl.def_static("LowerCase", (void (*)(const std::string &, std::string &)) &String::LowerCase, "C++: String::LowerCase(const class std::__1::basic_string<char> &, class std::__1::basic_string<char> &) --> void", pybind11::arg("inString"), pybind11::arg("outString"));
		cl.def_static("LowerCase", (void (*)(std::string &)) &String::LowerCase, "C++: String::LowerCase(class std::__1::basic_string<char> &) --> void", pybind11::arg("inOutString"));
		cl.def_static("UpperCase", (void (*)(const std::string &, std::string &)) &String::UpperCase, "C++: String::UpperCase(const class std::__1::basic_string<char> &, class std::__1::basic_string<char> &) --> void", pybind11::arg("inString"), pybind11::arg("outString"));
		cl.def_static("UpperCase", (void (*)(std::string &)) &String::UpperCase, "C++: String::UpperCase(class std::__1::basic_string<char> &) --> void", pybind11::arg("inOutString"));
		cl.def_static("RemoveWhiteSpace", (void (*)(const std::string &, std::string &)) &String::RemoveWhiteSpace, "C++: String::RemoveWhiteSpace(const class std::__1::basic_string<char> &, class std::__1::basic_string<char> &) --> void", pybind11::arg("inString"), pybind11::arg("outString"));
		cl.def_static("IntToString", (std::string (*)(int)) &String::IntToString, "C++: String::IntToString(int) --> std::string", pybind11::arg("inInteger"));
		cl.def_static("DoubleToString", (std::string (*)(double)) &String::DoubleToString, "C++: String::DoubleToString(double) --> std::string", pybind11::arg("inDouble"));
		cl.def_static("StringToInt", (int (*)(const std::string &)) &String::StringToInt, "C++: String::StringToInt(const class std::__1::basic_string<char> &) --> int", pybind11::arg("inString"));
		cl.def_static("StringToDouble", (double (*)(const std::string &)) &String::StringToDouble, "C++: String::StringToDouble(const class std::__1::basic_string<char> &) --> double", pybind11::arg("inString"));
		cl.def_static("IsScientific", (bool (*)(const std::string &)) &String::IsScientific, "C++: String::IsScientific(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("number"));
		cl.def_static("ToFixedFormat", (void (*)(std::string &, const std::string &)) &String::ToFixedFormat, "C++: String::ToFixedFormat(class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("fixedFormat"), pybind11::arg("number"));
		cl.def_static("StringToBoolean", (bool (*)(const std::string &)) &String::StringToBoolean, "C++: String::StringToBoolean(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("inString"));
		cl.def_static("IsNumber", (bool (*)(const std::string &)) &String::IsNumber, "C++: String::IsNumber(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("inString"));
		cl.def_static("IsCiEqual", (bool (*)(const std::string &, const std::string &)) &String::IsCiEqual, "C++: String::IsCiEqual(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> bool", pybind11::arg("firstString"), pybind11::arg("secondString"));
		cl.def_static("IsEqual", (bool (*)(const std::string &, const std::string &, const enum Char::eCompareType)) &String::IsEqual, "C++: String::IsEqual(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const enum Char::eCompareType) --> bool", pybind11::arg("firstString"), pybind11::arg("secondString"), pybind11::arg("compareType"));
		cl.def_static("StripLeadingWs", (void (*)(std::string &)) &String::StripLeadingWs, "C++: String::StripLeadingWs(class std::__1::basic_string<char> &) --> void", pybind11::arg("resString"));
		cl.def_static("StripTrailingWs", (void (*)(std::string &)) &String::StripTrailingWs, "C++: String::StripTrailingWs(class std::__1::basic_string<char> &) --> void", pybind11::arg("resString"));
		cl.def_static("StripAndCompressWs", (void (*)(std::string &)) &String::StripAndCompressWs, "C++: String::StripAndCompressWs(class std::__1::basic_string<char> &) --> void", pybind11::arg("resString"));
		cl.def_static("rcsb_clean_string", (void (*)(std::string &)) &String::rcsb_clean_string, "C++: String::rcsb_clean_string(class std::__1::basic_string<char> &) --> void", pybind11::arg("theString"));
		cl.def_static("UnEscape", (void (*)(std::string &, const std::string &)) &String::UnEscape, "C++: String::UnEscape(class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("outStr"), pybind11::arg("inStr"));
		cl.def_static("Replace", (void (*)(std::string &, const std::string &, const std::string &)) &String::Replace, "C++: String::Replace(class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("resString"), pybind11::arg("fromStr"), pybind11::arg("toStr"));
	}
}
