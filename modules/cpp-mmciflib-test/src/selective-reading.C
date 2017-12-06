/* Test for selective reading*/
#include "CifFile.h"
#include "CifParserBase.h"
#include "CifFileReadDef.h"
#include <iostream>


int main() {
  CifFile * fobjR = NULL;
  string diags;

  CifFileReadDef readDef;

  CifParser* cifParserR = NULL;


  vector<string> catlist;
  catlist.push_back("atom_site");
  readDef.SetCategoryList(catlist,D);

  vector<string> dblist;
  dblist.push_back("ADH041");
  readDef.SetDataBlockList(dblist,A);

  fobjR = new CifFile();

  cifParserR = new CifParser(fobjR, readDef, fobjR->GetVerbose());

  cifParserR->Parse("./ADH041.cif", diags);

  delete(cifParserR);

  fobjR->Write("./test.cif");
  
  delete (fobjR);
}
