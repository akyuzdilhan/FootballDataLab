import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
from common.data_loader import load_team_stats, load_player_stats
from layouts import home, table, team_analysis, player_analysis
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
        dcc.Link(
            html.Div([
                html.Img(src='assets/FootballDataLab.png', className='header-logo'),
                html.Span('Football DataLab', className='title')
            ], className='header-info'), href='/', style={'textDecoration': 'none'}
        ),
        dcc.Link('MLS 2023', href='/', style={'textAlign': 'center', 'flex': '1', 'fontSize': '24px', 'color': '#000', 'textDecoration': 'none'}),
        html.Div([
            dcc.Link('Table', href='/table', className='page'),
            dcc.Link('Team Analysis', href='/team-analysis', className='page'),
            dcc.Link('Team Rankings', href='/team-rankings', className='page'),
            dcc.Link('Player Analysis', href='/player-analysis', className='page'),
            dcc.Link('Player Rankings', href='/player-rankings', className='page'),
        ], style={'textAlign': 'right'})
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
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True) # False 