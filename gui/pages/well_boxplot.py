from dash import callback, dcc, html, Input, Output
import dash
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy.matlib as np

from process.cp_image_data import cp_image_data, image_stats

dash.register_page(__name__)

measurement = 'Mean_soma_Intensity_MedianIntensity_CellROX'
data, pm = cp_image_data()

data.index = pm['condition']
pm.index = pm['condition']
conditions = pm.index.unique().tolist()
ctrl_cond = ['NT-ctrl']

colorblind = ["#0173B2", "#DE8F05", "#029E73", "#D55E00", "#CC78BC",
            "#CA9161", "#FBAFE4", "#949494", "#ECE133", "#56B4E9"]

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
