#include <CifDataInfo.h>
#include <CifFile.h>
#include <DataInfo.h>
#include <DicFile.h>
#include <GenCont.h>
#include <GenString.h>
#include <ISTable.h>
#include <Serializer.h>
#include <TableFile.h>
#include <__string>
#include <initializer_list>
#include <iterator>
#include <math.h>
#include <memory>
#include <rcsb_types.h>
#include <sstream> // __str__
#include <string>
#include <string_view>
#include <vector>

#include <pybind11/pybind11.h>
#include "pybind11/stl.h"


#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

// CifDataInfo file:CifDataInfo.h line:25
struct PyCallBack_CifDataInfo : public CifDataInfo {
	using CifDataInfo::CifDataInfo;

	void GetVersion(class std::__1::basic_string<char> & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "GetVersion");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return CifDataInfo::GetVersion(a0);
	}
	using _binder_ret_0 = const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &;
	_binder_ret_0 GetCatNames() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "GetCatNames");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_0>::value) {
				static pybind11::detail::overload_caster_t<_binder_ret_0> caster;
				return pybind11::detail::cast_ref<_binder_ret_0>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_0>(std::move(o));
		}
		return CifDataInfo::GetCatNames();
	}
	using _binder_ret_1 = const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &;
	_binder_ret_1 GetItemsNames() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "GetItemsNames");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_1>::value) {
				static pybind11::detail::overload_caster_t<_binder_ret_1> caster;
				return pybind11::detail::cast_ref<_binder_ret_1>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_1>(std::move(o));
		}
		return CifDataInfo::GetItemsNames();
	}
	bool IsCatDefined(const class std::__1::basic_string<char> & a0) const override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "IsCatDefined");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::overload_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return CifDataInfo::IsCatDefined(a0);
	}
	bool IsItemDefined(const class std::__1::basic_string<char> & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "IsItemDefined");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::overload_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return CifDataInfo::IsItemDefined(a0);
	}
	using _binder_ret_2 = const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &;
	_binder_ret_2 GetCatKeys(const class std::__1::basic_string<char> & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "GetCatKeys");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_2>::value) {
				static pybind11::detail::overload_caster_t<_binder_ret_2> caster;
				return pybind11::detail::cast_ref<_binder_ret_2>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_2>(std::move(o));
		}
		return CifDataInfo::GetCatKeys(a0);
	}
	using _binder_ret_3 = const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &;
	_binder_ret_3 GetCatAttribute(const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1, const class std::__1::basic_string<char> & a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "GetCatAttribute");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_3>::value) {
				static pybind11::detail::overload_caster_t<_binder_ret_3> caster;
				return pybind11::detail::cast_ref<_binder_ret_3>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_3>(std::move(o));
		}
		return CifDataInfo::GetCatAttribute(a0, a1, a2);
	}
	using _binder_ret_4 = const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &;
	_binder_ret_4 GetItemAttribute(const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1, const class std::__1::basic_string<char> & a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "GetItemAttribute");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_4>::value) {
				static pybind11::detail::overload_caster_t<_binder_ret_4> caster;
				return pybind11::detail::cast_ref<_binder_ret_4>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_4>(std::move(o));
		}
		return CifDataInfo::GetItemAttribute(a0, a1, a2);
	}
	void GetCatItemsNames(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > & a0, const class std::__1::basic_string<char> & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "GetCatItemsNames");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return CifDataInfo::GetCatItemsNames(a0, a1);
	}
	bool AreAllKeyItems(const class std::__1::basic_string<char> & a0, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "AreAllKeyItems");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::overload_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return DataInfo::AreAllKeyItems(a0, a1);
	}
	bool IsUnknownValueAllowed(const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "IsUnknownValueAllowed");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::overload_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return DataInfo::IsUnknownValueAllowed(a0, a1);
	}
	bool IsKeyItem(const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1, const enum Char::eCompareType a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "IsKeyItem");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::overload_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return DataInfo::IsKeyItem(a0, a1, a2);
	}
	bool MustConvertItem(const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "MustConvertItem");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::overload_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return DataInfo::MustConvertItem(a0, a1);
	}
	void StandardizeEnumItem(class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1, const class std::__1::basic_string<char> & a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "StandardizeEnumItem");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return DataInfo::StandardizeEnumItem(a0, a1, a2);
	}
	bool IsItemMandatory(const class std::__1::basic_string<char> & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "IsItemMandatory");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::overload_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return DataInfo::IsItemMandatory(a0);
	}
	bool IsSimpleDataType(const class std::__1::basic_string<char> & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "IsSimpleDataType");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::overload_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return DataInfo::IsSimpleDataType(a0);
	}
	enum eTypeCode _GetDataType(const class std::__1::basic_string<char> & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const CifDataInfo *>(this), "_GetDataType");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<enum eTypeCode>::value) {
				static pybind11::detail::overload_caster_t<enum eTypeCode> caster;
				return pybind11::detail::cast_ref<enum eTypeCode>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<enum eTypeCode>(std::move(o));
		}
		return DataInfo::_GetDataType(a0);
	}
};

