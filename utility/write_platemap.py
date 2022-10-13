import pathlib
import pandas as pd

platemap = pd.DataFrame(columns = ['condition', 'filename', 'plate', 'row', 'col'])
exp_path = pathlib.Path('/fsx/processed-data/220929 Mattek 20x SD MIP TIFs/max_projections')

images = pd.Series([x.parts[-1] for x in exp_path.glob('*.tif')])
images = np.sort(images.loc[images.str.contains('561')])

platemap['filename'] = images
platemap['row'] = [x[20:21] for x in images]
platemap['col'] = [x[21:23] for x in images]
platemap['plate'] = 'Plate 1'

platemap.to_csv(exp_path.parent / 'platemap.csv')