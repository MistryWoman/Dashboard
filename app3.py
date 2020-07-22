import dash
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
                id='conf-dropdown',
                options=[{'label': year, 'value':year} for year in years],
                value = list(year_dict.keys())[0]
                ),
            ],style={'width': '20%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='year-dropdown',
                value = 'ipsn_2007'
                ),
            ],style={'width': '20%', 'display': 'inline-block'}
        ),
        
        
        html.Hr(),
        
        ## Adding graphs
        html.Div([
            html.Div([
                html.H3('col1'),
                dcc.Graph(id = 'TOP-20-TPC')
            ], className = 'six columns'),
            
            html.Div([
                html.H3('col2'),
                dcc.Graph(id = 'TOP-20-AUTH')   
            ], className = 'three columns'),
            
            html.Div([
                html.H3('col3'),
                dcc.Graph(id = 'Published-TPC')   
            ], className = 'three columns')

        ], className = 'row'),
           
        
        html.Div(id = 'out-of'), 
        
        html.Hr(),

        ### Creating slider for no of years given the conference
        
        html.H3('Lets compare TPC Retention amongst the conferences'),
        
        html.Div([
        
                    html.Div([

                        # create all the radio buttons for conf selection
                        
                        dcc.Checklist(
                            id = 'conf-checklist',
                            options=[
                                {'label': 'IPSN', 'value': 'ipsn'},
                                {'label': 'MobiHoc', 'value': 'mobihoc'},
                                {'label': 'MobiCom', 'value': 'mobicom'},
                                {'label' : 'SenSys', 'value' : 'sensys'},
                                {'label' : 'SigComm', 'value' : 'sigcomm'}
                            ],value=['ipsn', 'mobihoc'], labelStyle={'display': 'inline-block'}),
                    ], style={'width': '40%', 'display': 'inline-block'}),

                    html.Div([
            
                        dcc.Dropdown(
                            id='uni-auth-selection',
                            options = [{'label' : 'University/Organization', 'value' : 'university'},
                                       {'label' : 'Individual TPC member', 'value' : 'tpc'}],
                            value = 'university'
                           )
#                          html.H3('Choose between university and TPC composition')
                        ],style={'width': '20%', 'display': 'inline-block'}
                        
                    )]),
        
        dcc.Graph(id = 'tpc_retention'),
        html.H2('Bubble chart'),
        dcc.Dropdown(
                id='conf-dropdown-bubble',
                options=[{'label': year, 'value':year} for year in years],
                value = list(year_dict.keys())[0]
                ),
        
        dcc.Graph(id = 'bubble-chart'),
        
        html.Div([
            html.Img(id = 'wordcloud')
        ])
                
        
        
     #### this is the end of layout
])

@app.callback(
    dash.dependencies.Output('year-dropdown', 'options'),
    [dash.dependencies.Input('conf-dropdown', 'value')]
)
        
def update_date_dropdown(year):
    return [{'label': i.split('_')[-1], 'value': i} for i in year_dict[year]]



@app.callback(
    [dash.dependencies.Output('TOP-20-TPC', 'figure'),
     dash.dependencies.Output('TOP-20-AUTH', 'figure'),
     dash.dependencies.Output('Published-TPC', 'figure'),
     dash.dependencies.Output('out-of', 'children')],
    [dash.dependencies.Input('year-dropdown', 'value')])

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
            rank.append('TPC University')
            no_of_authors.append(conf_auth[key])
        else:
            rank.append('Other University')
            no_of_authors.append(conf_auth[key])
            
    pie_df = pd.DataFrame(list(zip(rank, no_of_authors)), columns = ['Rank', 'No_of_authors'])
    tpc_uni_pie = px.pie(pie_df, values = 'No_of_authors', names = 'Rank', title = "Rank wise distribution of no of authors published")
    tpc_uni_pie.update_layout(
        title_font_family = "Times New Roman",
        title_font_color = "black",
        title_font_size = 40
    )
        
    
    ## No of publications by TPC members
    # df is the dataframe containing TPC info for selected year
    # df1 is the dataframe containing author info for the selected year
    
    authors = set(df1['Author_Name'])
    tpc = set(df['Name'])
    
    
    published_tpc = authors.intersection(tpc)
    not_published_tpc = len(tpc) - len(published_tpc)
    
    status = ['Published TPC', 'Not Published TPC']
    count = [len(published_tpc), not_published_tpc]
    
    
    
    
