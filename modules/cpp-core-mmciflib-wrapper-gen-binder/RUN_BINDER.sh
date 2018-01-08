#!/bin/bash
# File: RUN_BINDER.sh
#
# First pre-process and make local copies of include files by running: reformat-includes.py
#
# Set the BINDER_PATH in the environment to point to the Rosetta binder app.
#
# ./RUN_BINDER.sh   will generate wrapper source file in src-Darwin or src-Linux.
#
myKernel="`uname -s`"
#set -x
if [ "$myKernel" == "Darwin" ]
then
    if [ -z $BINDER_PATH ]
    then
        BINDER_PATH="/opt/rosetta-binder/binder/build/llvm-4.0/build_release_40.macos.rtt.release/bin/binder"
    fi
elif [ "$myKernel" == "Linux" ]
then
    if [ -z $BINDER_PATH ]
    then
        BINDER_PATH="/opt/rosetta/binder/build/llvm-4.0/build_release_40.linux.pdb-hp-linux-17.rcsb.rutgers.edu.release/bin/binder"
    fi
else
    echo "Unsupported kernel: $myKernel"
fi
#
if [ -z $BINDER_PATH ]
then
    echo "BINDER_PATH is not set"
else
    if [ ! -e $BINDER_PATH ]
        then
            echo "BINDER_PATH is misassigned - no binary found at $BINDER_PATH"
        fi
fi
#
PREFIX="./src-${myKernel}"
#if [ -d $PREFIX ]
#then
#    rm -rf $PREFIX
#else
#    mkdir $PREFIX
#    mkdir $PREFIX/std
#fi

CONFIG_PATH="./core_mmciflib_binder_${myKernel}.config"

if [ "$myKernel" == "Darwin" ]
then
  XCODE_PATH="/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/../include/c++/v1"
  if [ -d $XCODE_PATH ]
    then
        $BINDER_PATH -v  --root-module mmciflib --config $CONFIG_PATH \
        --prefix ${PREFIX}/   \
        --bind "" \
        current-pybind-include-list.h \
        -- -std=c++11 -x c++ -fexceptions -fcxx-exceptions -I../cpp-core-mmciflib-wrapper-gen/include-binder \
          -isystem $XCODE_PATH
    else
        echo "Missing XCODE_PATH: %{XCODE_PATH}"
    fi
elif [ "$myKernel" == "Linux" ]
then
        $BINDER_PATH -v  --root-module mmciflib --config $CONFIG_PATH \
        --prefix ${PREFIX}/   \
        --bind "" \
        current-pybind-include-list.h \
        -- -std=c++11 -x c++ -fexceptions -fcxx-exceptions -I../cpp-core-mmciflib-wrapper-gen/include-binder
else
    echo "No binding code generated"
fi
#