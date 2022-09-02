from dash import Dash, dcc, html, Input, Output, State, ctx
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import skimage.io as sio
import pathlib
import pandas as pd
import numpy.matlib as np

app = Dash(__name__)

# neumora color palette
orange = '#E89377'
green = '#67C478'
purple = '#AAAADD'
blue = '#66CCDD'

# Load processed cellprofiler data from csv
data_path = '/fsx/processed-data/220811 96w 9 Gene KO /2022-08-22_soma_objects/2022-08-22_soma_objects_Image.csv'
data = pd.read_csv(data_path)

# Set index to well name
data.index = data['FileName_TMRM']

# Remove unwanted columns
drop_columns = pd.read_csv('/fsx/processed-data/220811 96w 9 Gene KO /2022-08-22_soma_objects/2022-08-30_soma_objects_image_column_drop_list.csv', header=None, dtype=str)
drop_columns = np.array(drop_columns).astype(str).flatten()
for col in drop_columns:
    data = data.drop(data.columns[data.columns.str.contains(col)], axis=1)

# Load platemap / well conditions
pm = pd.read_csv('/fsx/processed-data/220811 96w 9 Gene KO /2022-08-22_soma_objects/soma_outlines/220811_well_conditions.csv', index_col='filename')# Add condition labels to well dataframe
# data['conditions'] = pm.reindex(data.index)
data = data.reindex(pm.index)

app.layout = html.Div([

    html.Div([

        dcc.Dropdown(
            value='Mean_soma_Intensity_MedianIntensity_CellROX',
            options=data.columns, id='measurement-dropdown'
        ),
    ], style={'padding': 10, 'flex': 1, 'max-width': 400}),

    dcc.Graph(id='test')
])

@app.callback(
    Output(component_id='test', component_property='figure'),
    Input(component_id='measurement-dropdown', component_property='value'),
)
def select_plot_type(measurement):

    # Check if measurement is multi-channel or single-channel
    channel_names = (' LysoSensor', 'CellROX', 'TMRM', 'Syto')
    multi_channels = any([x in measurement for x in channel_names])

    # Return plotting fn
    if multi_channels:
        return update_multi_ch_fig(measurement, channel_names)
    else:
        return update_single_ch_fig(measurement)


def update_multi_ch_fig(measurement, ch_names):
    html.Br(),
    fig = make_subplots(rows=2, cols=2, subplot_titles=ch_names)

    ch = ch_names[np.where([x in measurement for x in ch_names])[0][0]]

    # Give it a better name
    m = measurement.replace(ch, 'LysoSensor')
    fig.add_trace(
        go.Box(
            x=pm['condition'], y=data[m], 
            boxpoints='all', pointpos=0, fillcolor=orange, jitter=0.5,
            marker={'color': '#666666', 'size': 5}, line={'color': orange}
        ),
        row=1, col=1
    )
    m = measurement.replace(ch, 'CellROX')
    fig.add_trace(
        go.Box(
            x=pm['condition'], y=data[m], 
            boxpoints='all', pointpos=0, fillcolor=green, jitter=0.5,
            marker={'color': '#666666', 'size': 5}, line={'color': green}
        ), 
        row=1, col=2
    )
    m = measurement.replace(ch, 'TMRM')
    fig.add_trace(
        go.Box(
            x=pm['condition'], y=data[m], 
            boxpoints='all', pointpos=0, fillcolor=purple, jitter=0.5,
            marker={'color': '#666666', 'size': 5}, line={'color': purple}
        ), 
        row=2, col=1
    )
    m = measurement.replace(ch, 'Syto')
    fig.add_trace(
        go.Box(
            x=pm['condition'], y=data[m], 
            boxpoints='all', pointpos=0, fillcolor=blue, jitter=0.5,
            marker={'color': '#666666', 'size': 5}, line={'color': blue}
        ), 
        row=2, col=2
    )

    fig.update_layout(
        width=1280,
        height=768
    )
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)
    return fig

def update_single_ch_fig(measurement):
    fig = px.box(x=pm['condition'], y=data[measurement],)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)