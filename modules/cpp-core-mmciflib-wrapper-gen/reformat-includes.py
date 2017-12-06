##
# File: reformat-includes.py
# Updated: 4-Dec-2017 jdw
#
# Convert #include "" to #include <> support wrapper code generation using Rosetta Binder -
#
# Processes all include files in the local module directories and makes a local copy of
# converted files in the ./include-binder directory.
#
# Updates the list of include files to be processed by binder in current-pybind-include-list.h
# subject to the exclusion list in exclude-include-pybind-list.txt.
#
import glob
import os


def wr_bind_list(incPath, bindIncFilePath="../cpp-core-mmciflib-wrapper-gen/current-pybind-include-list.h", exclFilePath="exclude-include-pybind.list"):
    exL = {}
    with open(exclFilePath, 'r') as ifh:
        for line in ifh:
            fn = str(line[:-1]).strip()
            if fn.startswith('#'):
                continue
            exL[fn] = True

    gP = os.path.join(incPath, '*')
    pL = glob.glob(gP)
    with open(bindIncFilePath, 'w') as ofh:
        for p in pL:
            d, f = os.path.split(p)
            if f in exL:
                continue
            s = "#include <%s>" % f
            ofh.write("%s\n" % s)


def get_include_file_list(pth="../../build/include"):
    oL = []
    pL = glob.glob(pth)
    for p in pL:
        d, f = os.path.split(p)
        #print(p)
        oL.append(p)
    return oL


def reformat_includes(pathList, oPath="../cpp-core-mmciflib-wrapper-gen/include-binder"):
    for inpPath in pathList:
        print("Reformattting include file %s" % inpPath)
        d, inpFn = os.path.split(inpPath)
        outFn = os.path.join(oPath, inpFn)
        with open(outFn, 'w') as outFh:
            with open(inpPath, 'r') as inpFh:
                for il in inpFh:
                    if il.startswith('#include "'):
                        fields = il.split()
                        f1 = fields[1].replace('"', '').strip()
                        outFh.write("#include <%s>\n" % f1)
                    else:
                        outFh.write(il)


if __name__ == "__main__":
    print("Starting")
    oPath = "../cpp-core-mmciflib-wrapper-gen/include-binder"
    if (not os.access(oPath, os.R_OK)):
        os.makedirs(oPath)
    moduleIncList = ['../cpp-common/include/*h',
                     '../cpp-common/src/mapped_*C',
                     '../cpp-tables/include/*h',
                     '../cpp-cif-file/include/*h',
                     '../cpp-cif-file-util/include/*h',
                     '../cc-regex/include/*h',
                     '../cpp-dict-obj-file/include/*h',
                     '../cpp-cif-parser/include/*h']
    pathList = []
    for m in moduleIncList:
        pathList.extend(get_include_file_list(pth=m))
    #
    reformat_includes(pathList, oPath=oPath)
    wr_bind_list(oPath, bindIncFilePath="../cpp-core-mmciflib-wrapper-gen/current-pybind-include-list.h")
    #
    #
