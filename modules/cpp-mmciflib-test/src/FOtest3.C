#include <iostream>

#include "GenString.h"
#include "CifFile.h"

using std::cout;
using std::cerr;
using std::endl;

#define FALSE 0


int main() {
  CifFile * fobjR = NULL;

  ISTable * s=NULL;
  string cs, cs1,cs2,cs3,cs4;
  int i,j,k, nRow=100, nCol=10; 

  fobjR = new CifFile(CREATE_MODE, "./test3.sdb", true);

  fobjR->AddBlock("BLOCK-1");
  Block& block = fobjR->GetBlock("BLOCK-1");

  vector<string> newRow;

  for (k=0; k < 10; k++) {
    cs.clear(); cs = "TABLE"; cs+=String::IntToString(k);
    s = new ISTable(cs);
    for (i=0; i < nCol; i++) {
      cs1.clear(); cs1 = "Column-"; cs1 += String::IntToString(i);
    s->AddColumn(cs1);
    }
    for (j = 0; j < nRow; j++) {
      s->AddRow();
      newRow.clear();
      for (i=0; i < nCol; i++) {
	cs2.clear(); cs2 = "C"; cs2+=String::IntToString(i); cs2+="-R"; cs2+=String::IntToString(j);
	newRow.push_back(cs2);
      }
      s->FillRow(j, newRow);
    }
    block.WriteTable(s);
  }

  cs1.clear(); cs1 = "Updated";

  for (k=1; k < 10; k++) {
    cs.clear(); cs = "TABLE"; cs+=String::IntToString(k);
    s=block.GetTablePtr(cs);
    for (i=0; i < nCol; i++) {
      string colName = string("Column-") + String::IntToString(i);
      for (j=0; j < nRow; j++ ) {
	s->UpdateCell(j, colName, cs1);
      }
    }
    cerr << "Table " << cs << endl;
    block.WriteTable(s);
  }

  cout << (*s);


  delete (fobjR);
}
