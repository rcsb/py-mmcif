/* Example for data chacking*/
#include <time.h>

#include <iostream>

#include "CifFile.h"
#include "DicFile.h"
#include "CifParserBase.h"
#include "DICParserBase.h"

using std::cout;
using std::cerr;
using std::endl;

#define FALSE 0
#define NS 10
int main(int argc, char *argv[]) {
  string diags;
  DicFile * ddl = NULL;
  DicFile * dic = NULL;
  CifFile * fobjR = NULL;
  time_t start,end;
  FILE * fpN;
  string cifFile;

  CifParser* cifParserR = NULL;
  DICParser* dicParserR = NULL;
  DICParser* ddlParserR = NULL;

  if (argc < 2)
  {
    cerr << argv[0] << ":  usage = cifFile <dicFile> <ddlFile>" << endl;
    return(1);
  }

  cifFile = argv[1];          

  string dicFile;

  if (argc > 2)
  {
    dicFile = argv[2];
  }

  string ddlFile = "./ddl-mm";

  if (argc > 3)
  {
    ddlFile = argv[3];
  }

  time(&start);
  ddl = new DicFile(true);

  CifFile* ddlRefFileP = ddl->GetRefFile();

  ddlParserR = new DICParser(ddl, ddlRefFileP, ddl->GetVerbose());

  ddlParserR->Parse(ddlFile, diags);

  delete(ddlParserR);

  cout<<"diags = ";
  if (!(diags.empty()))
  {
    cout<<diags;
  }

  ddl->DataChecking(*ddl, ddlFile + "-diag.log");

  cout<<endl;
  time(&end);

  cout<<"second(s)"<<difftime(end,start)<<endl;

  time(&start);
  if (dicFile.empty())
  {
    if((fpN=fopen("./dictionary.sdb","r")) == NULL)
    {
      cout<<"First time"<<endl;
      dic = new DicFile(CREATE_MODE, "./dictionary.sdb");
  
      dicParserR = new DICParser(dic, ddl, dic->GetVerbose());

      dicParserR->Parse("./dictionary.dic", diags);

      delete(dicParserR);

    }
    else
    {
      fclose(fpN);
      dic = new DicFile(READ_MODE, "./dictionary.sdb");
    }
  }
  else
  {
      dic = new DicFile();
  
      dicParserR = new DICParser(dic, ddl, dic->GetVerbose());

      dicParserR->Parse(dicFile, diags);

      delete(dicParserR);
  }
  time(&end);
  cout<<"second(s)"<<difftime(end,start)<<endl;
  cout<<"diags = ";
  if (!(diags.empty()))
  {
    cout<<diags;
  }
  cout<<endl;

  dic->Compress(ddl);

  string logFile;
  if (dicFile.empty())
    logFile = "dictionary.dic";
  else
    logFile = dicFile;

  logFile += "-diag.log";

  dic->DataChecking(*ddl, logFile);

  time(&start);
  fobjR = new CifFile(true);
  cout<<cifFile<<endl;

  cifParserR = new CifParser(fobjR, fobjR->GetVerbose());

  cifParserR->Parse(cifFile, diags);

  delete(cifParserR);

  time(&end);
  cout<<"second(s)"<<difftime(end,start)<<endl;
  cout<<"============================="<<endl;
  time(&start);
  fobjR->DataChecking(*dic, cifFile + "-diag.log");

  time(&end);
  cout<<"second(s)"<<difftime(end,start)<<endl;
  delete (ddl);
  delete (dic);
  delete (fobjR);
}
