import base64

# TODO adapt color for the label. ex : Goal for in green and agaist in red
metrics = [
    {'label': 'Goals For', 'value': 'GF', 'color': '#ff6347'},
    {'label': 'Goals Against', 'value': 'GA', 'color': '#ffa07a'},
    {'label': 'Goal Difference', 'value': 'GD', 'color': '#20b2aa'},
    {'label': 'Number of Players used in Games', 'value': '# Pl', 'color': '#8a2be2'},
    {'label': 'Average Age', 'value': 'Age', 'color': '#5f9ea0'},
    {'label': 'Possession', 'value': 'Poss', 'color': '#d2691e'},
    {'label': 'Non-Penalty Goals', 'value': 'G-PK', 'color': '#ff4500'},
    {'label': 'Penalty Kicks Made', 'value': 'PK', 'color': '#ffd700'},
    {'label': 'Yellow Cards', 'value': 'CrdY', 'color': '#ffd700'},
    {'label': 'Red Cards', 'value': 'CrdR', 'color': '#ff0000'},
    {'label': 'Expected Goals', 'value': 'xG', 'color': '#32cd32'},
    {'label': 'Non-Penalty xG', 'value': 'npxG', 'color': '#7cfc00'},
    {'label': 'Progressive Carries', 'value': 'PrgC', 'color': '#00ced1'},
    {'label': 'Progressive Passes', 'value': 'PrgP', 'color': '#4682b4'},
]

def encode_image(image_file):
    try:
        encoded = base64.b64encode(open(image_file, 'rb').read())
        return 'data:image/png;base64,{}'.format(encoded.decode())
    except FileNotFoundError:
        return None