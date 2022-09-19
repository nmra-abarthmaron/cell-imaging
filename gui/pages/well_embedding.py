from dash import callback, dcc, html, Input, Output
import dash
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import numpy.matlib as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap
from process.cp_image_data import cp_image_data
from process.compile_object_data import compile_object_data

colorblind = ["#0173B2", "#DE8F05", "#029E73", "#D55E00", "#CC78BC",
            "#CA9161", "#FBAFE4", "#949494", "#56B4E9"]


measurement = 'Mean_soma_Intensity_MedianIntensity_CellROX'
# data_path = '/fsx/processed-data/220811 96w 9 Gene KO /2022-08-22_soma_objects/2022-08-22_soma_objects_Image.csv'
data_path = '/fsx/processed-data/220811 96w 9 Gene KO /2022-08-16/soma_image/2022-08-16_soma_image_Image.csv'
# data, pm = cp_image_data(data_path)
data, pm = compile_object_data()

data = data - data.mean(axis=0)
data = data / data.std(axis=0)

# Remove a column (feature) if any values in that col are NA
data = data.drop(columns=data.columns[data.isna().any()].tolist())
pca = PCA(n_components=20, random_state=2)
latent_data = pca.fit_transform(data) # Excluding the no dye controls
reducer = TSNE(n_components=2, learning_rate='auto', init='pca', perplexity=3, random_state=2)
# reducer = umap.UMAP(n_neighbors=5, random_state=4)
embedded_data = reducer.fit_transform(latent_data)
embedded_data = pd.DataFrame(embedded_data, 
                             index = data.index,
                             columns = ['UMAP 1', 'UMAP 2'])
embedded_data['condition'] = pm['condition']

dash.register_page(__name__)

fig = px.scatter(
    embedded_data, 
    x='UMAP 1', 
    y='UMAP 2', 
    color='condition', 
    symbol='condition',
    color_discrete_sequence=colorblind
)
fig.update_traces(marker={'size': 6})
fig.update_layout(
        width=830,
        height=768
)
fig.update_yaxes(automargin=True)
fig.update_xaxes(automargin=True)

layout = html.Div([
    dcc.Graph(id='well-embedding', figure=fig)
])