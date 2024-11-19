import base64

# TODO adapt color for the label. ex : Goal for in green and agaist in red
metrics = [
    {'label': 'Goals For', 'value': 'GF', 'color': '#ff6347', 'ascending': False, 'metric_type': 'team'},
    {'label': 'Goals Against', 'value': 'GA', 'color': '#ffa07a', 'ascending': True, 'metric_type': 'team'},
    {'label': 'Goal Difference', 'value': 'GD', 'color': '#20b2aa', 'ascending': False, 'metric_type': 'team'},
    {'label': 'Number of Players used in Games', 'value': '# Pl', 'color': '#8a2be2', 'ascending': True, 'metric_type': 'team'},
    {'label': 'Average Age', 'value': 'Age', 'color': '#5f9ea0', 'ascending': True, 'metric_type': 'team'},
    {'label': 'Possession', 'value': 'Poss', 'color': '#d2691e', 'ascending': False, 'metric_type': 'team'},
    {'label': 'Non-Penalty Goals', 'value': 'G-PK', 'color': '#ff4500', 'ascending': False, 'metric_type': 'team'},
    {'label': 'Penalty Kicks Made', 'value': 'PK', 'color': '#ffd700', 'ascending': False, 'metric_type': 'team'},
    {'label': 'Yellow Cards', 'value': 'CrdY', 'color': '#ffd700', 'ascending': True, 'metric_type': 'team'},
    {'label': 'Red Cards', 'value': 'CrdR', 'color': '#ff0000', 'ascending': True, 'metric_type': 'team'},
    {'label': 'Expected Goals', 'value': 'xG', 'color': '#32cd32', 'ascending': False, 'metric_type': 'team'},
    {'label': 'Non-Penalty xG', 'value': 'npxG', 'color': '#7cfc00', 'ascending': False, 'metric_type': 'team'},
    {'label': 'Progressive Carries', 'value': 'PrgC', 'color': '#00ced1', 'ascending': False, 'metric_type': 'team'},
    {'label': 'Progressive Passes', 'value': 'PrgP', 'color': '#4682b4', 'ascending': False, 'metric_type': 'team'},
    {'label': 'Number of games missed by players', 'value': 'total_missed_games', 'color': '#585857', 'ascending': True, 'metric_type': 'team'},
    {'label': 'Number of players missing at least one game', 'value': 'unique_players_missing', 'color': '#57472d', 'ascending': True, 'metric_type': 'team'},
    {'label': 'Number of games missed by  opponent players', 'value': 'total_missed_games_by_opponent', 'color': '#c08321', 'ascending': False, 'metric_type': 'team'},
]

player_metrics = [
    {'label': 'Matches Played', 'value': 'MP', 'ascending': False, 'metric_type': 'player'},
    {'label': 'Minutes Played', 'value': 'Min', 'ascending': False, 'metric_type': 'player'},
    {'label': 'Goals', 'value': 'Gls', 'ascending': False, 'metric_type': 'player'},
    {'label': 'Assists', 'value': 'Ast', 'ascending': False, 'metric_type': 'player'},
    {'label': 'Goals + Assists', 'value': 'G+A', 'ascending': False, 'metric_type': 'player'},
    {'label': 'Non-Penalty Goals', 'value': 'G-PK', 'ascending': False, 'metric_type': 'player'},
    {'label': 'Penalty Goals', 'value': 'PK', 'ascending': False, 'metric_type': 'player'},
    {'label': 'Penalty Attempted', 'value': 'PKatt', 'ascending': False, 'metric_type': 'player'},
    {'label': 'Yellow Cards', 'value': 'CrdY', 'ascending': True, 'metric_type': 'player'},
    {'label': 'Red Cards', 'value': 'CrdR', 'ascending': True, 'metric_type': 'player'},
    {'label': 'Expected Goals', 'value': 'xG', 'ascending': False, 'metric_type': 'player'},
    {'label': 'Non-Penalty xG', 'value': 'npxG', 'ascending': False, 'metric_type': 'player'},
    {'label': 'Expected Assists', 'value': 'xAG', 'ascending': False, 'metric_type': 'player'},
    {'label': 'npxG + xAG', 'value': 'npxG+xAG', 'ascending': False, 'metric_type': 'player'},
    {'label': 'Progressive Carries', 'value': 'PrgC', 'ascending': False, 'metric_type': 'player'},
    {'label': 'Progressive Passes', 'value': 'PrgP', 'ascending': False, 'metric_type': 'player'},
    {'label': 'Progressive Passes Rec', 'value': 'PrgR', 'ascending': False, 'metric_type': 'player'},
    {'label': 'Goals per 90\'', 'value': 'Gls/90', 'ascending': False, 'metric_type': 'player'},
    {'label': 'Assists per 90\'', 'value': 'Ast/90', 'ascending': False, 'metric_type': 'player'},
    {'label': 'G+A per 90\'', 'value': 'G+A/90', 'ascending': False, 'metric_type': 'player'},
    {'label': 'G-PK per 90\'', 'value': 'G-PK/90', 'ascending': False, 'metric_type': 'player'},
    {'label': 'G+A-PK per 90\'', 'value': 'G+A-PK/90', 'ascending': False, 'metric_type': 'player'},
    {'label': 'xG per 90\'', 'value': 'xG/90', 'ascending': False, 'metric_type': 'player'},
    {'label': 'xAG per 90\'', 'value': 'xAG/90', 'ascending': False, 'metric_type': 'player'},
    {'label': 'xG+xAG per 90\'', 'value': 'xG+xAG/90', 'ascending': False, 'metric_type': 'player'},
    {'label': 'npxG per 90\'', 'value': 'npxG/90', 'ascending': False, 'metric_type': 'player'},
    {'label': 'npxG+xAG per 90\'', 'value': 'npxG+xAG/90', 'ascending': False, 'metric_type': 'player'},
]

def encode_image(image_file):
    try:
        encoded = base64.b64encode(open(image_file, 'rb').read())
        return 'data:image/png;base64,{}'.format(encoded.decode())
    except FileNotFoundError:
        return None

def calculate_global_stats(df):
    """Calculate the global statistics using only the team dataset."""
    return {
        "Goals per match": round(df['GF'].sum() / df['MP'].sum(), 2),
        "Number of players having played": int(df['# Pl'].sum()),
        "Average age": round(df['Age'].mean(), 1),
        "Matches missed by players": int(df['total_missed_games'].sum()),
        "Number of red cards": df['CrdR'].sum()
    }