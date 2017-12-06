//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$


/**
** \file DictDataInfo.h
**
** XML dictionary items class.
*/


#ifndef DICTDATAINFO_H
#define DICTDATAINFO_H


#include <string>
#include <vector>

#include <DataInfo.h>
#include <DictObjCont.h>


class DictDataInfo : public DataInfo
{
  public:
    DictDataInfo(const DictObjCont& dictObjCont);
    ~DictDataInfo();

    void GetVersion(std::string& version);

    virtual const std::vector<std::string>& GetCatNames();

    const std::vector<std::string>& GetItemsNames();

    bool IsCatDefined(const std::string& catName) const;

    bool IsItemDefined(const std::string& itemName);

    const std::vector<std::string>& GetCatKeys(const std::string& catName);

    const std::vector<std::string>& GetCatAttribute(const std::string& catName,
      const std::string& refCatName, const std::string& refAttrName);

    const std::vector<std::string>&
      GetItemAttribute(const std::string& itemName,
      const std::string& refCatName, const std::string& refAttrName);

    virtual void GetCatItemsNames(std::vector<std::string>& itemsNames,
      const std::string& catName);

    virtual void GetParentCifItems(std::vector<std::string>& parCifItems,
      const std::string& cifItemName);

  protected:
    const DictObjCont& _dictObjCont; 

  private:
    void _GetDictVersion(std::string& dictVer);
    bool _isDictCategory(const std::string& category) const;
};


#endif
