#include <CifExcept.h>
#include <DataInfo.h>
#include <DicFile.h>
#include <DictDataInfo.h>
#include <DictObjCont.h>
#include <DictObjContInfo.h>
#include <DictObjFile.h>
#include <DictParentChild.h>
#include <GenString.h>
#include <RcsbFile.h>
#include <RcsbPlatform.h>
#include <Serializer.h>
#include <__string>
#include <fstream>
#include <initializer_list>
#include <iterator>
#include <memory>
#include <rcsb_types.h>
#include <sstream> // __str__
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

// DataInfo file:DataInfo.h line:26
struct PyCallBack_DataInfo : public DataInfo {
	using DataInfo::DataInfo;

	void GetVersion(class std::__1::basic_string<char> & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "GetVersion");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"DataInfo::GetVersion\"");
	}
	using _binder_ret_0 = const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &;
	_binder_ret_0 GetCatNames() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "GetCatNames");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_0>::value) {
				static pybind11::detail::overload_caster_t<_binder_ret_0> caster;
				return pybind11::detail::cast_ref<_binder_ret_0>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_0>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"DataInfo::GetCatNames\"");
	}
	using _binder_ret_1 = const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &;
	_binder_ret_1 GetItemsNames() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "GetItemsNames");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_1>::value) {
				static pybind11::detail::overload_caster_t<_binder_ret_1> caster;
				return pybind11::detail::cast_ref<_binder_ret_1>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_1>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"DataInfo::GetItemsNames\"");
	}
	bool IsCatDefined(const class std::__1::basic_string<char> & a0) const override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "IsCatDefined");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::overload_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"DataInfo::IsCatDefined\"");
	}
	bool IsItemDefined(const class std::__1::basic_string<char> & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "IsItemDefined");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::overload_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"DataInfo::IsItemDefined\"");
	}
	using _binder_ret_2 = const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &;
	_binder_ret_2 GetCatKeys(const class std::__1::basic_string<char> & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "GetCatKeys");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_2>::value) {
				static pybind11::detail::overload_caster_t<_binder_ret_2> caster;
				return pybind11::detail::cast_ref<_binder_ret_2>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_2>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"DataInfo::GetCatKeys\"");
	}
	using _binder_ret_3 = const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &;
	_binder_ret_3 GetCatAttribute(const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1, const class std::__1::basic_string<char> & a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "GetCatAttribute");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_3>::value) {
				static pybind11::detail::overload_caster_t<_binder_ret_3> caster;
				return pybind11::detail::cast_ref<_binder_ret_3>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_3>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"DataInfo::GetCatAttribute\"");
	}
	using _binder_ret_4 = const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &;
	_binder_ret_4 GetItemAttribute(const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1, const class std::__1::basic_string<char> & a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "GetItemAttribute");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_4>::value) {
				static pybind11::detail::overload_caster_t<_binder_ret_4> caster;
				return pybind11::detail::cast_ref<_binder_ret_4>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_4>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"DataInfo::GetItemAttribute\"");
	}
	bool AreAllKeyItems(const class std::__1::basic_string<char> & a0, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "AreAllKeyItems");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "IsUnknownValueAllowed");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "IsKeyItem");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "MustConvertItem");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "StandardizeEnumItem");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "IsItemMandatory");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "IsSimpleDataType");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const DataInfo *>(this), "_GetDataType");
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

// DictDataInfo file:DictDataInfo.h line:25
struct PyCallBack_DictDataInfo : public DictDataInfo {
	using DictDataInfo::DictDataInfo;

