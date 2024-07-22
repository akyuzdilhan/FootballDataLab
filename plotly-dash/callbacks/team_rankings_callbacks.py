from dash.dependencies import Input, Output, State
from dash import html, callback_context
from common.utils import metrics

def register_team_rankings_callbacks(app, df_team_stats):
    @app.callback(
        Output('team-full-list-container', 'children'),
        [Input(f'view-full-list-{index}', 'n_clicks') for index in range(len(metrics))],
        [State('url', 'pathname')]
    )
    def display_team_full_list(*args):
        ctx = callback_context

        if not ctx.triggered:
            return []

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        index = int(button_id.split('-')[-1])
        metric = metrics[index]
        metric_value = metric['value']
        metric_label = metric['label']
        ascending = metric.get('ascending', False)

        sorted_df = df_team_stats.sort_values(by=metric_value, ascending=ascending).reset_index(drop=True)

        top_team_row = html.Div([
            html.Span(f"{sorted_df.loc[0, 'Team']}", className='top-team-name'),
            html.Img(src=sorted_df.loc[0, 'EncodedLogo'], className='top-team-logo')
        ], className='top-team-row')

        top_team_value = html.Span(f"{sorted_df.loc[0, metric_value]}", className='top-team-value')

        other_teams_rows = []
        for i in range(1, len(sorted_df)):
            other_teams_rows.append(html.Div([
                html.Div([
                    html.Span(f"{i + 1}."),
                    html.Span(f"{sorted_df.loc[i, 'Team']}", style={'padding-left': '20px'})
                ], style={'display': 'flex', 'flex': 1}),
                html.Span(f"{sorted_df.loc[i, metric_value]}", className='full-list-other-team-value'),
                html.Img(src=sorted_df.loc[i, 'EncodedLogo'], className='other-team-logo')
            ], className='other-team-row'))

        card_content = html.Div([
            html.Div([
                html.H3(metric_label, className='metric-label'),
                top_team_value
            ], className='metric-label-row'),
            top_team_row,
            html.Div(other_teams_rows, className='full-list-content')
        ], className='full-list-card', style={'width': '100%'})

        return [card_content]
