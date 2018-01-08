#include <CifFile.h>
#include <CifFileReadDef.h>
#include <CifFileUtil.h>
#include <DicFile.h>
#include <DictObjCont.h>
#include <DictObjContInfo.h>
#include <GenString.h>
#include <ISTable.h>
#include <ITTable.h>
#include <Serializer.h>
#include <TableFile.h>
#include <__string>
#include <initializer_list>
#include <ios>
#include <iterator>
#include <memory>
#include <ostream>
#include <sstream> // __str__
#include <string>
#include <string_view>
#include <utility>
#include <vector>

#include <pybind11/pybind11.h>
#include "pybind11/stl.h"


#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

// ObjCont file:DictObjCont.h line:35
struct PyCallBack_ObjCont : public ObjCont {
	using ObjCont::ObjCont;

	void Read(unsigned int a0, unsigned int a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const ObjCont *>(this), "Read");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return ObjCont::Read(a0, a1);
	}
	unsigned int Write() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const ObjCont *>(this), "Write");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<unsigned int>::value) {
				static pybind11::detail::overload_caster_t<unsigned int> caster;
				return pybind11::detail::cast_ref<unsigned int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<unsigned int>(std::move(o));
		}
		return ObjCont::Write();
	}
	void Build() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const ObjCont *>(this), "Build");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return ObjCont::Build();
	}
};

// ItemObjCont file:DictObjCont.h line:158
struct PyCallBack_ItemObjCont : public ItemObjCont {
	using ItemObjCont::ItemObjCont;

	void Build() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const ItemObjCont *>(this), "Build");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return ItemObjCont::Build();
	}
	void Read(unsigned int a0, unsigned int a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const ItemObjCont *>(this), "Read");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return ObjCont::Read(a0, a1);
	}
	unsigned int Write() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const ItemObjCont *>(this), "Write");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<unsigned int>::value) {
				static pybind11::detail::overload_caster_t<unsigned int> caster;
				return pybind11::detail::cast_ref<unsigned int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<unsigned int>(std::move(o));
		}
		return ObjCont::Write();
	}
};

// DictObjCont file:DictObjCont.h line:201
struct PyCallBack_DictObjCont : public DictObjCont {
	using DictObjCont::DictObjCont;

	void Build() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DictObjCont *>(this), "Build");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return DictObjCont::Build();
	}
	unsigned int Write() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DictObjCont *>(this), "Write");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<unsigned int>::value) {
				static pybind11::detail::overload_caster_t<unsigned int> caster;
				return pybind11::detail::cast_ref<unsigned int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<unsigned int>(std::move(o));
		}
		return DictObjCont::Write();
	}
	void Read(unsigned int a0, unsigned int a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DictObjCont *>(this), "Read");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return DictObjCont::Read(a0, a1);
	}
};

