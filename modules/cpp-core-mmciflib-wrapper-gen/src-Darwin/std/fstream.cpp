#include <__string>
#include <fstream>
#include <initializer_list>
#include <iosfwd>
#include <iterator>
#include <locale>
#include <memory>
#include <sstream> // __str__
#include <streambuf>
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

// std::basic_filebuf file:fstream line:183
struct PyCallBack_filebuf : public std::filebuf {
	using std::filebuf::basic_filebuf;

	int underflow() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const std::filebuf *>(this), "underflow");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<int>::value) {
				static pybind11::detail::overload_caster_t<int> caster;
				return pybind11::detail::cast_ref<int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<int>(std::move(o));
		}
		return basic_filebuf::underflow();
	}
	int pbackfail(int a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const std::filebuf *>(this), "pbackfail");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<int>::value) {
				static pybind11::detail::overload_caster_t<int> caster;
				return pybind11::detail::cast_ref<int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<int>(std::move(o));
		}
		return basic_filebuf::pbackfail(a0);
	}
	int overflow(int a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const std::filebuf *>(this), "overflow");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<int>::value) {
				static pybind11::detail::overload_caster_t<int> caster;
				return pybind11::detail::cast_ref<int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<int>(std::move(o));
		}
		return basic_filebuf::overflow(a0);
	}
	class std::__1::basic_streambuf<char> * setbuf(char * a0, long a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const std::filebuf *>(this), "setbuf");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<class std::__1::basic_streambuf<char> *>::value) {
				static pybind11::detail::overload_caster_t<class std::__1::basic_streambuf<char> *> caster;
				return pybind11::detail::cast_ref<class std::__1::basic_streambuf<char> *>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<class std::__1::basic_streambuf<char> *>(std::move(o));
		}
		return basic_filebuf::setbuf(a0, a1);
	}
	int sync() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const std::filebuf *>(this), "sync");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<int>::value) {
				static pybind11::detail::overload_caster_t<int> caster;
				return pybind11::detail::cast_ref<int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<int>(std::move(o));
		}
		return basic_filebuf::sync();
	}
	void imbue(const class std::__1::locale & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const std::filebuf *>(this), "imbue");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return basic_filebuf::imbue(a0);
	}
	long showmanyc() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const std::filebuf *>(this), "showmanyc");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<long>::value) {
				static pybind11::detail::overload_caster_t<long> caster;
				return pybind11::detail::cast_ref<long>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<long>(std::move(o));
		}
		return basic_streambuf::showmanyc();
	}
	long xsgetn(char * a0, long a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const std::filebuf *>(this), "xsgetn");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<long>::value) {
				static pybind11::detail::overload_caster_t<long> caster;
				return pybind11::detail::cast_ref<long>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<long>(std::move(o));
		}
		return basic_streambuf::xsgetn(a0, a1);
	}
	int uflow() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const std::filebuf *>(this), "uflow");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<int>::value) {
				static pybind11::detail::overload_caster_t<int> caster;
				return pybind11::detail::cast_ref<int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<int>(std::move(o));
		}
		return basic_streambuf::uflow();
	}
	long xsputn(const char * a0, long a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const std::filebuf *>(this), "xsputn");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<long>::value) {
				static pybind11::detail::overload_caster_t<long> caster;
				return pybind11::detail::cast_ref<long>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<long>(std::move(o));
		}
		return basic_streambuf::xsputn(a0, a1);
	}
};

