/* Example for dictionary chacking*/
#include <iostream>

#include "CifFile.h"
#include "DicFile.h"
#include "DICParserBase.h"

using std::cout;
using std::cerr;
using std::endl;

int main(int argc, char *argv[]) {
  string diags;
  DicFile * ddl = NULL;
  DicFile * dic = NULL;

  DICParser* dicParserR = NULL;
  DICParser* ddlParserR = NULL;


  int i;
  string ddlFile;
  string dicFile;


  if (argc < 4) {
    cerr << argv[0] << ":  usage = -ddl <ddlfile> -dic <dictionaryfile> " << endl;
    return(1);
  }

  for (i=1; i < argc; i++) {
    if ( argv[i][0] == '-' ) {
      if (strcmp(argv[i],"-ddl") == 0 ) {
	i++;
	ddlFile = argv[i];          
      }	else if (strcmp(argv[i],"-dic") == 0 ) {
	i++;
	dicFile = argv[i];          
      } else {
	cerr << argv[0] << ":  usage = -ddl <ddlfile> -dic <dictionaryfile> " << endl;
	return(1);
      }
    } else {
      cerr << argv[0] << ":  usage = -ddl <ddlfile> -dic <dictionaryfile> " << endl;
      return(1);
    }
  }

  ddl = new DicFile(true);

  CifFile* ddlRefFileP = ddl->GetRefFile();

  ddlParserR = new DICParser(ddl, ddlRefFileP, ddl->GetVerbose());

  ddlParserR->Parse(ddlFile, diags);

  delete(ddlParserR);

  cout<<"diags from DDL reading= "<<diags<<endl;

  dic = new DicFile(CREATE_MODE, "dictionary.sdb");

  dicParserR = new DICParser(dic, ddl, dic->GetVerbose());

  dicParserR->Parse(dicFile, diags);

  delete(dicParserR);

  cout<<"diags from Dictionary reding= "<<diags<<endl;

//  dic->Compress(ddl);

  delete (ddl);
  delete (dic);
}
