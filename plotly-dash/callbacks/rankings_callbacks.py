from dash.dependencies import Input, Output, State, ALL
from dash import callback_context
from common.layout_helpers import generate_full_list

def register_rankings_callbacks(app, df_stats_team, df_stats_player, metrics_team, metrics_player):
    @app.callback(
        [Output('full-list-container', 'children'),
         Output('page-store', 'data')],
        [
            Input({'type': 'view-full-list-button', 'metric_type': ALL, 'index': ALL}, 'n_clicks'),
            Input({'type': 'previous-page-button', 'metric_type': ALL, 'index': ALL}, 'n_clicks'),
            Input({'type': 'next-page-button', 'metric_type': ALL, 'index': ALL}, 'n_clicks'),
        ],
        [State('page-store', 'data')]
    )
    def display_full_list(view_n_clicks_list, prev_n_clicks_list, next_n_clicks_list, page_store):
        ctx = callback_context

        if not ctx.triggered:
            return [], page_store

        if page_store is None:
            page_store = {}

        triggered_id_str = ctx.triggered[0]['prop_id'].split('.')[0]
        triggered_id = eval(triggered_id_str)
        metric_index = triggered_id['index']
        metric_type = triggered_id['metric_type']

        key = f"{metric_type}_{metric_index}"

        if triggered_id['type'] == 'view-full-list-button':
            page_number = 1
            page_store[key] = page_number
        else:
            page_number = page_store.get(key, 1)
            if triggered_id['type'] == 'previous-page-button':
                page_number = max(1, page_number - 1)
            elif triggered_id['type'] == 'next-page-button':
                page_number += 1
            page_store[key] = page_number

        if metric_type == 'team':
            metric = metrics_team[metric_index]
            df = df_stats_team
            logo_column = 'EncodedLogo'
            name_column = 'Team'
        else:
            metric = metrics_player[metric_index]
            df = df_stats_player
            logo_column = 'encoded_image'
            name_column = 'player'

        metric_value = metric['value']
        metric_label = metric['label']
        ascending = metric.get('ascending', False)

        full_list_content = generate_full_list(
            df, metric_value, metric_label, logo_column, name_column,
            ascending, page_number, metric_index=metric_index, metric_type=metric_type
        )

        return full_list_content, page_store
