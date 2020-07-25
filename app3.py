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



# creating the years dictionary for dynamic dropdown
#############################################################
ipsn_df = pd.read_csv('data/Clean_Authors/ipsn_authors.csv')
ipsn_df = ipsn_df.drop(['Keywords'], axis = 1)

ipsn_tpc = pd.read_csv('data/Clean_TPC/ipsn_clean.csv')

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
        html.Br(),
        
        html.Div([
            html.Img(src = '../assets/bias_quote.png'),
        ], style = {'textAlign' : 'center'}),
        html.Br(),
        
        html.P('Is there bias in the research community ?', style = {'color' : '#30bf0f', 'fontSize' : 40, 'textAlign' : 'center', 'fontFamily' : "HelveticaNeue", 'fontStyle' : 'italic'}),
        
        html.Br(),
        html.Div([html.Img(src = '../assets/t1.png')], style = {'width' : '100%', 'height' : '100%', 'textAlign' :'center'}, className = 'one-column'),
        
        html.Hr(),
        html.P(children = 'Data Introduction', style = {'color' : 'white', 'fontSize' : 40, 'textAlign' : 'center'}),
        
        html.Hr(),
        html.Div([
            html.Blockquote(id = 'as', children = "We scraped websites like ACM Digital Library, IEEE Explore and numerous other public repositories, to collect data for 1000+ individual authors and 150+ TPCs over a span of 20 years.")           
        ], style = {'color' : '#ffffff', 'fontSize' : 30, 'fontStyle' : 'italic'}),
        
        html.Br(),
    
        
        html.Div([
             html.Div([
                        html.P(children = "Information on TPC for each conference", style = {'color' : 'white', 'fontSize' : 20, 'fontFamily' : 'sans-serif', 'textAlign' : 'center'}),
                        dash_table.DataTable(
                            data=ipsn_tpc[:5].to_dict('records'),
                            columns=[{'id': c, 'name': c} for c in ipsn_tpc.columns],

                            style_header={'backgroundColor': 'white'},
                            style_cell={
                                'backgroundColor': '#e4d5eb',
                                'color': 'black'
                            },),

                    ], className = 'six-columns'),
             html.Br(),
             html.Div([
                        html.P(children = "Information on Authors published in a given conference", style = {'color' : 'white', 'fontSize' : 20, 'fontFamily' : 'sans-serif', 'textAlign' : 'center'}),

                        dash_table.DataTable(
                            data=ipsn_df[110:116].to_dict('records'),
                            columns=[{'id': c, 'name': c} for c in ipsn_df.columns],

                            style_header={'backgroundColor': 'white'},
                            style_cell={
                                'backgroundColor': '#e4d5eb',
                                'color': 'black'
                            },),

                    ], className = 'six-columns'),
            
        ], ),
        
        html.Br(),
        html.Hr(),
        html.P(children = 'Year Wise Analysis of TPC', style = {'color' : 'white', 'fontSize' : 40, 'textAlign' : 'center'}),
        html.Hr(),
    
        html.Div([
            html.Blockquote(id = '2', children = "Let's investigate the TPC and author demographics for each conference by selecting the year of publication")           
        ], style = {'color' : '#ffffff', 'fontSize' : 30, 'fontStyle' : 'italic'}),
        html.Br(),

        
        
        
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
        
        html.Br(),
        html.Br(),
        
        ## Adding graphs
        html.Div([
            html.Div([
                html.Div([
                    html.Blockquote(id = '3', children = "The key to fair representation and diversity is to ensure that the TPC composition is not skewed due to majority of members belonging to the same organization. \n But here we see that for some conferences there are as many as 6 members from the same university.")           
                ], style = {'color' : '#ddf0d3', 'fontSize' : 20, 'fontStyle' : 'bold'}),

#                 html.H3('Most Influential TPC universities/organizations'),
                dcc.Graph(id = 'TOP-20-TPC')
            ], className = 'six columns'),
            
            html.Div([
#                 html.H3('col2'),
                html.Br(),
                html.Div([
                    html.Blockquote(id = '4', children = "This Pie chart shows how many TPC universities make up the authorship for the given year.      ")           
                ], style = {'color' : '#ddf0d3', 'fontSize' : 20, 'fontStyle' : 'bold'}),
                
                dcc.Graph(id = 'TOP-20-AUTH')   
            ], className = 'three columns'),
            
            html.Div([
#                 html.H3('col3'),
                html.Br(),
                html.Div([
                    html.Blockquote(id = '5', children = "A major indicator of bias is when TPC members feature as authors in the same year.")           
                ], style = {'color' : '#ddf0d3', 'fontSize' : 20, 'fontStyle' : 'bold'}),
                dcc.Graph(id = 'Published-TPC')   
            ], className = 'three columns')

        ], className = 'row'),
           
        html.Br(), 
        html.P('P.S : To view the count of TPC members/authors hover over the graphs', style = {'color' : '#03fcfc', 'fontSize' : 15}),
        html.Br(),
        html.Div([
            html.Blockquote(id = '6', children = "Using the above charts we can see that authors from TPC backed universities end up making a significant portion of the authorship. In some cases (sensys, 2003-5), the TPC universities make up 40% of the authorship indicating traces of bias")], style = {'color' : 'white', 'fontSize' : 30 , 'fontFamily' : 'sans-serif'}),
