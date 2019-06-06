##
# File:    DictionayMarkdownTests.py
# Author:  jdw
# Date:    19-Oct-2018
# Version: 0.001
##
"""
Example/test of dictionary API to format dictioanry definition content in Markdown markup -

"""
from __future__ import absolute_import

import logging
import os
import sys
import time
import unittest
from operator import itemgetter

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

try:
    from mmcif import __version__
except Exception as e:
    sys.path.insert(0, TOPDIR)
    from mmcif import __version__

from mmcif.api.DictionaryApi import DictionaryApi
from mmcif.api.PdbxContainers import CifName
from mmcif.io.IoAdapterPy import IoAdapterPy as IoAdapter
from mmcif.io.PdbxExceptions import PdbxError, SyntaxError

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DictionayMarkdownTests(unittest.TestCase):

    def setUp(self):
        self.__verbose = True
        self.__pathPdbxV50Dictionary = os.path.join(HERE, "data", "mmcif_pdbx_v5_next.dic")

    def tearDown(self):
        pass

    def testMarkupCategoryGroup(self):
        oFile = os.path.join(HERE, 'test-output', 'xfel_extension.md')
        self.__testMarkupCategoryGroup(oFile=oFile, groupSelectList=['xfel_group'])
        oFile = os.path.join(HERE, 'test-output', 'xfel_extension.md"')
        self.__testMarkupCategoryGroup(oFile=oFile, groupSelectList=['diffrn_data_set_group'])

    def __processbounds(self, bList):
        '''
            | columnName 1| columnName 2 |
            | ------------- | ------------ |
            | coldata1 | coldata2 |
            | coldata1 | coldata2 |
        '''
        retList = []
        # Boundary values -
        #  (min, max)
        skipEquivalentBounds = True
        boundaryList = []
        for b in bList:
            min = b[0]
            max = b[1]
            if skipEquivalentBounds and min == max:
                continue
            if min == '.':
                min = '<h3>-&infin;</h3>'
            if max == '.':
                max = '<h3>+&infin;</h3>'
            boundaryList.append((min, max))

        if boundaryList is not None and len(boundaryList) > 0:
            retList.append(('Minimum&nbsp;Value', 'Maximum&nbsp;Value'))
            retList.extend(boundaryList)

        return retList

    def __formatTupListInset(self, tupList, tab='     '):
        rL = []
        for tup in tupList:
            rL.append('')
            rL.append('```')
            if tup[1] and len(tup[1]) > 0:
                tL = tup[1].split('\n')
                for t in tL:
                    rL.append(tab + t)
            #
            tL = tup[0].split('\n')
            for t in tL:
                rL.append(tab + t)
            rL.append('```')
            rL.append('')
        #
        #
        return rL

    def __trB(self, iBool):
        if iBool:
            return 'yes'
        else:
            return 'no'

    def __sortIgnoreCase(self, iList):
        tL = []
        for i in iList:
            tL.append((i, i.upper()))
        #
        sL = sorted(tL, key=itemgetter(1), reverse=False)
        #
        rL = []
        for s in sL:
            rL.append(s[0])
        #
        return rL

    def __testMarkupCategoryGroup(self, oFile, groupSelectList=None):
        """Test case -  extract the content to be rendered -
        """
        startTime = time.time()
        logger.debug("\nStarting %s %s at %s\n" % (self.__class__.__name__,
                                                   sys._getframe().f_code.co_name,
                                                   time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            rL = []

            myIo = IoAdapter()
            self.__containerList = myIo.readFile(self.__pathPdbxV50Dictionary)
            dApi = DictionaryApi(containerList=self.__containerList, consolidate=True, verbose=self.__verbose)
            #
            groupList = dApi.getCategoryGroups()
            logger.debug('groupList %s\n' % groupList)
            for groupName in groupList:
                if groupSelectList and groupName not in groupSelectList:
                    continue

                #
                # Goup header details
                #
                rL.append("# Category Group %s" % groupName)
                rL.append("")
                rL.append("")
                rL.append("%s" % dApi.getCategoryGroupDescription(groupName))
                rL.append("")
                rL.append("---")
                rL.append("")
                catNameList = dApi.getCategoryGroupCategories(groupName=groupName)
                #
                cList = self.__sortIgnoreCase(catNameList)
                for catName in cList:
                    logger.debug('Group %s category %s\n' % (groupName, catName))
                    catDescription = dApi.getCategoryDescription(category=catName)
                    catExTupList = dApi.getCategoryExampleList(category=catName)
                    keyItemNameList = dApi.getCategoryKeyList(category=catName)
                    keyAttNameList = [CifName.attributePart(k) for k in keyItemNameList]
                    #
                    # Category header details
                    #
                    rL.append("## Category %s" % catName)
                    rL.append("")
                    rL.append("")
                    rL.append(" %s" % catDescription)
                    rL.append("")
                    rL.append("---")
                    rL.append("")
                    if catExTupList:
                        rL.extend(self.__formatTupListInset(catExTupList, tab='     '))
                        #
                        # summary table
                        #
                    rL.append("")
                    rL.append("---")
                    rL.append("")
                    rL.append("| Attribute | Key | Required | Type | Units | Enumerated | Bounded |")
                    rL.append("| --------- | --- | -------- | ---- | ----- | ---------- | ------- |")
                    aList = self.__sortIgnoreCase(dApi.getAttributeNameList(category=catName))
                    for attName in aList:
                        isKey = attName in keyAttNameList
                        attDescription = dApi.getDescription(category=catName, attribute=attName)
                        attUnits = dApi.getUnits(category=catName, attribute=attName)
                        attMandatory = dApi.getMandatoryCode(category=catName, attribute=attName)
                        attTypeCode = dApi.getTypeCode(category=catName, attribute=attName)

                        enumTupList = dApi.getEnumListWithDetail(category=catName, attribute=attName)
                        if len(enumTupList) > 0:
                            isEnum = True
                        else:
                            isEnum = False
                        bL = dApi.getBoundaryList(category=catName, attribute=attName)
                        if len(bL) > 0:
                            isBounded = True
                        else:
                            isBounded = False
                        rL.append(
                            '| %s | %s | %s | %s | %s | %s | %s |' %
                            (attName,
                             self.__trB(isKey),
                                attMandatory,
                                attTypeCode,
                                attUnits,
                                self.__trB(isEnum),
                                self.__trB(isBounded)))
                    #
                    rL.append("")
                    rL.append("---")
                    rL.append("")
                    #
                    for attName in aList:
                        isKey = attName in keyAttNameList
                        attMandatory = dApi.getMandatoryCode(category=catName, attribute=attName)
                        #
                        tN = '_' + catName + '.' + attName
                        if isKey:
                            tN = tN + ' (key)'
                        elif attMandatory.upper() in ['YES', 'Y']:
                            tN = tN + ' (required)'
                        #
                        rL.append("#### %s\n" % tN)
                        rL.append("")
                        attDescription = dApi.getDescription(category=catName, attribute=attName)
                        rL.append(" %s\n" % attDescription)
                        rL.append("")
                        attUnits = dApi.getUnits(category=catName, attribute=attName)
                        attTypeCode = dApi.getTypeCode(category=catName, attribute=attName)

                        enumTupList = dApi.getEnumListWithDetail(category=catName, attribute=attName)
                        if len(enumTupList) > 0:
                            rL.append("")
                            rL.append("---")
                            rL.append("")
                            rL.append("| Allowed Values | Detail |")
                            rL.append("| -------------- | ------ |")
                            for tup in enumTupList:
                                if tup[1] and len(tup[1]) > 0:
                                    rL.append("| %s | %s |" % (tup[0], tup[1]))
                                else:
                                    rL.append("| %s | %s |" % (tup[0], ' '))
                            rL.append("")

                        #
                        bL = dApi.getBoundaryList(category=catName, attribute=attName)
                        btL = self.__processbounds(bL)
                        if len(btL) > 0:
                            tup = btL[0]
                            rL.append("")
                            rL.append("---")
                            rL.append("")
                            rL.append("| %s | %s |" % (tup[0], tup[1]))
                            #
                            rL.append("| ------------- | ------ |")
                            for tup in btL[1:]:
                                rL.append("| %s | %s |" % (tup[0], tup[1]))
                            rL.append("")
                        rL.append("")
            with open(oFile, 'w') as ofh:
                ofh.write('\n'.join(rL))

        except Exception as e:
            logger.Exception("Failing with %s" % str(e))
            self.fail()

        endTime = time.time()
        logger.debug("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                   sys._getframe().f_code.co_name,
                                                                   time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                   endTime - startTime))


def suiteMarkdownTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(DictionayMarkdownTests("testMarkupCategoryGroup"))
    return suiteSelect


if __name__ == '__main__':
    if (True):
        mySuite = suiteMarkdownTests()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
