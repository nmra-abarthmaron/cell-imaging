#!/bin/bash

input_dir="/lab/processed-data/221121_45_Gene_KO_Screen/max_projections"
# input_dir="/fsx/processed-data/220929 Mattek 20x SD MIP TIFs/max_projections"
output_dir="/lab/processed-data/221121_45_Gene_KO_Screen/2022-12-03_soma_objects_cellpose"
plugins_dir="/home/ubuntu/CellProfiler-plugins"
cppipe_path='/home/ubuntu/cell-imaging/cellprofiler_pipelines/2022-12-03_soma_objects_cellpose.cppipe'

#conda init /bin/bash
#conda activate cell-imaging-2

cellprofiler -c -r -p "$cppipe_path" -i "$input_dir" -o "$output_dir" --plugins-directory "$plugins_dir"
# cellprofiler -c -r -p $cppipe_path -o $output_dir -i "$input_dir"
echo $input_dir?