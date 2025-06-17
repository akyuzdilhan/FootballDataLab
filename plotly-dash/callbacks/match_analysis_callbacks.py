from dash.dependencies import Input, Output
from common.data_loader import load_match_events
from common.pitch_utils import make_pass_network_figure, make_carry_network_figure

def register_match_analysis_callbacks(app):
    @app.callback(
        Output('pass-network-graph', 'figure'),
        [Input('pass-player-dropdown', 'value')]
    )
    def update_pass_graph(player_name):
        df = load_match_events(3877115)
        return make_pass_network_figure(df, player_name)

    @app.callback(
        Output('carry-network-graph', 'figure'),
        [Input('pass-player-dropdown', 'value')]
    )
    def update_carry_graph(player_name):
        df = load_match_events(3877115)
        return make_carry_network_figure(df, player_name)
