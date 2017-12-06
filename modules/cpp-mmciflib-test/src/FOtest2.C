#include <iostream>

#include "CifFile.h"
#include "CifParserBase.h"
#include "CifFileReadDef.h"

void FillTestTable(ISTable *s);

void  update_entry_ids(CifFile *fobj, const string& blockName, const string& idName);
void get_attribute_value_first(string& value, CifFile *fobj, const string& blockName, const string& category, const string& attribute);

#define defdb "DEPOSIT-0"

int main()
{

  CifFile* fobjR = new CifFile(CREATE_MODE, "./test2.sdb", true);

  CifParser* cifParserR = new CifParser(fobjR, fobjR->GetVerbose());

  string diags;
  cifParserR->Parse("./Test2.cif", diags);

  delete(cifParserR);

  delete (fobjR);


  fobjR = new CifFile(UPDATE_MODE, "./test2.sdb");

  string blockName = fobjR->GetFirstBlockName();

  string dbname;
  get_attribute_value_first(dbname, fobjR, blockName, "database",
    "ndb_code_NDB");

  if (dbname.empty())
  {
      get_attribute_value_first(dbname, fobjR, blockName, "database",
        "ndb_code_PDB");
  }

  if (dbname.empty())
  {
    dbname = defdb;
  }

  fobjR->Write("./YYtest.ocif");  
 
  update_entry_ids(fobjR, blockName, dbname);

  fobjR->RenameFirstBlock(dbname); 
  delete (fobjR);

  fobjR = new CifFile(UPDATE_MODE, "./test2.sdb");
  fobjR->Write("./ZZtest.ocif"); 
  delete (fobjR);

}

void  update_entry_ids(CifFile* fobj, const string& blockName,
  const string& idName)
{
  fobj->SetAttributeValue(blockName,"entry","id",idName);    
  fobj->SetAttributeValue(blockName,"struct_keywords","entry_id",idName);    
  fobj->SetAttributeValue(blockName,"database","entry_id",idName);    
  fobj->SetAttributeValue(blockName,"database","ndb_code_NDB",idName);    
  fobj->SetAttributeValue(blockName,"exptl","entry_id",idName);    
  
  fobj->SetAttributeValue(blockName,"struct","entry_id",idName);    
  fobj->SetAttributeValue(blockName,"ndb_na_struct_keywds","entry_id",idName);    
  fobj->SetAttributeValue(blockName,"ndb_database_status","entry_id",idName);    
  fobj->SetAttributeValue(blockName,"ndb_database_proc","entry_id",idName);    
  fobj->SetAttributeValue(blockName,"ndb_coord","entry_id",idName);    
  fobj->SetAttributeValue(blockName,"reflns","entry_id",idName);    
  fobj->SetAttributeValue(blockName,"computing","entry_id",idName);    
  fobj->SetAttributeValue(blockName,"symmetry","entry_id",idName);    
  fobj->SetAttributeValue(blockName,"cell","entry_id",idName);    
  fobj->SetAttributeValue(blockName,"refine","entry_id",idName);    
  fobj->SetAttributeValue(blockName,"refine_analyze","entry_id",idName);    
  fobj->SetAttributeValue(blockName,"ndb_refine","entry_id",idName); 
  fobj->SetAttributeValue(blockName,"atom_sites","entry_id",idName);    
}

void get_attribute_value_first(string& value, CifFile *fobj, const string& blockName, const string& category, const string& attribute)
{
  value.clear();

  ISTable *t=NULL;

  vector<string> col;
  int nRow;


  Block& block = fobj->GetBlock(blockName);

  if (block.IsTablePresent(category)) {
    t=block.GetTablePtr(category);
    nRow = t->GetNumRows();
    if (nRow > 0) {
      if (t->IsColumnPresent(attribute)) {
  t->GetColumn(col, attribute);
  if (!col.empty() && (col[0].size() > 0) ) {
 value = col[0];
  }
      }
    }
  }

}

