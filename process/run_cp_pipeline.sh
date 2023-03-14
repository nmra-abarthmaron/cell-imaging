#!/bin/bash

input_dir="/lab/raw-data/ALS0006_KO01_TDP43_20X/ALS0006_KO01_TDP43_20X_01__2023-03-08T11_11_56-Measurement 1/Images"
# input_dir="/fsx/processed-data/220929 Mattek 20x SD MIP TIFs/max_projections"
output_dir="/lab/processed-data/ALS0006_KO01_TDP43_20X/ALS0006_KO01_TDP43_20X_01__2023-03-08T11_11_56-Measurement 1/2023-02-17_tdp43seg_tdp-43"
plugins_dir="/home/ubuntu/CellProfiler-plugins"
cppipe_path='/home/ubuntu/cell-imaging/cellprofiler_pipelines/2023-02-17_tdp43seg_tdp-43.cppipe'

#conda init /bin/bash
#conda activate cell-imaging-2

cellprofiler -c -r -p "$cppipe_path" -i "$input_dir" -o "$output_dir" --plugins-directory "$plugins_dir"
# cellprofiler -c -r -p $cppipe_path -o $output_dir -i "$input_dir"
echo $input_dir?