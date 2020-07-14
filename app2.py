
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px


import pandas as pd

df = pd.read_csv('data/Clean_TPC/top_ipsn_tpc.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    
    
                        dcc.Dropdown(
                            id='conf-selector',
                            options=[
                                {'label': 'IPSN', 'value': 'ipsn'},
                                {'label': 'MobiCom', 'value': 'mobicom'},
                                {'label': 'MobiHoc', 'value': 'mobihoc'},
                                {'label': 'SenSys', 'value': 'sensys'},
                                {'label': 'SigComm', 'value': 'sigcomm'}
                            ],
                            value='ipsn'
                        ),
    
                        dcc.Dropdown(
                            id = 'year-selector',
                            options = [
                                {'label': ''}
                            ]
                        
                        
                        
                        
                        ),
                        dcc.Graph(id = 'influential-tpc'),
                        
             
    
])


@app.callback(
    Output('influential-tpc', 'figure'),
    [Input('conf-selector', 'value')])

def update_figure(value):
    file_name = 'top_' + str(value) + '_tpc.csv'
    df = pd.read_csv('data/Clean_TPC/' + file_name)
    df = df.sort_values(by = ['No_of_times_as_TPC'], ascending = False)
    top_10 = set()
    names = []
    unis = []
    counts = []
    
    for row_no in range(20):
        name = df['Name'][row_no]
        count = df['No_of_times_as_TPC'][row_no]
        uni = df['University/Organization'][row_no]
        
        if uni not in top_10:
            top_10.add(uni)
            names.append(name)
            unis.append(uni)
            counts.append(count)
            
    new_df = pd.DataFrame(list(zip(names, unis, counts)), columns = ['Name', 'University/Organization', 'No_of_times_as_TPC'])
    new_df = new_df.sort_values(by = ['No_of_times_as_TPC'], ascending = False)
    new_df = new_df[:10]

    
    fig = fig = px.bar(new_df, y = 'University/Organization', x ="No_of_times_as_TPC", hover_data = [], hover_name = 'Name',
                       title = 'Most Influential TPC Members')
    fig.update_yaxes(autorange = 'reversed')
    fig.update_layout(
    title_font_family="Times New Roman",
    title_font_color="blue",
    title_font_size = 40
)
    

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)

