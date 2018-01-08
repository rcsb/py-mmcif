//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$


/*!
** \file DictParentChild.h
**
** \brief Header file for DictParentChild class.
*/


#ifndef DICTPARENTCHILD_H
#define DICTPARENTCHILD_H


#include <string>
#include <vector>

#include <ISTable.h>
#include <DictObjCont.h>
#include <DictDataInfo.h>
#include <ParentChild.h>


class DictParentChild : public ParentChild
{
  public:
    DictParentChild(const DictObjCont& dictObjCont, DictDataInfo& dictDataInfo);
    virtual ~DictParentChild();

    const DictObjCont& GetDictObjCont();

  protected:
    const DictObjCont& _dictObjCont;
    DictDataInfo& _dictDataInfo;

    void GetParentCifItems(std::vector<std::string>& parCifItems,
      const std::string& cifItemName);

  private:
    void FillGroupTable(ISTable& groupTable);
    void FillGroupListTable(ISTable& groupListTable, ISTable& groupTable);
};


#endif

