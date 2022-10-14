from dash import callback, dcc, html, Input, Output, State
import dash
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy.matlib as np
import pathlib 

from process.cp_image_data import cp_image_data, image_stats

dash.register_page(__name__)

drop_columns = pd.read_csv('/fsx/processed-data/220811 96w 9 Gene KO /2022-08-22_soma_objects/2022-08-30_soma_objects_image_column_drop_list.csv', header=None, dtype=str)
exp_path = pathlib.Path('/fsx/processed-data')
exps = np.array([x.name for x in exp_path.iterdir() if x.is_dir()])

# Load platemap / well conditions
# pm = pd.read_csv('/fsx/processed-data/220929 Mattek 20x SD MIP TIFs/platemap.csv', index_col='filename')# Add condition labels to well dataframe
# pm = pd.read_csv('/fsx/processed-data/220811 96w 9 Gene KO /platemap.csv', index_col='filename')# Add condition labels to well dataframe

measurement = 'Mean_soma_Intensity_MedianIntensity_CellROX'
# data_path = '/fsx/processed-data/220929 Mattek 20x SD MIP TIFs/2022-10-11_soma_objects/2022-10-11_soma_objects_Image.csv'
# csv_name = '2022-10-11_soma_objects_Image.csv'
# data_path = '/fsx/processed-data/220811 96w 9 Gene KO /2022-10-11_soma_objects/2022-10-11_soma_objects_Image.csv'
# data, pm = cp_image_data(data_path, pm, drop_columns)
ctrl_cond = ['ctrl']

colorblind = ["#0173B2", "#DE8F05", "#029E73", "#D55E00", "#CC78BC",
            "#CA9161", "#FBAFE4", "#949494", "#ECE133", "#56B4E9"]

layout = html.Div([

    html.Div([

        html.Label('Experiment:'),
        dcc.Dropdown(
            exps,
            '220811 96w 9 Gene KO ',
            id='wb-experiment-dropdown'
        ),

        html.Label('Analysis:'),
        dcc.Dropdown(
            value='2022-10-11_soma_objects',
            id='wb-analysis-dropdown'
        ),
        html.Label('Measurement:'),
        dcc.Dropdown(
            value='Mean_soma_Intensity_MedianIntensity_CellROX',
            # value='Intensity_MedianIntensity_CellROX',
            id='measurement-dropdown'
        ),
    ], style={'padding': 10, 'flex': 1, 'max-width': 400}),

    dcc.Graph(id='image-boxplots')
])

# Set options in analysis dropdown, given an experiment name
@callback(
    Output('wb-analysis-dropdown', 'options'),
    Input('wb-experiment-dropdown', 'value')
)
def set_analysis_options(exp_name):
    sub_dirs = (exp_path / exps[exps == exp_name])[0].iterdir()
    analysis_opts = [x.parts[-1] for x in sub_dirs]
    return analysis_opts

# Set options in measurement dropdown, given an analysis name and experiment name
@callback(
    Output('measurement-dropdown', 'options'),
    Input('wb-analysis-dropdown', 'value'),
    State('wb-experiment-dropdown', 'value')
)
def set_measurement_options(analysis_name, exp_name):
    # Load data
    pm = pd.read_csv(exp_path / exp_name / 'platemap.csv')
    data_path = exp_path / exp_name / analysis_name / (analysis_name + '_Image.csv')
    data, pm = cp_image_data(data_path, pm, drop_columns)
    return data.columns

