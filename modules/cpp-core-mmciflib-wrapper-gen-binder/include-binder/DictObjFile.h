/*$$FILE$$*/
/*$$VERSION$$*/
/*$$DATE$$*/
/*$$LICENSE$$*/


/*!
** \file DictObjFile.h
**
** \brief Header file for DictObjFile class.
*/


#ifndef DICTOBJFILE_H
#define DICTOBJFILE_H


#include <mapped_ptr_vector.h>
#include <mapped_ptr_vector.C>

#include <DictObjCont.h>

#include <DicFile.h>


/**
**  \class DictObjFile
**
**  \brief Public class that represents a dictionary object file.
**
**  This class represents a dictionary object file. This file is a container
**  of dictionary objects. Each dictionary object is a container of its
**  attributes and of objects of type: item, sub-category and category. Each
**  of those objects is a container of relevant attributes for that object
**  type. This class provides methods for construction/destruction, building
**  the dictionary object file from a dictionary, writing/reading dictionary
**  object file to/from the persistent storage file, accessing the
**  dictionaries and printing the content of the dictionary object file.
*/
class DictObjFile
{
  public:

    /**
    **  Constructs a dictionary object file.
    **
    **  \param[in] persStoreFileName - relative or absolute name of the
    **    persistent storage file
    **  \param[in] fileMode - optional parameter that indicates the dictionary
    **    object file mode. Possible values are read-only and create. Default
    **    is read mode.
    **  \param[in] verbose - optional parameter that indicates whether
    **    logging should be turned on (if true) or off (if false).
    **    If \e verbose is not specified, logging is turned off.
    **  \param[in] dictSdbFileName - optional parameter that indicates relative
    **    or absolute name of the SDB dictionary file. Must be specified if
    **    dictionary object file is in create mode. In read mode, the
    **    dictionary object file content is retrieved from the persistent
    **    storage file. In create mode its content will be built from the file
    **    specified by this parameter.
    **
    **  \return Not applicable
    **
    **  \pre None
    **
    **  \post None
    **
    **  \exception FileModeException - if dictionary object file is not in
    **    create mode
    **  \exception InvalidStateException - if dictionary and/or DDL file are
    **    specified for dictionary object file in read mode.
    **  \exception EmptyValueException - if dictionary and/or DDL file are
    **    not specified for dictionary object file in create mode.
    */
    DictObjFile(const string& persStorFileName, const eFileMode fileMode =
      READ_MODE, const bool verbose = false, const string& dictSdbFileName =
      std::string());

    /**
    **  Destructs a dictionary object file, by releasing all consumed
    **  resources.
    **
    **  \param: Not applicable 
    **    
    **  \return Not applicable
    **
    **  \pre None
    **
    **  \post None
    **
    **  \exception: None
    */
    ~DictObjFile();

    /**
    **  Builds a dictionary object file from the dictionary. This method
    **  parses the dictionary, parses the DDL, verifies the dictionary
    **  against the DDL and constructs objects.
    **
    **  \param: None
    **
    **  \return None
    **
    **  \pre None
    **
    **  \post None
    **
    **  \exception FileModeException - if dictionary object file is not in
    **    create mode
    */
    void Build();

    /**
    **  Writes a dictionary object file to the persistent storage file.
    **
    **  \param: None
    **
    **  \return None
    **
    **  \pre None
    **
    **  \post None
    **
    **  \exception FileModeException - if dictionary object file is not in
    **    create mode
    */
    void Write();

    /**
    **  Reads a dictionary object file from the persistent storage file.
    **
    **  \param: None
    **
    **  \return None
    **
    **  \pre None
    **
    **  \post None
    **
    **  \exception FileModeException - if dictionary object file is not in
    **    read mode
    */
    void Read();

    /**
    **  Retrieves the number of dictionaries in the dictionary object file.
    **
    **  \param: None
    **
    **  \return The number of dictionaries in the dictionary object file.
    **
    **  \pre None
    **
    **  \post None
    **
    **  \exception: None
    */
    unsigned int GetNumDictionaries();

    /**
    **  Retrieves dictionary names of the dictionaries in the dictionary
    **  object file.
    **
    **  \param[out] dictNames - retrieved dictionary names
    **
    **  \return None
    **
    **  \pre None
    **
    **  \post None
    **
    **  \exception: None
    */
    void GetDictionaryNames(vector<string>& dictNames);

    /**
    **  Retrieves a reference to the dictionary object.
    **
    **  \param[in] dictName - dictionary name
    **
    **  \return Reference to the dictionary object.
    **
    **  \pre Dictionary with name \e dictName must be present
    **
    **  \post None
    **
    **  \exception NotFoundException - if dictionary with name \e dictName
    **    does not exist
    */
    DictObjCont& GetDictObjCont(const string& dictName);

    /**
    **  Prints the content of the dictionary object file.
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
    eFileMode _fileMode;
    bool _verbose;

    string _dictSdbFileName;

    DicFile* _dicFileP;
    Serializer& _ser;

    mapped_ptr_vector<DictObjCont> _dictionaries;

    DictObjCont* _currDictObjContP;
};


#endif // DICTOBJFILE_H

