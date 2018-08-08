## mmCIF Core Access Library

### Introduction

This module includes a native Python mmCIF API for data files and dictionaries along with
[pybind11](https://github.com/pybind/pybind11) wrappers for the PDB C++ Core mmCIF Library.

### Installation

Download the library source software from the project repository:

```bash

git clone  --recurse-submodules  https://github.com/rcsb/py-mmcif.git

```

Optionally, run test suite using the Tox test runner. The C++ library bindings have been tested
on Centos 7 Linux with GCC/G++ 4.8.5 and MacOS with clang-900.0.39.2 using Python versions 2.7.14,
3.6.6, and 3.7.0

```bash
tox
```

Installation is via the program [pip](https://pypi.python.org/pypi/pip).

```bash
pip install .
```

To generate API documentation using [Sphinx](http://www.sphinx-doc.org/):

```bash
cd scripts
# Check Sphinx dependencies in the introductory comments to the following script.
./initdocs.sh

```
