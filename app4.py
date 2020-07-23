import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import collections
import plotly.io as pio
from PIL import Image 
pio.renderers.default = 'browser'

# app = dash.Dash()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 

app.layout = html.Div([
                        html.Div([
                            html.H1('pppp'),
                            html.Aside(id = 'as', children = 'asdnsad'),
                            html.P('oooo')
                        ])
                        
    
])

if __name__ == '__main__':
    app.run_server(debug = True)
