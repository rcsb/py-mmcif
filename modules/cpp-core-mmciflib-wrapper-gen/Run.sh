#!/bin/bash
#
python ../../../py-wrap_pybind11/wrap_pybind11/WrapPybind11Exec.py \
    --module_name mmciflib \
    --config_path ./mmciflib.cfg \
    --output_path ./src \
    --export_json
#