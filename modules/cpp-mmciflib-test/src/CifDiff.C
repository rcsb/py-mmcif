#include <iostream>

#include "CifFile.h"
#include "CifParserBase.h"

using std::cout;
using std::endl;

static void ShowUsage(void);


int main(int argc, char** argv)
{

    string firstCifFileName;
    string secondCifFileName;

    CifFile* firstCifFileP = NULL;
    CifFile* secondCifFileP = NULL;

    CifParser* cifParserP = NULL;

    string diags;


    if (argc < 3)
    {
        ShowUsage();
        return(1);
    }

    firstCifFileName = argv[1];
    secondCifFileName = argv[2];

    firstCifFileP = new CifFile(true);

    cifParserP = new CifParser(firstCifFileP, firstCifFileP->GetVerbose());

    cifParserP->Parse(firstCifFileName, diags);

    delete(cifParserP);

    if (!diags.empty())
    {
        cout << " Diagnostics [" << diags.size() << "] " << diags << endl;
    }

    diags.clear();


    secondCifFileP = new CifFile(true);

    cifParserP = new CifParser(secondCifFileP, secondCifFileP->GetVerbose());

    cifParserP->Parse(secondCifFileName, diags);

    delete(cifParserP);

    if (!diags.empty())
    {
        cout << " Diagnostics [" << diags.size() << "] " << diags << endl;
    }

    vector<string> firstCifFileBlocks;
    vector<string> secondCifFileBlocks;

    firstCifFileP->GetBlockNames(firstCifFileBlocks);
    secondCifFileP->GetBlockNames(secondCifFileBlocks);

#ifdef VLAD_LATER
    vector<pair<string, vector<pair<string, ISTable::eTableDiff> > > fileDiff;
#endif

    for (unsigned int blockI = 0; blockI < firstCifFileBlocks.size();
      ++blockI)
    {
        if (!secondCifFileP->IsBlockPresent(firstCifFileBlocks[blockI]))
        {
#ifdef VLAD_LATER
            fileDiff.push_back(make_pair(firstCifFileBlocks[blockI],
              ISTable::eEXTRA));
#else
            cout << "Block \"" << firstCifFileBlocks[blockI] <<
              "\" in file \"" << firstCifFileName << "\", but not "\
              "in file \"" << secondCifFileName << "\"." << endl;
#endif
        }
        else
        {
            Block& firstFileBlock =
              firstCifFileP->GetBlock(firstCifFileBlocks[blockI]);
            Block& secondFileBlock =
              secondCifFileP->GetBlock(firstCifFileBlocks[blockI]);

            vector<pair<string, ISTable::eTableDiff> > blockDiff = 
              (firstFileBlock == secondFileBlock);

            if (!blockDiff.empty())
            {
#ifdef VLAD_LATER
                fileDiff.push_back(make_pair(firstCifFileBlocks[blockI],
                  blockDiff));
#else
                cout << "Block \"" << firstCifFileBlocks[blockI] <<
                  "\" different:" << endl;

                for (unsigned int diffI = 0; diffI < blockDiff.size(); ++diffI)
                {
                    cout << "  Table \"" << blockDiff[diffI].first << "\"";
                    switch(blockDiff[diffI].second)
                    {
                        case ISTable::eEXTRA:
                          cout << " in the first file block, but not in the"\
                            " second file block.";
                          break;
                        case ISTable::eMISSING:
                          cout << " not in the first file block, but in the"\
                            " second file block.";
                          break;
                        case ISTable::eCASE_SENSE:
                          cout << " differs in column case sensitivity.";
                          break;
                        case ISTable::eMORE_ROWS:
                          cout << " of the first file block"\
                            " has more rows.";
                          break;
                        case ISTable::eLESS_ROWS:
                          cout << " of the first file block"\
                            " has less rows.";
                          break;
                        case ISTable::eMORE_COLS:
                          cout << " of the first file block"\
                            " has more columns.";
                          break;
                        case ISTable::eLESS_COLS:
                          cout << " of the first file block"\
                            " has less columns.";
                          break;
                        case ISTable::eCOL_NAMES:
                          cout << " differs in column names.";
                          break;
                        case ISTable::eCELLS:
                          cout << " differs in content.";
                          break;
                        default:
                          break; 
                    }
                    cout << endl;
                }
#endif
            }
        }
    }

    for (unsigned int blockI = 0; blockI < secondCifFileBlocks.size();
      ++blockI)
    {
        if (!firstCifFileP->IsBlockPresent(secondCifFileBlocks[blockI]))
        {
#ifdef VLAD_LATER
            diff.push_back(make_pair(secondBlockTableNames[tableI],
              ISTable::eMISSING));
#else
            cout << "Block \"" << secondCifFileBlocks[blockI] <<
              "\" not in file \"" << firstCifFileName << "\", but "\
              "in file \"" << secondCifFileName << "\"." << endl;
#endif
        }
    }

    delete (firstCifFileP);
    delete (secondCifFileP);

} /* End of main() */


void ShowUsage(void)
{

    cout << "Usage: CifDiff first_cif_file second_cif_file" << endl;

}

