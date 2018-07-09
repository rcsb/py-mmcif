##
#  File:  mmcif/api/__init__.py
#
#  Date: 9-July-2018 jdw get this py2/3 stuff out of the main code base.
#
#
import sys

__isPy3 = sys.version_info[0] == 3

if __isPy3:
    __STRING_TYPES__ = str
else:
    __STRING_TYPES__ = basestring
#
