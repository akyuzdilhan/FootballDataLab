import dash
import dash_bootstrap_components as dbc

from dash import html, dcc
from dash.dependencies import Input, Output
from layouts import home, table, team_analysis, player_analysis

app = dash.Dash(__name__, suppress_callback_exceptions=True, title='Football Data Lab') # , external_stylesheets=[dbc.themes.BOOTSTRAP]

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
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
    
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/table':
        return table.layout
    elif pathname == '/team-analysis':
        return team_analysis.layout
    elif pathname == '/player-analysis':
        return player_analysis.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)
