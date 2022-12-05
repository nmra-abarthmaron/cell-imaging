from dash import callback, dcc, html, Input, Output, State
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
import pathlib

colorblind = ["#0173B2", "#DE8F05", "#029E73", "#D55E00", "#CC78BC",
            "#CA9161", "#FBAFE4", "#949494", "#56B4E9"]


measurement = 'Mean_soma_Intensity_MedianIntensity_CellROX'
exp_path = pathlib.Path('/lab/processed-data')
exps = np.array([x.name for x in exp_path.iterdir() if x.is_dir()])
drop_columns = pd.read_csv('/lab/processed-data/220811 96w 9 Gene KO /2022-08-22_soma_objects/2022-08-30_soma_objects_soma_column_drop_list.csv', header=None, dtype=str)
# data, pm = cp_image_data(data_path)
# data, pm = compile_object_data(data_path, pm, drop_columns)

dash.register_page(__name__)



layout = html.Div([
    html.Label('Experiment:'),
    dcc.Dropdown(
        exps,
        '220811 96w 9 Gene KO ',
        id='we-experiment-dropdown'
    ),

    html.Label('Analysis:'),
    dcc.Dropdown(
        value='2022-10-11_soma_objects',
        id='we-analysis-dropdown'
    ),
    dcc.Graph(id='well-embedding')
])

# Set options in analysis dropdown, given an experiment name
@callback(
    Output('we-analysis-dropdown', 'options'),
    Input('we-experiment-dropdown', 'value')
)
def set_analysis_options(exp_name):
    sub_dirs = (exp_path / exps[exps == exp_name])[0].iterdir()
    analysis_opts = [x.parts[-1] for x in sub_dirs]
    return analysis_opts

@callback(
    Output(component_id='well-embedding', component_property='figure'),
    Input('we-analysis-dropdown', 'value'),
    State('we-experiment-dropdown', 'value')
)
def plot_embedding(analysis_name, exp_name):
    pm = pd.read_csv(exp_path / exp_name / 'platemap.csv')
    data_path = exp_path / exp_name / analysis_name /  (analysis_name + '_soma.csv')
    embedded_data = compile_object_data(data_path, pm, drop_columns)

    fig = px.scatter(
        embedded_data, 
        x='tSNE 1', 
        y='tSNE 2', 
        color='condition', 
        symbol='condition',
        color_discrete_sequence=colorblind
    )
    fig.update_traces(marker={'size': 8})
    fig.update_layout(
            width=830,
            height=768,
            font = dict(size=20)
    )
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    return fig