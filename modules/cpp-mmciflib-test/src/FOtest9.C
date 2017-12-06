#include <iostream>

#include "DICParserBase.h"

using std::cout;
using std::endl;

#define FALSE 0
int main() {
  string diags;
  DicFile * fobjR = NULL;

  DICParser* ddlParserR = NULL;

  fobjR = new DicFile(CREATE_MODE, "./test5.sdb", true);

  CifFile* ddlRefFileP = fobjR->GetRefFile();

  ddlParserR = new DICParser(fobjR, ddlRefFileP, fobjR->GetVerbose());

  ddlParserR->Parse("./ndb_ddl", diags);

  delete(ddlParserR);

  cout<<"diags = ";
  if (!(diags.empty()))
  {
    cout<<diags;
  }
  cout<<endl;
  
  fobjR->Write("./view1.cif");

  fobjR->WriteFormatted("./view1.ddl");

  delete (fobjR);
}

