import pandas as pd
from dash import html, dash_table

df_player_stats = pd.read_csv('../datasets/player_stats_FBref.csv')

# Column groups and headers
column_groups = {
    "": ['team', 'player', 'nation', 'pos', 'age', 'born'],
    "Playing Time": ['MP', 'Starts', 'Min', '90s'],
    "Performance": ['Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR'],
    "Expected": ['xG', 'npxG', 'xAG', 'npxG+xAG'],
    "Progression": ['PrgC', 'PrgP', 'PrgR'],
    "Per 90 Minutes": ['Gls', 'Ast', 'G+A', 'G-PK', 'G+A-PK', 'xG', 'xAG', 'xG+xAG', 'npxG', 'npxG+xAG']
}

def get_columns_with_headers(groups):
    columns = []
    for group, cols in groups.items():
        for col in cols:
            col_name = col.replace("/90", "") if group == "Per 90 Minutes" else col
            columns.append({"name": [group, col_name], "id": col})
    return columns
df_player_stats_display = df_player_stats.copy()

# Distinguishing separator for column groups
header_style = [
    {'if': {'header_index': 1, 'column_id': col}, 'border-right': '3px solid #919191'}
    for group in column_groups for col in [column_groups[group][-1]]
]
# Group separators for first-level headers
group_separator_style = [
    {'if': {'header_index': 0, 'column_id': col}, 'border-right': '3px solid #919191'}
    for group in column_groups for col in column_groups[group]
]
header_style.extend(group_separator_style)

cell_style = [
    {'if': {'column_id': col}, 'border-right': '3px solid #919191'} 
    for group in column_groups for col in [column_groups[group][-1]]
]

layout = html.Div([
    html.Div([
        dash_table.DataTable(
            id='player-stats-table',
            columns=get_columns_with_headers(column_groups),
            data=df_player_stats_display.to_dict('records'),
            style_table={'overflowX': 'auto', 'width': '98%', 'margin': 'auto'},
            page_size=30,
            sort_action='native',
            sort_mode="single",
            merge_duplicate_headers=True,
            style_header_conditional=header_style,
            style_data_conditional=cell_style,
            tooltip_header={
                'team': 'Team',
                'player': 'Player',
                'nation': 'Nationality',
                'pos': 'Position',
                'age': 'Age',
                'born': 'Year Born',
                'MP': 'Matches Played',
                'Starts': 'Starts',
                'Min': 'Minutes Played',
                'Gls': 'Goals',
                'Ast': 'Assists',
                'G+A': 'Goals + Assists',
                'G-PK': 'Goals - Penalty Kicks',
                'PK': 'Penalty Kicks Made',
                'PKatt': 'Penalty Kicks Attempted',
                'CrdY': 'Yellow Cards',
                'CrdR': 'Red Cards',
                'xG': 'Expected Goals',
                'npxG': 'Non-Penalty Expected Goals',
                'xAG': 'Expected Assists',
                'npxG+xAG': 'Non-Penalty Expected Goals + Assists',
                'PrgC': 'Progressive Carries',
                'PrgP': 'Progressive Passes',
                'PrgR': 'Progressive Runs'
            },
            style_cell={
                'textAlign': 'center',
                'whiteSpace': 'normal',
                'fontSize': '15px',
                'border': '1px solid #d3d3d3'
            },
            style_header={
                'backgroundColor': '#F8F5F0',
                'fontWeight': 'bold',
                'fontSize': '17px',
                'border': '1px solid #d3d3d3',
            },
        )
    ], style={'width': '100%', 'padding': '2'}),
], className='data-table-container')
