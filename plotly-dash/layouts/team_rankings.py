from dash import html
import pandas as pd
from common.utils import metrics, encode_image

df_team_stats = pd.read_csv('../datasets/stats_mls.csv')

goals_per_match = df_team_stats['GF'].sum() / df_team_stats['MP'].sum()
number_of_players = df_team_stats['# Pl'].sum()
average_age = df_team_stats['Age'].mean()
matches_missed_by_players = df_team_stats['total_missed_games'].sum()
number_of_red_cards = df_team_stats['CrdR'].sum()

global_stats = {
    "Goals per match": round(goals_per_match, 2),
    "Number of players having played": int(number_of_players),
    "Average age": round(average_age, 1),
    "Match missed by the players": int(matches_missed_by_players),
    "Number of red cards": number_of_red_cards
}

df_team_stats['logo'] = df_team_stats['Logo path'].str.replace('datasets/', 'assets/')
df_team_stats['EncodedLogo'] = df_team_stats['logo'].apply(encode_image)

def create_stat_card(metric, index):
    metric_label = metric['label']
    metric_value = metric['value']
    ascending = metric.get('ascending', False)

    sorted_df = df_team_stats.sort_values(by=metric_value, ascending=ascending).reset_index(drop=True)

    top_team_row = html.Div([
        html.Span(f"{sorted_df.loc[0, 'Team']}", className='top-team-name'),
        html.Img(src=sorted_df.loc[0, 'EncodedLogo'], className='top-team-logo'),
    ], className='top-team-row')

    top_team_value = html.Span(f"{sorted_df.loc[0, metric_value]}", className='top-team-value')

    other_teams_rows = [
        html.Div([
            html.Span(f"{i + 2} {sorted_df.loc[i + 1, 'Team']}", className='other-team-name'),
            html.Span(f"{sorted_df.loc[i + 1, metric_value]}", className='other-team-value'),
            html.Img(src=sorted_df.loc[i + 1, 'EncodedLogo'], className='other-team-logo'),
        ], className='other-team-row')
        for i in range(4)
    ]

    card_content = [
        html.Div([
            html.Div([
                html.H3(metric_label, className='metric-label'),
                top_team_value,
            ], className='metric-label-row'),
            top_team_row,
            html.Div(other_teams_rows)
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
        for index, metric in enumerate(metrics)
    ], id='stat-cards-container', className='stat-cards-container')
], className='stat-cards-wrapper')
