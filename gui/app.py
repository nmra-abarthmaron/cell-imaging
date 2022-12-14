from dash import Dash, dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go
import skimage.io as sio
import pathlib
import pandas as pd

app = Dash(__name__)

# img = sio.imread('/fsx/processed-data/220811 96w 9 Gene KO /2022-08-22_soma_objects/soma_outlines/Plate 2 20x SD_B08_561 SD.tiff')
exp_path = pathlib.Path('/fsx/processed-data/220811 96w 9 Gene KO /')
exps = [x.name for x in exp_path.iterdir() if x.is_dir()]
img_path = pathlib.Path(
    '/fsx/processed-data/220811 96w 9 Gene KO /2022-08-22_soma_objects/soma_outlines'
)
img_df = pd.read_csv(img_path / '220811_well_conditions.csv', index_col='condition')

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

# Set condition name options in image dropdown, given an experiment
@app.callback(
    Output('condition-dropdown', 'options'),
    Input('experiment-dropdown', 'value')
)
def set_image_options(condition):
    return img_df.index.unique()

# Set image name options in image dropdown, given a well condition
@app.callback(
    Output('image-dropdown', 'options'),
    Input('condition-dropdown', 'value')
)
def set_image_options(condition):
    return img_df.loc[condition].filename

# Set image name value in the image dropdown menu, contextually.
# Contexts - default, next button, prev button
@app.callback(
    Output('image-dropdown', 'value'),
    Input('next-button', 'n_clicks'),
    Input('prev-button', 'n_clicks'),
    Input('image-dropdown', 'options'),
    State('image-dropdown', 'value'),
    prevent_initial_call=True
)
def update_image_name(_0, _1, img_options, img_name):
    triggered_id = ctx.triggered_id
    if triggered_id == 'image-dropdown':
        return set_default_img(img_options)
    if triggered_id == 'next-button':
        return next_image(img_options, img_name)
    if triggered_id == 'prev-button':
        return prev_image(img_options, img_name)

def set_default_img(img_options):
    return img_options[0]

def next_image(img_options, img_name):
    i_img = img_options.index(img_name)
    i_img += 1
    i_img = i_img % len(img_options)
    return img_options[i_img]

def prev_image(img_options, img_name):
    i_img = img_options.index(img_name)
    i_img -= 1
    i_img = i_img % len(img_options)
    return img_options[i_img]

# Take image name, load images, and plot
@app.callback(
    Output(component_id='soma-outlines', component_property='figure'),
    Input(component_id='image-dropdown', component_property='value'),
    Input('overlay-outlines', 'value'),
    Input('img-max-slider', 'value')
    # Input(component_id='next-image-button', component_property='n_clicks')
)
def update_image(img_name, soma_outlines, max_intensity):

    # Load outline file
    # img_name = pd.read_json(img_name)
    outline_name = img_name + 'f'   # because cp saves them as 'tiff' not 'tif'
    outline = sio.imread(img_path / outline_name)
    outline = outline.astype(object)
    outline[outline == 0] = None

    # This is kinda a hack, should be done with the cp image csv
    ch_names = [405, 488, 561, 647]
    img = sio.imread(img_path.parent.parent /'max_projections'/ img_name.replace('tif', 'tif'))

    # Set max intensity
    img[img > (img.max() * max_intensity)] = img.max() * max_intensity

    fig = go.Figure()
    fig.add_trace(go.Heatmap(z=img, colorscale=['#000000', '#FFFFFF'], 
                             showscale=False))
    if soma_outlines == 'Yes':
        fig.add_trace(go.Heatmap(z=outline, colorscale=['#FFFFFF', '#00FF00'], showscale=False))
    
    # fig = px.imshow(img, color_continuous_scale=['#000000', '#FFFFFF'])
    # fig.add_trace(px.imshow(img, color_continuous_scale=['#000000', '#00FF00']).data[0])
    

    fig.update_layout(
        xaxis={'showticklabels': False},
        yaxis={'showticklabels': False}, 
        width=1024, height=1024
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
