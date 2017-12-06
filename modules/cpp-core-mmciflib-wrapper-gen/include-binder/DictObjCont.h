/*$$FILE$$*/
/*$$VERSION$$*/
/*$$DATE$$*/
/*$$LICENSE$$*/


/*!
** \file DictObjCont.h
**
** \brief Header file for ObjCont, ItemObjCont and DictObjCont classes.
*/


#ifndef DICTOBJCONT_H
#define DICTOBJCONT_H


#include <mapped_ptr_vector.h>
#include <mapped_ptr_vector.C>

#include <DictObjContInfo.h>
#include <DicFile.h>


/**
**  \class ObjCont
**
**  \brief Public class that represents a generic object container.
**
**  This class represents a generic object container of attributes. It is
**  to be used directly or as a base class for non-generic object containers.
**  This class provides methods for retrieving its attributes and
**  printing its content.
*/
class ObjCont
{
  public:
    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    ObjCont(Serializer& ser, DicFile& dicFile, const string& blockName,
      const string& id, const ObjContInfo& objContInfo);

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    virtual ~ObjCont();

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    void Init();

    /**
    **  Must stay in public API.
    */
    const string& GetName() const;

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    virtual void Read(UInt32 which, unsigned int Index = 0);

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    virtual UInt32 Write();

    /**
    **  Retrieves a constant reference to the vector of values of the
    **  object container attribute, which is specified with a category name
    **  and an item name.
    **
    **  \param[in] catName - category name
    **  \param[in] itemName - item name
    **
    **  \return Constant reference to the vector of attribute values.
    **
    **  \pre Category with name \e catName and item with name \e itemName
    **    must be present
    **
    **  \post None
    **
    **  \exception NotFoundException - if category with name \e catName
    **    or item with name \e itemName does not exist
    */
    const vector<string>& GetAttribute(const string& catName,
      const string& itemName) const;

    /**
    **  Prints the content of the object container.
    **
    **  \param: None 
    **
    **  \return None
    **
    **  \pre None
    **
    **  \post None
    **
    **  \exception: None
    */
    void Print() const;

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    void SetVerbose(bool verbose);

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    virtual void Build();

  protected:
    Serializer& _ser;

    DicFile& _dicFile;

    const ObjContInfo& _objContInfo;

    string _blockName;
    string _id; 

    bool _verbose;

    vector<UInt32> _index;

    vector<vector<vector<string> > > _itemsStore;

    virtual void BuildItems(vector<vector<string> >& combo,
      const unsigned int configIndex);
    void BuildItems(vector<vector<string> >& combo,
      const unsigned int configIndex, const string& value);

  private:
    void ReadItem(const pair<unsigned int, unsigned int>& indexPair,
      unsigned int Index);
};


/**
**  \class ItemObjCont
**
**  \brief Private class that represents an item object container.
**
**  This class represents an item object container, i.e., an object
**  container of type "item". In addition to ObjCont features, this class
**  adds support for item decendents.
*/
class ItemObjCont : public ObjCont
{
  public:
    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    ItemObjCont(Serializer& ser, DicFile& dicFile,
      const string& blockName, const string& itemName);

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    ~ItemObjCont();

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    void Build();

  private:
    vector<string> _decendency;

    void GetItemDecendency();

    void BuildItems(vector<vector<string> >& combo,
      const unsigned int configIndex);
};


/**
**  \class DictObjCont
**
**  \brief Public class that represents a dictionary object container.
**
**  This class represents a dictionary object container, i.e., an object
**  container of type "dictionary". A dictionary object container is a
**  container of its attributes and of objects of type: item, sub-category
**  and category. In addition to ObjCont features, this class has a method
**  to get references to other object containers that it contains.
*/
class DictObjCont : public ObjCont
{
  public:
    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    DictObjCont(Serializer& ser, DicFile& dicFile,
      const string& blockName);

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    ~DictObjCont();

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    void Build();

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    UInt32 Write();

    /**
    **  Utility method, not part of users public API, and will soon be
    **  removed.
    */
    void Read(UInt32 which, unsigned int Index = 0);

    /**
    **  Retrieves a reference to the generic object container, which is
    **  specified with its name and its type.
    **
    **  \param[in] contName - object container name
    **  \param[in] objContInfo - reference to the object container
    **    information, that defines object container's type. It can have the
    **    following values: \n
    **    RcsbItem - indicates that the object container is of type "item" \n
    **    RcsbSubcat - indicates that the object container is of type
    **      "sub-category" \n
    **    RcsbCat - indicates that the object container is of type "category"
    **
    **  \return Reference to the generic object container
    **
    **  \pre Object container with name \e contName must be present
    **
    **  \post None
    **
    **  \exception NotFoundException - if object container with name
    **    \e contName does not exist
    */
    const ObjCont& GetObjCont(const string& contName,
      const ObjContInfo& objContInfo) const;

    /**
    **  Prints the content of the object container, which includes its
    **  attributes and the content of all the object containers that it
    **  contains.
    **
    **  \param: None 
    **
    **  \return None
    **
    **  \pre None
    **
    **  \post None
    **
    **  \exception: None
    */
    void Print();

  private:
    mutable mapped_ptr_vector<ObjCont> _items;
    mutable mapped_ptr_vector<ObjCont> _subcategories;
    mutable mapped_ptr_vector<ObjCont> _categories;

    DictObjCont(const DictObjCont& dictObjCont);
    DictObjCont& operator=(const DictObjCont& inDictObjCont);

    UInt32 WriteContLocations(const vector<UInt32>& indices);

    void BuildContainers(unsigned int index, const string& catName,
      const string& itemName, mapped_ptr_vector<ObjCont>& containers);

    void BuildItems(vector<vector<string> >& combo,
      const unsigned int configIndex);

    ObjCont& GetContainers(const string& contName,
      mapped_ptr_vector<ObjCont>& containers, const ObjContInfo& objContInfo)
      const;

    void PrintContainers(const string& catName,
      const string& itemName, const ObjContInfo& objContInfo);
};


#endif // DICTOBJCONT_H