void bind_GenCont(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // GenCont file:GenCont.h line:21
		pybind11::class_<GenCont, GenCont*> cl(M(""), "GenCont", "");
		pybind11::handle cl_type = cl;

		cl.def_static("IsInVector", [](const class std::__1::basic_string<char> & a0, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > & a1) -> bool { return GenCont::IsInVector(a0, a1); }, "", pybind11::arg("element"), pybind11::arg("contVector"));
		cl.def_static("IsInVector", (bool (*)(const std::string &, const class std::vector<std::string, class std::allocator<std::string > > &, const enum Char::eCompareType)) &GenCont::IsInVector, "C++: GenCont::IsInVector(const class std::__1::basic_string<char> &, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &, const enum Char::eCompareType) --> bool", pybind11::arg("element"), pybind11::arg("contVector"), pybind11::arg("compareType"));
		cl.def_static("IsInVectorCi", (bool (*)(const std::string &, const class std::vector<std::string, class std::allocator<std::string > > &)) &GenCont::IsInVectorCi, "C++: GenCont::IsInVectorCi(const class std::__1::basic_string<char> &, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &) --> bool", pybind11::arg("element"), pybind11::arg("contVector"));
	}
	{ // CifDataInfo file:CifDataInfo.h line:25
		pybind11::class_<CifDataInfo, std::shared_ptr<CifDataInfo>, PyCallBack_CifDataInfo, DataInfo> cl(M(""), "CifDataInfo", "");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init<class DicFile &>(), pybind11::arg("dictFile"));

		cl.def("GetVersion", (void (CifDataInfo::*)(std::string &)) &CifDataInfo::GetVersion, "C++: CifDataInfo::GetVersion(class std::__1::basic_string<char> &) --> void", pybind11::arg("version"));
		cl.def("GetCatNames", (const class std::vector<std::string, class std::allocator<std::string > > & (CifDataInfo::*)()) &CifDataInfo::GetCatNames, "C++: CifDataInfo::GetCatNames() --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic);
		cl.def("GetItemsNames", (const class std::vector<std::string, class std::allocator<std::string > > & (CifDataInfo::*)()) &CifDataInfo::GetItemsNames, "C++: CifDataInfo::GetItemsNames() --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic);
		cl.def("IsCatDefined", (bool (CifDataInfo::*)(const std::string &) const) &CifDataInfo::IsCatDefined, "C++: CifDataInfo::IsCatDefined(const class std::__1::basic_string<char> &) const --> bool", pybind11::arg("catName"));
		cl.def("IsItemDefined", (bool (CifDataInfo::*)(const std::string &)) &CifDataInfo::IsItemDefined, "C++: CifDataInfo::IsItemDefined(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("itemName"));
		cl.def("GetCatKeys", (const class std::vector<std::string, class std::allocator<std::string > > & (CifDataInfo::*)(const std::string &)) &CifDataInfo::GetCatKeys, "C++: CifDataInfo::GetCatKeys(const class std::__1::basic_string<char> &) --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic, pybind11::arg("catName"));
		cl.def("GetCatAttribute", (const class std::vector<std::string, class std::allocator<std::string > > & (CifDataInfo::*)(const std::string &, const std::string &, const std::string &)) &CifDataInfo::GetCatAttribute, "C++: CifDataInfo::GetCatAttribute(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic, pybind11::arg("catName"), pybind11::arg("refCatName"), pybind11::arg("refAttrName"));
		cl.def("GetItemAttribute", (const class std::vector<std::string, class std::allocator<std::string > > & (CifDataInfo::*)(const std::string &, const std::string &, const std::string &)) &CifDataInfo::GetItemAttribute, "C++: CifDataInfo::GetItemAttribute(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic, pybind11::arg("itemName"), pybind11::arg("refCatName"), pybind11::arg("refAttrName"));
		cl.def("GetCatItemsNames", (void (CifDataInfo::*)(class std::vector<std::string, class std::allocator<std::string > > &, const std::string &)) &CifDataInfo::GetCatItemsNames, "C++: CifDataInfo::GetCatItemsNames(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("itemsNames"), pybind11::arg("catName"));
	}
}