#         
#         html.P('Using the above charts we can see that authors from TPC backed universities end up making a significant portion of the authorship. In some cases (sensys, 2003-5), the TPC universities make up 40% of the authorship indicating traces of bias', style = {'color' : 'white', 'fontSIze' : 20}),
        
        html.Div(id = 'out-of'), 
        html.Hr(),
        html.P(id = '34', children = 'TPC Retention', style = {'color' : 'white', 'fontSize' : 40, 'textAlign' : 'center'}),
        html.Hr(),
        html.Br(),

        ### Creating slider for no of years given the conference
        
        html.Div([
            html.Blockquote(id = '7', children = 'From the above analysis we can see that TPC composition plays a big role in reducing selection bias. We propose a metric called "TPC Retention" , to highlight the fact that most TPCs continue with the same people year after year. This restricts the possibility of having wider representation and confines the TPC privileges to a fixed set of universities/organizations/researchers. ')], style = {'color' : 'white', 'fontSize' : 30 , 'fontFamily' : 'sans-serif'}),
        
        html.Br(),
        
        
        html.H3('Lets compare TPC Retention amongst the conferences', style = {'color' : 'white'}),
        
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
                            ],value=['ipsn', 'mobihoc'], labelStyle={'display': 'inline-block', 'color' : 'white'}),
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
        html.Br(),
        html.Div([
            html.Blockquote(id = '8', children = "It's quite alarming to see that TPC retention based on university composition has been on a slow rise and in recent years the average tpc retention % is 60%. This phenomenon is exaggerated when analysing tpc retention based on individual tpc member, the high percentages indicate that the exact same people have been continuing on as members year after year.")], style = {'color' : 'white', 'fontSize' : 30 , 'fontFamily' : 'sans-serif'}
            
        ),
        html.Br(),
        html.Hr(),
        html.P(children = "Bird's Eye View" , style = {'color' : 'white', 'fontSize' : 40, 'textAlign' : 'center'}),
        html.Hr(),
        html.Br(),
        html.Div([
            dcc.Dropdown(
                id='conf-dropdown-bubble',
                options=[{'label': year, 'value':year} for year in years],
                value = list(year_dict.keys())[0]
                )
        ], style = {'width' : '20%'}),
        
        html.Br(),
        html.Div([
            html.Blockquote(id = '11', children = "Using the data collected over the past 20 years, we created a bubble chart to represent the key organizations and the no. of authors that have been published over the years. The size of each bubble corresponds to the author base from that organization. It comes with no surprise that the largest bubbles correspond to the universities with higher TPC representation.")], style = {'color' : 'white', 'fontSize' : 30 , 'fontFamily' : 'sans-serif'}
            
        ),
        
        html.Br(),
        dcc.Graph(id = 'bubble-chart'),
        html.Br(),
        html.P(children = 'P.S : For the purposes of the above chart, we have considered the presence of the same author/TPC in more than one year as two separate counts', style = {'color' : 'white'}),
        
        html.Br(),
        
        html.Div([
            html.Blockquote(id = '10', children = "The following word cloud indicates the most popular ideas or themes that were reflected in the body of publications made by the conference over a period of the last 20 years.")], style = {'color' : 'white', 'fontSize' : 30 , 'fontFamily' : 'sans-serif'}
            
        ),
        html.Br(),
        
    
        
        html.Div([
            html.Img(id = 'wordcloud')
        ], style = {'textAlign' : 'center'}),
        
        html.Hr(),
        html.Div([
            html.Blockquote(id = '19', children = "The aim of this investigative tool and the analysis it produces is not to blame TPC members and the universities they are affiliated with. Our only hope is that this tool can initiate a much needed conversation on diversity and representation in the research community.")], style = {'color' : 'white', 'fontSize' : 30 , 'fontFamily' : 'sans-serif'}
            
        ),
        
        
        
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
                       title = 'Most Influential TPC organizations')
