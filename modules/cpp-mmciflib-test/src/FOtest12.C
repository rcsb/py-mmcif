#include <iostream>

#include "DicFile.h"
#include "DICParserBase.h"

using std::cout;
using std::endl;

#define FALSE 0
int main() {
  string diags;
  DicFile * fobjR = NULL;
  DicFile * ddl = NULL;
  ISTable *tbl;

  DICParser* dicParserR = NULL;
  DICParser* ddlParserR = NULL;


  ddl = new DicFile(true);

  CifFile* ddlRefFileP = ddl->GetRefFile();

  ddlParserR = new DICParser(ddl, ddlRefFileP, ddl->GetVerbose());

  ddlParserR->Parse("./ddl-mm", diags);

  delete(ddlParserR);

  cout<<"diags = ";
  if (!(diags.empty()))
  {
    cout<<diags;
  }
  cout<<endl;


  fobjR = new DicFile();

  dicParserR = new DICParser(fobjR, ddl, fobjR->GetVerbose());

  dicParserR->Parse("./dictionary.dic", diags);

  delete(dicParserR);

  cout<<"diags = ";
  if (!(diags.empty()))
  {
    cout<<diags;
  }
  cout<<endl;

  fobjR->Compress(ddl);

/**************** Adding new definitions *****************/
  string cs;

  Block& block = fobjR->GetBlock(fobjR->GetFirstBlockName());
  tbl=block.GetTablePtr("category");
  cout<<tbl->GetNumRows()<<endl;
  tbl->AddRow();
  cout<<tbl->GetNumRows()<<endl;
  cout<<tbl->GetLastRowIndex()<<endl;

  cs=fobjR->GetFirstBlockName();
  tbl->UpdateCell(tbl->GetLastRowIndex(), "implicit_key", cs);
  /* GetLastRowIndex() is different from GetNumRows() because some rows might be deleted,
     they actually are marked as deleted, but they are still in a table
  */

  cs="no";
  tbl->UpdateCell(tbl->GetLastRowIndex(), "mandatory_code", cs);

  cs="category_1";
  tbl->UpdateCell(tbl->GetLastRowIndex(), "id", cs);

  cs="Description for category_1";
  tbl->UpdateCell(tbl->GetLastRowIndex(), "description", cs);
  block.WriteTable(tbl);
  

  tbl=block.GetTablePtr("category_key");
  tbl->AddRow();

  cs="category_1.item_1";
  tbl->UpdateCell(tbl->GetLastRowIndex(), "name", cs);

  cs="category_1";
  tbl->UpdateCell(tbl->GetLastRowIndex(), "id", cs);

  block.WriteTable(tbl);

  tbl=block.GetTablePtr("item");
  tbl->AddRow();

  cs="item_1";
  tbl->UpdateCell(tbl->GetLastRowIndex(), "name", cs);

  cs="no";
  tbl->UpdateCell(tbl->GetLastRowIndex(), "mandatory_code", cs);

  cs="category_1";
  tbl->UpdateCell(tbl->GetLastRowIndex(), "category_id", cs);

  block.WriteTable(tbl);
  
/*********************************************************/

  fobjR->Write("./view13.ocif");
  fobjR->WriteFormatted("./view13.dic", ddl);

  delete (ddl);
  delete (fobjR);
}