# Select between multi ch and single ch figure. 
@callback(
    Output(component_id='image-boxplots', component_property='figure'),
    Input(component_id='measurement-dropdown', component_property='value'),
    State('wb-experiment-dropdown', 'value'),
    State('wb-analysis-dropdown', 'value')
)
def select_plot_type(measurement, exp_name, analysis_name):

    # Check if measurement is multi-channel or single-channel
    channel_names = ('LysoSensor', 'CellROX', 'TMRM', 'Syto')
    multi_channels = any([x in measurement for x in channel_names])

    # Load data
    pm = pd.read_csv(exp_path / exp_name / 'platemap.csv')
    data_path = exp_path / exp_name / analysis_name / (analysis_name + '_Image.csv')
    data, pm = cp_image_data(data_path, pm, drop_columns)
    data.index = pm['condition']
    pm.index = pm['condition']
    conditions = pm.index.unique().tolist()

    # Return plotting fn
    if multi_channels:
        return update_multi_ch_fig(data, pm, measurement, channel_names)
    else:
        return update_single_ch_fig(data, pm, measurement)


def update_multi_ch_fig(data, pm, measurement, ch_names):
    html.Br(),
    n_rows = 2
    n_cols = 2
    fig = make_subplots(rows=2, cols=2, subplot_titles=ch_names)

    ch = ch_names[np.where([x in measurement for x in ch_names])[0][0]]
    conditions = pm.index.unique().tolist()

    # Give it a better name

    for i_ch in range(len(ch_names)):
        
        m = measurement.replace(ch, ch_names[i_ch])
        subplot_inds = np.unravel_index(i_ch, [n_rows, n_cols])

        p_vals, p_adj, h  = image_stats(data, m, conditions, ctrl_cond)
        y_data_max = data[m].max()

        # Draw boxplots, one condition at a time to use diff colors
        for i_cond in range(len(conditions)):
            bar_data = data[m].loc[conditions[i_cond]]
            fig.add_trace(
                go.Box(
                    x=i_cond * np.array(np.ones(bar_data.shape[0])).flatten(),
                    y=bar_data, 
                    boxpoints='all', pointpos=0, jitter=0.5, 
                    line={'color': '#444444', 'width': 1.5},
                    marker={'color': '#666666', 'size': 4}, 
                    # fillcolor= 'rgb' + str(palette[i_cond]),
                    fillcolor= colorblind[i_cond % len(colorblind)]
                ),
                row=subplot_inds[0]+1, col=subplot_inds[1]+1
            )

            # Add a star if condiiton is significantly different from ctrl
            if [conditions[i_cond]] != ctrl_cond: 
                if h.loc[conditions[i_cond]].bool():
                    fig.add_trace(
                        go.Scatter(
                            y=[y_data_max*1.15],
                            x=[i_cond],line=None,
                            marker={'color': '#000000', 'size': 8},
                            marker_line_width=1.5,
                            marker_symbol='asterisk'
                        ),
                        row=subplot_inds[0]+1, col=subplot_inds[1]+1
                    )


    fig.update_layout(
        width=1280,
        height=768,
        showlegend=False,
        yaxis1_title="Normalized Intensity",
        yaxis2_title="Normalized Intensity",
        yaxis3_title="Normalized Intensity",
        yaxis4_title="Normalized Intensity",
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

def update_single_ch_fig(data, pm, measurement):
    
    conditions = pm.index.unique().tolist()

    p_vals, p_adj, h  = image_stats(data, measurement, conditions, ctrl_cond)
    y_data_max = data[measurement].max()

    fig = go.Figure()
    for i_cond in range(len(conditions)):
        bar_data = data[measurement].loc[conditions[i_cond]]
        fig.add_trace(
            go.Box(
                x=i_cond * np.array(np.ones(bar_data.shape[0])).flatten(),
                y=bar_data,
                boxpoints='all', pointpos=0, jitter=0.5, 
                line={'color': '#444444', 'width': 2},
                marker={'color': '#555555', 'size': 6}, 
                fillcolor=  colorblind[i_cond % len(colorblind)]

            )
        )
        # Add a star if condiiton is significantly different from ctrl
        if [conditions[i_cond]] != ctrl_cond: 
            if h.loc[conditions[i_cond]].bool():
                fig.add_trace(
                    go.Scatter(
                        y=[y_data_max*1.15],
                        x=[i_cond],line=None,
                        marker={'color': '#000000', 'size': 12},
                        marker_line_width=2,
                        marker_symbol='asterisk'
                    )
                )

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
