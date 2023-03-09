#!/bin/bash

input_dir="/lab/raw-data/20230223_GBA_EG_probetest_HeLa/20230223v3__2023-02-23T12_29_12-Measurement 1/Images"
# input_dir="/fsx/processed-data/220929 Mattek 20x SD MIP TIFs/max_projections"
output_dir="/lab/processed-data/20230223_GBA_EG_probetest_HeLa/20230223v3__2023-02-23T12_29_12-Measurement 1/2023-03-08_GBA_analysis"
plugins_dir="/home/ubuntu/CellProfiler-plugins"
cppipe_path='/home/ubuntu/cell-imaging/cellprofiler_pipelines/2023-03-08_GBA_analysis.cppipe'

#conda init /bin/bash
#conda activate cell-imaging-2

cellprofiler -c -r -p "$cppipe_path" -i "$input_dir" -o "$output_dir" --plugins-directory "$plugins_dir"
# cellprofiler -c -r -p $cppipe_path -o $output_dir -i "$input_dir"
echo $input_dir?