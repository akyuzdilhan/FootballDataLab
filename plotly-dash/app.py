import dash
import dash_bootstrap_components as dbc
import pandas as pd

from dash import html, dcc, dash_table
from dash.dependencies import Input, Output

df_team_stats = pd.read_csv('../datasets/squad_stats_FBref.csv')
df_team_missed_games = pd.read_csv('../datasets/missed_games_by_club.csv')
df_player_stats = pd.read_csv('../datasets/player_stats_FBref.csv')
df_MLS23_table = pd.read_csv('../datasets/MLS_23_table.csv')
df_MLS23_table['logo'] = df_MLS23_table['Logo path'].str.replace('datasets/', 'assets/')
df_MLS23_table['Team'] = df_MLS23_table.apply(lambda x: f"<img src='{x['logo']}' style='height:25px; width:25px; margin-right: 5px; margin-left: 5px;'/> {x['Team']}", axis=1)

column_order = ["Pos", "Team", "Pld", "W", "L", "T", "GF", "GA", "GD", "Pts", "SalaryGuaranteed ($)"]
df_MLS23_table = df_MLS23_table[column_order]

app = dash.Dash(__name__, suppress_callback_exceptions=True, title='Football Data Lab') # , external_stylesheets=[dbc.themes.BOOTSTRAP]

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([  # Header
        dcc.Link("Football Data Lab", href='/', className='link', style={'fontSize': '24px', 'color': '#000'}),
        dcc.Link("MLS 2023", href='/', className='link', style={'textAlign': 'center', 'flex': '1', 'fontSize': '24px', 'color': '#000'}),
        html.Div([
            dcc.Link('Table', href='/table', className='link'),
            dcc.Link('Team Analysis', href='/team-analysis', className='link'),
            dcc.Link('Player Analysis', href='/player-analysis', className='link'),
        ], style={'textAlign': 'right'})
    ], className='header'),
    html.Div(id='page-content', className='content')
], id='wrapper')


def get_columns(dataframe):
    columns = []
    for col in dataframe.columns:
        columns.append({"name": col, "id": col, 'presentation': 'markdown' if col == 'Team' else 'input'})
    return columns
    
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/table':
        return html.Div([
            dash_table.DataTable(
                id='mls-table',
                columns=get_columns(df_MLS23_table),
                data=df_MLS23_table.to_dict('records'),
                style_table={'overflowX': 'auto'},
                page_size=30,
                sort_action='native',
                sort_mode="single",
                sort_by=[{'column_id': 'Pos', 'direction': 'asc'}],
                markdown_options={'html': True},
                tooltip_header={
                    'Pld': 'Played',
                    'W': 'Wins',
                    'L': 'Losses',
                    'T': 'Ties',
                    'GF': 'Goals For',
                    'GA': 'Goals Against',
                    'GD': 'Goal Difference',
                    'Pts': 'Points',
                    'SalaryGuaranteed ($)': 'Guaranteed Salary'
                },
                style_cell={
                    'textAlign': 'center',
                    'borderLeft': '0px'
                },
                style_header={
                    'backgroundColor': '#F8F5F0',
                    'fontWeight': 'bold',
                    'border': '0px'
                }
            )
        ], className='data-table-container')
    elif pathname == '/player-analysis':
        return html.H3("Player Analysis Content")
    else:
        return html.H3("Welcome to the Football Data Lab Dashboard!")
    
if __name__ == '__main__':
    app.run_server(debug=True)
