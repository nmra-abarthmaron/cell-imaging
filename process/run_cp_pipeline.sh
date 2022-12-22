#!/bin/bash

input_dir="/lab/raw-data/221214_EA_GenTONIK_SM/max_projections"
# input_dir="/fsx/processed-data/220929 Mattek 20x SD MIP TIFs/max_projections"
output_dir="/lab/processed-data/221214_EA_GenTONIK_SM/2022-12-19_neurite_segment_Emin"
plugins_dir="/home/ubuntu/CellProfiler-plugins"
cppipe_path='/home/ubuntu/cell-imaging/cellprofiler_pipelines/2022-12-19_neurite_segment_Emin.cppipe'

#conda init /bin/bash
#conda activate cell-imaging-2

cellprofiler -c -r -p "$cppipe_path" -i "$input_dir" -o "$output_dir" --plugins-directory "$plugins_dir"
# cellprofiler -c -r -p $cppipe_path -o $output_dir -i "$input_dir"
echo $input_dir?