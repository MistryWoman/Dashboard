import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import collections

app = dash.Dash()


# creating the years dictionary for dynamic dropdown
#############################################################
ipsn_df = pd.read_csv('data/Clean_Authors/ipsn_authors.csv')

mobicom_df = pd.read_csv('data/Clean_Authors/mobicom_authors.csv')

mobihoc_df = pd.read_csv('data/Clean_Authors/mobihoc_authors.csv')

sigcomm_df = pd.read_csv('data/Clean_Authors/sigcomm_authors.csv')

sensys_df = pd.read_csv('data/Clean_Authors/sensys_authors.csv')

def conf_years(conf, conf_df):
    "Given the conf name and the dataframe for the same returns a list of the years for that conference "
    year_list = list(set(conf_df['Year']))
    year_list.sort()
    
    new_year_list = []
    for year in year_list:
        year = str(conf) + "_" + str(year)
        new_year_list.append(year)
    
    return new_year_list

year_dict = collections.defaultdict(list)

year_dict['ipsn'] = conf_years('ipsn', ipsn_df)

year_dict['mobicom'] = conf_years('mobicom', mobicom_df)

year_dict['mobihoc'] = conf_years('mobihoc', mobihoc_df)

year_dict['sensys'] = conf_years('sensys', sensys_df)

year_dict['sigcomm'] = conf_years('sigcomm', sigcomm_df)
################################################################





years = list(year_dict.keys())
nestedOptions = year_dict[years[0]]

app.layout = html.Div(
    [
        
        # Title Banner
        html.Div([
            html.H2('CHAINS OF RESEARCH'),
            html.Img(src = '../assets/chains.png')
        ], className = 'banner'),
        
        html.Hr(),
        
        # Creating the conference and year selection dropdowns
        html.Div([
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': year, 'value':year} for year in years],
                value = list(year_dict.keys())[0]
                ),
            ],style={'width': '20%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='opt-dropdown',
                ),
            ],style={'width': '20%', 'display': 'inline-block'}
        ),
        
        
        html.Hr(),
        html.Div(id='display-selected')
        
    ]
)

@app.callback(
    dash.dependencies.Output('opt-dropdown', 'options'),
    [dash.dependencies.Input('year-dropdown', 'value')]
)
def update_date_dropdown(year):
    return [{'label': i.split('_')[-1], 'value': i} for i in year_dict[year]]


# @app.callback(
#     [dash.dependencies.Output('top-five-tpc', 'figure'),
#      dash.dependencies.Output('top-five-author', 'figure'),
#      dash.dependencies.Output('middle-tpc', 'figure'),
#      dash.dependencies.Output('middle-author', 'figure'),
#      dash.dependencies.Output('last-five-tpc', 'figure'),
#      dash.dependencies.Output('last-five-author', 'figure')
#     ]
#     [dash.dependencies.Input('opt-dropdown', 'value')])

@app.callback(
    dash.dependencies.Output('display-selected', 'figure'),
    [dash.dependencies.Input('opt-dropdown', 'value')])

def set_display_children(selected_value):
    conf, year = selected_value.split('_')
    tpc_df = pd.read_csv('data/Clean_TPC/' + str(conf) + "_clean.csv")
    df = tpc_df[tpc_df['Year'] == int(year)]
    
    conf_year_dict = collections.Counter(df['University/Organization'])
    uni_count_df = pd.DataFrame(conf_year_dict.items(), columns=['University/Organization', 'Count'])
    uni_count_df = uni_count_df.sort_values(by = ['Count'], ascending = False)
    top_20_percent = len(uni_count_df) * 0.20
    
    final_df = uni_count_df[:top_20_percent]
    
    fig = fig = px.bar(final_df, y = 'University/Organization', x ="Count", hover_data = [], hover_name = 'Name',
                       title = 'Most Influential TPC Members')
    fig.update_yaxes(autorange = 'reversed')
    fig.update_layout(
    title_font_family="Times New Roman",
    title_font_color="blue",
    title_font_size = 40
)
    

    return len(final_df)
    
#     return 'you have selected {} option'.format(conf)



# def display_tpc_authors(selected_value):
#     "Has to return all 6 figures"
    
    
#     return 'you have selected {} option'.format(selected_value)




if __name__ == '__main__':
    app.run_server()

