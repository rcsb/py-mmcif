/* Test for reading binary files of two different versions*/
#include "CifFile.h"
#include <iostream>


#define FALSE 0
int main() {
  CifFile * fobjR1 = NULL;
  CifFile * fobjR2 = NULL;


  fobjR1 = new CifFile(READ_MODE, "./infile01.db");
  fobjR1->Write("./Test9.1.ocif");

  fobjR2 = new CifFile(READ_MODE, "./infile02.db");
  fobjR2->Write("./Test9.2.ocif");

  delete (fobjR1);

  delete (fobjR2);
}
