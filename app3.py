import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import collections

# app = dash.Dash()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 



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


## Describes the layout of the dash board components

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
#         html.Div([
#             html.H2('Lets see the distribution of the most influential universities by exploring the members that make up the top 20 % of TPC and authors published in a given year'),
#              ], className = 'banner_2'),
        
        
        html.Div([
            html.Div([
                html.H3('col1'),
                dcc.Graph(id = 'TOP-20-TPC')
            ], className = 'six columns'),
            
            html.Div([
                html.H3('col2'),
                dcc.Graph(id = 'TOP-20-AUTH')   
            ], className = 'six columns')

        ], className = 'row'),
           
        
#         dcc.Graph(id='TOP-20-TPC'),
#         html.Div(id = 'TOP-20-AUTH'),
#         dcc.Graph(id = 'TOP-20-AUTH'),
        html.Div(id = 'out-of'), 
        
        html.Hr()

        
    ]
)

@app.callback(
    dash.dependencies.Output('opt-dropdown', 'options'),
    [dash.dependencies.Input('year-dropdown', 'value')]
)
def update_date_dropdown(year):
    return [{'label': i.split('_')[-1], 'value': i} for i in year_dict[year]]



@app.callback(
    [dash.dependencies.Output('TOP-20-TPC', 'figure'),
     dash.dependencies.Output('TOP-20-AUTH', 'figure'),
     dash.dependencies.Output('out-of', 'children')],
    [dash.dependencies.Input('opt-dropdown', 'value')])

def set_display_children(selected_value):
    try:
        conf, year = selected_value.split('_')
    except:
        conf, year = 'ipsn', 2000
        
        
    ## Top 20 TPC    
    tpc_df = pd.read_csv('data/Clean_TPC/' + str(conf) + "_clean.csv")
    df = tpc_df[tpc_df['Year'] == int(year)]
    
    conf_year_dict = collections.Counter(df['University/Organization'])
    uni_count_df = pd.DataFrame(conf_year_dict.items(), columns=['University/Organization', 'No_of_members'])
    uni_count_df = uni_count_df.sort_values(by = ['No_of_members'], ascending = False)
    top_20_percent = int(len(uni_count_df) * 0.20)
    
    final_df = uni_count_df[:top_20_percent]
    
    fig = fig = px.bar(final_df, y = 'University/Organization', x ="No_of_members",
                       title = 'TPC top 20 % of ' + str(len(uni_count_df)) + " different universities/organizations)"  )
    fig.update_yaxes(autorange = 'reversed')
    fig.update_layout(
    title_font_family="Times New Roman",
    title_font_color="black",
    title_font_size = 40
    )
    
    
    ## Top 20 Authors
    top_20_uni = set(uni_count_df['University/Organization'])
    authors_df = pd.read_csv('data/Clean_Authors/' + str(conf) + "_authors.csv")
    df1 = authors_df[authors_df['Year'] == int(year)]  
    conf_auth = dict(collections.Counter(df1['University/Organization']))
    
    rank = []
    no_of_authors = []
    for key in conf_auth.keys():
        if key in top_20_uni:
            rank.append('TPC')
            no_of_authors.append(conf_auth[key])
        else:
            rank.append('Other')
            no_of_authors.append(conf_auth[key])
            
    pie_df = pd.DataFrame(list(zip(rank, no_of_authors)), columns = ['Rank', 'No_of_authors'])
    pie = px.pie(pie_df, values = 'No_of_authors', names = 'Rank', title = "Rank wise distribution of no of authors published")
    pie.update_layout(
        title_font_family = "Times New Roman",
        title_font_color = "black",
        title_font_size = 40
    )
        
    
    
    
    ## last line at the bottom
    top_tpc = final_df['No_of_members'].sum()
    tot_tpc = uni_count_df['No_of_members'].sum()
#     try:
#         pc = int(top_tpc /tot_tpc * 100)
#         tot_members_a = "Top 20 % represents " + str(pc) + " % of the total TPC strength "
#     except:
#         tot_members_a = ""

    tot_members_a = list(final_df['University/Organization'])

    
    return fig, pie,  tot_members_a
    
    
    
    





if __name__ == '__main__':
    app.run_server(debug = True)


