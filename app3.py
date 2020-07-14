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

def conf_years(conf_df):
    "Given the df for a conference returns the list of years "
    year_list = list(set(conf_df['Year']))
    year_list.sort()
    return year_list

year_dict = collections.defaultdict(list)

year_dict['ipsn'] = conf_years(ipsn_df)

year_dict['mobicom'] = conf_years(mobicom_df)

year_dict['mobihoc'] = conf_years(mobihoc_df)

year_dict['sensys'] = conf_years(sensys_df)

year_dict['sigcomm'] = conf_years(sigcomm_df)

################################################################3


years = list(year_dict.keys())
nestedOptions = year_dict[years[0]]

app.layout = html.Div(
    [
        html.Div([
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label':year, 'value':year} for year in years],
            value = list(year_dict.keys())[0]
            ),
            ],style={'width': '20%', 'display': 'inline-block'}),
        html.Div([
        dcc.Dropdown(
            id='opt-dropdown',
            ),
            ],style={'width': '20%', 'display': 'inline-block'}
        ),
        html.Hr()
        
    ]
)

@app.callback(
    dash.dependencies.Output('opt-dropdown', 'options'),
    [dash.dependencies.Input('year-dropdown', 'value')]
)
def update_date_dropdown(year):
    return [{'label': i, 'value': i} for i in year_dict[year]]



if __name__ == '__main__':
    app.run_server()


