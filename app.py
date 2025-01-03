import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
from common.data_loader import load_team_stats, load_player_stats
from layouts import home, table, team_analysis, player_analysis, match_analysis
from layouts.team_rankings import create_layout as create_team_rankings_layout
from layouts.player_rankings import create_layout as create_player_rankings_layout
from callbacks.team_analysis_callbacks import register_callbacks
from callbacks.rankings_callbacks import register_rankings_callbacks
from common.utils import metrics, player_metrics

app = dash.Dash(__name__, suppress_callback_exceptions=True, title='Football DataLab', external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df_team_stats = load_team_stats()
df_player_stats = load_player_stats()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.A(
            html.Div([
                html.Img(src='assets/FootballDataLab.png', className='header-logo', alt='Football DataLab Logo'),
                html.Span('Football DataLab', className='title')
            ], className='brand'),
            href='/', style={'textDecoration': 'none'}
        ),
        html.A('MLS 2023', href='/', className='season-link'),

        html.Div(
            dbc.DropdownMenu(
                [
                    dbc.DropdownMenuItem("Table", href='/table'),
                    dbc.DropdownMenuItem("Team Analysis", href='/team-analysis'),
                    dbc.DropdownMenuItem("Team Rankings", href='/team-rankings'),
                    dbc.DropdownMenuItem("Player Analysis", href='/player-analysis'),
                    dbc.DropdownMenuItem("Player Rankings", href='/player-rankings'),
                    #dbc.DropdownMenuItem("Match Analysis", href='/match-analysis'),
                ],
                label=html.Img(src='assets/menu.png', alt='Open menu', className='menu-icon'),
                direction="down",
                className="dropdown-nav menu-button",
                caret=False,
                toggle_style={
                    "background": "transparent",
                    "border": "none",
                    "boxShadow": "none",
                    "padding": "0"
                }
            ),
            className='menu-button'
        ),

        html.Nav(
            [
                html.A('Table', href='/table', className='page'),
                html.A('Team Analysis', href='/team-analysis', className='page'),
                html.A('Team Rankings', href='/team-rankings', className='page'),
                html.A('Player Analysis', href='/player-analysis', className='page'),
                html.A('Player Rankings', href='/player-rankings', className='page'),
            ],
            className='nav-links',
            id='nav-links'
        )
    ], className='header'),


    html.Div(id='page-content', className='content'),
    html.Div(id='full-list-container', style={'display': 'none'}),
    html.Div(id='dummy-scroll-div', style={'display': 'none'}),

    html.Footer([
        html.Div([
            dcc.Link(
                html.Div([
                    html.Img(src='assets/FootballDataLab.png', className='footer-logo'),
                    html.Span('Football DataLab', className='footer-title')
                ], className='footer-section-left'), href='/', style={'textDecoration': 'none'}
            ),
            html.Div([
                html.Span("© 2024 Football DataLab | Licensed under GNU GPL-3.0", className='footer-legal'),
            ], className='footer-section-middle'),
            html.Div([
                html.A(html.Img(src='/assets/github-icon.png', className='footer-icon'), href="https://github.com/akyuzdilhan/FootballDataLab", target="_blank"),
                html.A(html.Img(src='/assets/email-icon.png', className='footer-icon'), href="mailto:footballdatalab.contact@gmail.com", target="_blank"),
            ], className='footer-section-right'),
        ], className='footer-container'),
    ], className='footer')
], id='wrapper')

register_callbacks(app, df_team_stats)
register_rankings_callbacks(app, df_team_stats, df_player_stats, metrics, player_metrics)

import callbacks.home_callbacks

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
        return create_team_rankings_layout()
    elif pathname == '/player-analysis':
        return player_analysis.layout
    elif pathname == '/player-rankings':
        return create_player_rankings_layout()
    #elif pathname == '/match-analysis':
        #return match_analysis.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True) # app.run_server(host='0.0.0.0', port=8050, debug=False)