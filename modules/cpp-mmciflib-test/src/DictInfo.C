#include <iostream>

#include "ISTable.h"
#include "DicFile.h"
#include "DICParserBase.h"

using std::cout;
using std::endl;

static void ShowUsage(void);

int main(int argc, char** argv)
{

    if (argc < 4)
    {
        ShowUsage();
        return(1);
    }

    string dicFileName = argv[1];
    string ddlFileName = argv[2];
    string catName = argv[3];

    DicFile* ddlFileP = new DicFile();

    CifFile* ddlRefFileP = ddlFileP->GetRefFile();

    DICParser* ddlParserP = new DICParser(ddlFileP, ddlRefFileP);

    string diags;
    ddlParserP->Parse(ddlFileName, diags);

    delete(ddlParserP);

    if (!diags.empty())
    {
        cout << diags << endl;
    }

    DicFile* dicFileP = new DicFile();

    DICParser* dicParserP = new DICParser(dicFileP, ddlFileP);

    dicParserP->Parse(dicFileName, diags);

    delete(dicParserP);

    if (!diags.empty())
    {
        cout << diags << endl;
    }

    // Get the first block of the dictionary
    Block& dictBlock = dicFileP->GetBlock(dicFileP->GetFirstBlockName());

    // Get "item" table
    ISTable* itemTableP = dictBlock.GetTablePtr("item");

    // Prepare search arguments 
    vector<string> searchList;
    searchList.push_back("category_id");

    vector<string> searchTarget;
    searchTarget.push_back(catName);

    // Search for the category
    vector<unsigned int> indices;
    itemTableP->Search(indices, searchTarget, searchList);

    cout << endl;
    cout << "Category \"" << catName << "\" has the following items"\
      " defined in the dictionary:" << endl;
    for (unsigned int i = 0; i < indices.size(); ++i)
    {
        const string& cell = (*itemTableP)(indices[i], "name");
        string itemName;
        CifString::GetItemFromCifItem(itemName, cell);
        cout << "  " << itemName << endl;
    }

} /* End of main() */

void ShowUsage(void)
{

    cout << "Usage: DictInfo dict_file ddl_file category_name" << endl;

}

