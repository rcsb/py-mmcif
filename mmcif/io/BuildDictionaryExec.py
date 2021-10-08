##
# File: BuildDictionaryExec.py
# Date: 4-Apr-2021  jdw
#
#  CLI to materialize text dictionary files from dictionary components and include directives.
#
#  Updates:
##
__docformat__ = "google en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import argparse
import logging
import os
import sys

from mmcif.api.DictionaryInclude import DictionaryInclude
from mmcif.io.IoAdapterPy import IoAdapterPy as IoAdapter

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()


def main():
    parser = argparse.ArgumentParser()
    #
    #
    parser.add_argument("--op", default=None, required=True, help="Operation (build | get_version)")
    parser.add_argument("--input_dict_path", required=True, default=None, help="Path to dictionary generator file")
    parser.add_argument("--output_dict_path", default=None, help="Path to output dictionary text file")
    parser.add_argument("--cleanup", default=False, action="store_true", help="Remove include instruction categories after processing")
    args = parser.parse_args()
    #
    try:
        op = args.op.lower() if args.op else None
        inputDictPath = args.input_dict_path
        outputDictPath = args.output_dict_path
        cleanup = args.cleanup
    except Exception as e:
        logger.exception("Argument processing problem %s", str(e))
        parser.print_help(sys.stderr)
        exit(1)

    ##
    if op == "build" and inputDictPath and outputDictPath:
        dirPath = os.path.abspath(os.path.dirname(inputDictPath))
        logger.info("Starting dictionary path %s", dirPath)
        myIo = IoAdapter(raiseExceptions=True)
        containerList = myIo.readFile(inputFilePath=inputDictPath)
        logger.info("Starting dictionary container list length (%d)", len(containerList))
        dIncl = DictionaryInclude(dirPath=dirPath)
        inclL = dIncl.processIncludedContent(containerList, cleanup=cleanup)
        logger.info("Processed dictionary container length (%d)", len(inclL))
        ok = myIo.writeFile(outputFilePath=outputDictPath, containerList=inclL)
        logger.info("Operation completed with status %r", ok)
    elif op == "get_version" and inputDictPath:
        logger.setLevel(logging.ERROR)
        myIo = IoAdapter(raiseExceptions=True)
        containerList = myIo.readFile(inputFilePath=inputDictPath)
        dIncl = DictionaryInclude()
        inclL = dIncl.processIncludedContent(containerList)
        baseContainer = inclL[0]
        if baseContainer.exists("dictionary"):
            cObj = baseContainer.getObj("dictionary")
            version = cObj.getValueOrDefault("version", 0, None)
            print(version)


if __name__ == "__main__":
    main()
