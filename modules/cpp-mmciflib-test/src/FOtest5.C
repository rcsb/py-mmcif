/* Test for quoted strings*/
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


  fobjR = new CifFile(CREATE_MODE, "./test5.sdb", true);

  cifParserR = new CifParser(fobjR, fobjR->GetVerbose());

  cifParserR->Parse("./Test1.cif", diags);

  delete(cifParserR);

  if (!(diags.empty())) cout << " Diagnostics [" << diags.size() << "] " << diags << endl;

#if 0
  cerr << "PrintHeaderInfo() - After Read()" << endl;
  fobjR->PrintHeaderInfo();
  cerr << "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" << endl;
  cerr << "PrintIndex() - After Read()" << endl;
  fobjR->PrintIndex();
#endif

  cout<<fobjR->GetNumBlocks()<<endl;

#if 0
  fobjR->SetQuoting(CifFile::eDOUBLE);
#endif
  fobjR->Write("./Test1.ocif");

#if 0
  cerr << "PrintHeaderInfo() - After Write" << endl;
  fobjR->PrintHeaderInfo();
  cerr << "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" << endl;
  cerr << "PrintIndex() - After Write" << endl;
  fobjR->PrintIndex();
#endif

  delete (fobjR);

  fobjR = new CifFile(READ_MODE, "./test5.sdb");
  Block& block = fobjR->GetBlock("DATABLOCK_1");
  ISTable* sst=block.GetTablePtr("category0");
  cout << (*sst);
  cout<<sst->GetNumColumns()<<endl;
  delete (fobjR);
}
