# mmCIF Core Access Library

[![Build Status](https://dev.azure.com/rcsb/RCSB%20PDB%20Python%20Projects/_apis/build/status/rcsb.py-mmcif?branchName=master)](https://dev.azure.com/rcsb/RCSB%20PDB%20Python%20Projects/_build/latest?definitionId=16&branchName=master)

## Introduction

This module includes a native Python mmCIF API for data files and dictionaries along with
[pybind11](https://github.com/pybind/pybind11) wrappers for the PDB C++ Core mmCIF Library.

### Installation

Download the library source software from the project repository:

```bash

git clone  --recurse-submodules  https://github.com/rcsb/py-mmcif.git

```

Optionally, run test suite using the Tox test runner. The C++ library bindings have been tested
on Centos 7 Linux with GCC/G++ 4.8.5 and MacOS with clang-900.0.39.2 using Python versions 2.7.16 and 3.7.3.

```bash
tox
```

Installation is via the program [pip](https://pypi.python.org/pypi/pip).

```bash
pip install mmcif

or from the local repository:

pip install .
```

To generate API documentation using [Sphinx](http://www.sphinx-doc.org/):

```bash
cd scripts
# Check Sphinx dependencies in the introductory comments to the following script.
./initdocs.sh

```
