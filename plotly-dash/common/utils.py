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
]

def encode_image(image_file):
    try:
        encoded = base64.b64encode(open(image_file, 'rb').read())
        return 'data:image/png;base64,{}'.format(encoded.decode())
    except FileNotFoundError:
        return None