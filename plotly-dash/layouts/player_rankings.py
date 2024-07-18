from dash import html
import pandas as pd
from common.utils import player_metrics, encode_image

# Load player statistics data
df_player_stats = pd.read_csv('../datasets/player_stats_FBref.csv')

# Calculate global statistics (example: average age)
average_age = df_player_stats['age'].mean()

global_stats = {
    "Average Age": round(average_age, 1)
    # Add more global stats as needed
}

def create_stat_card(metric, index):
    metric_label = metric['label']
    metric_value = metric['value']
    ascending = metric.get('ascending', False)

    sorted_df = df_player_stats.sort_values(by=metric_value, ascending=ascending).reset_index(drop=True)

    top_player_row = html.Div([
        html.Span(f"{sorted_df.loc[0, 'player']}", className='top-player-name'),
        html.Img(src=encode_image(f"../assets/{sorted_df.loc[0, 'team']}.png"), className='top-player-logo'),
    ], className='top-player-row')

    top_player_value = html.Span(f"{sorted_df.loc[0, metric_value]}", className='top-player-value')

    other_players_rows = [
        html.Div([
            html.Span(f"{i + 2} {sorted_df.loc[i + 1, 'player']}", className='other-player-name'),
            html.Span(f"{sorted_df.loc[i + 1, metric_value]}", className='other-player-value'),
            html.Img(src=encode_image(f"../assets/{sorted_df.loc[i + 1, 'team']}.png"), className='other-player-logo'),
        ], className='other-player-row')
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
        html.Button('View full list', id=f'view-full-list-{index}', className='view-full-list-button', n_clicks=0)
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
    html.Div(id='full-list-container', style={'paddingTop': '20px'}),
    html.Div([
        create_stat_card(metric, index)
        for index, metric in enumerate(player_metrics)
    ], id='stat-cards-container', className='stat-cards-container')
], className='stat-cards-wrapper')