#                        title = 'TPC top 20 % of ' + str(len(uni_count_df)) + " different universities/organizations)"  )
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6),
    
    fig.update_yaxes(autorange = 'reversed')
    fig.update_layout(
    title_font_family="sans-serif",
    title_font_color= 'rgb(66, 75, 107)',
    title_font_size = 40,
    plot_bgcolor = '#e3e8e8',
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
            
    night_colors = ['rgb(56, 75, 126)', 'rgb(158,202,225)']
            
    pie_df = pd.DataFrame(list(zip(rank, no_of_authors)), columns = ['Rank', 'No_of_authors'])
    tpc_uni_pie = px.pie(pie_df, values = 'No_of_authors', names = 'Rank', title = "University/Organization composition of author base.", color_discrete_sequence=px.colors.qualitative.Prism, opacity = 0.6)
    
#     tpc_uni_pie.update_traces(line=dict(color='#000000', width=2))
    
    
    tpc_uni_pie.update_layout(
        title_font_family = "sans-serif",
        title_font_color = 'rgb(66, 75, 107)',
        title_font_size = 14,
        plot_bgcolor = '#e3e8e8',
        
        
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
    
        
    tpc_overlap = pd.DataFrame(list(zip(status, count)), columns = ['status', 'count'])
    
    tpc_auth_pie = px.pie(tpc_overlap, values = 'count', names = 'status', title = "TPC Member and Author overlap", color_discrete_sequence=px.colors.qualitative.Prism, opacity = 0.6)
    
#     tpc_auth_pie = go.Figure(data=[go.Pie(labels = tpc_overlap['status'], values = tpc_overlap['count'], title = "TPC Member and author overlap")])
    
    tpc_auth_pie.update_layout(
        title_font_family = "sans-serif",
        title_font_color = "rgb(66, 75, 107)",
        title_font_size = 20
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
                                   name=group)
                data.append(trace)

                layout =  go.Layout(xaxis={'title': 'Year'},
                                    yaxis={'title': 'Retention Percentage over 2 years'},
                                    margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                                    hovermode='closest')

                figure = go.Figure(data=data, layout=layout)         
        
        
    if uni_auth == 'tpc':
        retention_df = pd.read_csv('data/retention_authors.csv')
        final_df = retention_df.loc[retention_df['Name'].isin(conf_list)]
        
        groups = final_df.groupby(by = 'Name')
        data = []
        
        for group, dataframe in groups:
                dataframe = dataframe.sort_values(by=['Year'])
                trace = go.Scatter(x=dataframe.Year.tolist(), 
                                   y= list(dataframe['Retention(%over2yrs)']),
                                   name=group)
                data.append(trace)

                layout =  go.Layout(xaxis={'title': 'Year'},
                                    yaxis={'title': 'Retention Percentage over 2 years'},
                                    margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                                    hovermode='closest')

                figure = go.Figure(data=data, layout=layout)  

        
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


