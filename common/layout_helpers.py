from dash import html
from common.data_loader import load_team_stats, load_player_stats
from common.utils import calculate_global_stats, encode_image

def load_team_data():
    df_team_stats = load_team_stats()
    global_stats = calculate_global_stats(df_team_stats)
    return df_team_stats, global_stats

def load_player_data():
    df_team_stats = load_team_stats()
    df_player_stats = load_player_stats()
    global_stats = calculate_global_stats(df_team_stats)
    return df_team_stats, df_player_stats, global_stats

def create_global_stats_layout(global_stats):
    return html.Div([
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

def create_stat_card(metric, index, sorted_df, logo_column, name_column, id_prefix):
    metric_label = metric['label']
    metric_value = metric['value']

    top_row = html.Div([
        html.Span(f"{sorted_df.loc[0, name_column]}", className='top-name'),
        html.Img(src=sorted_df.loc[0, logo_column], className='top-logo'),
    ], className='top-row')

    top_value = html.Span(f"{sorted_df.loc[0, metric_value]}", className='top-value')

    other_rows = [
        html.Div([
            html.Span(f"{i + 2}. {sorted_df.loc[i + 1, name_column]}", className='other-name'),
            html.Span(f"{sorted_df.loc[i + 1, metric_value]}", className='other-value'),
            html.Img(src=sorted_df.loc[i + 1, logo_column], className='other-logo'),
        ], className='other-row') for i in range(4)
    ]

    card_content = [
        html.Div([
            html.Div([
                html.H3(metric_label, className='metric-label'),
                top_value
            ], className='metric-label-row'),
            top_row,
            html.Div(other_rows)
        ], className='card-content'),
        html.Button('View full list', id={'type': id_prefix, 'index': index}, className='view-full-list-button', n_clicks=0)
    ]
    return html.Div(card_content, className='stat-card')

def create_layout_with_cards(global_stats_layout, cards, full_list_container_id):
    return html.Div([
        global_stats_layout,
        html.Div(id=full_list_container_id, style={'paddingTop': '20px'}),
        html.Div(cards, id='stat-cards-container', className='stat-cards-container')
    ], className='stat-cards-wrapper')

# Full list for both teams and players
def generate_full_list(df, metric_value, metric_label, logo_column, name_column):
    sorted_df = df.sort_values(by=metric_value, ascending=True).reset_index(drop=True)

    top_row = html.Div([
        html.Span(f"{sorted_df.loc[0, name_column]}", className='top-name'),
        html.Img(src=sorted_df.loc[0, logo_column], className='top-logo'),
    ], className='top-row')

    top_value = html.Span(f"{sorted_df.loc[0, metric_value]}", className='top-value')

    other_rows = [
        html.Div([
            html.Span(f"{i + 1}. {sorted_df.loc[i, name_column]}", className='other-name'),
            html.Span(f"{sorted_df.loc[i, metric_value]}", className='other-value'),
            html.Img(src=sorted_df.loc[i, logo_column], className='other-logo'),
        ], className='other-row') for i in range(1, len(sorted_df))
    ]

    card_content = html.Div([
        html.H3(metric_label, className='metric-label'),
        top_value,
        top_row,
        html.Div(other_rows, className='full-list-content')
    ], className='full-list-card', style={'width': '100%'})

    return card_content