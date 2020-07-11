import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

colors = {
    'background': '#e0ffff',
    'text': '#7FDBFF'
}


app.layout = html.Div([
    
    # Title Banner
    html.Div([
        html.H2('CHAINS OF RESEARCH'),
        html.Img(src = '../assets/chains.png')
        ], className = 'banner'),

    # Conference Selection Box
    
    html.Div([
        
        html.Content("""
        Chains of Research is an online investigative and analytical tool built by parsing five popular ACM conferences which are particularly relevant for IoT research.
        
        
        
        """, style = {'color' : 'text'}),
        
        
        
        html.Label('Conference Name', style = {'color' : 'text'}),
        dcc.Dropdown(id = 'conf_selection',
        options = [
                {'label': 'MobiCom', 'value' : 'mobicom'},
                {'label' : 'MobiHoc', 'value': 'mobihoc'},
                {'label' : 'SigComm', 'value': 'sigcomm'},
                {'label' : 'IPSN', 'value': 'ipsn'},
                {'label' : 'SenSys', 'value': 'sensys'},
                    ],
                value = 'mobicom'
                        )
    
        
        
        ],style = {'columnCount' : 2})
    
])
#e0ffff

app.css.append_css({
    "external_url":"https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == '__main__':
    app.run_server(debug=True)