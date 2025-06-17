from dash import html, dcc
from common.data_loader import load_match_players

MATCH_ID = 3877115
players = load_match_players(MATCH_ID)

layout = html.Div(className='match-analysis-container', children=[

    html.Div(className='controls-row', style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'}, children=[
        html.Label('Select Player:', htmlFor='pass-player-dropdown'),
        dcc.Dropdown(
            id='pass-player-dropdown',
            options=[{'label': p, 'value': p} for p in players],
            placeholder='Choose a player',
            value=players[0],
            style={'minWidth': '300px'}
        ),
    ]),

    html.Div(className='graph-row', style={'display': 'flex', 'gap': '20px', 'marginTop': '20px'}, children=[
        dcc.Graph(
            id='pass-network-graph',
            config={'responsive': True},
            style={'width': '50%', 'height': '600px'}
        ),
        dcc.Graph(
            id='carry-network-graph',
            config={'responsive': True},
            style={'width': '50%', 'height': '600px'}
        )
    ])
])