import pathlib
import pandas as pd
import numpy as np

platemap = pd.DataFrame(columns = ['condition', 'filename', 'plate', 'row', 'col'])
exp_path = pathlib.Path('/fsx/processed-data/220929 CellVis Plastic 20x SD MIP TIFs/max_projections')

images = pd.Series([x.parts[-1] for x in exp_path.glob('*.tif')])
images = np.sort(images.loc[images.str.contains('c3.tif')])

platemap['filename'] = images
platemap['row'] = [x[10] for x in images]
platemap['col'] = [x[11:13] for x in images]
platemap['plate'] = 'Plate 1'

platemap.to_csv(exp_path.parent / 'platemap.csv')