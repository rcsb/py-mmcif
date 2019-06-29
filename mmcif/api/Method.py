##
# File:      Method.py
# Orignal:   Aug 12, 2013   Jdw
#
# Updates:
#   01-Aug-2017   jdw migrate portions to public repo
#   12-Jun-2018   jdw add missing accessor for MethodDefinition getCode()
#    9-Sep-2018   jdw add priority to method definition
#
##
"""
Utility classes for applying dictionary methods on PDBx/mmCIF data files.
"""

from __future__ import absolute_import

import sys

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


class MethodDefinition(object):
    def __init__(self, methodId, code="calculate", language="Python", inline=None, priority=None, implementation=None, implementationSource="inline"):
        self.methodId = methodId
        self.language = language
        self.code = code
        self.inline = inline
        self.priority = priority if priority else 1
        self.implementationSource = implementationSource
        self.implementation = implementation

    def getId(self):
        return self.methodId

    def getLanguage(self):
        return self.language

    def getCode(self):
        return self.code

    def getInline(self):
        return self.inline

    def getImplementation(self):
        return self.implementation

    def getImplementationSource(self):
        return self.implementationSource

    def getPriority(self):
        return self.priority

    def printIt(self, fh=sys.stdout):
        fh.write("------------- Method definition -------------\n")
        fh.write("Id:                      %s\n" % self.methodId)
        fh.write("Code:                    %s\n" % self.code)
        fh.write("Language:                %s\n" % str(self.language))
        fh.write("Inline text:             %s\n" % str(self.inline))
        fh.write("Imlementation:           %s\n" % str(self.implementation))
        fh.write("Implementation source:   %s\n" % str(self.implementationSource))
        fh.write("Priority:                %d\n" % self.priority)

    def __repr__(self):
        oL = []
        oL.append("\n------------- Method definition -------------")
        oL.append("Id:                      %s" % self.methodId)
        oL.append("Code:                    %s" % self.code)
        oL.append("Language:                %s" % str(self.language))
        oL.append("Inline text:             %s" % str(self.inline))
        oL.append("Imlementation:           %s" % str(self.implementation))
        oL.append("Implementation source:   %s" % str(self.implementationSource))
        oL.append("Priority:                %d" % self.priority)
        return "\n".join(oL)


class MethodReference(object):
    def __init__(self, methodId, mType="attribute", category=None, attribute=None):
        self.methodId = methodId
        self.type = mType
        self.categoryName = category
        self.attributeName = attribute

    def getId(self):
        return self.methodId

    def getType(self):
        return self.type

    def getCategoryName(self):
        return self.categoryName

    def getAttributeName(self):
        return self.attributeName

    def printIt(self, fh=sys.stdout):
        fh.write("--------------- Method Reference -----------------\n")
        fh.write("Id:             %s\n" % self.methodId)
        fh.write("Type:           %s\n" % self.type)
        fh.write("Category name:  %s\n" % str(self.categoryName))
        fh.write("Attribute name: %s\n" % str(self.attributeName))

    def __repr__(self):
        oL = []
        oL.append("--------------- Method Reference -----------------")
        oL.append("Id:             %s" % self.methodId)
        oL.append("Type:           %s" % self.type)
        oL.append("Category name:  %s" % str(self.categoryName))
        oL.append("Attribute name: %s" % str(self.attributeName))
        return "\n".join(oL)