	void GetVersion(class std::__1::basic_string<char> & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "GetVersion");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return DictDataInfo::GetVersion(a0);
	}
	using _binder_ret_0 = const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &;
	_binder_ret_0 GetCatNames() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "GetCatNames");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_0>::value) {
				static pybind11::detail::overload_caster_t<_binder_ret_0> caster;
				return pybind11::detail::cast_ref<_binder_ret_0>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_0>(std::move(o));
		}
		return DictDataInfo::GetCatNames();
	}
	using _binder_ret_1 = const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &;
	_binder_ret_1 GetItemsNames() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "GetItemsNames");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_1>::value) {
				static pybind11::detail::overload_caster_t<_binder_ret_1> caster;
				return pybind11::detail::cast_ref<_binder_ret_1>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_1>(std::move(o));
		}
		return DictDataInfo::GetItemsNames();
	}
	bool IsCatDefined(const class std::__1::basic_string<char> & a0) const override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "IsCatDefined");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::overload_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return DictDataInfo::IsCatDefined(a0);
	}
	bool IsItemDefined(const class std::__1::basic_string<char> & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "IsItemDefined");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::overload_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return DictDataInfo::IsItemDefined(a0);
	}
	using _binder_ret_2 = const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &;
	_binder_ret_2 GetCatKeys(const class std::__1::basic_string<char> & a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "GetCatKeys");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_2>::value) {
				static pybind11::detail::overload_caster_t<_binder_ret_2> caster;
				return pybind11::detail::cast_ref<_binder_ret_2>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_2>(std::move(o));
		}
		return DictDataInfo::GetCatKeys(a0);
	}
	using _binder_ret_3 = const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &;
	_binder_ret_3 GetCatAttribute(const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1, const class std::__1::basic_string<char> & a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "GetCatAttribute");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_3>::value) {
				static pybind11::detail::overload_caster_t<_binder_ret_3> caster;
				return pybind11::detail::cast_ref<_binder_ret_3>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_3>(std::move(o));
		}
		return DictDataInfo::GetCatAttribute(a0, a1, a2);
	}
	using _binder_ret_4 = const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &;
	_binder_ret_4 GetItemAttribute(const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1, const class std::__1::basic_string<char> & a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "GetItemAttribute");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<_binder_ret_4>::value) {
				static pybind11::detail::overload_caster_t<_binder_ret_4> caster;
				return pybind11::detail::cast_ref<_binder_ret_4>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<_binder_ret_4>(std::move(o));
		}
		return DictDataInfo::GetItemAttribute(a0, a1, a2);
	}
	void GetCatItemsNames(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > & a0, const class std::__1::basic_string<char> & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "GetCatItemsNames");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return DictDataInfo::GetCatItemsNames(a0, a1);
	}
	void GetParentCifItems(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > & a0, const class std::__1::basic_string<char> & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "GetParentCifItems");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return DictDataInfo::GetParentCifItems(a0, a1);
	}
	bool AreAllKeyItems(const class std::__1::basic_string<char> & a0, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "AreAllKeyItems");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "IsUnknownValueAllowed");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "IsKeyItem");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "MustConvertItem");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "StandardizeEnumItem");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "IsItemMandatory");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "IsSimpleDataType");
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
		pybind11::function overload = pybind11::get_overload(static_cast<const DictDataInfo *>(this), "_GetDataType");
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

// DictParentChild file:DictParentChild.h line:27
struct PyCallBack_DictParentChild : public DictParentChild {
	using DictParentChild::DictParentChild;

	void GetParentCifItems(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > & a0, const class std::__1::basic_string<char> & a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const DictParentChild *>(this), "GetParentCifItems");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::overload_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return DictParentChild::GetParentCifItems(a0, a1);
	}
};

