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
on Centos 7/Ubuntu 20.04 Linux with GCC/G++ > 4.8.5 and MacOS (10.15) with > clang-900.0.39.2 using
Python versions 2.7.18 and 3.9.4.

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

A command-line script is provided as a preprocessor for modular dictionaries that
include definition and data content using categories pdbx_include_dictionary,
pdbx_include_category and pdbx_include_item.

```bash

build_dict_cli --help
usage: build_dict_cli [-h] --op OP --input_dict_path INPUT_DICT_PATH [--output_dict_path OUTPUT_DICT_PATH] [--cleanup]

optional arguments:
  -h, --help            show this help message and exit
  --op OP               Operation (build | get_version)
  --input_dict_path INPUT_DICT_PATH
                        Path to dictionary generator file
  --output_dict_path OUTPUT_DICT_PATH
                        Path to output dictionary text file
  --cleanup             Remove include instruction categories after processing
________________________________________________________________________________
```
