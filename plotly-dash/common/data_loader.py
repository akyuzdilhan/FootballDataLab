import os
import pandas as pd
from common.utils import encode_image

# Singleton-style loader
df_team_stats = None
df_player_stats = None

def load_team_stats():
    global df_team_stats
    def load_and_process_team_stats():
        df = pd.read_csv('assets/stats_team_mls.csv')
        df['logo'] = df['Logo path'].str.replace('datasets/', 'assets/')
        df['EncodedLogo'] = df['logo'].apply(encode_image)
        return df

    if df_team_stats is None:
        df_team_stats = load_and_process_team_stats()
    return df_team_stats

def load_player_stats():
    global df_player_stats
    def load_and_process_player_stats():
        df = pd.read_csv('assets/stats_player_mls.csv')
        df['local_image_path'] = df['local_image_path'].str.replace('plotly-dash/', '')
        df['encoded_image'] = df['local_image_path'].apply(encode_image)
        return df

    if df_player_stats is None:
        df_player_stats = load_and_process_player_stats()
    return df_player_stats

def load_match_events(match_id: int) -> pd.DataFrame:
    path = os.path.join('assets', f'match_{match_id}', 'events.csv')
    df = pd.read_csv(path)
    return df


def load_match_players(match_id: int) -> list:
    df = load_match_events(match_id)
    return sorted(df['player_name'].dropna().unique().tolist())