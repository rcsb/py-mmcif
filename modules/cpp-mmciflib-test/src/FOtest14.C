/* example how to create dictionary from scratch */
/* we have to have DDL anyway   */
#include <iostream>

#include "DicFile.h"
#include "DICParserBase.h"

using std::cout;
using std::endl;

#define FALSE 0
int main() {
  DicFile * fobjR = NULL;

  string diags;
  DicFile * ddl = NULL;
  ISTable* format;
  string datablockName = "Dictionary";
  string cs;

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
/*
 Table format defines how save frames look like. This table
has three rows:
    dbName - is datablock name. This is the same datablock
name as datablock name in dictionary. If we have more than
one datablock, than we have to define this for every
datablock.
    type - this column defines where to put data from
particular table. It can have one of three values: data,
category, item. Data means that value from table (column
catName) will be put out of any save frame, as in data file.
"category"/"item" means that data from table will be put in
category/item save frame.
    catName - is name of table

example:
    dbName  = cif_mm.dic
    type          = category
    catName = category_key
this means that data from table category_key which is
belongs to cif_mm.dic dictionary (datablock) will be put in
category save frame.

    For every table it has to be defined one row in this
format table, otherwise this information will be lost. You
can just see them in tabulated written cif file.
*/


  format = new ISTable("format");
  format->AddColumn("dbName");
  format->AddColumn("type");
  format->AddColumn("catName");
  format->AddRow();
  format->UpdateCell(format->GetLastRowIndex(), "dbName", datablockName);
  cs = "category";
  format->UpdateCell(format->GetLastRowIndex(), "type", cs);
  format->UpdateCell(format->GetLastRowIndex(), "catName", cs);

  format->AddRow();
  format->UpdateCell(format->GetLastRowIndex(), "dbName", datablockName);
  cs = "item";
  format->UpdateCell(format->GetLastRowIndex(), "type", cs);
  format->UpdateCell(format->GetLastRowIndex(), "catName", cs);

  fobjR = new DicFile(true);

  ISTable *tbl;
/*
    the following line describe how to add/update tables,
information, new definitions to the dictionary.
    Tables category and item have to exist, and have to have
all columns that are defined here, in this example
*/
  tbl = new ISTable("category");
  tbl->AddColumn("description");
  tbl->AddColumn("mandatory_code");
  tbl->AddColumn("id");
  tbl->AddColumn("implicit_key");

  tbl->AddRow();

  /* GetLastRowIndex() is different from GetNumRows() because some rows might be deleted,
     they actually are marked as deleted, but they are stil in a table
  */
  cs="no";
  tbl->UpdateCell(tbl->GetLastRowIndex(), "mandatory_code", cs);

  cs="category_1";
  tbl->UpdateCell(tbl->GetLastRowIndex(), "id", cs);

  cs="Description for category_1";
  tbl->UpdateCell(tbl->GetLastRowIndex(), "description", cs);

  tbl->UpdateCell(tbl->GetLastRowIndex(), "implicit_key", datablockName);

  fobjR->AddBlock(datablockName);
  Block& block = fobjR->GetBlock(datablockName);
  block.WriteTable(tbl);

  tbl = new ISTable("item");
  tbl->AddColumn("name");
  tbl->AddColumn("category_id");
  tbl->AddColumn("mandatory_code");
  tbl->AddRow();
  cs="_item_1";
  tbl->UpdateCell(tbl->GetLastRowIndex(), "name", cs);

  cs="category_1";
  tbl->UpdateCell(tbl->GetLastRowIndex(), "category_id", cs);

  cs="no";
  tbl->UpdateCell(tbl->GetLastRowIndex(), "mandatory_code", cs);
  block.WriteTable(tbl);

/*********************************************************/

  fobjR->Write("./Test15.ocif");
  fobjR->WriteFormatted("./Test15.dic",ddl,format);

  delete(format);
  delete (ddl);
  delete (fobjR);
}
