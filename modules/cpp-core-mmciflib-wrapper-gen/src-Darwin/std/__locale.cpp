#include <__string>
#include <initializer_list>
#include <ios>
#include <iterator>
#include <locale>
#include <memory>
#include <sstream> // __str__
#include <string>
#include <string_view>
#include <system_error>

#include <pybind11/pybind11.h>

#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void bind_std___locale(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // std::locale file:__locale line:72
		pybind11::class_<std::locale, std::shared_ptr<std::locale>> cl(M("std"), "locale", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new std::locale(); } ) );
		cl.def(pybind11::init<std::locale const &>());
		cl.def(pybind11::init<const char *>(), pybind11::arg(""));

		cl.def(pybind11::init<const class std::__1::basic_string<char> &>(), pybind11::arg(""));

		cl.def(pybind11::init<const class std::__1::locale &, const char *, int>(), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));

		cl.def(pybind11::init<const class std::__1::locale &, const class std::__1::basic_string<char> &, int>(), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));

		cl.def(pybind11::init<const class std::__1::locale &, const class std::__1::locale &, int>(), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));

		cl.def("assign", (const class std::locale & (std::locale::*)(const class std::locale &)) &std::locale::operator=, "C++: std::__1::locale::operator=(const class std::__1::locale &) --> const class std::locale &", pybind11::return_value_policy::automatic, pybind11::arg(""));
		cl.def("name", (std::string (std::locale::*)() const) &std::locale::name, "C++: std::__1::locale::name() const --> std::string");
		cl.def("__eq__", (bool (std::locale::*)(const class std::locale &) const) &std::locale::operator==, "C++: std::__1::locale::operator==(const class std::__1::locale &) const --> bool", pybind11::arg(""));
		cl.def("__ne__", (bool (std::locale::*)(const class std::locale &) const) &std::locale::operator!=, "C++: std::__1::locale::operator!=(const class std::__1::locale &) const --> bool", pybind11::arg("__y"));
		cl.def_static("global", (class std::locale (*)(const class std::locale &)) &std::locale::global, "C++: std::__1::locale::global(const class std::__1::locale &) --> class std::locale", pybind11::arg(""));
		cl.def_static("classic", (const class std::locale & (*)()) &std::locale::classic, "C++: std::__1::locale::classic() --> const class std::locale &", pybind11::return_value_policy::automatic);
	}
}
