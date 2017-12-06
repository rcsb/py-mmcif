/* More flexible parser*/
#include <iostream>

#include "CifFile.h"
#include "CifParserBase.h"

using std::cout;
using std::endl;

#define FALSE 0
int main() {
  string diags;
  CifFile * fobjR = NULL;

  CifParser* cifParserR = NULL;


  fobjR = new CifFile(true);

  cifParserR = new CifParser(fobjR, fobjR->GetVerbose());

  cifParserR->Parse("./Test14.cif", diags);

  delete(cifParserR);

  if (!(diags.empty())) cout << " Diagnostics [" << diags.size() << "] " << diags << endl;

  fobjR->Write("./Test14.ocif");
  delete (fobjR);
}
