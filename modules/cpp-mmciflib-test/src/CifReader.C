#include <time.h>

#include <iostream>

#include "CifFile.h"
#include "CifParserBase.h"

using std::cout;
using std::endl;

static void ShowUsage(void);


int main(int argc, char** argv)
{

    string inFile;
    string sdbFile;
    string outFile;
    string diags;
    CifFile* fobjR = NULL;
    CifFileReadDef readDef;
    type readType;
    vector<string> catlist;
#ifdef VLAD_DELETED_FOR_NOW
    bool retTest;
#endif
    time_t start, end;

    CifParser* cifParserR = NULL;


    if (argc < 2)
    {
        ShowUsage();
        return(1);
    }

    inFile = argv[1];

    outFile = inFile;
    outFile += ".cif";

    sdbFile = inFile;
    sdbFile += ".sdb";

    if (argc > 2)
    {
        if (argc == 3)
        {
            ShowUsage();
            return(1);
        }
 
        if (strcmp(argv[2], "A") == 0)
        {
            readType = A;
        }
        else
        {
            readType = D;
        }

        for (int i = 3; i < argc; i++)
        {
            /* Add categories to the list. */
            catlist.push_back(argv[i]);
        }

        readDef.SetCategoryList(catlist, readType);
    }

//    vector<string> blocklist;
//    blocklist.Add("ADH041");

    /* Set the datablock list to accepted. */
//    readDef.SetDataBlockList(blocklist, A);

//    fobjR = new CifFile(CREATE_MODE, sdbFile, true,
//      Char::eCASE_INSENSITIVE);

    // Start parsing
    cout << "Begin parsing" << endl;

    time(&start);

    fobjR = new CifFile(CREATE_MODE, sdbFile, true);

    cifParserR = new CifParser(fobjR, readDef, fobjR->GetVerbose());

    cifParserR->Parse(inFile, diags);

    delete(cifParserR);

    if (!(diags.empty()))
    {
        cout << " Diagnostics [" << diags.size() << "] " << diags << endl;
    }

#ifdef VLAD_DELETED_FOR_NOW
    Block& block = fobjR->GetBlock(fobjR->GetFirstBlockName());
    retTest = block.IsTablePresent("atom_site");
    cout << "Return from IsTablePresent(atom_site): " << retTest << endl;
    retTest = block.IsTablePresent("ATOM_site");
    cout << "Return from IsTablePresent(ATOM_site): " << retTest << endl;
#endif

    time(&end);

    // End parsing
    cout << "Done parsing in " << difftime(end, start) << " second(s)" << endl;

    // Start writing
    cout << "Begin writing" << endl;

    time(&start);

    fobjR->Write(outFile);

    time(&end);

    // End writing
    cout << "Done writing in " << difftime(end, start) << " second(s)" << endl;

    // Start closing
    cout << "Begin closing" << endl;

    time(&start);

    delete (fobjR);

    time(&end);

    // End closing
    cout << "Done closing in " << difftime(end, start) << " second(s)" << endl;

} /* End of main() */


void ShowUsage(void)
{

    cout << "Usage: CifReader input_file [readType] [category]*" << endl;

}
