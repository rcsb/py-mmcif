#!/bin/bash
#
#cmake -DPYTHON_LIBRARY=$(python-config --prefix)/lib/libpython2.7.dylib -DPYTHON_INCLUDE_DIR=$(python-config --prefix)/include/python2.7 .
#
# cmake .. \
# -DPYTHON_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")  \
# -DPYTHON_LIBRARY=$(python -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))") \
# -DPYTHON_EXECUTABLE:FILEPATH=`which python`
# -DPYTHON_LIBRARY=$(python -c "import distutils.sysconfig as sysconfig; import os; print(os.path.join(sysconfig.get_config_var('LIBDIR'), sysconfig.get_config_var('LDLIBRARY')))")
#
LIBDIR=$(python -c "import distutils.sysconfig as sysconfig; import os; print(os.path.join(sysconfig.get_config_var('LIBDIR'), sysconfig.get_config_var('LDLIBRARY')))")
INCDIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")
#
echo "Using INCDIR=${INCDIR}"
echo "Using LIBDIR=${LIBDIR}"
#
rm -rf build
mkdir build
cd build
#cmake ..
cmake -DPYTHON_LIBRARY=${LIBDIR}  -DPYTHON_INCLUDE_DIR=${INCDIR} ..
#
make
#
cd lib
python -c "import mmciflib" | grep "Symbol not found"
#