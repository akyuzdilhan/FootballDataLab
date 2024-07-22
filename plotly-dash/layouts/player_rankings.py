from dash import html
import pandas as pd
from dash import dcc
from common.utils import player_metrics, encode_image

df_player_stats = pd.read_csv('../datasets/player_stats_FBref.csv')
average_age = df_player_stats['age'].mean()

global_stats = {
    "Average Age": round(average_age, 1)
    # ...
    # TODO change stats by filters (age, min, team, ect...) and can choose the number of player selected for each table
}

df_player_stats['logo'] = df_player_stats['Logo path'].str.replace('datasets/', 'assets/')
df_player_stats['EncodedLogo'] = df_player_stats['logo'].apply(encode_image)

# TODO add params : choose for each table if it's ascending or not
def create_player_stat_card(metric, index):
    metric_label = metric['label']
    metric_value = metric['value']
    ascending = metric.get('ascending', False)

    sorted_df = df_player_stats.sort_values(by=metric_value, ascending=ascending).reset_index(drop=True)

    top_player_row = html.Div([
        html.Span(f"{sorted_df.loc[0, 'player']}", className='top-team-name'),
        html.Img(src=sorted_df.loc[0, 'EncodedLogo'], className='top-team-logo'),
    ], className='top-team-row')

    top_player_value = html.Span(f"{sorted_df.loc[0, metric_value]}", className='top-team-value')

    other_players_rows = [
        html.Div([
            html.Span(f"{i + 2} {sorted_df.loc[i + 1, 'player']}", className='other-team-name'),
            html.Span(f"{sorted_df.loc[i + 1, metric_value]}", className='other-team-value'),
            html.Img(src=sorted_df.loc[i + 1, 'EncodedLogo'], className='other-team-logo'),
        ], className='other-team-row')
        for i in range(4)
    ]

    card_content = [
        html.Div([
            html.Div([
                html.H3(metric_label, className='metric-label'),
                top_player_value,
            ], className='metric-label-row'),
            top_player_row,
            html.Div(other_players_rows)
        ], className='card-content'),
        html.Button('View full list', id=f'player-view-full-list-{index}', className='view-full-list-button', n_clicks=0)
    ]

    return html.Div(card_content, className='stat-card')

global_stats_layout = html.Div([
    html.Div([
        html.Img(src='assets/MLS.png', className='league-logo'),
        html.Div([
            html.H2("MLS", className='league-name'),
            html.P("2023 Season", className='season')
        ], className='league-details')
    ], className='league-info'),
    html.Div([
        html.Div([
            html.H3(f"{value}", className='global-stat-value'),
            html.P(f"{key}", className='global-stat-label')
        ], className='global-stat') for key, value in global_stats.items()
    ], className='global-stats-container')
], className='global-stats-header')

layout = html.Div([
    global_stats_layout,
    html.Div(id='player-full-list-container', style={'paddingTop': '20px'}),
    html.Div([
        create_player_stat_card(metric, index)
        for index, metric in enumerate(player_metrics)
    ], id='stat-cards-container', className='stat-cards-container')
], className='stat-cards-wrapper')
