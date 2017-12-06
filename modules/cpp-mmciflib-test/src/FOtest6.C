#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include <iostream>

#include "CifFile.h"
#include "CifParserBase.h"
#include "CifFileReadDef.h"

using std::cout;
using std::endl;

#define FALSE 0
int main() {
  string diags;
  CifFile * fobjR = NULL;

  CifParser* cifParserR = NULL;


  fobjR = new CifFile(CREATE_MODE, "./test6.sdb");

  cifParserR = new CifParser(fobjR, fobjR->GetVerbose());

  cifParserR->Parse("./ADH041.cif", diags);

  delete(cifParserR);

  cout<<"diags = ";
  if (!(diags.empty()))
  {
    cout<<diags;
  }
  cout<<endl;

  if (!(diags.empty())) cout << " Diagnostics [" << diags.size() << "] " << diags << endl;

#ifndef VLAD_TEST
  Block& block = fobjR->GetBlock("ADH041");
  block.DeleteTable("atom_site");
#endif

  delete (fobjR);
#ifndef VLAD_TEST
  fobjR = new CifFile( READ_MODE, "./test6.sdb", true);
#else
  fobjR = new CifFile( UPDATE_MODE, "./test6.sdb", true);
  Block& block = fobjR->GetBlock("ADH041");
  block.DeleteTable("atom_site");
#endif

  fobjR->Write("./Test10.ocif");
#ifdef VLAD_TEST
  fobjR = new CifFile( READ_MODE, "./test6.sdb", true);
  fobjR->Write("./Test10-10.ocif");
#endif
  delete (fobjR);
}
