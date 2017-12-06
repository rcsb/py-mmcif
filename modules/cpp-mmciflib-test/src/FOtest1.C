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


  fobjR = new CifFile(CREATE_MODE, "./test1.sdb", true);

  cifParserR = new CifParser(fobjR, fobjR->GetVerbose());

  cifParserR->Parse("./view1.cif", diags);

  delete(cifParserR);

  if (!(diags.empty())) cout << " Diagnostics [" << diags.size() << "] " << diags << endl;

  cifParserR = new CifParser(fobjR, fobjR->GetVerbose());

  cifParserR->Parse("./view2.cif", diags);

  delete(cifParserR);

  if (!(diags.empty())) cout << " Diagnostics [" << diags.size() << "] " << diags << endl;

  ISTable *cst = new ISTable("ndb_tool_category_state1");
  cst->AddColumn("category");
  cst->AddColumn("row_current");
  cst->AddColumn("row_maximum");
  cst->AddColumn("status");
  vector<string> *c0 = NULL;
  vector<string> *c1 = NULL;
  vector<string> *c2 = NULL;
  vector<string> *c3 = NULL;
  
  c0 = new  vector<string>;
  c1 = new  vector<string>;
  c2 = new  vector<string>;
  c3 = new  vector<string>;
  string cs;
  
  for (int i=0; i < 100;  i++) {
      cs.clear(); cs = "data point"; c0->push_back(cs);
      cs.clear(); cs = "0";          c1->push_back(cs);
      cs.clear(); cs = "1";            c2->push_back(cs);
      cs.clear(); cs = "0";            c3->push_back(cs);
  }
  cst->FillColumn("category", *c0);
  cst->FillColumn("row_current", *c1);
  cst->FillColumn("row_maximum", *c2);
  cst->FillColumn("status", *c3);

  fobjR->AddBlock("view1");

  Block& block = fobjR->GetBlock("view1");

  block.WriteTable(cst);

  fobjR->RenameFirstBlock("view100");
  fobjR->Write("./view-all.ocif");

  fobjR->Serialize("./test1-ser.sdb");

  delete (fobjR);
  if (c0) delete c0;
  if (c1) delete c1;
  if (c2) delete c2;
  if (c3) delete c3;

}
