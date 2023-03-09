import skimage
import tifffile
import numpy as np
from pathlib import Path
import os

def max_project_PE(data_dir, overwrite_stacks=True):
    """
    Create max_projections from a Perkin Elmer Harmony Export. 

    Parameters
    ----------
    data_dir: pathlib.Path
        Path to PE Export.
    overwrite_stacks: bool, default = True
        Whether or not to remove z-plane images. Default behavior is to remove
        z-section files and replace with max projections. If set to False a 
        new directory called 'MIPs' will be created and 'Images' will be left
        alone.
    """

    input_dir = data_dir / 'Images'
    if overwrite_stacks:
        output_dir = input_dir
    else:
        output_dir = data_dir / 'MIPs'

    # Find common field-of-view (fov) prefixes and channel numbers, using 
    # standardized Harmony nomenclature. 
    fov_prefixes = np.sort(np.unique([f.name[:9] for f in data_dir.glob('*.tiff')]))
    channels = np.sort(np.unique([f.name[13:16] for f in data_dir.glob('*.tiff')]))

    # Load test file to get dimesnions, would be nice to get this from xml
    test_file = [f for f in data_dir.glob('*.tiff')][0]
    tif = skimage.io.imread(test_file)
    img_dims = tif.shape

    for prefix in fov_prefixes:
        for ch in channels:
            
            # Get all filenames associated with a specific fov and channel
            z_section_files = [x.name for x in 
                            data_dir.glob(prefix + '*' + ch +'*')]
            z_section_files = np.sort(z_section_files)

            # Alllocate stack array
            img_stack = np.zeros(
                (z_section_files.shape[0], 
                img_dims[0],
                img_dims[1])
            ).astype('uint16')

            # Load all z-sections within 'stack'
            for i_f, f in enumerate(z_section_files):
                tif = skimage.io.imread(data_dir / f)
                img_stack[i_f, :, :] = tif

            # Max project
            mip = img_stack.max(axis=0)

            # Save results
            if overwrite_stacks:
                skimage.io.imsave(data_dir / z_section_files[0], mip)
                for file in z_section_files[1:]:
                    os.remove(data_dir / file)
            else:
                skimage.io.imsave(data_dir.parents[0] / 'MIPs' / z_section_files[0], mip)
    
def max_project(data_path, save_dir, overwrite=False):
    """
    Max projection function from earlier (pre 2023) experiments. 
    Deprecated
    """

    # Check if max projections have already been created or should be overwritten
    if not save_dir.exists():
        save_dir.mkdir(parents=True)
    elif not overwrite:
        print('Max projections already exist for ' 
              + save_dir.as_posix())
        return
        # raise Exception('Max projections already exist for ' 
        #                 + save_dir.as_posix())

    # Create max projections
    for tif in data_path.glob('*.tif'):

        # Read image (z-stack), pil plugin required bc of ome-tif xml data
        img = skimage.io.imread(tif, plugin='pil')

        # Create max projection
        max_projection = img.max(axis=0)

        # Save max projection in data_path
        fname = tif.name
        skimage.io.imsave(save_dir / fname, max_projection)