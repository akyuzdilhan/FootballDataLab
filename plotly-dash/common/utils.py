import base64

# TODO adapt color for the label. ex : Goal for in green and agaist in red
metrics = [
    {'label': 'Goals For', 'value': 'GF', 'color': '#ff6347', 'ascending': False},
    {'label': 'Goals Against', 'value': 'GA', 'color': '#ffa07a', 'ascending': True},
    {'label': 'Goal Difference', 'value': 'GD', 'color': '#20b2aa', 'ascending': False},
    {'label': 'Number of Players used in Games', 'value': '# Pl', 'color': '#8a2be2', 'ascending': True},
    {'label': 'Average Age', 'value': 'Age', 'color': '#5f9ea0', 'ascending': True},
    {'label': 'Possession', 'value': 'Poss', 'color': '#d2691e', 'ascending': False},
    {'label': 'Non-Penalty Goals', 'value': 'G-PK', 'color': '#ff4500', 'ascending': False},
    {'label': 'Penalty Kicks Made', 'value': 'PK', 'color': '#ffd700', 'ascending': False},
    {'label': 'Yellow Cards', 'value': 'CrdY', 'color': '#ffd700', 'ascending': True},
    {'label': 'Red Cards', 'value': 'CrdR', 'color': '#ff0000', 'ascending': True},
    {'label': 'Expected Goals', 'value': 'xG', 'color': '#32cd32', 'ascending': False},
    {'label': 'Non-Penalty xG', 'value': 'npxG', 'color': '#7cfc00', 'ascending': False},
    {'label': 'Progressive Carries', 'value': 'PrgC', 'color': '#00ced1', 'ascending': False},
    {'label': 'Progressive Passes', 'value': 'PrgP', 'color': '#4682b4', 'ascending': False},
    {'label': 'Number of games missed by players', 'value': 'total_missed_games', 'color': '#585857', 'ascending': True},
    {'label': 'Number of players missing at least one game', 'value': 'unique_players_missing', 'color': '#57472d', 'ascending': True},
    {'label': 'Number of games missed by  opponent players', 'value': 'total_missed_games_by_opponent', 'color': '#c08321', 'ascending': False},
]

player_metrics = [
    {'label': 'Matches Played', 'value': 'MP', 'ascending': False},
    {'label': 'Minutes Played', 'value': 'Min', 'ascending': False},
    {'label': 'Goals', 'value': 'Gls', 'ascending': False},
    {'label': 'Assists', 'value': 'Ast', 'ascending': False},
    {'label': 'Goals + Assists', 'value': 'G+A', 'ascending': False},
    {'label': 'Non-Penalty Goals', 'value': 'G-PK', 'ascending': False},
    {'label': 'Penalty Goals', 'value': 'PK', 'ascending': False},
    {'label': 'Penalty Attempted', 'value': 'PKatt', 'ascending': False},
    {'label': 'Yellow Cards', 'value': 'CrdY', 'ascending': True},
    {'label': 'Red Cards', 'value': 'CrdR', 'ascending': True},
    {'label': 'Expected Goals', 'value': 'xG', 'ascending': False},
    {'label': 'Non-Penalty xG', 'value': 'npxG', 'ascending': False},
    {'label': 'Expected Assists', 'value': 'xAG', 'ascending': False},
    {'label': 'npxG + xAG', 'value': 'npxG+xAG', 'ascending': False},
    {'label': 'Progressive Carries', 'value': 'PrgC', 'ascending': False},
    {'label': 'Progressive Passes', 'value': 'PrgP', 'ascending': False},
    {'label': 'Progressive Passes Rec', 'value': 'PrgR', 'ascending': False},
    {'label': 'Goals per 90\'', 'value': 'Gls/90', 'ascending': False},
    {'label': 'Assists per 90\'', 'value': 'Ast/90', 'ascending': False},
    {'label': 'G+A per 90\'', 'value': 'G+A/90', 'ascending': False},
    {'label': 'G-PK per 90\'', 'value': 'G-PK/90', 'ascending': False},
    {'label': 'G+A-PK per 90\'', 'value': 'G+A-PK/90', 'ascending': False},
    {'label': 'xG per 90\'', 'value': 'xG/90', 'ascending': False},
    {'label': 'xAG per 90\'', 'value': 'xAG/90', 'ascending': False},
    {'label': 'xG+xAG per 90\'', 'value': 'xG+xAG/90', 'ascending': False},
    {'label': 'npxG per 90\'', 'value': 'npxG/90', 'ascending': False},
    {'label': 'npxG+xAG per 90\'', 'value': 'npxG+xAG/90', 'ascending': False},
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