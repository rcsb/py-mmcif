//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$


/*!
** \file DictObjContInfo.h
**
** \brief Header file for ObjContInfo, DictObjContInfo, CatObjContInfo,
**   SubcatObjContInfo and ItemObjContInfo classes.
*/


#ifndef DICTOBJCONTINFO_H
#define DICTOBJCONTINFO_H


#include <string>
#include <map>

#include <Serializer.h>
#include <rcsb_types.h>
#include <CifString.h>


/**
**  \class ObjContInfo
**
**  \brief Public class that represents a generic information class for the
**    generic object container.
**
**  This class represents a generic information class for the generic object
**  container. It is intended to be used as a base class for information
**  classes of object containers. It defines the names of categories and the
**  names of items, that are used in attributes retrieval method of ObjCont
**  class.
*/
class ObjContInfo
{
  public:
    /**
    **  \class Item
    **
    **  \brief Private class that represents an item.
    */
    class Item
    {
      public:
        std::string descr;
        std::string itemName;
    };

    /**
    **  \class Cat
    **
    **  \brief Private class that represents a category.
    */
    class Cat
    {
      public:
        std::string catName;
        std::string col1;
        bool nonDefaultValue;
        bool inheritance;
        std::vector<Item> items;
    };

    std::string _objContInfoDescr;

    std::vector<Cat> _cats;

    std::map<std::pair<std::string, std::string>, std::pair<unsigned int,
      unsigned int> > _catMap;

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    void AddCat(const std::string& catName);

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    void AddCat(const std::string& catName, const std::string& col1,
      const bool nonDefaultValue = false, const bool inheritance = false);

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    void AddItem(const std::string& descr, const std::string& itemName);

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    unsigned int GetItemIndex(const std::string& catName,
      const std::string& itemName) const;

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    std::pair<unsigned int, unsigned int> GetItemIndices(
      const std::string& catName, const std::string& itemName) const;

#ifndef VLAD_PYTHON_GLUE
    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    virtual ~ObjContInfo();
#endif

  protected:
    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    ObjContInfo();

  private:
    std::vector<Cat>::iterator currCat;
};


/**
**  \class DictObjContInfo
**
**  \brief Private class that represents an information class for the
**    dictionary object container.
*/
class DictObjContInfo : public ObjContInfo
{
  public:
    static DictObjContInfo& GetInstance();

  private:
    DictObjContInfo();
    DictObjContInfo(const DictObjContInfo& in);

    ~DictObjContInfo();

    DictObjContInfo& operator=(const DictObjContInfo& in);
};


/**
**  \class CatObjContInfo
**
**  \brief Private class that represents an information class for the
**    category object container.
*/
class CatObjContInfo : public ObjContInfo
{
  public:
    static CatObjContInfo& GetInstance();

  private:
    CatObjContInfo();
    CatObjContInfo(const CatObjContInfo& in);

    ~CatObjContInfo();

    CatObjContInfo& operator=(const CatObjContInfo& in);
};


/**
**  \class SubcatObjContInfo
**
**  \brief Private class that represents an information class for the
**    sub-category object container.
*/
class SubcatObjContInfo : public ObjContInfo
{
  public:
    static SubcatObjContInfo& GetInstance();

  private:
    SubcatObjContInfo();
    SubcatObjContInfo(const SubcatObjContInfo& in);

    ~SubcatObjContInfo();

    SubcatObjContInfo& operator=(const SubcatObjContInfo& in);
};


/**
**  \class ItemObjContInfo
**
**  \brief Private class that represents an information class for the
**    item object container.
*/
class ItemObjContInfo : public ObjContInfo
{
  public:
    static ItemObjContInfo& GetInstance();

  private:
    ItemObjContInfo();
    ItemObjContInfo(const ItemObjContInfo& in);

    ~ItemObjContInfo();

    ItemObjContInfo& operator=(const ItemObjContInfo& in);
};


#endif // DICTOBJCONTINFO_H
