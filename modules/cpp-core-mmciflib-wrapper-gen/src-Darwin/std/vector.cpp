#include <DicFile.h>
#include <DictObjCont.h>
#include <DictObjContInfo.h>
#include <GenString.h>
#include <ISTable.h>
#include <ITTable.h>
#include <Serializer.h>
#include <TableFile.h>
#include <__string>
#include <functional>
#include <initializer_list>
#include <iterator>
#include <memory>
#include <sstream> // __str__
#include <string>
#include <string_view>
#include <system_error>
#include <vector>

#include <pybind11/pybind11.h>

#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

void bind_std_vector(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // std::vector file:vector line:450
		pybind11::class_<std::vector<unsigned int>, std::shared_ptr<std::vector<unsigned int>>> cl(M("std"), "vector_unsigned_int_t", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new std::vector<unsigned int>(); } ) );
		cl.def(pybind11::init<const class std::__1::allocator<unsigned int> &>(), pybind11::arg("__a"));

		cl.def(pybind11::init<unsigned long>(), pybind11::arg("__n"));

		cl.def(pybind11::init<unsigned long, const unsigned int &>(), pybind11::arg("__n"), pybind11::arg("__x"));

		cl.def(pybind11::init<unsigned long, const unsigned int &, const class std::__1::allocator<unsigned int> &>(), pybind11::arg("__n"), pybind11::arg("__x"), pybind11::arg("__a"));

		cl.def(pybind11::init<class std::initializer_list<unsigned int>>(), pybind11::arg("__il"));

		cl.def(pybind11::init<class std::initializer_list<unsigned int>, const class std::__1::allocator<unsigned int> &>(), pybind11::arg("__il"), pybind11::arg("__a"));

		cl.def(pybind11::init<std::vector<unsigned int> const &>());
		cl.def(pybind11::init<const class std::__1::vector<unsigned int, class std::__1::allocator<unsigned int> > &, const class std::__1::allocator<unsigned int> &>(), pybind11::arg("__x"), pybind11::arg("__a"));

		cl.def("assign", (class std::vector<unsigned int, class std::allocator<unsigned int> > & (std::vector<unsigned int>::*)(const class std::vector<unsigned int, class std::allocator<unsigned int> > &)) &std::vector<unsigned int, std::allocator<unsigned int> >::operator=, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::operator=(const class std::__1::vector<unsigned int, class std::__1::allocator<unsigned int> > &) --> class std::vector<unsigned int, class std::allocator<unsigned int> > &", pybind11::return_value_policy::automatic, pybind11::arg("__x"));
		cl.def("assign", (class std::vector<unsigned int, class std::allocator<unsigned int> > & (std::vector<unsigned int>::*)(class std::initializer_list<unsigned int>)) &std::vector<unsigned int, std::allocator<unsigned int> >::operator=, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::operator=(class std::initializer_list<unsigned int>) --> class std::vector<unsigned int, class std::allocator<unsigned int> > &", pybind11::return_value_policy::automatic, pybind11::arg("__il"));
		cl.def("assign", (void (std::vector<unsigned int>::*)(unsigned long, const unsigned int &)) &std::vector<unsigned int, std::allocator<unsigned int> >::assign, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::assign(unsigned long, const unsigned int &) --> void", pybind11::arg("__n"), pybind11::arg("__u"));
		cl.def("assign", (void (std::vector<unsigned int>::*)(class std::initializer_list<unsigned int>)) &std::vector<unsigned int, std::allocator<unsigned int> >::assign, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::assign(class std::initializer_list<unsigned int>) --> void", pybind11::arg("__il"));
		cl.def("get_allocator", (class std::allocator<unsigned int> (std::vector<unsigned int>::*)() const) &std::vector<unsigned int, std::allocator<unsigned int> >::get_allocator, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::get_allocator() const --> class std::allocator<unsigned int>");
		cl.def("begin", (class std::__wrap_iter<unsigned int *> (std::vector<unsigned int>::*)()) &std::vector<unsigned int, std::allocator<unsigned int> >::begin, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::begin() --> class std::__wrap_iter<unsigned int *>");
		cl.def("end", (class std::__wrap_iter<unsigned int *> (std::vector<unsigned int>::*)()) &std::vector<unsigned int, std::allocator<unsigned int> >::end, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::end() --> class std::__wrap_iter<unsigned int *>");
		cl.def("cbegin", (class std::__wrap_iter<const unsigned int *> (std::vector<unsigned int>::*)() const) &std::vector<unsigned int, std::allocator<unsigned int> >::cbegin, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::cbegin() const --> class std::__wrap_iter<const unsigned int *>");
		cl.def("cend", (class std::__wrap_iter<const unsigned int *> (std::vector<unsigned int>::*)() const) &std::vector<unsigned int, std::allocator<unsigned int> >::cend, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::cend() const --> class std::__wrap_iter<const unsigned int *>");
		cl.def("size", (unsigned long (std::vector<unsigned int>::*)() const) &std::vector<unsigned int, std::allocator<unsigned int> >::size, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::size() const --> unsigned long");
		cl.def("capacity", (unsigned long (std::vector<unsigned int>::*)() const) &std::vector<unsigned int, std::allocator<unsigned int> >::capacity, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::capacity() const --> unsigned long");
		cl.def("empty", (bool (std::vector<unsigned int>::*)() const) &std::vector<unsigned int, std::allocator<unsigned int> >::empty, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::empty() const --> bool");
		cl.def("max_size", (unsigned long (std::vector<unsigned int>::*)() const) &std::vector<unsigned int, std::allocator<unsigned int> >::max_size, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::max_size() const --> unsigned long");
		cl.def("reserve", (void (std::vector<unsigned int>::*)(unsigned long)) &std::vector<unsigned int, std::allocator<unsigned int> >::reserve, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::reserve(unsigned long) --> void", pybind11::arg("__n"));
		cl.def("shrink_to_fit", (void (std::vector<unsigned int>::*)()) &std::vector<unsigned int, std::allocator<unsigned int> >::shrink_to_fit, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::shrink_to_fit() --> void");
		cl.def("__getitem__", (unsigned int & (std::vector<unsigned int>::*)(unsigned long)) &std::vector<unsigned int, std::allocator<unsigned int> >::operator[], "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::operator[](unsigned long) --> unsigned int &", pybind11::return_value_policy::automatic, pybind11::arg("__n"));
		cl.def("at", (unsigned int & (std::vector<unsigned int>::*)(unsigned long)) &std::vector<unsigned int, std::allocator<unsigned int> >::at, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::at(unsigned long) --> unsigned int &", pybind11::return_value_policy::automatic, pybind11::arg("__n"));
		cl.def("front", (unsigned int & (std::vector<unsigned int>::*)()) &std::vector<unsigned int, std::allocator<unsigned int> >::front, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::front() --> unsigned int &", pybind11::return_value_policy::automatic);
		cl.def("back", (unsigned int & (std::vector<unsigned int>::*)()) &std::vector<unsigned int, std::allocator<unsigned int> >::back, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::back() --> unsigned int &", pybind11::return_value_policy::automatic);
		cl.def("data", (unsigned int * (std::vector<unsigned int>::*)()) &std::vector<unsigned int, std::allocator<unsigned int> >::data, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::data() --> unsigned int *", pybind11::return_value_policy::automatic);
		cl.def("push_back", (void (std::vector<unsigned int>::*)(const unsigned int &)) &std::vector<unsigned int, std::allocator<unsigned int> >::push_back, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::push_back(const unsigned int &) --> void", pybind11::arg("__x"));
		cl.def("pop_back", (void (std::vector<unsigned int>::*)()) &std::vector<unsigned int, std::allocator<unsigned int> >::pop_back, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::pop_back() --> void");
		cl.def("insert", (class std::__wrap_iter<unsigned int *> (std::vector<unsigned int>::*)(class std::__wrap_iter<const unsigned int *>, const unsigned int &)) &std::vector<unsigned int, std::allocator<unsigned int> >::insert, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::insert(class std::__1::__wrap_iter<const unsigned int *>, const unsigned int &) --> class std::__wrap_iter<unsigned int *>", pybind11::arg("__position"), pybind11::arg("__x"));
		cl.def("insert", (class std::__wrap_iter<unsigned int *> (std::vector<unsigned int>::*)(class std::__wrap_iter<const unsigned int *>, unsigned long, const unsigned int &)) &std::vector<unsigned int, std::allocator<unsigned int> >::insert, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::insert(class std::__1::__wrap_iter<const unsigned int *>, unsigned long, const unsigned int &) --> class std::__wrap_iter<unsigned int *>", pybind11::arg("__position"), pybind11::arg("__n"), pybind11::arg("__x"));
		cl.def("insert", (class std::__wrap_iter<unsigned int *> (std::vector<unsigned int>::*)(class std::__wrap_iter<const unsigned int *>, class std::initializer_list<unsigned int>)) &std::vector<unsigned int, std::allocator<unsigned int> >::insert, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::insert(class std::__1::__wrap_iter<const unsigned int *>, class std::initializer_list<unsigned int>) --> class std::__wrap_iter<unsigned int *>", pybind11::arg("__position"), pybind11::arg("__il"));
		cl.def("erase", (class std::__wrap_iter<unsigned int *> (std::vector<unsigned int>::*)(class std::__wrap_iter<const unsigned int *>)) &std::vector<unsigned int, std::allocator<unsigned int> >::erase, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::erase(class std::__1::__wrap_iter<const unsigned int *>) --> class std::__wrap_iter<unsigned int *>", pybind11::arg("__position"));
		cl.def("erase", (class std::__wrap_iter<unsigned int *> (std::vector<unsigned int>::*)(class std::__wrap_iter<const unsigned int *>, class std::__wrap_iter<const unsigned int *>)) &std::vector<unsigned int, std::allocator<unsigned int> >::erase, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::erase(class std::__1::__wrap_iter<const unsigned int *>, class std::__1::__wrap_iter<const unsigned int *>) --> class std::__wrap_iter<unsigned int *>", pybind11::arg("__first"), pybind11::arg("__last"));
		cl.def("clear", (void (std::vector<unsigned int>::*)()) &std::vector<unsigned int, std::allocator<unsigned int> >::clear, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::clear() --> void");
		cl.def("resize", (void (std::vector<unsigned int>::*)(unsigned long)) &std::vector<unsigned int, std::allocator<unsigned int> >::resize, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::resize(unsigned long) --> void", pybind11::arg("__sz"));
		cl.def("resize", (void (std::vector<unsigned int>::*)(unsigned long, const unsigned int &)) &std::vector<unsigned int, std::allocator<unsigned int> >::resize, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::resize(unsigned long, const unsigned int &) --> void", pybind11::arg("__sz"), pybind11::arg("__x"));
		cl.def("swap", (void (std::vector<unsigned int>::*)(class std::vector<unsigned int, class std::allocator<unsigned int> > &)) &std::vector<unsigned int, std::allocator<unsigned int> >::swap, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::swap(class std::__1::vector<unsigned int, class std::__1::allocator<unsigned int> > &) --> void", pybind11::arg(""));
		cl.def("__invariants", (bool (std::vector<unsigned int>::*)() const) &std::vector<unsigned int, std::allocator<unsigned int> >::__invariants, "C++: std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >::__invariants() const --> bool");
	}
}
