/* Example how to work with two CifFileObj objects,
   one is opened for reading, another for writing
*/
#include <iostream>

#include "CifFile.h"

using std::cout;
using std::endl;

void FillTestTable(ISTable *s);
void TwoCifFileObj();

#define FALSE 0

int main() {

  TwoCifFileObj();

}


void TwoCifFileObj()
{
  CifFile * fobjR = NULL;
  CifFile * fobjW = NULL;
  int i=0;
  char tname[50];

  fobjR = new CifFile(READ_MODE, "./test2.sdb");
  fobjW = new CifFile(CREATE_MODE, "./DBtest.sdb");

  ISTable* tmpTableP = NULL;

  ISTable *sst1 = new ISTable;

  Block& block = fobjR->GetBlock("DEPOSIT-0");
  tmpTableP = block.GetTablePtr("citation");

  *sst1 = *tmpTableP;
  sst1->SetName("chem_comp");

  if (sst1==NULL) cout<<"Table does not exist"<<endl;
  fobjW->AddBlock("061");
  Block& wBlock = fobjW->GetBlock("061");
  wBlock.WriteTable(sst1);

  ISTable *sst2=new ISTable("prazna");
  sst2->AddColumn("start_v");
  sst2->AddColumn("end_v");
  sst2->AddColumn("lp_lenght");
  wBlock.WriteTable(sst2);

  for (i=0;i<20;i++){
    sprintf(tname,"%d",i);
    ISTable *sst=new ISTable(tname);
    FillTestTable(sst);
    wBlock.WriteTable(sst);
  }

  fobjW->Write("./test3.ocif");

  delete (fobjW);

  delete (fobjR);

}

void FillTestTable(ISTable *s) {
 int i;
 vector<string>* ColStart;
 vector<string>* ColEnd;
 vector<string>* ColLen;
 ColStart = new vector<string>;
 ColEnd = new vector<string>;
 ColLen = new vector<string>;
 string length;
 char a[5];
 s->AddColumn("start_v");
 s->AddColumn("end_v");
 s->AddColumn("lp_lenght");
 for (i=1; i<50; i++) {
   sprintf(a,"%d",i);
   length = a;
	ColStart->push_back(length);
	ColEnd->push_back(length);
	ColLen->push_back(length);
 }

 s->FillColumn("start_v", *ColStart);
 s->FillColumn("end_v", *ColEnd);
 s->FillColumn("lp_lenght", *ColLen);

 delete ColStart;
 delete ColEnd;
 delete ColLen;
}

