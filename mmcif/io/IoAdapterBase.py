##
# File:    IoAdapterBase.py
# Author:  J. Westbrook
# Date:    1-Aug-2017
# Version: 0.001 Initial version
#
# Updates:
##
"""
Base class presenting essential PDBx/mmCIF IO methods.

"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


class IoAdapterBase(object):

    """ Base class presenting essential PDBx/mmCIF IO methods.
    """

    def __init__(self, *args, **kwargs):
        self._raiseExceptions = kwargs.get('raiseExceptions', False)

    def readFile(self, inputFile, **kwargs):
        """ Read file method -

            inputFile:  Input file path/uri
                   kw:  optional key-value arguments

            Returns:
                  containerList = list of data or definition container objects
        """
        raise NotImplementedError("To be implemented in subclass")

    def writeFile(self, outputFile, containerList, **kwargs):
        """ Write file method -

            outputFile:  output file path
            containerList:  list of data or definition containers objects for output

        """
        raise NotImplementedError("To be implemented in subclass")
