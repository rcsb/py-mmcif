#!/bin/bash
#
rm -rf build
mkdir build
cd build
cmake ..
make
#
cd lib
python -c "import mmciflib" | grep "Symbol not found"
#