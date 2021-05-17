import os

apiL = [
    "DataCategory",
    "DataCategoryBase",
    "DataCategoryFormatted",
    "DataCategoryTyped",
    "DictMethodRunner",
    "DictionaryApi",
    "DictionaryInclude",
    "Method",
    "MethodUtils",
    "PdbxContainers",
]

ioL = ["BinaryCifReader", "BinaryCifWriter", "CifFile", "IoAdapterBase", "IoAdapterCore", "IoAdapterPy", "PdbxExceptions", "PdbxReader", "PdbxWriter"]

for nm in apiL:
    with open(os.path.join(".", "api_reference", nm + ".md"), "w") as ofh:
        ofh.write("::: mmcif.api.%s:%s\n" % (nm, nm))
for nm in ioL:
    with open(os.path.join(".", "api_reference", nm + ".md"), "w") as ofh:
        ofh.write("::: mmcif.io.%s:%s\n" % (nm, nm))
