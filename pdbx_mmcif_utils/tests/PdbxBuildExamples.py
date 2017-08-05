##
#
# File:    PdbxBuildExamples.py
# Author:  jdw
# Date:    12-October-2009
# Version: 0.001
##
"""
Some examples dictionary maintenace functions using the PdbxBuild class.

"""
from __future__ import absolute_import
from __future__ import print_function
__docformat__ = "restructuredtext en"
__author__    = "John Westbrook"
__email__     = "jwest@rcsb.rutgers.edu"
__license__   = "Creative Commons Attribution 3.0 Unported"
__version__   = "V0.01"

import sys, unittest, traceback
import sys, time, os, os.path, shutil

from pdbx_v2.reader.PdbxBuild  import PdbxBuild


def findUnmappedDefinitions():
    """ Find the list of un-mapped definitions in RCSB dictionaries.
    
        Return the list (name,type) along with the complete list of names in PDB (name,type).
    """
    unMappedList=[]
    myBuild=PdbxBuild(True)
    myDict=myBuild.readDictionary("../data/mmcif_pdbx_v4_internal.dic")
    fh = open("dumpPdbxDictionaryAliases.out",'w')
    aDict={}
    nList=[]
    (aDict,nList)=myBuild.dumpDictionaryAliases(fh)    
    fh.close()
    #
    myDict=myBuild.readDictionary("../data/mmcif_rcsb_xray.dic")
    fh = open("dumpRcsbDictionaryAliases.out",'w')
    rcsbAliasDict={}
    rcsbNameList=[]
    (rcsbAliasDict,rcsbNameList)=myBuild.dumpDictionaryAliases(fh)    
    fh.close()
    #
    myDict=myBuild.readDictionary("../data/mmcif_rcsb_nmr.dic")
    fh = open("dumpRcsbNmrDictionaryAliases.out",'w')
    rcsbAliasDictNmr={}
    rcsbNameListNmr=[]
    (rcsbAliasDictNmr,rcsbNameListNmr)=myBuild.dumpDictionaryAliases(fh)    
    fh.close()
    for n,t in rcsbNameListNmr:
        if (n,t) not in rcsbNameList:
            rcsbNameList.append((n,t))
    #
    # how many names in both X-ray and NMR RCSB dictionaries are not mapped in PDBx.
    #
    
    fh = open("unmappedRcsbItems.out",'w')
    rCatP=""
    for rName,rType in rcsbNameList:
        if ((rName,rType) in nList  or rName in aDict):
            # mapped
            pass
        else:
            if (rType == "category"):
                fh.write("\n----------------------------------\n")            
                fh.write("%s (unmapped category)\n" % rName)
                #rCat=rName
                unMappedList.append((rName,rType))            
            else:
                rCat=rName[1:rName.find(".")]
                if rCatP != rCat:
                    fh.write("\n----------------------------------\n")
                    fh.write("%s (unmapped items in category)\n" % rCat)                    
                fh.write("      %s\n" % rName)
                unMappedList.append((rName,rType))
                rCatP = rCat
        
    fh.close()
    return unMappedList, nList, aDict

def renameUM():
    
    uL,pdbxList,aliasDict=findUnmappedDefinitions()
    sys.stdout.write("Number of unmapped definitions is %d\n" % len(uL))
    
    prefixList = ["rcsb","ccp4","ndb","bmcd","ebi"]
    
    myBuild=PdbxBuild(True)    
    myDict=myBuild.readDictionary("../data/mmcif_rcsb_internal.dic",True)
    myBuild.setDdlFilePath("../data/mmcif_ddl.dic")
    fh = open("dumpRename.out",'w')
    #
    # Build rename list and flag cases lacking prefixes -
    replaceList=[]
    for uNm,type in uL:
        rNm=uNm
        if type == "category":
            catC=uNm
            for prefix in prefixList:
                if catC.startswith(prefix):
                    catC=catC.replace(prefix,"pdbx",1)
                    break
                else:
                    pass
            rNm=catC
        elif type == "attribute":
            catC=CifName.categoryPart(uNm)
            attC=CifName.attributePart(uNm)
            iC=False
            for prefix in prefixList:
                if catC.startswith(prefix):
                    catC=catC.replace(prefix,"pdbx",1)
                    iC=True
                    break
                else:
                    pass
            if (not iC):
                iA=False
                for prefix in prefixList:
                    if attC.startswith(prefix):
                        attC=attC.replace(prefix,"pdbx",1)
                        iA=True
                        break
                    else:
                        pass
            rNm="_"+catC+"."+attC
        else:
            pass


#        if (rNm,type) in pdbxList and type == "attribute":
#            print "Conflicting item ",rNm

            #        if (rNm,type) in pdbxList and type == "category":

        if (uNm != rNm):
            replaceList.append((type,uNm,rNm))
        else:
            print("Unresolved unmapped name",uNm)
            
    
    #    for nameType,uNm,rNm  in replaceList:
    #        myBuild.renameDefinition(uNm,rNm,nameType,fh)
    
    oL=myBuild.renameDefinitionList(replaceList,aliasDict,fh)
    #
    wL=[]
    for ob in oL:
        name =  ob.getName()

        if ob.isAttribute():
            type="attribute"
        elif ob.isCategory():
            type="category"
        else:
            type = "unk"

        if (name,type)  in pdbxList:
            print("skipping ", name)
        else:
            wL.append(ob)
    #
    fh.close()
    myBuild.writeDictionaryObjList("renamedDict.dic",wL)
    
if __name__ == "__main__":
    renameUM()
    
