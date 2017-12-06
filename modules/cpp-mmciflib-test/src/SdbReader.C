#include <iostream>

#include "CifFile.h"

using std::cout;
using std::endl;

static void ShowUsage(void);


int main(int argc, char** argv)
{

    string inSdbFile;
    string outCifFile;
    CifFile* fobjR = NULL;


    if (argc < 2)
    {
        ShowUsage();
        return(1);
    }

    inSdbFile = argv[1];

    outCifFile = inSdbFile;
    outCifFile += ".cif";

    fobjR = new CifFile(READ_MODE, inSdbFile, true);

    fobjR->Write(outCifFile);

    delete (fobjR);

} /* End of main() */


void ShowUsage(void)
{

    cout << "Usage: SdbReader input_sdb_file" << endl;

}
