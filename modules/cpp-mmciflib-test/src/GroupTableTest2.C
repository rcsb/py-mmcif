/* dealing with group table - from scratch*/
#include "CifFile.h"
#include <iostream>

void FillTestTable(ISTable *s,int n);
int main() {
  CifFile * fobjR = NULL;
  ISTable *tblP;
  ISTable *tblC;
  fobjR = new CifFile(CREATE_MODE, "tmp");
  tblP=new ISTable("table1");
  tblC=new ISTable("table2");
  FillTestTable(tblP,0);
  FillTestTable(tblC,51);

  fobjR->WriteTable(tblP,"datablock");
  fobjR->WriteTable(tblC,"datablock");
  fobjR->AddTableToGroup("table","datablock","table1");
  fobjR->AddTableToGroup("table","datablock","table2");

  fobjR->Write("./group1.cif");
  fobjR->WriteGrouped("./group2.cif",0);
  fobjR->CloseFile(false);
  if (fobjR) delete fobjR;

}
void FillTestTable(ISTable *s, int n) {
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
 for (i=n; i<n+50; i++) {
   sprintf(a,"%d",49-i);
   length.Copy(a);
	ColStart->Add(length);
   sprintf(a,"%d",i);
   length.Copy(a);
	ColEnd->Add(length);
	ColLen->Add(length);
 }

 s->FillColumn(*ColStart,0);
 s->FillColumn(*ColEnd,1);
 s->FillColumn(*ColLen,2);

 delete ColStart;
 delete ColEnd;
 delete ColLen;
}
