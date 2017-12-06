#include <__string>
#include <ios>
#include <istream>
#include <locale>
#include <ostream>
#include <sstream> // __str__
#include <streambuf>

#include <pybind11/pybind11.h>

#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void bind_std_unknown_unknown_1(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // std::basic_ostream file: line:1086
		pybind11::class_<std::ostream, std::shared_ptr<std::ostream>> cl(M("std"), "ostream", "");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init<class std::__1::basic_streambuf<char> *>(), pybind11::arg("__sb"));

		cl.def("put", (std::ostream & (std::ostream::*)(char)) &std::basic_ostream<char, std::char_traits<char> >::put, "C++: std::__1::basic_ostream<char, std::__1::char_traits<char> >::put(char) --> std::ostream &", pybind11::return_value_policy::automatic, pybind11::arg("__c"));
		cl.def("write", (std::ostream & (std::ostream::*)(const char *, long)) &std::basic_ostream<char, std::char_traits<char> >::write, "C++: std::__1::basic_ostream<char, std::__1::char_traits<char> >::write(const char *, long) --> std::ostream &", pybind11::return_value_policy::automatic, pybind11::arg("__s"), pybind11::arg("__n"));
		cl.def("flush", (std::ostream & (std::ostream::*)()) &std::basic_ostream<char, std::char_traits<char> >::flush, "C++: std::__1::basic_ostream<char, std::__1::char_traits<char> >::flush() --> std::ostream &", pybind11::return_value_policy::automatic);
		cl.def("seekp", (std::ostream & (std::ostream::*)(long long, enum std::ios_base::seekdir)) &std::basic_ostream<char, std::char_traits<char> >::seekp, "C++: std::__1::basic_ostream<char, std::__1::char_traits<char> >::seekp(long long, enum std::__1::ios_base::seekdir) --> std::ostream &", pybind11::return_value_policy::automatic, pybind11::arg("__off"), pybind11::arg("__dir"));
	}
}
