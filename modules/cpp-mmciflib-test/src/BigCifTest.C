/* Test for reading very very large cif files*/
#include <time.h>

#include <iostream>

#include "CifFile.h"
#include "CifParserBase.h"

using std::cout;
using std::cerr;
using std::endl;

int main(int argc, char *argv[]) {
  CifFile * fobjR2 = NULL;
  time_t start,end;
  string iFile;
  string oFile;
  int i;
  char *pname=NULL;
  string diags;
  pname = argv[0];

  CifParser* cifParserR = NULL;



  if (argc < 4) {
    cerr << pname << ":  usage = -f <inputfile> -o <outputfile> " << endl;
    return(1);
  }

   time(&start);
  for (i=1; i < argc; i++) {
    if ( argv[i][0] == '-' ) {
      if (strcmp(argv[i],"-f") == 0 ) {
	i++;
	iFile = argv[i];          
      }	else if (strcmp(argv[i],"-o") == 0 ) {
	i++;
	oFile = argv[i];          
      } else {
	cerr << pname << ":  usage = -f <inputfile> -o <outputfile> " << endl;
	return(1);
      }
    } else {
      cerr << pname << ":  usage = -f <inputfile> -o <outputfile> " << endl;
      return(1);
    }
  }

  fobjR2 = new CifFile(CREATE_MODE, oFile);

  cifParserR = new CifParser(fobjR2);

  cifParserR->Parse(iFile, diags);

  delete(cifParserR);

  time(&end);
  cout<<"File is READ in "<<difftime(end,start)<<" second(s)"<<endl;

  time(&start);
  
  time(&end);
  cout<<"Binary file is created in "<<difftime(end,start)<<" second(s)"<<endl;
  delete (fobjR2);
}
