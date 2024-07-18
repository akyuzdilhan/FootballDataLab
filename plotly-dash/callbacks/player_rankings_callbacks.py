from dash.dependencies import Input, Output, State
from dash import html, callback_context
from common.utils import player_metrics

def register_player_rankings_callbacks(app, df_player_stats):
    @app.callback(
        Output('full-list-container', 'children'),
        [Input(f'view-full-list-{index}', 'n_clicks') for index in range(len(player_metrics))],
        [State('full-list-container', 'children')]
    )
    def display_full_list(*args):
        ctx = callback_context

        if not ctx.triggered:
            return []

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        index = int(button_id.split('-')[-1])
        metric = player_metrics[index]
        metric_value = metric['value']
        metric_label = metric['label']
        ascending = metric.get('ascending', False)

        sorted_df = df_player_stats.sort_values(by=metric_value, ascending=ascending).reset_index(drop=True)

        top_player_row = html.Div([
            html.Span(f"{sorted_df.loc[0, 'player']}", className='top-player-name'),
            #html.Img(src=encode_image(f"../assets/{sorted_df.loc[0, 'team']}.png"), className='top-player-logo')
        ], className='top-player-row')

        top_player_value = html.Span(f"{sorted_df.loc[0, metric_value]}", className='top-player-value')

        other_players_rows = []
        for i in range(1, len(sorted_df)):
            other_players_rows.append(html.Div([
                html.Div([
                    html.Span(f"{i + 1}."),
                    html.Span(f"{sorted_df.loc[i, 'player']}", style={'padding-left': '20px'})
                ], style={'display': 'flex', 'flex': 1}),
                html.Span(f"{sorted_df.loc[i, metric_value]}", className='full-list-other-player-value'),
                #html.Img(src=encode_image(f"../assets/{sorted_df.loc[i, 'team']}.png"), className='other-player-logo')
            ], className='other-player-row'))

        card_content = html.Div([
            html.Div([
                html.H3(metric_label, className='metric-label'),
                top_player_value
            ], className='metric-label-row'),
            top_player_row,
            html.Div(other_players_rows, className='full-list-content')
        ], className='full-list-card', style={'width': '100%'})

        return [card_content]
    