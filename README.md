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

## build_dict_cli tool

### Overview

`build_dict_cli` is a command-line tool that serves as a preprocessor for modular mmCIF dictionaries. It resolves and combines dictionary components from multiple source files using include directives specified in categories such as `pdbx_include_dictionary`, `pdbx_include_category`, and `pdbx_include_item`.

### Purpose

The tool allows dictionary maintainers to:
- Combine multiple dictionary extensions (or combining extension with a parent dictionary) into a single comprehensive dictionary
- Get dictionary version of the dictionary

#### Command-Line Arguments

```
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
```

##### Argument Details

- `--op`: Specifies the operation to perform
  - `build`: Generates a complete dictionary by processing includes
  - `get_version`: Retrieves and outputs the version of the specified dictionary
  
- `--input_dict_path`: Path to the dictionary generator file that contains include directives
  
- `--output_dict_path`: Path where the combined output dictionary will be written
  
- `--cleanup`: If specified, removes the include instruction categories from the final output

### Creating a Generator File

A generator file is a special mmCIF dictionary file that primarily contains include directives. This file serves as the entry point for the dictionary build process.

#### Example Generator File

```
# mmcif_pdbx_v50-generator.dic

data_mmcif_pdbx.dic
#
loop_
_pdbx_include_dictionary.dictionary_id
_pdbx_include_dictionary.dictionary_locator
_pdbx_include_dictionary.include_mode
_pdbx_include_dictionary.dictionary_namespace_prefix
_pdbx_include_dictionary.dictionary_namespace_prefix_replace
mmcif_pdbx_v50.dic          mmcif_pdbx_v50.dic          extend . .
mmcif_investigation_fraghub_ext.dic      mmcif_investigation_fraghub_ext.dic  extend . .
```

#### Key Components in a Generator File

- `dictionary_id`: Identifier for the dictionary to be included
- `dictionary_locator`: File path to the dictionary (relative to the generator file)
- `include_mode`: How to incorporate the dictionary (typically "extend")
- `dictionary_namespace_prefix`: Namespace prefix for the included dictionary (use "." for none)
- `dictionary_namespace_prefix_replace`: Replacement for the namespace prefix (use "." for none)

### Usage Workflow

1. **Prepare Dictionary Components**:
   - Create or obtain the dictionary files you want to combine
   - Ensure all dictionary files are present in the same directory or specify the correct relative paths

2. **Create a Generator File**:
   - Define a new mmCIF file with `_pdbx_include_dictionary` loop
   - List all dictionaries to be included with their proper attributes

3. **Run the Build Command**:
   ```bash
   build_dict_cli --op build --input_dict_path generator-file.dic --output_dict_path output-dictionary.dic
   ```

4. **Verify the Output**:
   - The tool will combine all specified dictionaries into a single output file
   - Check that all expected categories and items are present in the output

### Example Use Case

To combine a base PDBx dictionary with a InvestigationCIF extension dictionary:

1. Ensure both dictionaries are available in your working directory:
   ```
   mmcif_pdbx_v50.dic
   mmcif_investigation_fraghub_ext.dic
   ```

2. Create a generator file (e.g., `mmcif_pdbx_v50-generator-local.dic`):
   ```
   data_mmcif_pdbx.dic
   #
   loop_
   _pdbx_include_dictionary.dictionary_id
   _pdbx_include_dictionary.dictionary_locator
   _pdbx_include_dictionary.include_mode
   _pdbx_include_dictionary.dictionary_namespace_prefix
   _pdbx_include_dictionary.dictionary_namespace_prefix_replace
   mmcif_pdbx_v50.dic          mmcif_pdbx_v50.dic          extend . .
   mmcif_investigation_fraghub_ext.dic      mmcif_investigation_fraghub_ext.dic  extend . .
   ```

3. Run the build command:
   ```bash
    build_dict_cli --op build --input_dict_path mmcif_pdbx_v50-generator-local.dic --output_dict_path ./mmcif_investigation_fraghub.dic
   ```

4. The tool will produce `mmcif_investigation_fraghub.dic` containing the combined content of both dictionaries.

### Retrieving Dictionary Version

To get the version of a dictionary:

```bash
build_dict_cli --op get_version --input_dict_path mmcif_pdbx_v50.dic
```

This will output only the version number to stdout.
