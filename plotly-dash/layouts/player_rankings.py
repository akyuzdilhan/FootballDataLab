from dash import html
from common.layout_helpers import load_player_data, create_global_stats_layout, create_stat_card, create_layout_with_cards
from common.utils import player_metrics
from callbacks.rankings_callbacks import register_rankings_callbacks

def create_layout():
    df_team_stats, df_player_stats, global_stats = load_player_data()
    global_stats_layout = create_global_stats_layout(global_stats)

    stat_cards = [
        create_stat_card(
            metric, index, df_player_stats.sort_values(by=metric['value'], ascending=metric.get('ascending', False)).reset_index(drop=True),
            'encoded_image', 'player', id_prefix='player-view-full-list-button'
        )
        for index, metric in enumerate(player_metrics)
    ]

    return create_layout_with_cards(global_stats_layout, stat_cards, 'full-list-container')
