import skimage.io

def max_project(data_path, save_dir, overwrite=False):

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