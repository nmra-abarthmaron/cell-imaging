#!/bin/bash

input_dir="/lab/raw-data/TDP43_ALS0013_NGN2_KO1_20x_DIV25_2023-04-11/TDP43_ALS0013_NGN2_KO1_20x_DIV25_2023-04-11__2023-04-11T17_22_35-Measurement 1/Images"
# input_dir="/fsx/processed-data/220929 Mattek 20x SD MIP TIFs/max_projections"
output_dir="/lab/processed-data/TDP43_ALS0013_NGN2_KO1_20x_DIV25_2023-04-11/TDP43_ALS0013_NGN2_KO1_20x_DIV25_2023-04-11__2023-04-11T17_22_35-Measurement 1/2023-04-11_cellpose_tdp-43"
plugins_dir="/home/ubuntu/CellProfiler-plugins"
cppipe_path='/home/ubuntu/cell-imaging/cellprofiler_pipelines/2023-04-11_cellpose_tdp-43.cppipe'

#conda init /bin/bash
#conda activate cell-imaging-2

cellprofiler -c -r -p "$cppipe_path" -i "$input_dir" -o "$output_dir" --plugins-directory "$plugins_dir"
# cellprofiler -c -r -p $cppipe_path -o $output_dir -i "$input_dir"
echo $input_dir?