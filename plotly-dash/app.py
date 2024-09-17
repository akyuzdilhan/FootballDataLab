import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output, State, MATCH
from flask_caching import Cache
from common.data_loader import load_team_stats, load_player_stats
from layouts import home, table, team_analysis, player_analysis, team_rankings, player_rankings
from layouts.team_rankings import create_layout as create_team_rankings_layout
from layouts.player_rankings import create_layout as create_player_rankings_layout
from callbacks.team_analysis_callbacks import register_callbacks
from callbacks.rankings_callbacks import register_rankings_callbacks
from common.utils import encode_image, metrics, player_metrics, calculate_global_stats

EXTERNAL_STYLESHEETS = [dbc.themes.BOOTSTRAP]
APP_TITLE = 'Football Data Lab'

app = dash.Dash(__name__, suppress_callback_exceptions=True, title=APP_TITLE, external_stylesheets=EXTERNAL_STYLESHEETS)

cache = Cache(app.server, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 300})

df_team_stats = load_team_stats(cache)
df_player_stats = load_player_stats(cache)

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
register_rankings_callbacks(app, df_team_stats, df_player_stats, metrics, player_metrics)
    
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
        return create_team_rankings_layout(cache)
    elif pathname == '/player-analysis':
        return player_analysis.layout
    elif pathname == '/player-rankings':
        return create_player_rankings_layout(cache)
    else:
        return home.layout

# TODO Why and what is FootballDataLab ?
# TODO What are the uses of Data Science in Football ?
# ...

if __name__ == '__main__':
    app.run_server(debug=True) # set 'debug=True' to display errors on the browser or 'False' to hide it
