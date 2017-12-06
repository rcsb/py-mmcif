#include <iostream>

#include "CifFile.h"
#include "CifParserBase.h"
#include "CifFileReadDef.h"

using std::cout;
using std::cerr;
using std::endl;

int main(int argc, char *argv[]) {

  string diags;
  CifFile * fobjR = NULL;
  string iFile;
  string oFile;
  string blockName;
  ISTable *t = NULL;
  int i;

  CifParser* cifParserR = NULL;


  if (argc < 4) {
    cerr << argv[0] << ":  usage = -f <inputfile> -o <outputfile> " << endl;
    return(1);
  }
  

  for (i=1; i < argc; i++) {
    if ( argv[i][0] == '-' ) {
      if (strcmp(argv[i],"-f") == 0 ) {
	i++;
	iFile = argv[i];          
      }	else if (strcmp(argv[i],"-o") == 0 ) {
	i++;
	oFile = argv[i];          
      } else {
	cerr << argv[0] << ":  usage = -f <inputfile> -o <outputfile> " << endl;
	return(1);
      }
    } else {
      cerr << argv[0] << ":  usage = -f <inputfile> -o <outputfile> " << endl;
      return(1);
    }
  }
  fobjR = new CifFile(CREATE_MODE, "./test4.sdb");

  cifParserR = new CifParser(fobjR, fobjR->GetVerbose());

  cifParserR->Parse(iFile, diags);

  delete(cifParserR);

  if (!(diags.empty())) cout << " Diagnostics [" << diags.size() << "] " << diags << endl;  
  fobjR->Write(oFile,1);
  delete (fobjR);


  for (i=0; i < 10; i++) {
    cout << "--------------------STARTING CYCLE " << i << endl;

    fobjR = new CifFile(UPDATE_MODE, "./test4.sdb");
    if (!(diags.empty())) cout << " Diagnostics [" << diags.size() << "] " << diags << endl;  
    blockName = fobjR->GetFirstBlockName();    
    Block& block = fobjR->GetBlock(blockName);
    t = block.GetTablePtr("cell");
    cout << "--------------------AFTER READ ON CYCLE " << i << endl;
    cout << "Table name is " << t->GetName() << endl;
    vector<string> qcolNames;
    CifString::MakeCifItems(qcolNames, t->GetName(), t->GetColumnNames());
    if (!qcolNames.empty()) {
      for (int j=0; j < (int)qcolNames.size(); j++){
	cout << qcolNames[j] << endl;
      }
      qcolNames.clear();
    }

    block.WriteTable(t);

    cout << "--------------------AFTER WRITE ON CYCLE " << i << endl;
    cout << "Table name is " << t->GetName() << endl;
    vector<string> qqcolNames;
    CifString::MakeCifItems(qqcolNames, t->GetName(), t->GetColumnNames());
    if (!qqcolNames.empty()) {
      for (int j=0; j < (int)qqcolNames.size(); j++){
	cout << qqcolNames[j] << endl;
      }
      qqcolNames.clear();
    }
    delete (fobjR);
  }
  
}

