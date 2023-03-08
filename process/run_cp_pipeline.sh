#!/bin/bash

input_dir="/lab/raw-data/230227_iN_B3_DIV28_LiveCell/1__2023-02-27T21_51_31-Measurement 5/Images"
# input_dir="/fsx/processed-data/220929 Mattek 20x SD MIP TIFs/max_projections"
output_dir="/lab/processed-data/230227_iN_B3_DIV28_LiveCell/1__2023-02-27T21_51_31-Measurement 5/2023-02-28_soma_objects"
plugins_dir="/home/ubuntu/CellProfiler-plugins"
cppipe_path='/home/ubuntu/cell-imaging/cellprofiler_pipelines/2023-02-28_soma_objects.cppipe'

#conda init /bin/bash
#conda activate cell-imaging-2

cellprofiler -c -r -p "$cppipe_path" -i "$input_dir" -o "$output_dir" --plugins-directory "$plugins_dir"
# cellprofiler -c -r -p $cppipe_path -o $output_dir -i "$input_dir"
echo $input_dir?