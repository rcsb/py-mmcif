#include <CifString.h>
#include <DicFile.h>
#include <DictObjCont.h>
#include <DictObjContInfo.h>
#include <Exceptions.h>
#include <GenString.h>
#include <ISTable.h>
#include <ITTable.h>
#include <Serializer.h>
#include <TableFile.h>
#include <__string>
#include <functional>
#include <initializer_list>
#include <iterator>
#include <mapped_ptr_vector.h>
#include <memory>
#include <sstream> // __str__
#include <string>
#include <string_view>
#include <utility>
#include <vector>

#include <pybind11/pybind11.h>

#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

// RcsbException file:Exceptions.h line:23
struct PyCallBack_RcsbException : public RcsbException {
	using RcsbException::RcsbException;

	const char * what() const throw() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const RcsbException *>(this), "what");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<const char *>::value) {
				static pybind11::detail::overload_caster_t<const char *> caster;
				return pybind11::detail::cast_ref<const char *>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<const char *>(std::move(o));
		}
		return RcsbException::what();
	}
};

// EmptyValueException file:Exceptions.h line:41
struct PyCallBack_EmptyValueException : public EmptyValueException {
	using EmptyValueException::EmptyValueException;

	const char * what() const throw() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const EmptyValueException *>(this), "what");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<const char *>::value) {
				static pybind11::detail::overload_caster_t<const char *> caster;
				return pybind11::detail::cast_ref<const char *>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<const char *>(std::move(o));
		}
		return RcsbException::what();
	}
};

// NotFoundException file:Exceptions.h line:53
struct PyCallBack_NotFoundException : public NotFoundException {
	using NotFoundException::NotFoundException;

	const char * what() const throw() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const NotFoundException *>(this), "what");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<const char *>::value) {
				static pybind11::detail::overload_caster_t<const char *> caster;
				return pybind11::detail::cast_ref<const char *>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<const char *>(std::move(o));
		}
		return RcsbException::what();
	}
};

// AlreadyExistsException file:Exceptions.h line:65
struct PyCallBack_AlreadyExistsException : public AlreadyExistsException {
	using AlreadyExistsException::AlreadyExistsException;

	const char * what() const throw() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const AlreadyExistsException *>(this), "what");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<const char *>::value) {
				static pybind11::detail::overload_caster_t<const char *> caster;
				return pybind11::detail::cast_ref<const char *>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<const char *>(std::move(o));
		}
		return RcsbException::what();
	}
};

// EmptyContainerException file:Exceptions.h line:77
struct PyCallBack_EmptyContainerException : public EmptyContainerException {
	using EmptyContainerException::EmptyContainerException;

	const char * what() const throw() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const EmptyContainerException *>(this), "what");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<const char *>::value) {
				static pybind11::detail::overload_caster_t<const char *> caster;
				return pybind11::detail::cast_ref<const char *>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<const char *>(std::move(o));
		}
		return RcsbException::what();
	}
};

// FileModeException file:Exceptions.h line:89
struct PyCallBack_FileModeException : public FileModeException {
	using FileModeException::FileModeException;

	const char * what() const throw() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const FileModeException *>(this), "what");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<const char *>::value) {
				static pybind11::detail::overload_caster_t<const char *> caster;
				return pybind11::detail::cast_ref<const char *>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<const char *>(std::move(o));
		}
		return RcsbException::what();
	}
};

// InvalidStateException file:Exceptions.h line:101
struct PyCallBack_InvalidStateException : public InvalidStateException {
	using InvalidStateException::InvalidStateException;

	const char * what() const throw() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const InvalidStateException *>(this), "what");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<const char *>::value) {
				static pybind11::detail::overload_caster_t<const char *> caster;
				return pybind11::detail::cast_ref<const char *>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<const char *>(std::move(o));
		}
		return RcsbException::what();
	}
};

// FileException file:Exceptions.h line:113
struct PyCallBack_FileException : public FileException {
	using FileException::FileException;

	const char * what() const throw() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const FileException *>(this), "what");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<const char *>::value) {
				static pybind11::detail::overload_caster_t<const char *> caster;
				return pybind11::detail::cast_ref<const char *>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<const char *>(std::move(o));
		}
		return RcsbException::what();
	}
};

