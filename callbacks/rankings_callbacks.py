from dash.dependencies import Input, Output, ALL
from dash import callback_context
from common.layout_helpers import generate_full_list

def register_rankings_callbacks(app, df_stats_team, df_stats_player, metrics_team, metrics_player):
    @app.callback(
        Output('full-list-container', 'children'),
        [
            Input({'type': 'view-full-list-button', 'index': ALL}, 'n_clicks'),
            Input({'type': 'player-view-full-list-button', 'index': ALL}, 'n_clicks')
        ],
    )
    def display_full_list(team_n_clicks_list, player_n_clicks_list):
        ctx = callback_context

        if not ctx.triggered:
            return []

        button_id_str = ctx.triggered[0]['prop_id'].split('.')[0]
        button_id = eval(button_id_str)

        if button_id['type'] == 'view-full-list-button':
            index = button_id['index']
            metric = metrics_team[index]
            metric_value = metric['value']
            metric_label = metric['label']
            ascending = metric.get('ascending', False)
            return [generate_full_list(df_stats_team, metric_value, metric_label, 'EncodedLogo', 'Team', ascending)]

        elif button_id['type'] == 'player-view-full-list-button':
            index = button_id['index']
            metric = metrics_player[index]
            metric_value = metric['value']
            metric_label = metric['label']
            ascending = metric.get('ascending', False)
            return [generate_full_list(df_stats_player, metric_value, metric_label, 'encoded_image', 'player', ascending)]

        return []
