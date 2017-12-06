#include <DictObjCont.h>
#include <DictObjContInfo.h>
#include <ISTable.h>
#include <ITTable.h>
#include <Serializer.h>
#include <TableFile.h>
#include <__string>
#include <atomic>
#include <functional>
#include <initializer_list>
#include <iterator>
#include <map>
#include <memory>
#include <sstream> // __str__
#include <stdexcept>
#include <string>
#include <string_view>
#include <tuple>
#include <utility>
#include <vector>

#include <pybind11/pybind11.h>

#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void bind_std___functional_base(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // std::binary_function file:__functional_base line:34
		pybind11::class_<std::binary_function<char,char,bool>, std::shared_ptr<std::binary_function<char,char,bool>>> cl(M("std"), "binary_function_char_char_bool_t", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new std::binary_function<char,char,bool>(); } ) );
	}
	{ // std::binary_function file:__functional_base line:34
		pybind11::class_<std::binary_function<std::string,std::string,bool>, std::shared_ptr<std::binary_function<std::string,std::string,bool>>> cl(M("std"), "binary_function_std_string_std_string_bool_t", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new std::binary_function<std::string,std::string,bool>(); } ) );
	}
}
