from dash import html
import pandas as pd
from dash import dcc
from common.utils import metrics, encode_image

df_team_stats = pd.read_csv('../datasets/squad_stats_FBref.csv')

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

layout = html.Div([
    # TODO Add a general presentation header for the statistics of the championship presented
    html.Div(id='full-list-container', style={'paddingTop': '20px'}),
    html.Div([
        create_stat_card(metric, index)
        for index, metric in enumerate(metrics)
    ], id='stat-cards-container', className='stat-cards-container')
], className='stat-cards-wrapper')
