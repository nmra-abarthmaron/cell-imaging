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

if __name__ == '__main__':
    app.run_server(debug=True)