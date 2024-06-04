import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output
from layouts import home, table, team_analysis, player_analysis, team_rankings, player_rankings
from callbacks.team_analysis_callbacks import register_callbacks
from callbacks.team_rankings_callbacks import register_team_rankings_callbacks
from common.utils import encode_image

EXTERNAL_STYLESHEETS = [dbc.themes.BOOTSTRAP]
APP_TITLE = 'Football Data Lab'

df_team_stats = pd.read_csv('../datasets/squad_stats_FBref.csv')
df_team_stats['logo'] = df_team_stats['Logo path'].str.replace('datasets/', 'assets/')
df_team_stats['EncodedLogo'] = df_team_stats['logo'].apply(encode_image)

app = dash.Dash(__name__, suppress_callback_exceptions=True, title=APP_TITLE, external_stylesheets=EXTERNAL_STYLESHEETS)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Football Data Lab', href='/', className='link', style={'fontSize': '24px', 'color': '#000'}),
        dcc.Link('MLS 2023', href='/', className='link', style={'textAlign': 'center', 'flex': '1', 'fontSize': '24px', 'color': '#000'}),
        html.Div([
            dcc.Link('Table', href='/table', className='link'),
            dcc.Link('Team Analysis', href='/team-analysis', className='link'),
            dcc.Link('Team Rankings', href='/team-rankings', className='link'),
            dcc.Link('Player Analysis', href='/player-analysis', className='link'),
            dcc.Link('Player Rankings', href='/player-rankings', className='link'),
        ], style={'textAlign': 'right'})
    ], className='header'),
    html.Div(id='page-content', className='content')
], id='wrapper')
    
register_callbacks(app, df_team_stats)
register_team_rankings_callbacks(app, df_team_stats)

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/table':
        return table.layout
    elif pathname == '/team-analysis':
        return team_analysis.layout
    elif pathname == '/team-rankings':
        return team_rankings.layout
    elif pathname == '/player-analysis':
        return player_analysis.layout
    elif pathname == '/player-rankings':
        return player_rankings.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)
