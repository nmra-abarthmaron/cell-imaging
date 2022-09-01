"""
Primary entrypoint for running the data-processing pipeline.

"""

import pathlib
import matplotlib.pyplot as plt
from max_project import max_project
from run_cp_pipeline import run_cp_pipeline

# Path for raw image data (z-stack tifs from confocal)
raw_data_path = pathlib.Path(
    '/fsx/raw-data/220811 96w 9 Gene KO /tifs'
)
# Path for saving max projections
mp_data_path = pathlib.Path(
    '/fsx/processed-data/220811 96w 9 Gene KO /max_projections'
)

# Path for cp pipeline
cp_pipeline_path = pathlib.Path(
    '/home/ubuntu/cell-imaging/cellprofiler_pipelines/2022-08-22_soma_objects.cppipe'
)

# Create max projections (if they do not already exist)
max_project(raw_data_path, mp_data_path, overwrite=False)

# Run the cellprofiler pipeline
cp_data_path = run_cp_pipeline(mp_data_path, cp_pipeline_path)