#     tpc_auth = authors.intersection(tpc)
    
#     other_auth = authors - tpc
    
#     status = ['TPC Member', 'Other']
#     count = [len(tpc_auth), len(other_auth)]
    
    tpc_overlap = pd.DataFrame(list(zip(status, count)), columns = ['status', 'count'])
    
    tpc_auth_pie = go.Figure(data=[go.Pie(labels = tpc_overlap['status'], values = tpc_overlap['count'], hole=.3, title = "TPC Member and author overlap")])
    
#     tpc_auth_pie = px.pie(tpc_overlap, values = 'count', names = 'status', title = "TPC Author overlap")
    tpc_auth_pie.update_layout(
        title_font_family = "Times New Roman",
        title_font_color = "black",
        title_font_size = 40
    )
    
    
    
    
    ## last line at the bottom
    top_tpc = final_df['No_of_members'].sum()
    tot_tpc = uni_count_df['No_of_members'].sum()
    try:
        pc = int(top_tpc /tot_tpc * 100)
        tot_members_a = "Top 20 % represents " + str(pc) + " % of the total TPC strength "
    except:
        tot_members_a = ""

    
    return fig, tpc_uni_pie, tpc_auth_pie , tot_members_a
    
    
    
@app.callback(
    dash.dependencies.Output('tpc_retention', 'figure'),
    [dash.dependencies.Input('conf-checklist', 'value'),
     dash.dependencies.Input('uni-auth-selection', 'value')])

def tpc_retention(conf_list, uni_auth):
    "This creates the tpc retention graph for the selected universities"
    
    if uni_auth == 'university':
        retention_df = pd.read_csv('data/retention_uni.csv')
        final_df = retention_df.loc[retention_df['Name'].isin(conf_list)]
        
        groups = final_df.groupby(by = 'Name')
        data = []
        
        for group, dataframe in groups:
                dataframe = dataframe.sort_values(by=['Year'])
                trace = go.Scatter(x=dataframe.Year.tolist(), 
                                   y= list(dataframe['Retention(%over2yrs)']),
#                                    marker=dict(color=colors[len(data)]),
                                   name=group)
                data.append(trace)

                layout =  go.Layout(xaxis={'title': 'Year'},
                                    yaxis={'title': 'Retention Percentage over 2 years'},
                                    margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                                    hovermode='closest')

                figure = go.Figure(data=data, layout=layout)  
#                 figure.show()

        
        
        
        
        
    if uni_auth == 'tpc':
        retention_df = pd.read_csv('data/retention_authors.csv')
        final_df = retention_df.loc[retention_df['Name'].isin(conf_list)]
        
        groups = final_df.groupby(by = 'Name')
        data = []
        
        for group, dataframe in groups:
                dataframe = dataframe.sort_values(by=['Year'])
                trace = go.Scatter(x=dataframe.Year.tolist(), 
                                   y= list(dataframe['Retention(%over2yrs)']),
#                                    marker=dict(color=colors[len(data)]),
                                   name=group)
                data.append(trace)

                layout =  go.Layout(xaxis={'title': 'Year'},
                                    yaxis={'title': 'Retention Percentage over 2 years'},
                                    margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                                    hovermode='closest')

                figure = go.Figure(data=data, layout=layout)  
#                 figure.show()

        
    return figure




@app.callback(
    [dash.dependencies.Output(component_id='bubble-chart', component_property='figure'),
     dash.dependencies.Output(component_id = 'wordcloud', component_property = 'src')],
    [dash.dependencies.Input(component_id='conf-dropdown-bubble', component_property='value')])


def create_bubble(selected_conf):
    "For a selected conference return the bubble plot"

    
    file_name = str(selected_conf) + "_bubble.csv"
    df = pd.read_csv('data/Bubble/' + str(file_name))
    
    fig = px.scatter(df, x="No_of_tpc", y="No_of_publications",size="No_of_authors",color = 'University/Organization',size_max=60)
    
    file_name = str(selected_conf) + "_wordcloud.png"
    src = "assets/" + str(file_name)
    
    img = Image.open('assets/' + str(file_name))
    
    
 
    return fig, src
    


if __name__ == '__main__':
    app.run_server(debug = True)


