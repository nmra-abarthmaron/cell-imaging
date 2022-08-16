"""
Primary entrypoint for running the data-processing pipeline.

"""

import pathlib
import skimage.io
import matplotlib.pyplot as plt
import os

# Path for raw image data (z-stack tifs from confocal)
data_path = pathlib.Path(
    '/fsx/raw-data/220810 96w Dye Chem Controls/tifs'
)
# Path for saving max projections
save_dir = pathlib.Path(
    '/fsx/processed-data/220810 96w Dye Chem Controls/max_projections'
)

# Check if max projections have already been created
if not save_dir.exists():
    save_dir.mkdir(parents=True)

# Create max projections
for tif in data_path.glob('*.tif'):

    # Read image (z-stack), pil plugin required bc of ome-tif xml data
    img = skimage.io.imread(tif, plugin='pil')

    # Create max projection
    max_projection = img.max(axis=0)

    # Save max projection in data_path
    fname = tif.name
    skimage.io.imsave(save_dir / fname, max_projection)