void bind_CifFileUtil(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	// ParseCifSelective(const class std::__1::basic_string<char> &, const class CifFileReadDef &, const bool, const unsigned int, const unsigned int, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) file:CifFileUtil.h line:44
	M("").def("ParseCifSelective", [](const class std::__1::basic_string<char> & a0, const class CifFileReadDef & a1) -> CifFile * { return ParseCifSelective(a0, a1); }, "", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("readDef"));
	M("").def("ParseCifSelective", [](const class std::__1::basic_string<char> & a0, const class CifFileReadDef & a1, const bool  &a2) -> CifFile * { return ParseCifSelective(a0, a1, a2); }, "", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("readDef"), pybind11::arg("verbose"));
	M("").def("ParseCifSelective", [](const class std::__1::basic_string<char> & a0, const class CifFileReadDef & a1, const bool  &a2, const unsigned int  &a3) -> CifFile * { return ParseCifSelective(a0, a1, a2, a3); }, "", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("readDef"), pybind11::arg("verbose"), pybind11::arg("intCaseSense"));
	M("").def("ParseCifSelective", [](const class std::__1::basic_string<char> & a0, const class CifFileReadDef & a1, const bool  &a2, const unsigned int  &a3, const unsigned int  &a4) -> CifFile * { return ParseCifSelective(a0, a1, a2, a3, a4); }, "", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("readDef"), pybind11::arg("verbose"), pybind11::arg("intCaseSense"), pybind11::arg("maxLineLength"));
	M("").def("ParseCifSelective", [](const class std::__1::basic_string<char> & a0, const class CifFileReadDef & a1, const bool  &a2, const unsigned int  &a3, const unsigned int  &a4, const class std::__1::basic_string<char> & a5) -> CifFile * { return ParseCifSelective(a0, a1, a2, a3, a4, a5); }, "", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("readDef"), pybind11::arg("verbose"), pybind11::arg("intCaseSense"), pybind11::arg("maxLineLength"), pybind11::arg("nullValue"));
	M("").def("ParseCifSelective", (class CifFile * (*)(const std::string &, const class CifFileReadDef &, const bool, const unsigned int, const unsigned int, const std::string &, const std::string &)) &ParseCifSelective, "C++: ParseCifSelective(const class std::__1::basic_string<char> &, const class CifFileReadDef &, const bool, const unsigned int, const unsigned int, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> class CifFile *", pybind11::return_value_policy::automatic, pybind11::arg("fileName"), pybind11::arg("readDef"), pybind11::arg("verbose"), pybind11::arg("intCaseSense"), pybind11::arg("maxLineLength"), pybind11::arg("nullValue"), pybind11::arg("parseLogFileName"));

	// DataCorrection(class CifFile &, class DicFile &) file:CifFileUtil.h line:66
	M("").def("DataCorrection", (void (*)(class CifFile &, class DicFile &)) &DataCorrection, "*  Corrects a CIF file with respect to the following:\n*    - Sets proper casing of the case-insensitive enumerations\n*\n*  \n\n - reference to a dictionary file. The check is\n*    done against the first block in the dictionary file.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: DataCorrection(class CifFile &, class DicFile &) --> void", pybind11::arg("cifFile"), pybind11::arg("dicRef"));

	{ // ObjContInfo file:DictObjContInfo.h line:39
		pybind11::class_<ObjContInfo, std::shared_ptr<ObjContInfo>> cl(M(""), "ObjContInfo", "*  \n\n*\n*  \n\n Public class that represents a generic information class for the\n*    generic object container.\n*\n*  This class represents a generic information class for the generic object\n*  container. It is intended to be used as a base class for information\n*  classes of object containers. It defines the names of categories and the\n*  names of items, that are used in attributes retrieval method of ObjCont\n*  class.");
		pybind11::handle cl_type = cl;

		cl.def_readwrite("_objContInfoDescr", &ObjContInfo::_objContInfoDescr);
		cl.def_readwrite("_cats", &ObjContInfo::_cats);
		cl.def_readwrite("_catMap", &ObjContInfo::_catMap);
		cl.def("AddCat", (void (ObjContInfo::*)(const std::string &)) &ObjContInfo::AddCat, "*  Utility method, not part of users public API, and will soon be\n*  removed.\n\nC++: ObjContInfo::AddCat(const class std::__1::basic_string<char> &) --> void", pybind11::arg("catName"));
		cl.def("AddCat", [](ObjContInfo &o, const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1) -> void { return o.AddCat(a0, a1); }, "", pybind11::arg("catName"), pybind11::arg("col1"));
		cl.def("AddCat", [](ObjContInfo &o, const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1, const bool  &a2) -> void { return o.AddCat(a0, a1, a2); }, "", pybind11::arg("catName"), pybind11::arg("col1"), pybind11::arg("nonDefaultValue"));
		cl.def("AddCat", (void (ObjContInfo::*)(const std::string &, const std::string &, const bool, const bool)) &ObjContInfo::AddCat, "*  Utility method, not part of users public API, and will soon be\n*  removed.\n\nC++: ObjContInfo::AddCat(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const bool, const bool) --> void", pybind11::arg("catName"), pybind11::arg("col1"), pybind11::arg("nonDefaultValue"), pybind11::arg("inheritance"));
		cl.def("AddItem", (void (ObjContInfo::*)(const std::string &, const std::string &)) &ObjContInfo::AddItem, "*  Utility method, not part of users public API, and will soon be\n*  removed.\n\nC++: ObjContInfo::AddItem(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("descr"), pybind11::arg("itemName"));
		cl.def("GetItemIndex", (unsigned int (ObjContInfo::*)(const std::string &, const std::string &) const) &ObjContInfo::GetItemIndex, "*  Utility method, not part of users public API, and will soon be\n*  removed.\n\nC++: ObjContInfo::GetItemIndex(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) const --> unsigned int", pybind11::arg("catName"), pybind11::arg("itemName"));
		cl.def("GetItemIndices", (struct std::pair<unsigned int, unsigned int> (ObjContInfo::*)(const std::string &, const std::string &) const) &ObjContInfo::GetItemIndices, "*  Utility method, not part of users public API, and will soon be\n*  removed.\n\nC++: ObjContInfo::GetItemIndices(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) const --> struct std::pair<unsigned int, unsigned int>", pybind11::arg("catName"), pybind11::arg("itemName"));
		cl.def("assign", (class ObjContInfo & (ObjContInfo::*)(const class ObjContInfo &)) &ObjContInfo::operator=, "C++: ObjContInfo::operator=(const class ObjContInfo &) --> class ObjContInfo &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	{ // DictObjContInfo file:DictObjContInfo.h line:135
		pybind11::class_<DictObjContInfo, DictObjContInfo*, ObjContInfo> cl(M(""), "DictObjContInfo", "*  \n\n*\n*  \n\n Private class that represents an information class for the\n*    dictionary object container.");
		pybind11::handle cl_type = cl;

		cl.def_static("GetInstance", (class DictObjContInfo & (*)()) &DictObjContInfo::GetInstance, "C++: DictObjContInfo::GetInstance() --> class DictObjContInfo &", pybind11::return_value_policy::automatic);
	}
	{ // CatObjContInfo file:DictObjContInfo.h line:156
		pybind11::class_<CatObjContInfo, CatObjContInfo*, ObjContInfo> cl(M(""), "CatObjContInfo", "*  \n\n*\n*  \n\n Private class that represents an information class for the\n*    category object container.");
		pybind11::handle cl_type = cl;

		cl.def_static("GetInstance", (class CatObjContInfo & (*)()) &CatObjContInfo::GetInstance, "C++: CatObjContInfo::GetInstance() --> class CatObjContInfo &", pybind11::return_value_policy::automatic);
	}
	{ // SubcatObjContInfo file:DictObjContInfo.h line:177
		pybind11::class_<SubcatObjContInfo, SubcatObjContInfo*, ObjContInfo> cl(M(""), "SubcatObjContInfo", "*  \n\n*\n*  \n\n Private class that represents an information class for the\n*    sub-category object container.");
		pybind11::handle cl_type = cl;

		cl.def_static("GetInstance", (class SubcatObjContInfo & (*)()) &SubcatObjContInfo::GetInstance, "C++: SubcatObjContInfo::GetInstance() --> class SubcatObjContInfo &", pybind11::return_value_policy::automatic);
	}
	{ // ItemObjContInfo file:DictObjContInfo.h line:198
		pybind11::class_<ItemObjContInfo, ItemObjContInfo*, ObjContInfo> cl(M(""), "ItemObjContInfo", "*  \n\n*\n*  \n\n Private class that represents an information class for the\n*    item object container.");
		pybind11::handle cl_type = cl;

		cl.def_static("GetInstance", (class ItemObjContInfo & (*)()) &ItemObjContInfo::GetInstance, "C++: ItemObjContInfo::GetInstance() --> class ItemObjContInfo &", pybind11::return_value_policy::automatic);
	}
	{ // ObjCont file:DictObjCont.h line:35
		pybind11::class_<ObjCont, std::shared_ptr<ObjCont>, PyCallBack_ObjCont> cl(M(""), "ObjCont", "*  \n\n*\n*  \n\n Public class that represents a generic object container.\n*\n*  This class represents a generic object container of attributes. It is\n*  to be used directly or as a base class for non-generic object containers.\n*  This class provides methods for retrieving its attributes and\n*  printing its content.");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init<class Serializer &, class DicFile &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class ObjContInfo &>(), pybind11::arg("ser"), pybind11::arg("dicFile"), pybind11::arg("blockName"), pybind11::arg("id"), pybind11::arg("objContInfo"));

		cl.def("Init", (void (ObjCont::*)()) &ObjCont::Init, "*  Utility method, not part of users public API, and will soon be\n*  removed.\n\nC++: ObjCont::Init() --> void");
		cl.def("GetName", (const std::string & (ObjCont::*)() const) &ObjCont::GetName, "*  Must stay in public API.\n\nC++: ObjCont::GetName() const --> const std::string &", pybind11::return_value_policy::automatic);
		cl.def("Read", [](ObjCont &o, unsigned int  const &a0) -> void { return o.Read(a0); }, "", pybind11::arg("which"));
		cl.def("Read", (void (ObjCont::*)(unsigned int, unsigned int)) &ObjCont::Read, "*  Utility method, not part of users public API, and will soon be\n*  removed.\n\nC++: ObjCont::Read(unsigned int, unsigned int) --> void", pybind11::arg("which"), pybind11::arg("Index"));
		cl.def("Write", (unsigned int (ObjCont::*)()) &ObjCont::Write, "*  Utility method, not part of users public API, and will soon be\n*  removed.\n\nC++: ObjCont::Write() --> unsigned int");
		cl.def("GetAttribute", (const class std::vector<std::string, class std::allocator<std::string > > & (ObjCont::*)(const std::string &, const std::string &) const) &ObjCont::GetAttribute, "*  Retrieves a constant reference to the vector of values of the\n*  object container attribute, which is specified with a category name\n*  and an item name.\n*\n*  \n\n - category name\n*  \n\n - item name\n*\n*  \n\n Constant reference to the vector of attribute values.\n*\n*  \n\n Category with name  and item with name \n    must be present\n*\n*  \n\n None\n*\n*  \n\n NotFoundException - if category with name \n    or item with name  does not exist\n\nC++: ObjCont::GetAttribute(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) const --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic, pybind11::arg("catName"), pybind11::arg("itemName"));
		cl.def("Print", (void (ObjCont::*)() const) &ObjCont::Print, "*  Prints the content of the object container.\n*\n*  \n\n None \n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: ObjCont::Print() const --> void");
		cl.def("SetVerbose", (void (ObjCont::*)(bool)) &ObjCont::SetVerbose, "*  Utility method, not part of users public API, and will soon be\n*  removed.\n\nC++: ObjCont::SetVerbose(bool) --> void", pybind11::arg("verbose"));
		cl.def("Build", (void (ObjCont::*)()) &ObjCont::Build, "*  Utility method, not part of users public API, and will soon be\n*  removed.\n\nC++: ObjCont::Build() --> void");
	}
	{ // ItemObjCont file:DictObjCont.h line:158
		pybind11::class_<ItemObjCont, std::shared_ptr<ItemObjCont>, PyCallBack_ItemObjCont, ObjCont> cl(M(""), "ItemObjCont", "*  \n\n*\n*  \n\n Private class that represents an item object container.\n*\n*  This class represents an item object container, i.e., an object\n*  container of type \"item\". In addition to ObjCont features, this class\n*  adds support for item decendents.");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init<class Serializer &, class DicFile &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &>(), pybind11::arg("ser"), pybind11::arg("dicFile"), pybind11::arg("blockName"), pybind11::arg("itemName"));

		cl.def("Build", (void (ItemObjCont::*)()) &ItemObjCont::Build, "*  Utility method, not part of users public API, and will soon be\n*  removed.\n\nC++: ItemObjCont::Build() --> void");
	}
	{ // DictObjCont file:DictObjCont.h line:201
		pybind11::class_<DictObjCont, std::shared_ptr<DictObjCont>, PyCallBack_DictObjCont, ObjCont> cl(M(""), "DictObjCont", "*  \n\n*\n*  \n\n Public class that represents a dictionary object container.\n*\n*  This class represents a dictionary object container, i.e., an object\n*  container of type \"dictionary\". A dictionary object container is a\n*  container of its attributes and of objects of type: item, sub-category\n*  and category. In addition to ObjCont features, this class has a method\n*  to get references to other object containers that it contains.");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init<class Serializer &, class DicFile &, const class std::__1::basic_string<char> &>(), pybind11::arg("ser"), pybind11::arg("dicFile"), pybind11::arg("blockName"));

		cl.def("Build", (void (DictObjCont::*)()) &DictObjCont::Build, "*  Utility method, not part of users public API, and will soon be\n*  removed.\n\nC++: DictObjCont::Build() --> void");
		cl.def("Write", (unsigned int (DictObjCont::*)()) &DictObjCont::Write, "*  Utility method, not part of users public API, and will soon be\n*  removed.\n\nC++: DictObjCont::Write() --> unsigned int");
		cl.def("Read", [](DictObjCont &o, unsigned int  const &a0) -> void { return o.Read(a0); }, "", pybind11::arg("which"));
		cl.def("Read", (void (DictObjCont::*)(unsigned int, unsigned int)) &DictObjCont::Read, "*  Utility method, not part of users public API, and will soon be\n*  removed.\n\nC++: DictObjCont::Read(unsigned int, unsigned int) --> void", pybind11::arg("which"), pybind11::arg("Index"));
		cl.def("GetObjCont", (const class ObjCont & (DictObjCont::*)(const std::string &, const class ObjContInfo &) const) &DictObjCont::GetObjCont, "*  Retrieves a reference to the generic object container, which is\n*  specified with its name and its type.\n*\n*  \n\n - object container name\n*  \n\n - reference to the object container\n*    information, that defines object container's type. It can have the\n*    following values: \n*    RcsbItem - indicates that the object container is of type \"item\" \n*    RcsbSubcat - indicates that the object container is of type\n*      \"sub-category\" \n*    RcsbCat - indicates that the object container is of type \"category\"\n*\n*  \n\n Reference to the generic object container\n*\n*  \n\n Object container with name  must be present\n*\n*  \n\n None\n*\n*  \n\n NotFoundException - if object container with name\n*     does not exist\n\nC++: DictObjCont::GetObjCont(const class std::__1::basic_string<char> &, const class ObjContInfo &) const --> const class ObjCont &", pybind11::return_value_policy::automatic, pybind11::arg("contName"), pybind11::arg("objContInfo"));
		cl.def("Print", (void (DictObjCont::*)()) &DictObjCont::Print, "*  Prints the content of the object container, which includes its\n*  attributes and the content of all the object containers that it\n*  contains.\n*\n*  \n\n None \n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: DictObjCont::Print() --> void");
	}
}
