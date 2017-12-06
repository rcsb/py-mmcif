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
  ISTable * tbl;
  vector<string> colName;
  vector<string> target;
  vector<unsigned int> listOut;

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


  fobjR = new DicFile(CREATE_MODE, "./test11.sdb", true);

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
  
  fobjR->Write("./view2.ocif");
  Block& block = fobjR->GetBlock(fobjR->GetFirstBlockName());
  tbl=block.GetTablePtr("item_aliases");
  colName.push_back("name");
  colName.push_back("dictionary");
  colName.push_back("version");
  tbl->CreateIndex("index0",colName);

  target.push_back("_atom_site.attached_hydrogens");
  target.push_back("cif_core.dic");
  target.push_back("2.0.1");

  tbl->Search(listOut, target, colName);

  string theCell;

  if (!listOut.empty()) {
    for(int i=0;i<(int)listOut.size();i++) {
      theCell.clear();
      theCell = (*tbl)(listOut[i], "alias_name");
      cout<<theCell<<endl;
    }
  }

  listOut.clear();
  delete (fobjR);

  fobjR = new DicFile(READ_MODE, "./test11.sdb", true);
  
  Block& block2 = fobjR->GetBlock(fobjR->GetFirstBlockName());
  tbl=block2.GetTablePtr("item_aliases");

  tbl->Search(listOut, target, colName);

  if (!listOut.empty()) {
    for(int i=0;i<(int)listOut.size();i++) {
      theCell.clear();
      theCell = (*tbl)(listOut[i], "alias_name");
      cout<<theCell<<endl;
    }
  }

  delete (ddl);
  delete (fobjR);

}

