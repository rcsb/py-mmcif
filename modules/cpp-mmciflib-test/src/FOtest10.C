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

  DICParser* dicParserR = NULL;
  DICParser* ddlParserR = NULL;


  ddl = new DicFile(true);

  CifFile* ddlRefFileP = ddl->GetRefFile();

  ddlParserR = new DICParser(ddl, ddlRefFileP, ddl->GetVerbose());

  ddlParserR->Parse("./ddl-mm", diags);

  ddl->DataChecking(*ddl, "ddl-mm-diag.log");

  delete(ddlParserR);

  cout<<"diags = ";
  if (!(diags.empty()))
  {
    cout<<diags;
  }
  cout<<endl;


  fobjR = new DicFile(CREATE_MODE, "./test5.sdb");

  dicParserR = new DICParser(fobjR, ddl, fobjR->GetVerbose());

  dicParserR->Parse("./dictionary.dic", diags);
  
  fobjR->DataChecking(*ddl, "dictionary.dic-diag.log");

  delete(dicParserR);

  cout<<"diags = ";
  if (!(diags.empty()))
  {
    cout<<diags;
  }
  cout<<endl;

  fobjR->Compress(ddl);
  fobjR->Write("./view2.ocif");
  fobjR->WriteFormatted("./view2.dic",ddl);

  delete (ddl);
  delete (fobjR);
}

