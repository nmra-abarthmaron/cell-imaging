from dash import callback, dcc, html, Input, Output, State, ctx
import dash
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import skimage.io as sio
import pathlib
import pandas as pd
import numpy.matlib as np
from itertools import cycle
import seaborn as sns

dash.register_page(__name__)

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

data.index = pm['condition']
pm.index = pm['condition']
conditions = pm.index.unique().tolist()

# neumora color palette
orange = '#E89377'
green = '#67C478'
purple = '#AAAADD'
blue = '#66CCDD'
colorblind = ["#0173B2", "#DE8F05", "#029E73", "#D55E00", "#CC78BC",
            "#CA9161", "#FBAFE4", "#949494", "#ECE133", "#56B4E9"]
palette = sns.color_palette("husl", pm['condition'].unique().shape[0])

layout = html.Div([

    html.Div([

        dcc.Dropdown(
            value='Mean_soma_Intensity_MedianIntensity_CellROX',
            # value='Mean_soma_AreaShape_Area',
            options=data.columns, id='measurement-dropdown'
        ),
    ], style={'padding': 10, 'flex': 1, 'max-width': 400}),

    dcc.Graph(id='image-boxplots')
])

@callback(
    Output(component_id='image-boxplots', component_property='figure'),
    Input(component_id='measurement-dropdown', component_property='value'),
)
def select_plot_type(measurement):

    # Check if measurement is multi-channel or single-channel
    channel_names = ('LysoSensor', 'CellROX', 'TMRM', 'Syto')
    multi_channels = any([x in measurement for x in channel_names])

    # Return plotting fn
    if multi_channels:
        return update_multi_ch_fig(measurement, channel_names)
    else:
        return update_single_ch_fig(measurement)


def update_multi_ch_fig(measurement, ch_names):
    html.Br(),
    n_rows = 2
    n_cols = 2
    fig = make_subplots(rows=2, cols=2, subplot_titles=ch_names)

    ch = ch_names[np.where([x in measurement for x in ch_names])[0][0]]

    # Give it a better name

    for i_ch in range(len(ch_names)):
        
        m = measurement.replace(ch, ch_names[i_ch])
        subplot_inds = np.unravel_index(i_ch, [n_rows, n_cols])

        for i_cond in range(len(conditions)):
            bar_data = data[m].loc[conditions[i_cond]]
            fig.add_trace(
                go.Box(
                    y=bar_data, 
                    boxpoints='all', pointpos=0, jitter=0.5, 
                    line={'color': '#444444', 'width': 1.5},
                    marker={'color': '#666666', 'size': 4}, 
                    # fillcolor= 'rgb' + str(palette[i_cond]),
                    fillcolor= colorblind[i_cond % len(colorblind)]
                ),
                row=subplot_inds[0]+1, col=subplot_inds[1]+1
            )

    fig.update_layout(
        width=1280,
        height=768,
        showlegend=False,
        xaxis1 = dict(
            tickmode = 'array',
            tickvals = np.arange(len(conditions)),
            ticktext = conditions
        ),
        xaxis2 = dict(
            tickmode = 'array',
            tickvals = np.arange(len(conditions)),
            ticktext = conditions
        ),
        xaxis3 = dict(
            tickmode = 'array',
            tickvals = np.arange(len(conditions)),
            ticktext = conditions
        ),
        xaxis4 = dict(
            tickmode = 'array',
            tickvals = np.arange(len(conditions)),
            ticktext = conditions
        )
    )
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    return fig

def update_single_ch_fig(measurement):
    fig = go.Figure()
    for i_cond in range(len(conditions)):
        bar_data = data[measurement].loc[conditions[i_cond]]
        fig.add_trace(
            go.Box(
                y=bar_data,
                boxpoints='all', pointpos=0, jitter=0.5, 
                line={'color': '#444444', 'width': 2},
                marker={'color': '#555555', 'size': 6}, 
                # fillcolor= 'rgb' + str(palette[i_cond]),
                fillcolor=  colorblind[i_cond % len(colorblind)]

            )
        )
    # fig = px.box(x=pm['condition'], y=data[measurement],)
    fig.update_layout(
        width=1024,
        height=512,
        showlegend=False,
        xaxis = dict(
            tickmode = 'array',
            tickvals = np.arange(len(conditions)),
            ticktext = conditions
        )
    )
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)
    return fig