void bind_DataInfo(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // DataInfo file:DataInfo.h line:26
		pybind11::class_<DataInfo, std::shared_ptr<DataInfo>, PyCallBack_DataInfo> cl(M(""), "DataInfo", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new PyCallBack_DataInfo(); } ) );
		cl.def("GetVersion", (void (DataInfo::*)(std::string &)) &DataInfo::GetVersion, "C++: DataInfo::GetVersion(class std::__1::basic_string<char> &) --> void", pybind11::arg("version"));
		cl.def("GetCatNames", (const class std::vector<std::string, class std::allocator<std::string > > & (DataInfo::*)()) &DataInfo::GetCatNames, "C++: DataInfo::GetCatNames() --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic);
		cl.def("GetItemsNames", (const class std::vector<std::string, class std::allocator<std::string > > & (DataInfo::*)()) &DataInfo::GetItemsNames, "C++: DataInfo::GetItemsNames() --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic);
		cl.def("IsCatDefined", (bool (DataInfo::*)(const std::string &) const) &DataInfo::IsCatDefined, "C++: DataInfo::IsCatDefined(const class std::__1::basic_string<char> &) const --> bool", pybind11::arg("catName"));
		cl.def("IsItemDefined", (bool (DataInfo::*)(const std::string &)) &DataInfo::IsItemDefined, "C++: DataInfo::IsItemDefined(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("itemName"));
		cl.def("GetCatKeys", (const class std::vector<std::string, class std::allocator<std::string > > & (DataInfo::*)(const std::string &)) &DataInfo::GetCatKeys, "C++: DataInfo::GetCatKeys(const class std::__1::basic_string<char> &) --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic, pybind11::arg("catName"));
		cl.def("GetCatAttribute", (const class std::vector<std::string, class std::allocator<std::string > > & (DataInfo::*)(const std::string &, const std::string &, const std::string &)) &DataInfo::GetCatAttribute, "C++: DataInfo::GetCatAttribute(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic, pybind11::arg("catName"), pybind11::arg("refCatName"), pybind11::arg("refAttribName"));
		cl.def("GetItemAttribute", (const class std::vector<std::string, class std::allocator<std::string > > & (DataInfo::*)(const std::string &, const std::string &, const std::string &)) &DataInfo::GetItemAttribute, "C++: DataInfo::GetItemAttribute(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic, pybind11::arg("itemName"), pybind11::arg("refCatName"), pybind11::arg("refAttribName"));
		cl.def("AreAllKeyItems", (bool (DataInfo::*)(const std::string &, const class std::vector<std::string, class std::allocator<std::string > > &)) &DataInfo::AreAllKeyItems, "C++: DataInfo::AreAllKeyItems(const class std::__1::basic_string<char> &, const class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &) --> bool", pybind11::arg("catName"), pybind11::arg("attribsNames"));
		cl.def("IsUnknownValueAllowed", (bool (DataInfo::*)(const std::string &, const std::string &)) &DataInfo::IsUnknownValueAllowed, "C++: DataInfo::IsUnknownValueAllowed(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> bool", pybind11::arg("catName"), pybind11::arg("attribName"));
		cl.def("IsKeyItem", [](DataInfo &o, const class std::__1::basic_string<char> & a0, const class std::__1::basic_string<char> & a1) -> bool { return o.IsKeyItem(a0, a1); }, "", pybind11::arg("catName"), pybind11::arg("attribName"));
		cl.def("IsKeyItem", (bool (DataInfo::*)(const std::string &, const std::string &, const enum Char::eCompareType)) &DataInfo::IsKeyItem, "C++: DataInfo::IsKeyItem(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const enum Char::eCompareType) --> bool", pybind11::arg("catName"), pybind11::arg("attribName"), pybind11::arg("compareType"));
		cl.def("MustConvertItem", (bool (DataInfo::*)(const std::string &, const std::string &)) &DataInfo::MustConvertItem, "C++: DataInfo::MustConvertItem(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> bool", pybind11::arg("catName"), pybind11::arg("attribName"));
		cl.def("StandardizeEnumItem", (void (DataInfo::*)(std::string &, const std::string &, const std::string &)) &DataInfo::StandardizeEnumItem, "C++: DataInfo::StandardizeEnumItem(class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("value"), pybind11::arg("catName"), pybind11::arg("attribName"));
		cl.def("GetMandatoryItems", (void (DataInfo::*)(class std::vector<std::string, class std::allocator<std::string > > &, const std::string &)) &DataInfo::GetMandatoryItems, "C++: DataInfo::GetMandatoryItems(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("mandItemsNames"), pybind11::arg("catName"));
		cl.def("IsItemMandatory", (bool (DataInfo::*)(const std::string &, const std::string &)) &DataInfo::IsItemMandatory, "C++: DataInfo::IsItemMandatory(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> bool", pybind11::arg("catName"), pybind11::arg("attribName"));
		cl.def("IsItemMandatory", (bool (DataInfo::*)(const std::string &)) &DataInfo::IsItemMandatory, "C++: DataInfo::IsItemMandatory(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("itemName"));
		cl.def("IsSimpleDataType", (bool (DataInfo::*)(const std::string &)) &DataInfo::IsSimpleDataType, "C++: DataInfo::IsSimpleDataType(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("itemName"));
		cl.def("_GetDataType", (enum eTypeCode (DataInfo::*)(const std::string &)) &DataInfo::_GetDataType, "C++: DataInfo::_GetDataType(const class std::__1::basic_string<char> &) --> enum eTypeCode", pybind11::arg("itemName"));
		cl.def("assign", (class DataInfo & (DataInfo::*)(const class DataInfo &)) &DataInfo::operator=, "C++: DataInfo::operator=(const class DataInfo &) --> class DataInfo &", pybind11::return_value_policy::automatic, pybind11::arg(""));
	}
	{ // DictDataInfo file:DictDataInfo.h line:25
		pybind11::class_<DictDataInfo, std::shared_ptr<DictDataInfo>, PyCallBack_DictDataInfo, DataInfo> cl(M(""), "DictDataInfo", "");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init<const class DictObjCont &>(), pybind11::arg("dictObjCont"));

		cl.def("GetVersion", (void (DictDataInfo::*)(std::string &)) &DictDataInfo::GetVersion, "C++: DictDataInfo::GetVersion(class std::__1::basic_string<char> &) --> void", pybind11::arg("version"));
		cl.def("GetCatNames", (const class std::vector<std::string, class std::allocator<std::string > > & (DictDataInfo::*)()) &DictDataInfo::GetCatNames, "C++: DictDataInfo::GetCatNames() --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic);
		cl.def("GetItemsNames", (const class std::vector<std::string, class std::allocator<std::string > > & (DictDataInfo::*)()) &DictDataInfo::GetItemsNames, "C++: DictDataInfo::GetItemsNames() --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic);
		cl.def("IsCatDefined", (bool (DictDataInfo::*)(const std::string &) const) &DictDataInfo::IsCatDefined, "C++: DictDataInfo::IsCatDefined(const class std::__1::basic_string<char> &) const --> bool", pybind11::arg("catName"));
		cl.def("IsItemDefined", (bool (DictDataInfo::*)(const std::string &)) &DictDataInfo::IsItemDefined, "C++: DictDataInfo::IsItemDefined(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("itemName"));
		cl.def("GetCatKeys", (const class std::vector<std::string, class std::allocator<std::string > > & (DictDataInfo::*)(const std::string &)) &DictDataInfo::GetCatKeys, "C++: DictDataInfo::GetCatKeys(const class std::__1::basic_string<char> &) --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic, pybind11::arg("catName"));
		cl.def("GetCatAttribute", (const class std::vector<std::string, class std::allocator<std::string > > & (DictDataInfo::*)(const std::string &, const std::string &, const std::string &)) &DictDataInfo::GetCatAttribute, "C++: DictDataInfo::GetCatAttribute(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic, pybind11::arg("catName"), pybind11::arg("refCatName"), pybind11::arg("refAttrName"));
		cl.def("GetItemAttribute", (const class std::vector<std::string, class std::allocator<std::string > > & (DictDataInfo::*)(const std::string &, const std::string &, const std::string &)) &DictDataInfo::GetItemAttribute, "C++: DictDataInfo::GetItemAttribute(const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> const class std::vector<std::string, class std::allocator<std::string > > &", pybind11::return_value_policy::automatic, pybind11::arg("itemName"), pybind11::arg("refCatName"), pybind11::arg("refAttrName"));
		cl.def("GetCatItemsNames", (void (DictDataInfo::*)(class std::vector<std::string, class std::allocator<std::string > > &, const std::string &)) &DictDataInfo::GetCatItemsNames, "C++: DictDataInfo::GetCatItemsNames(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("itemsNames"), pybind11::arg("catName"));
		cl.def("GetParentCifItems", (void (DictDataInfo::*)(class std::vector<std::string, class std::allocator<std::string > > &, const std::string &)) &DictDataInfo::GetParentCifItems, "C++: DictDataInfo::GetParentCifItems(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("parCifItems"), pybind11::arg("cifItemName"));
	}
	{ // DictParentChild file:DictParentChild.h line:27
		pybind11::class_<DictParentChild, std::shared_ptr<DictParentChild>, PyCallBack_DictParentChild, ParentChild> cl(M(""), "DictParentChild", "");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init<const class DictObjCont &, class DictDataInfo &>(), pybind11::arg("dictObjCont"), pybind11::arg("dictDataInfo"));

		cl.def("GetDictObjCont", (const class DictObjCont & (DictParentChild::*)()) &DictParentChild::GetDictObjCont, "C++: DictParentChild::GetDictObjCont() --> const class DictObjCont &", pybind11::return_value_policy::automatic);
	}
	{ // RcsbPlatform file:RcsbPlatform.h line:14
		pybind11::class_<RcsbPlatform, std::shared_ptr<RcsbPlatform>> cl(M(""), "RcsbPlatform", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new RcsbPlatform(); } ) );
		cl.def_static("IsLittleEndian", (bool (*)()) &RcsbPlatform::IsLittleEndian, "C++: RcsbPlatform::IsLittleEndian() --> bool");
	}
	{ // CifExcept file:CifExcept.h line:28
		pybind11::class_<CifExcept, std::shared_ptr<CifExcept>> cl(M(""), "CifExcept", "*  \n\n*\n*  \n\n Static class that represents some exceptions in CIF files\n*    related to data values.\n*");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new CifExcept(); } ) );
		cl.def_static("CanBeUnknown", (bool (*)(const std::string &)) &CifExcept::CanBeUnknown, "C++: CifExcept::CanBeUnknown(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("itemName"));
		cl.def_static("CanBeInapplicable", (bool (*)(const std::string &)) &CifExcept::CanBeInapplicable, "C++: CifExcept::CanBeInapplicable(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("itemName"));
		cl.def_static("IsBadParentRelation", (bool (*)(const std::string &)) &CifExcept::IsBadParentRelation, "C++: CifExcept::IsBadParentRelation(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("itemName"));
		cl.def_static("IsBadChildRelation", (bool (*)(const std::string &)) &CifExcept::IsBadChildRelation, "C++: CifExcept::IsBadChildRelation(const class std::__1::basic_string<char> &) --> bool", pybind11::arg("itemName"));
	}
	{ // RcsbFile file:RcsbFile.h line:15
		pybind11::class_<RcsbFile, RcsbFile*> cl(M(""), "RcsbFile", "");
		pybind11::handle cl_type = cl;

		cl.def_static("IsEmpty", (bool (*)(class std::basic_ofstream<char, struct std::char_traits<char> > &)) &RcsbFile::IsEmpty, "C++: RcsbFile::IsEmpty(class std::__1::basic_ofstream<char, struct std::__1::char_traits<char> > &) --> bool", pybind11::arg("fileStream"));
		cl.def_static("Delete", (void (*)(const std::string &)) &RcsbFile::Delete, "C++: RcsbFile::Delete(const class std::__1::basic_string<char> &) --> void", pybind11::arg("fileName"));
		cl.def_static("RelativeFileName", (void (*)(std::string &, const std::string &)) &RcsbFile::RelativeFileName, "C++: RcsbFile::RelativeFileName(class std::__1::basic_string<char> &, const class std::__1::basic_string<char> &) --> void", pybind11::arg("relName"), pybind11::arg("absName"));
	}
	{ // DictObjFile file:DictObjFile.h line:40
		pybind11::class_<DictObjFile, std::shared_ptr<DictObjFile>> cl(M(""), "DictObjFile", "*  \n\n*\n*  \n\n Public class that represents a dictionary object file.\n*\n*  This class represents a dictionary object file. This file is a container\n*  of dictionary objects. Each dictionary object is a container of its\n*  attributes and of objects of type: item, sub-category and category. Each\n*  of those objects is a container of relevant attributes for that object\n*  type. This class provides methods for construction/destruction, building\n*  the dictionary object file from a dictionary, writing/reading dictionary\n*  object file to/from the persistent storage file, accessing the\n*  dictionaries and printing the content of the dictionary object file.");
		pybind11::handle cl_type = cl;

		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0){ return new DictObjFile(a0); }), "doc");
		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0, const enum eFileMode  &a1){ return new DictObjFile(a0, a1); }), "doc");
		cl.def(pybind11::init([](const class std::__1::basic_string<char> & a0, const enum eFileMode  &a1, const bool  &a2){ return new DictObjFile(a0, a1, a2); }), "doc");
		cl.def(pybind11::init<const class std::__1::basic_string<char> &, const enum eFileMode, const bool, const class std::__1::basic_string<char> &>(), pybind11::arg("persStorFileName"), pybind11::arg("fileMode"), pybind11::arg("verbose"), pybind11::arg("dictSdbFileName"));

		cl.def("Build", (void (DictObjFile::*)()) &DictObjFile::Build, "*  Builds a dictionary object file from the dictionary. This method\n*  parses the dictionary, parses the DDL, verifies the dictionary\n*  against the DDL and constructs objects.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n FileModeException - if dictionary object file is not in\n*    create mode\n\nC++: DictObjFile::Build() --> void");
		cl.def("Write", (void (DictObjFile::*)()) &DictObjFile::Write, "*  Writes a dictionary object file to the persistent storage file.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n FileModeException - if dictionary object file is not in\n*    create mode\n\nC++: DictObjFile::Write() --> void");
		cl.def("Read", (void (DictObjFile::*)()) &DictObjFile::Read, "*  Reads a dictionary object file from the persistent storage file.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n FileModeException - if dictionary object file is not in\n*    read mode\n\nC++: DictObjFile::Read() --> void");
		cl.def("GetNumDictionaries", (unsigned int (DictObjFile::*)()) &DictObjFile::GetNumDictionaries, "*  Retrieves the number of dictionaries in the dictionary object file.\n*\n*  \n\n None\n*\n*  \n\n The number of dictionaries in the dictionary object file.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: DictObjFile::GetNumDictionaries() --> unsigned int");
		cl.def("GetDictionaryNames", (void (DictObjFile::*)(class std::vector<std::string, class std::allocator<std::string > > &)) &DictObjFile::GetDictionaryNames, "*  Retrieves dictionary names of the dictionaries in the dictionary\n*  object file.\n*\n*  \n\n - retrieved dictionary names\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: DictObjFile::GetDictionaryNames(class std::__1::vector<class std::__1::basic_string<char>, class std::__1::allocator<class std::__1::basic_string<char> > > &) --> void", pybind11::arg("dictNames"));
		cl.def("GetDictObjCont", (class DictObjCont & (DictObjFile::*)(const std::string &)) &DictObjFile::GetDictObjCont, "*  Retrieves a reference to the dictionary object.\n*\n*  \n\n - dictionary name\n*\n*  \n\n Reference to the dictionary object.\n*\n*  \n\n Dictionary with name  must be present\n*\n*  \n\n None\n*\n*  \n\n NotFoundException - if dictionary with name \n    does not exist\n\nC++: DictObjFile::GetDictObjCont(const class std::__1::basic_string<char> &) --> class DictObjCont &", pybind11::return_value_policy::automatic, pybind11::arg("dictName"));
		cl.def("Print", (void (DictObjFile::*)()) &DictObjFile::Print, "*  Prints the content of the dictionary object file.\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n None\n*\n*  \n\n: None\n\nC++: DictObjFile::Print() --> void");
	}
}