// InvalidOptionsException file:Exceptions.h line:124
struct PyCallBack_InvalidOptionsException : public InvalidOptionsException {
	using InvalidOptionsException::InvalidOptionsException;

	const char * what() const throw() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const InvalidOptionsException *>(this), "what");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<const char *>::value) {
				static pybind11::detail::overload_caster_t<const char *> caster;
				return pybind11::detail::cast_ref<const char *>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<const char *>(std::move(o));
		}
		return RcsbException::what();
	}
};

// VersionMismatchException file:Exceptions.h line:133
struct PyCallBack_VersionMismatchException : public VersionMismatchException {
	using VersionMismatchException::VersionMismatchException;

	const char * what() const throw() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const VersionMismatchException *>(this), "what");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<const char *>::value) {
				static pybind11::detail::overload_caster_t<const char *> caster;
				return pybind11::detail::cast_ref<const char *>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<const char *>(std::move(o));
		}
		return RcsbException::what();
	}
};

void bind_CifString(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // CifString file:CifString.h line:30
		pybind11::class_<CifString, std::shared_ptr<CifString>> cl(M(""), "CifString", "* \n\n* \n* \n\n Public class that contains CIF string related static methods.\n* \n* This class is not a full abstraction of a CIF string. It only contains\n* static constants and methods, that are related to a CIF string. A CIF\n* string is a string, prefixed with an underscore, that consists of a\n* category name and an item name concatenated by a dot, as specified here:\n*\n* _categoryName.itemName\n*\n* The class provides methods for creating a CIF string, extracting category\n* name and item name from a CIF string.");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new CifString(); } ) );
		cl.def_static("MakeCifItem", (void (*)(std::string &, const std::string &, const std::string &)) &CifString::MakeCifItem, "C++: CifString::MakeCifItem(class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("cifItem"), pybind11::arg("categoryName"), pybind11::arg("itemName"));
		cl.def_static("MakeCifItems", (void (*)(class std::vector<std::string, class std::allocator<std::string > > &, const std::string &, const class std::vector<std::string, class std::allocator<std::string > > &)) &CifString::MakeCifItems, "C++: CifString::MakeCifItems(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &, const class std::__1::basic_string<char> &, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &) --> void", pybind11::arg("cifItems"), pybind11::arg("categoryName"), pybind11::arg("attribsNames"));
		cl.def_static("GetItemFromCifItem", (void (*)(std::string &, const std::string &)) &CifString::GetItemFromCifItem, "C++: CifString::GetItemFromCifItem(class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("keyword"), pybind11::arg("itemName"));
		cl.def_static("GetCategoryFromCifItem", (void (*)(std::string &, const std::string &)) &CifString::GetCategoryFromCifItem, "C++: CifString::GetCategoryFromCifItem(class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("categoryName"), pybind11::arg("itemName"));
		cl.def_static("IsEmptyValue", (bool (*)(const std::string &)) &CifString::IsEmptyValue, "C++: CifString::IsEmptyValue(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("value"));
		cl.def_static("IsUnknownValue", (bool (*)(const std::string &)) &CifString::IsUnknownValue, "C++: CifString::IsUnknownValue(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("value"));
		cl.def_static("IsSpecialChar", (bool (*)(const char)) &CifString::IsSpecialChar, "C++: CifString::IsSpecialChar(const char) --> bool", pybind11::arg("charValue"));
		cl.def_static("IsSpecialFirstChar", (bool (*)(const char)) &CifString::IsSpecialFirstChar, "C++: CifString::IsSpecialFirstChar(const char) --> bool", pybind11::arg("charValue"));
	}
	{ // RcsbException file:Exceptions.h line:23
		pybind11::class_<RcsbException, std::shared_ptr<RcsbException>, PyCallBack_RcsbException, std::exception> cl(M(""), "RcsbException", "Base class for all RCSB exceptions");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](){ return new RcsbException(); }, [](){ return new PyCallBack_RcsbException(); } ), "doc");
		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0){ return new RcsbException(a0); }, [](const class std::__1::basic_string<char> & a0){ return new PyCallBack_RcsbException(a0); } ), "doc");
		cl.def(pybind11::init<const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &>(), pybind11::arg("message"), pybind11::arg("location"));

		cl.def(pybind11::init<PyCallBack_RcsbException const &>());
		cl.def("AppendMessage", [](RcsbException &o) -> void { return o.AppendMessage(); }, "");
		cl.def("AppendMessage", [](RcsbException &o, const class std::__1::basic_string<char> & a0) -> void { return o.AppendMessage(a0); }, "", pybind11::arg("message"));
		cl.def("AppendMessage", (void (RcsbException::*)(const std::string &, const std::string &)) &RcsbException::AppendMessage, "C++: RcsbException::AppendMessage(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("message"), pybind11::arg("location"));
		cl.def("what", (const char * (RcsbException::*)() const) &RcsbException::what, "C++: RcsbException::what() const --> const char *", pybind11::return_value_policy::automatic);
		cl.def("assign", (class RcsbException & (RcsbException::*)(const class RcsbException &)) &RcsbException::operator=, "C++: RcsbException::operator=(const class RcsbException &) --> class RcsbException &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	{ // EmptyValueException file:Exceptions.h line:41
		pybind11::class_<EmptyValueException, std::shared_ptr<EmptyValueException>, PyCallBack_EmptyValueException, RcsbException> cl(M(""), "EmptyValueException", "Empty value exception (e.g. NULL pointer, empty string)");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](){ return new EmptyValueException(); }, [](){ return new PyCallBack_EmptyValueException(); } ), "doc");
		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0){ return new EmptyValueException(a0); }, [](const class std::__1::basic_string<char> & a0){ return new PyCallBack_EmptyValueException(a0); } ), "doc");
		cl.def(pybind11::init<const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &>(), pybind11::arg("message"), pybind11::arg("location"));

		cl.def(pybind11::init<PyCallBack_EmptyValueException const &>());
		cl.def("assign", (class EmptyValueException & (EmptyValueException::*)(const class EmptyValueException &)) &EmptyValueException::operator=, "C++: EmptyValueException::operator=(const class EmptyValueException &) --> class EmptyValueException &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	{ // NotFoundException file:Exceptions.h line:53
		pybind11::class_<NotFoundException, std::shared_ptr<NotFoundException>, PyCallBack_NotFoundException, RcsbException> cl(M(""), "NotFoundException", "Object not found (thrown everywhere except from .find() methods)");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](){ return new NotFoundException(); }, [](){ return new PyCallBack_NotFoundException(); } ), "doc");
		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0){ return new NotFoundException(a0); }, [](const class std::__1::basic_string<char> & a0){ return new PyCallBack_NotFoundException(a0); } ), "doc");
		cl.def(pybind11::init<const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &>(), pybind11::arg("message"), pybind11::arg("location"));

		cl.def(pybind11::init<PyCallBack_NotFoundException const &>());
		cl.def("assign", (class NotFoundException & (NotFoundException::*)(const class NotFoundException &)) &NotFoundException::operator=, "C++: NotFoundException::operator=(const class NotFoundException &) --> class NotFoundException &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	{ // AlreadyExistsException file:Exceptions.h line:65
		pybind11::class_<AlreadyExistsException, std::shared_ptr<AlreadyExistsException>, PyCallBack_AlreadyExistsException, RcsbException> cl(M(""), "AlreadyExistsException", "Object already exists");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](){ return new AlreadyExistsException(); }, [](){ return new PyCallBack_AlreadyExistsException(); } ), "doc");
		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0){ return new AlreadyExistsException(a0); }, [](const class std::__1::basic_string<char> & a0){ return new PyCallBack_AlreadyExistsException(a0); } ), "doc");
		cl.def(pybind11::init<const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &>(), pybind11::arg("message"), pybind11::arg("location"));

		cl.def("assign", (class AlreadyExistsException & (AlreadyExistsException::*)(const class AlreadyExistsException &)) &AlreadyExistsException::operator=, "C++: AlreadyExistsException::operator=(const class AlreadyExistsException &) --> class AlreadyExistsException &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	{ // EmptyContainerException file:Exceptions.h line:77
		pybind11::class_<EmptyContainerException, std::shared_ptr<EmptyContainerException>, PyCallBack_EmptyContainerException, RcsbException> cl(M(""), "EmptyContainerException", "Empty container");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](){ return new EmptyContainerException(); }, [](){ return new PyCallBack_EmptyContainerException(); } ), "doc");
		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0){ return new EmptyContainerException(a0); }, [](const class std::__1::basic_string<char> & a0){ return new PyCallBack_EmptyContainerException(a0); } ), "doc");
		cl.def(pybind11::init<const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &>(), pybind11::arg("message"), pybind11::arg("location"));

		cl.def("assign", (class EmptyContainerException & (EmptyContainerException::*)(const class EmptyContainerException &)) &EmptyContainerException::operator=, "C++: EmptyContainerException::operator=(const class EmptyContainerException &) --> class EmptyContainerException &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	{ // FileModeException file:Exceptions.h line:89
		pybind11::class_<FileModeException, std::shared_ptr<FileModeException>, PyCallBack_FileModeException, RcsbException> cl(M(""), "FileModeException", "File mode exception (e.g. attempt to write to read-only file, invalid mode.)");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](){ return new FileModeException(); }, [](){ return new PyCallBack_FileModeException(); } ), "doc");
		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0){ return new FileModeException(a0); }, [](const class std::__1::basic_string<char> & a0){ return new PyCallBack_FileModeException(a0); } ), "doc");
		cl.def(pybind11::init<const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &>(), pybind11::arg("message"), pybind11::arg("location"));

		cl.def("assign", (class FileModeException & (FileModeException::*)(const class FileModeException &)) &FileModeException::operator=, "C++: FileModeException::operator=(const class FileModeException &) --> class FileModeException &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	{ // InvalidStateException file:Exceptions.h line:101
		pybind11::class_<InvalidStateException, std::shared_ptr<InvalidStateException>, PyCallBack_InvalidStateException, RcsbException> cl(M(""), "InvalidStateException", "Invalid state exception (e.g. getting a row reference in a column-wise table/// )");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](){ return new InvalidStateException(); }, [](){ return new PyCallBack_InvalidStateException(); } ), "doc");
		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0){ return new InvalidStateException(a0); }, [](const class std::__1::basic_string<char> & a0){ return new PyCallBack_InvalidStateException(a0); } ), "doc");
		cl.def(pybind11::init<const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &>(), pybind11::arg("message"), pybind11::arg("location"));

		cl.def("assign", (class InvalidStateException & (InvalidStateException::*)(const class InvalidStateException &)) &InvalidStateException::operator=, "C++: InvalidStateException::operator=(const class InvalidStateException &) --> class InvalidStateException &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	{ // FileException file:Exceptions.h line:113
		pybind11::class_<FileException, std::shared_ptr<FileException>, PyCallBack_FileException, RcsbException> cl(M(""), "FileException", "Generic files related exception (e.g. read error, write errror, etc.)");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](){ return new FileException(); }, [](){ return new PyCallBack_FileException(); } ), "doc");
		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0){ return new FileException(a0); }, [](const class std::__1::basic_string<char> & a0){ return new PyCallBack_FileException(a0); } ), "doc");
		cl.def(pybind11::init<const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &>(), pybind11::arg("message"), pybind11::arg("location"));

		cl.def("assign", (class FileException & (FileException::*)(const class FileException &)) &FileException::operator=, "C++: FileException::operator=(const class FileException &) --> class FileException &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	{ // InvalidOptionsException file:Exceptions.h line:124
		pybind11::class_<InvalidOptionsException, std::shared_ptr<InvalidOptionsException>, PyCallBack_InvalidOptionsException, RcsbException> cl(M(""), "InvalidOptionsException", "Invalid command line options");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](){ return new InvalidOptionsException(); }, [](){ return new PyCallBack_InvalidOptionsException(); } ), "doc");
		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0){ return new InvalidOptionsException(a0); }, [](const class std::__1::basic_string<char> & a0){ return new PyCallBack_InvalidOptionsException(a0); } ), "doc");
		cl.def(pybind11::init<const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &>(), pybind11::arg("message"), pybind11::arg("location"));

		cl.def("assign", (class InvalidOptionsException & (InvalidOptionsException::*)(const class InvalidOptionsException &)) &InvalidOptionsException::operator=, "C++: InvalidOptionsException::operator=(const class InvalidOptionsException &) --> class InvalidOptionsException &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	{ // VersionMismatchException file:Exceptions.h line:133
		pybind11::class_<VersionMismatchException, std::shared_ptr<VersionMismatchException>, PyCallBack_VersionMismatchException, RcsbException> cl(M(""), "VersionMismatchException", "Versions do not match");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](){ return new VersionMismatchException(); }, [](){ return new PyCallBack_VersionMismatchException(); } ), "doc");
		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0){ return new VersionMismatchException(a0); }, [](const class std::__1::basic_string<char> & a0){ return new PyCallBack_VersionMismatchException(a0); } ), "doc");
		cl.def(pybind11::init<const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &>(), pybind11::arg("message"), pybind11::arg("location"));

		cl.def("assign", (class VersionMismatchException & (VersionMismatchException::*)(const class VersionMismatchException &)) &VersionMismatchException::operator=, "C++: VersionMismatchException::operator=(const class VersionMismatchException &) --> class VersionMismatchException &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	{ // Block file:TableFile.h line:40
		pybind11::class_<Block, std::shared_ptr<Block>> cl(M(""), "Block", "*  \n\n*\n*  \n\n Public class that represents a data block, that contains tables.\n*\n*  This class represents a data block, that can come from DDL,\n*  dictionary or CIF files. Data block is a container of tables.\n*  This class provides methods for construction and destruction, tables\n*  manipulation (addition, retrieval, deleting, writing), data blocks\n*  comparison.");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0, class Serializer * a1){ return new Block(a0, a1); }), "doc");
		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0, class Serializer * a1, const enum eFileMode  &a2){ return new Block(a0, a1, a2); }), "doc");
		cl.def(pybind11::init<const class std::__1::basic_string<char> &, class Serializer *, const enum eFileMode, const enum Char::eCompareType>(), pybind11::arg("name"), pybind11::arg("serP"), pybind11::arg("fileMode"), pybind11::arg("caseSense"));

		cl.def_readwrite("_tables", &Block::_tables);
		cl.def("SetName", (void (Block::*)(const std::string &)) &Block::SetName, "*  Utility method, not part of users public API, and will soon be removed.\n*\n*  Sets the name of a data block.\n*\n*  \n\n - the name of the data block\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: Block::SetName(const class std::__1::basic_string<char> &) --> void", pybind11::arg("name"));
		cl.def("GetName", (const std::string & (Block::*)() const) &Block::GetName, "*  Retrieves data block name.\n*\n*  \n\n None\n*\n*  \n\n Constant reference to a string that contains data block name.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: Block::GetName() const --> const std::string &", pybind11::return_value_policy::automatic);
		cl.def("AddTable", [](Block &o) -> ISTable & { return o.AddTable(); }, "", pybind11::return_value_policy::automatic);
		cl.def("AddTable", [](Block &o, const class std::__1::basic_string<char> & a0) -> ISTable & { return o.AddTable(a0); }, "", pybind11::return_value_policy::automatic, pybind11::arg("name"));
		cl.def("AddTable", (class ISTable & (Block::*)(const std::string &, const enum Char::eCompareType)) &Block::AddTable, "*  Adds a table to the block. If a table with the specified name\n*  already exists, it will be overwritten.\n*\n*  \n\n - optional parameter that indicates the name of the\n*    table to be added\n*  \n\n - optional parameter that indicates case\n*    sensitivity of column names. Possible values are case sensitive and\n*    case in-sensitive. If not specified, a table with case sensitive\n*    column names is constructed.\n*\n*  \n\n Reference to the table\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: Block::AddTable(const class std::__1::basic_string<char> &, const enum Char::eCompareType) --> class ISTable &", pybind11::return_value_policy::automatic, pybind11::arg("name"), pybind11::arg("colCaseSense"));
		cl.def("RenameTable", (void (Block::*)(const std::string &, const std::string &)) &Block::RenameTable, "*  Changes the name of a table in the data block.\n*\n*  \n\n - the name of the table which is to be renamed\n*  \n\n - the new table name\n*\n*  \n\n None\n*\n*  \n\n  must be non-empty\n*  \n\n Table with name  must be present\n*  \n\n  must be non-empty\n*  \n\n Table with name  must not be present\n*  \n\n Block must be in create or update mode\n*\n*\n*  \n\n None\n*\n*  \n\n EmptyValueException - if  is empty\n*  \n\n NotFoundException - if table with name  does\n*    not exist\n*  \n\n EmptyValueException - if  is empty\n*  \n\n AlreadyExistsException - if table with name \n    already exists\n*  \n\n FileModeException - if block is not in create or\n*    update mode\n\nC++: Block::RenameTable(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("oldName"), pybind11::arg("newName"));
		cl.def("GetTableNames", (void (Block::*)(class std::vector<std::string, class std::allocator<std::string > > &)) &Block::GetTableNames, "*  Retrieves names of all tables in a data block.\n*\n*  \n\n - retrieved table names\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: Block::GetTableNames(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &) --> void", pybind11::arg("tableNames"));
		cl.def("IsTablePresent", (bool (Block::*)(const std::string &)) &Block::IsTablePresent, "*  Checks for table presence in the data block.\n*\n*  \n\n - table name\n*\n*  \n\n true - if table exists\n*  \n\n false - if table does not exist\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: Block::IsTablePresent(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("tableName"));
		cl.def("GetTable", (class ISTable & (Block::*)(const std::string &)) &Block::GetTable, "*  Retrieves a table reference.\n*\n*  \n\n - table name\n*\n*  \n\n Reference to the table, if table was found\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n NotFoundException - if table with name \n    does not exist\n\nC++: Block::GetTable(const class std::__1::basic_string<char> &) --> class ISTable &", pybind11::return_value_policy::automatic, pybind11::arg("tableName"));
		cl.def("GetTablePtr", (class ISTable * (Block::*)(const std::string &)) &Block::GetTablePtr, "*  Retrieves a pointer to the table.\n*\n*  \n\n - table name\n*\n*  \n\n Pointer to the table, if table was found\n*  \n\n NULL, if table was not found\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: Block::GetTablePtr(const class std::__1::basic_string<char> &) --> class ISTable *", pybind11::return_value_policy::automatic, pybind11::arg("tableName"));
		cl.def("DeleteTable", (void (Block::*)(const std::string &)) &Block::DeleteTable, "*  Deletes a table from a data block.\n*\n*  \n\n - table name\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: Block::DeleteTable(const class std::__1::basic_string<char> &) --> void", pybind11::arg("tableName"));
		cl.def("WriteTable", (void (Block::*)(class ISTable &)) &Block::WriteTable, "*  Writes a table to the data block. In this context, writing means\n*  adding it (if it does not already exist) or updating it (if it\n*  already exists).\n*\n*  \n\n - reference to the table\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: Block::WriteTable(class ISTable &) --> void", pybind11::arg("isTable"));
		cl.def("WriteTable", (void (Block::*)(class ISTable *)) &Block::WriteTable, "*  Writes a table to the data block. In this context, writing means\n*  adding it (if it does not already exist) or updating it (if it\n*  already exists).\n*\n*  \n\n - pointer to the table\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: Block::WriteTable(class ISTable *) --> void", pybind11::arg("isTableP"));
		cl.def("Print", (void (Block::*)()) &Block::Print, "*  Utility method, not part of users public API, and will soon be removed.\n\nC++: Block::Print() --> void");
		cl.def("_AddTable", [](Block &o, const class std::__1::basic_string<char> & a0) -> void { return o._AddTable(a0); }, "", pybind11::arg("name"));
		cl.def("_AddTable", [](Block &o, const class std::__1::basic_string<char> & a0, const int  &a1) -> void { return o._AddTable(a0, a1); }, "", pybind11::arg("name"), pybind11::arg("indexInFile"));
		cl.def("_AddTable", (void (Block::*)(const std::string &, const int, class ISTable *)) &Block::_AddTable, "*  Utility method, not part of users public API, and will soon be removed.\n\n  JDW rename this method to resolve llvm ambiguity issues with public method signature -\n\nC++: Block::_AddTable(const class std::__1::basic_string<char> &, const int, class ISTable *) --> void", pybind11::arg("name"), pybind11::arg("indexInFile"), pybind11::arg("isTableP"));
	}
}
