import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

# assume you have a "wide-form" data frame with no index
# see https://plotly.com/python/wide-form/ for more options

app.layout = html.Div([
    html.H2('CHAINS OF RESEARCH'),
    html.Img(src = '../assets/chains.png')
], className = 'banner')





# app.css.append_css({
#     "external_url":"https://codepen.io/chriddyp/pen/bWLwgP.css"
# })

if __name__ == '__main__':
    app.run_server(debug=True)