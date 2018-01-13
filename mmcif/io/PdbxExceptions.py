##
# File:  PdbxExceptions.py
# Date:  2012-01-09  Jdw  Adapted from PdbxParser
#
##
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


class PdbxError(Exception):
    """ Class for catch general errors
    """

    def __init__(self, msg):
        super(PdbxError, self).__init__(msg)


class SyntaxError(Exception):
    """ Class for catching syntax errors
    """

    def __init__(self, msg):
        super(SyntaxError, self).__init__(msg)
#
