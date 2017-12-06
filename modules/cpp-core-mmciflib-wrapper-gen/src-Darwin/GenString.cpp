#include <GenString.h>
#include <sstream> // __str__

#include <pybind11/pybind11.h>

#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void bind_GenString(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // CharEqualTo file:GenString.h line:80
		pybind11::class_<CharEqualTo, std::shared_ptr<CharEqualTo>, std::binary_function<char,char,bool>> cl(M(""), "CharEqualTo", "* \n\n*\n* \n\n Public class that encapsulates generic character equal_to functor.\n*\n* This class is equal_to functor for generic character. It supports the\n* following compare types: case-sensitive and case-insensitive.");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](){ return new CharEqualTo(); }), "doc");
		cl.def(pybind11::init<enum Char::eCompareType>(), pybind11::arg("compareType"));

		cl.def("assign", (class CharEqualTo & (CharEqualTo::*)(const class CharEqualTo &)) &CharEqualTo::operator=, "C++: CharEqualTo::operator=(const class CharEqualTo &) --> class CharEqualTo &", pybind11::return_value_policy::automatic, pybind11::arg("in"));
		cl.def("__call__", (bool (CharEqualTo::*)(const char, const char) const) &CharEqualTo::operator(), "C++: CharEqualTo::operator()(const char, const char) const --> bool", pybind11::arg("c1"), pybind11::arg("c2"));
	}
}
