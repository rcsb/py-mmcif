#include <functional>
#include <sstream> // __str__

#include <pybind11/pybind11.h>

#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void bind_std___functional_base_1(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // std::unary_function file:__functional_base line:27
		pybind11::class_<std::unary_function<char,bool>, std::shared_ptr<std::unary_function<char,bool>>> cl(M("std"), "unary_function_char_bool_t", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new std::unary_function<char,bool>(); } ) );
	}
}
