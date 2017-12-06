#include <iostream>

#include "ISTable.h"
#include "CifFile.h"
#include "CifParserBase.h"

using std::cout;
using std::endl;

static void ShowUsage(void);
static unsigned int CountPopulatedItemsInFile(CifFile* cifFileP);
static unsigned int CountPopulatedItemsInTable(ISTable* tableP);

static unsigned int NumNonPopulatedItems = 0;
static bool Verbose = false;

int main(int argc, char** argv)
{

    if (argc < 2)
    {
        ShowUsage();
        return(1);
    }

    string cifFileName = argv[1];

    CifFile* cifFileP = new CifFile;

    CifParser* cifParserP = new CifParser(cifFileP);

    string diags;
    cifParserP->Parse(cifFileName, diags);

    delete(cifParserP);

    if (!diags.empty())
    {
        cout << " Diagnostics [" << diags.size() << "] " << diags << endl;
    }

    diags.clear();

    unsigned int numPopulatedItems = CountPopulatedItemsInFile(cifFileP);

    cout << "File: \"" << cifFileName << "\" has " << numPopulatedItems <<
      " populated items." << endl;

    if (Verbose)
    {
        cout << "File: \"" << cifFileName << "\" has " <<
          NumNonPopulatedItems << " non-populated items." << endl;
    }
} /* End of main() */

unsigned int CountPopulatedItemsInFile(CifFile* cifFileP)
{
    unsigned int numPopItems = 0;

    vector<string> cifFileBlocks;
    cifFileP->GetBlockNames(cifFileBlocks);

    for (unsigned int blockI = 0; blockI < cifFileBlocks.size(); ++blockI)
    {
        if (Verbose)
            cout << "Block: \"" << cifFileBlocks[blockI] << "\"" << endl;

        // Get block reference
        Block& block = cifFileP->GetBlock(cifFileBlocks[blockI]);

        // Get all the tables in a block
        vector<string> tableNames;

        block.GetTableNames(tableNames);
        for (unsigned int tableI = 0; tableI < tableNames.size(); ++tableI)
        {
            if (Verbose)
                cout << "  Table: \"" << tableNames[tableI] << "\"" << endl;

            ISTable* tableP = block.GetTablePtr(tableNames[tableI]);

            numPopItems += CountPopulatedItemsInTable(tableP);
        }
    }

    return (numPopItems);
}

unsigned int CountPopulatedItemsInTable(ISTable* tableP)
{

    unsigned int numPopItems = 0;

    unsigned int numRows = tableP->GetNumRows();

    const vector<string>& colNames = tableP->GetColumnNames();
    
    for (unsigned int colI = 0; colI < colNames.size(); ++colI)
    {
        bool populated = false;
        for (unsigned int rowI = 0; rowI < numRows; ++rowI)
        {
            const string& cell = (*tableP)(rowI, colNames[colI]);

            if (!CifString::IsEmptyValue(cell))
            {
                populated = true;
                break;
            }
        }

        if (populated)
        {
            numPopItems++;
        }
        else
        {
            NumNonPopulatedItems++;
            if (Verbose)
                cout << "    Column: \"" << colNames[colI] <<
                  "\" not populated." << endl;
            continue;
        }
    }

    return (numPopItems);
}

void ShowUsage(void)
{

    cout << "Usage: CifInfo cif_file" << endl;

}

