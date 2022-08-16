"""
Primary entrypoint for running the data-processing pipeline.

"""

import pathlib
import skimage.io
import matplotlib.pyplot as plt

# Path for raw image data (z-stack tifs from confocal)
data_path = pathlib.Path(
    '/shared-data/research/cell-imaging/220811 96w 9 Gene KO /tifs'
)

# Check if max projections have already been created
if not data_path.exists():
    data_path.mkdir()

    # Create max projections
    for tif in data_path.glob('*.tif'):

        # Read image (z-stack), pil plugin required bc of ome-tif xml data
        img = skimage.io.imread(tif, plugin='pil')

        # Create max projection
        max_projection = img.max(axis=0)

        # Save max projection in data_path
        fname = tif.name
        save_dir = data_path.parent / 'max_projections'
        skimage.io.imsave(save_dir / fname, max_projection)