void bind_std_fstream(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // std::basic_filebuf file:fstream line:183
		pybind11::class_<std::filebuf, std::shared_ptr<std::filebuf>, PyCallBack_filebuf, std::streambuf> cl(M("std"), "filebuf", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new PyCallBack_filebuf(); } ) );
		cl.def("swap", (void (std::filebuf::*)(class std::basic_filebuf<char, struct std::char_traits<char> > &)) &std::basic_filebuf<char, std::char_traits<char> >::swap, "C++: std::__1::basic_filebuf<char, std::__1::char_traits<char> >::swap(class std::__1::basic_filebuf<char, struct std::__1::char_traits<char> > &) --> void", pybind11::arg("__rhs"));
		cl.def("is_open", (bool (std::filebuf::*)() const) &std::basic_filebuf<char, std::char_traits<char> >::is_open, "C++: std::__1::basic_filebuf<char, std::__1::char_traits<char> >::is_open() const --> bool");
		cl.def("open", (class std::basic_filebuf<char, struct std::char_traits<char> > * (std::filebuf::*)(const char *, unsigned int)) &std::basic_filebuf<char, std::char_traits<char> >::open, "C++: std::__1::basic_filebuf<char, std::__1::char_traits<char> >::open(const char *, unsigned int) --> class std::basic_filebuf<char, struct std::char_traits<char> > *", pybind11::return_value_policy::automatic, pybind11::arg("__s"), pybind11::arg("__mode"));
		cl.def("open", (class std::basic_filebuf<char, struct std::char_traits<char> > * (std::filebuf::*)(const std::string &, unsigned int)) &std::basic_filebuf<char, std::char_traits<char> >::open, "C++: std::__1::basic_filebuf<char, std::__1::char_traits<char> >::open(const class std::__1::basic_string<char> &, unsigned int) --> class std::basic_filebuf<char, struct std::char_traits<char> > *", pybind11::return_value_policy::automatic, pybind11::arg("__s"), pybind11::arg("__mode"));
		cl.def("close", (class std::basic_filebuf<char, struct std::char_traits<char> > * (std::filebuf::*)()) &std::basic_filebuf<char, std::char_traits<char> >::close, "C++: std::__1::basic_filebuf<char, std::__1::char_traits<char> >::close() --> class std::basic_filebuf<char, struct std::char_traits<char> > *", pybind11::return_value_policy::automatic);
		cl.def("pubimbue", (class std::locale (std::streambuf::*)(const class std::locale &)) &std::basic_streambuf<char, std::char_traits<char> >::pubimbue, "C++: std::__1::basic_streambuf<char, std::__1::char_traits<char> >::pubimbue(const class std::__1::locale &) --> class std::locale", pybind11::arg("__loc"));
		cl.def("getloc", (class std::locale (std::streambuf::*)() const) &std::basic_streambuf<char, std::char_traits<char> >::getloc, "C++: std::__1::basic_streambuf<char, std::__1::char_traits<char> >::getloc() const --> class std::locale");
		cl.def("pubsetbuf", (class std::basic_streambuf<char> * (std::streambuf::*)(char *, long)) &std::basic_streambuf<char, std::char_traits<char> >::pubsetbuf, "C++: std::__1::basic_streambuf<char, std::__1::char_traits<char> >::pubsetbuf(char *, long) --> class std::basic_streambuf<char> *", pybind11::return_value_policy::automatic, pybind11::arg("__s"), pybind11::arg("__n"));
		cl.def("pubsync", (int (std::streambuf::*)()) &std::basic_streambuf<char, std::char_traits<char> >::pubsync, "C++: std::__1::basic_streambuf<char, std::__1::char_traits<char> >::pubsync() --> int");
		cl.def("in_avail", (long (std::streambuf::*)()) &std::basic_streambuf<char, std::char_traits<char> >::in_avail, "C++: std::__1::basic_streambuf<char, std::__1::char_traits<char> >::in_avail() --> long");
		cl.def("snextc", (int (std::streambuf::*)()) &std::basic_streambuf<char, std::char_traits<char> >::snextc, "C++: std::__1::basic_streambuf<char, std::__1::char_traits<char> >::snextc() --> int");
		cl.def("sbumpc", (int (std::streambuf::*)()) &std::basic_streambuf<char, std::char_traits<char> >::sbumpc, "C++: std::__1::basic_streambuf<char, std::__1::char_traits<char> >::sbumpc() --> int");
		cl.def("sgetc", (int (std::streambuf::*)()) &std::basic_streambuf<char, std::char_traits<char> >::sgetc, "C++: std::__1::basic_streambuf<char, std::__1::char_traits<char> >::sgetc() --> int");
		cl.def("sgetn", (long (std::streambuf::*)(char *, long)) &std::basic_streambuf<char, std::char_traits<char> >::sgetn, "C++: std::__1::basic_streambuf<char, std::__1::char_traits<char> >::sgetn(char *, long) --> long", pybind11::arg("__s"), pybind11::arg("__n"));
		cl.def("sputbackc", (int (std::streambuf::*)(char)) &std::basic_streambuf<char, std::char_traits<char> >::sputbackc, "C++: std::__1::basic_streambuf<char, std::__1::char_traits<char> >::sputbackc(char) --> int", pybind11::arg("__c"));
		cl.def("sungetc", (int (std::streambuf::*)()) &std::basic_streambuf<char, std::char_traits<char> >::sungetc, "C++: std::__1::basic_streambuf<char, std::__1::char_traits<char> >::sungetc() --> int");
		cl.def("sputc", (int (std::streambuf::*)(char)) &std::basic_streambuf<char, std::char_traits<char> >::sputc, "C++: std::__1::basic_streambuf<char, std::__1::char_traits<char> >::sputc(char) --> int", pybind11::arg("__c"));
		cl.def("sputn", (long (std::streambuf::*)(const char *, long)) &std::basic_streambuf<char, std::char_traits<char> >::sputn, "C++: std::__1::basic_streambuf<char, std::__1::char_traits<char> >::sputn(const char *, long) --> long", pybind11::arg("__s"), pybind11::arg("__n"));
	}
	{ // std::basic_ofstream file:fstream line:1164
		pybind11::class_<std::ofstream, std::shared_ptr<std::ofstream>, std::ostream> cl(M("std"), "ofstream", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new std::ofstream(); } ) );
		cl.def(pybind11::init([](const char * a0){ return new std::ofstream(a0); }), "doc");
		cl.def(pybind11::init<const char *, unsigned int>(), pybind11::arg("__s"), pybind11::arg("__mode"));

		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0){ return new std::ofstream(a0); }), "doc");
		cl.def(pybind11::init<const class std::__1::basic_string<char> &, unsigned int>(), pybind11::arg("__s"), pybind11::arg("__mode"));

		cl.def("swap", (void (std::ofstream::*)(class std::basic_ofstream<char, struct std::char_traits<char> > &)) &std::basic_ofstream<char, std::char_traits<char> >::swap, "C++: std::__1::basic_ofstream<char, std::__1::char_traits<char> >::swap(class std::__1::basic_ofstream<char, struct std::__1::char_traits<char> > &) --> void", pybind11::arg("__rhs"));
		cl.def("rdbuf", (class std::basic_filebuf<char, struct std::char_traits<char> > * (std::ofstream::*)() const) &std::basic_ofstream<char, std::char_traits<char> >::rdbuf, "C++: std::__1::basic_ofstream<char, std::__1::char_traits<char> >::rdbuf() const --> class std::basic_filebuf<char, struct std::char_traits<char> > *", pybind11::return_value_policy::automatic);
		cl.def("is_open", (bool (std::ofstream::*)() const) &std::basic_ofstream<char, std::char_traits<char> >::is_open, "C++: std::__1::basic_ofstream<char, std::__1::char_traits<char> >::is_open() const --> bool");
		cl.def("open", [](std::ofstream &o, const char * a0) -> void { return o.open(a0); }, "", pybind11::arg("__s"));
		cl.def("open", (void (std::ofstream::*)(const char *, unsigned int)) &std::basic_ofstream<char, std::char_traits<char> >::open, "C++: std::__1::basic_ofstream<char, std::__1::char_traits<char> >::open(const char *, unsigned int) --> void", pybind11::arg("__s"), pybind11::arg("__mode"));
		cl.def("open", [](std::ofstream &o, const class std::__1::basic_string<char> & a0) -> void { return o.open(a0); }, "", pybind11::arg("__s"));
		cl.def("open", (void (std::ofstream::*)(const std::string &, unsigned int)) &std::basic_ofstream<char, std::char_traits<char> >::open, "C++: std::__1::basic_ofstream<char, std::__1::char_traits<char> >::open(const class std::__1::basic_string<char> &, unsigned int) --> void", pybind11::arg("__s"), pybind11::arg("__mode"));
		cl.def("close", (void (std::ofstream::*)()) &std::basic_ofstream<char, std::char_traits<char> >::close, "C++: std::__1::basic_ofstream<char, std::__1::char_traits<char> >::close() --> void");
		cl.def("put", (std::ostream & (std::ostream::*)(char)) &std::basic_ostream<char, std::char_traits<char> >::put, "C++: std::__1::basic_ostream<char, std::__1::char_traits<char> >::put(char) --> std::ostream &", pybind11::return_value_policy::automatic, pybind11::arg("__c"));
		cl.def("write", (std::ostream & (std::ostream::*)(const char *, long)) &std::basic_ostream<char, std::char_traits<char> >::write, "C++: std::__1::basic_ostream<char, std::__1::char_traits<char> >::write(const char *, long) --> std::ostream &", pybind11::return_value_policy::automatic, pybind11::arg("__s"), pybind11::arg("__n"));
		cl.def("flush", (std::ostream & (std::ostream::*)()) &std::basic_ostream<char, std::char_traits<char> >::flush, "C++: std::__1::basic_ostream<char, std::__1::char_traits<char> >::flush() --> std::ostream &", pybind11::return_value_policy::automatic);
		cl.def("seekp", (std::ostream & (std::ostream::*)(long long, enum std::ios_base::seekdir)) &std::basic_ostream<char, std::char_traits<char> >::seekp, "C++: std::__1::basic_ostream<char, std::__1::char_traits<char> >::seekp(long long, enum std::__1::ios_base::seekdir) --> std::ostream &", pybind11::return_value_policy::automatic, pybind11::arg("__off"), pybind11::arg("__dir"));
	}
	{ // std::vector file:vector line:450
		pybind11::class_<std::vector<std::string,std::allocator<std::string >>, std::shared_ptr<std::vector<std::string,std::allocator<std::string >>>> cl(M("std"), "vector_std_string_std_allocator_std_string_t", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new std::vector<std::string,std::allocator<std::string >>(); } ) );
		cl.def(pybind11::init<const class std::__1::allocator<class std::__1::basic_string<char> > &>(), pybind11::arg("__a"));

		cl.def(pybind11::init<unsigned long>(), pybind11::arg("__n"));

		cl.def(pybind11::init<unsigned long, const class std::__1::basic_string<char> &>(), pybind11::arg("__n"), pybind11::arg("__x"));

		cl.def(pybind11::init<unsigned long, const class std::__1::basic_string<char> &, const class std::__1::allocator<class std::__1::basic_string<char> > &>(), pybind11::arg("__n"), pybind11::arg("__x"), pybind11::arg("__a"));

		cl.def(pybind11::init<class std::initializer_list<class std::__1::basic_string<char> >>(), pybind11::arg("__il"));

		cl.def(pybind11::init<class std::initializer_list<class std::__1::basic_string<char> >, const class std::__1::allocator<class std::__1::basic_string<char> > &>(), pybind11::arg("__il"), pybind11::arg("__a"));

		cl.def(pybind11::init<std::vector<std::string,std::allocator<std::string >> const &>());
		cl.def(pybind11::init<const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &, const class std::__1::allocator<class std::__1::basic_string<char> > &>(), pybind11::arg("__x"), pybind11::arg("__a"));

		cl.def("assign", (class std::vector<std::string, class std::allocator<std::string > > & (std::vector<std::string,std::allocator<std::string >>::*)(const class std::vector<std::string, class std::allocator<std::string > > &)) &std::vector<std::string, std::allocator<std::string > >::operator=, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::operator=(const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &) --> class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic, pybind11::arg("__x"));
		cl.def("assign", (class std::vector<std::string, class std::allocator<std::string > > & (std::vector<std::string,std::allocator<std::string >>::*)(class std::initializer_list<std::string >)) &std::vector<std::string, std::allocator<std::string > >::operator=, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::operator=(class std::initializer_list<class std::__1::basic_string<char> >) --> class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic, pybind11::arg("__il"));
		cl.def("assign", (void (std::vector<std::string,std::allocator<std::string >>::*)(unsigned long, const std::string &)) &std::vector<std::string, std::allocator<std::string > >::assign, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::assign(unsigned long, const class std::__1::basic_string<char> &) --> void", pybind11::arg("__n"), pybind11::arg("__u"));
		cl.def("assign", (void (std::vector<std::string,std::allocator<std::string >>::*)(class std::initializer_list<std::string >)) &std::vector<std::string, std::allocator<std::string > >::assign, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::assign(class std::initializer_list<class std::__1::basic_string<char> >) --> void", pybind11::arg("__il"));
		cl.def("get_allocator", (class std::allocator<std::string > (std::vector<std::string,std::allocator<std::string >>::*)() const) &std::vector<std::string, std::allocator<std::string > >::get_allocator, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::get_allocator() const --> class std::allocator<std::string >");
		cl.def("begin", (class std::__wrap_iter<std::string *> (std::vector<std::string,std::allocator<std::string >>::*)()) &std::vector<std::string, std::allocator<std::string > >::begin, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::begin() --> class std::__wrap_iter<std::string *>");
		cl.def("end", (class std::__wrap_iter<std::string *> (std::vector<std::string,std::allocator<std::string >>::*)()) &std::vector<std::string, std::allocator<std::string > >::end, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::end() --> class std::__wrap_iter<std::string *>");
		cl.def("cbegin", (class std::__wrap_iter<const std::string *> (std::vector<std::string,std::allocator<std::string >>::*)() const) &std::vector<std::string, std::allocator<std::string > >::cbegin, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::cbegin() const --> class std::__wrap_iter<const std::string *>");
		cl.def("cend", (class std::__wrap_iter<const std::string *> (std::vector<std::string,std::allocator<std::string >>::*)() const) &std::vector<std::string, std::allocator<std::string > >::cend, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::cend() const --> class std::__wrap_iter<const std::string *>");
		cl.def("size", (unsigned long (std::vector<std::string,std::allocator<std::string >>::*)() const) &std::vector<std::string, std::allocator<std::string > >::size, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::size() const --> unsigned long");
		cl.def("capacity", (unsigned long (std::vector<std::string,std::allocator<std::string >>::*)() const) &std::vector<std::string, std::allocator<std::string > >::capacity, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::capacity() const --> unsigned long");
		cl.def("empty", (bool (std::vector<std::string,std::allocator<std::string >>::*)() const) &std::vector<std::string, std::allocator<std::string > >::empty, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::empty() const --> bool");
		cl.def("max_size", (unsigned long (std::vector<std::string,std::allocator<std::string >>::*)() const) &std::vector<std::string, std::allocator<std::string > >::max_size, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::max_size() const --> unsigned long");
		cl.def("reserve", (void (std::vector<std::string,std::allocator<std::string >>::*)(unsigned long)) &std::vector<std::string, std::allocator<std::string > >::reserve, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::reserve(unsigned long) --> void", pybind11::arg("__n"));
		cl.def("shrink_to_fit", (void (std::vector<std::string,std::allocator<std::string >>::*)()) &std::vector<std::string, std::allocator<std::string > >::shrink_to_fit, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::shrink_to_fit() --> void");
		cl.def("__getitem__", (std::string & (std::vector<std::string,std::allocator<std::string >>::*)(unsigned long)) &std::vector<std::string, std::allocator<std::string > >::operator[], "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::operator[](unsigned long) --> std::string &", pybind11::return_value_policy::automatic, pybind11::arg("__n"));
		cl.def("at", (std::string & (std::vector<std::string,std::allocator<std::string >>::*)(unsigned long)) &std::vector<std::string, std::allocator<std::string > >::at, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::at(unsigned long) --> std::string &", pybind11::return_value_policy::automatic, pybind11::arg("__n"));
		cl.def("front", (std::string & (std::vector<std::string,std::allocator<std::string >>::*)()) &std::vector<std::string, std::allocator<std::string > >::front, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::front() --> std::string &", pybind11::return_value_policy::automatic);
		cl.def("back", (std::string & (std::vector<std::string,std::allocator<std::string >>::*)()) &std::vector<std::string, std::allocator<std::string > >::back, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::back() --> std::string &", pybind11::return_value_policy::automatic);
		cl.def("data", (std::string * (std::vector<std::string,std::allocator<std::string >>::*)()) &std::vector<std::string, std::allocator<std::string > >::data, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::data() --> std::string *", pybind11::return_value_policy::automatic);
		cl.def("push_back", (void (std::vector<std::string,std::allocator<std::string >>::*)(const std::string &)) &std::vector<std::string, std::allocator<std::string > >::push_back, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::push_back(const class std::__1::basic_string<char> &) --> void", pybind11::arg("__x"));
		cl.def("pop_back", (void (std::vector<std::string,std::allocator<std::string >>::*)()) &std::vector<std::string, std::allocator<std::string > >::pop_back, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::pop_back() --> void");
		cl.def("insert", (class std::__wrap_iter<std::string *> (std::vector<std::string,std::allocator<std::string >>::*)(class std::__wrap_iter<const std::string *>, const std::string &)) &std::vector<std::string, std::allocator<std::string > >::insert, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::insert(class std::__1::__wrap_iter<const class std::__1::basic_string<char> *>, const class std::__1::basic_string<char> &) --> class std::__wrap_iter<std::string *>", pybind11::arg("__position"), pybind11::arg("__x"));
		cl.def("insert", (class std::__wrap_iter<std::string *> (std::vector<std::string,std::allocator<std::string >>::*)(class std::__wrap_iter<const std::string *>, unsigned long, const std::string &)) &std::vector<std::string, std::allocator<std::string > >::insert, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::insert(class std::__1::__wrap_iter<const class std::__1::basic_string<char> *>, unsigned long, const class std::__1::basic_string<char> &) --> class std::__wrap_iter<std::string *>", pybind11::arg("__position"), pybind11::arg("__n"), pybind11::arg("__x"));
		cl.def("insert", (class std::__wrap_iter<std::string *> (std::vector<std::string,std::allocator<std::string >>::*)(class std::__wrap_iter<const std::string *>, class std::initializer_list<std::string >)) &std::vector<std::string, std::allocator<std::string > >::insert, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::insert(class std::__1::__wrap_iter<const class std::__1::basic_string<char> *>, class std::initializer_list<class std::__1::basic_string<char> >) --> class std::__wrap_iter<std::string *>", pybind11::arg("__position"), pybind11::arg("__il"));
		cl.def("erase", (class std::__wrap_iter<std::string *> (std::vector<std::string,std::allocator<std::string >>::*)(class std::__wrap_iter<const std::string *>)) &std::vector<std::string, std::allocator<std::string > >::erase, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::erase(class std::__1::__wrap_iter<const class std::__1::basic_string<char> *>) --> class std::__wrap_iter<std::string *>", pybind11::arg("__position"));
		cl.def("erase", (class std::__wrap_iter<std::string *> (std::vector<std::string,std::allocator<std::string >>::*)(class std::__wrap_iter<const std::string *>, class std::__wrap_iter<const std::string *>)) &std::vector<std::string, std::allocator<std::string > >::erase, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::erase(class std::__1::__wrap_iter<const class std::__1::basic_string<char> *>, class std::__1::__wrap_iter<const class std::__1::basic_string<char> *>) --> class std::__wrap_iter<std::string *>", pybind11::arg("__first"), pybind11::arg("__last"));
		cl.def("clear", (void (std::vector<std::string,std::allocator<std::string >>::*)()) &std::vector<std::string, std::allocator<std::string > >::clear, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::clear() --> void");
		cl.def("resize", (void (std::vector<std::string,std::allocator<std::string >>::*)(unsigned long)) &std::vector<std::string, std::allocator<std::string > >::resize, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::resize(unsigned long) --> void", pybind11::arg("__sz"));
		cl.def("resize", (void (std::vector<std::string,std::allocator<std::string >>::*)(unsigned long, const std::string &)) &std::vector<std::string, std::allocator<std::string > >::resize, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::resize(unsigned long, const class std::__1::basic_string<char> &) --> void", pybind11::arg("__sz"), pybind11::arg("__x"));
		cl.def("swap", (void (std::vector<std::string,std::allocator<std::string >>::*)(class std::vector<std::string, class std::allocator<std::string > > &)) &std::vector<std::string, std::allocator<std::string > >::swap, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::swap(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &) --> void", pybind11::arg(""));
		cl.def("__invariants", (bool (std::vector<std::string,std::allocator<std::string >>::*)() const) &std::vector<std::string, std::allocator<std::string > >::__invariants, "C++: std::__1::vector<std::__1::basic_string<char>, std::__1::allocator<std::__1::basic_string<char> > >::__invariants() const --> bool");
	}
}
