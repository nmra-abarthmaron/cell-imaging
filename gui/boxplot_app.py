from dash import Dash, dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go
import plotly.express as px
import skimage.io as sio
import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import plotly.matplotlylib as pplt

app = Dash(__name__)

img_path = ('/fsx/processed-data/220811 96w 9 Gene KO /2022-08-22_soma_objects/soma_outlines/Plate 2 20x SD_B08_561 SD.tiff')
app.layout = html.Div([
    dcc.Dropdown(value=img_path, id='image-dropdown'),
    dcc.Graph(id='test')
])

@app.callback(
    Output(component_id='test', component_property='figure'),
    Input(component_id='image-dropdown', component_property='value'),
)
def update_image(img_path):
    img = sio.imread(img_path)
    # fig = plt.imshow(img)
    fig = px.imshow(img)
    renderer = pplt.PlotlyRenderer(fig)
    exporter = pplt.Exporter(renderer)
    exporter.run(fig)
    # plt.show()
    return fig
app.layout = html.Div([

    html.Div([
            html.Br(),
            html.Label('Experiment:'),
            dcc.Dropdown(
                exps,
                '2022-08-22_soma_objects',
                id='experiment-dropdown'
            ),

            html.Br(),
            html.Label('Condition:'),
            dcc.Dropdown(value=img_df.index[0], id='condition-dropdown'),

            html.Br(),
            html.Label('Image:'),
            dcc.Dropdown(id='image-dropdown'),

            html.Br(),
            html.Button(id='prev-button', n_clicks=0, children='Prev image'),
            html.Button(id='next-button', n_clicks=0, children='Next image'),

            html.Br(),
            html.Br(),
            html.Label('Overlay soma outlines?'),
            dcc.RadioItems(
                id='overlay-outlines', 
                # options={True : 'Yes', False : 'No'},
                options=['Yes', 'No'],
                value = 'Yes'
                ),

            html.Br(),
            html.Label('Set max. intensity:'),
            dcc.Slider(0, 1,
                    value=1,
                    marks = {0: 'min', 1 : 'max'},
                    id='img-max-slider'
            ),            
            
        ], 
        style={'padding': 10, 'flex': 1, 'max-width': 300}
    ),
    
    dcc.Graph(id='soma-outlines')

], style={'display': 'flex', 'flex-direction': 'row'})


if __name__ == '__main__':
    app.run_server(debug=True)