import pandas as pd
from dash import html, dash_table, dcc

df_player_stats = pd.read_csv('../datasets/stats_player_mls.csv')
flags_iso = pd.read_csv('../datasets/flags_iso.csv')

# Map Alpha-3 codes to flag URLs
flags_dict = pd.Series(flags_iso.URL.values, index=flags_iso['Alpha-3 code']).to_dict()

def add_flag_to_nation(row):
    flag_url = flags_dict.get(row['nation'], '')
    if flag_url:
        return f"![flag]({flag_url}) {row['nation']}"
    else:
        return row['nation'] if pd.notna(row['nation']) else ''

# Add flag images to the nation column
df_player_stats['nation'] = df_player_stats.apply(lambda row: add_flag_to_nation(row), axis=1)

# Column groups and headers
column_groups = {
    "": ['Team', 'player', 'nation', 'pos', 'age', 'born'],
    "Playing Time": ['MP', 'Starts', 'Min', '90s'],
    "Performance": ['Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR'],
    "Expected": ['xG', 'npxG', 'xAG', 'npxG+xAG'],
    "Progression": ['PrgC', 'PrgP', 'PrgR'],
    "Per 90 Minutes": ['Gls/90', 'Ast/90', 'G+A/90', 'G-PK/90', 'G+A-PK/90', 'xG/90', 'xAG/90', 'xG+xAG/90', 'npxG/90', 'npxG+xAG/90']
}

def get_columns_with_headers(groups):
    columns = []
    for group, cols in groups.items():
        for col in cols:
            display_name = col.replace("/90", "") if group == "Per 90 Minutes" else col
            col_type = "numeric" if col not in ['Team', 'player', 'nation', 'pos'] else "text"
            
            column = {
                "name": [group, display_name], 
                "id": col, 
                "type": col_type,
            }
            
            if col == 'nation':
                column['presentation'] = 'markdown'
            
            columns.append(column)
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

filter_style = [
    {'if': {'column_id': col}, 'border-right': '3px solid #919191'}
    for group in column_groups for col in [column_groups[group][-1]]
]

layout = html.Div([
    html.Div([
        dash_table.DataTable(
            id='player-stats-table',
            columns=get_columns_with_headers(column_groups),
            data=df_player_stats_display.to_dict('records'),

            style_table={'overflowX': 'auto', 'width': '100%', 'minWidth': '100%'},
            style_cell={
                'textAlign': 'center',
                'whiteSpace': 'nowrap',
                'fontSize': '6px',
                'border': '1px solid #d3d3d3'
            },
            style_header={
                'backgroundColor': '#F8F5F0',
                'fontWeight': 'bold',
                'fontSize': '14px',
                'border': '1px solid #d3d3d3',
                'whiteSpace': 'nowrap'
            },
            style_filter={'height': '30px', 'fontSize': '14px'},

            # DataTable options
            page_size=30,
            filter_action="native",
            sort_action='native',
            sort_mode="multi",

            # Merge headers and apply styles
            merge_duplicate_headers=True,
            style_header_conditional=header_style,
            style_data_conditional=cell_style,
            style_filter_conditional=filter_style,

            filter_options={'placeholder_text': 'Filter'}, # 'case': 'insensitive', → Option deleted because it creates a filtering bug for integers

            tooltip_header={
                'nation': 'Nationality',
                'pos': 'Position',
                'born': 'Year Born',
                'MP': 'Matches Played',
                'Starts': 'Games Started by Player',
                'Min': 'Minutes Played',
                'Gls': 'Goals',
                'Ast': 'Assists',
                'G+A': 'Goals + Assists',
                'G-PK': 'Non-Penalty Goals',
                'PK': 'Penalty Kicks Made',
                'PKatt': 'Penalty Kicks Attempted',
                'CrdY': 'Yellow Cards',
                'CrdR': 'Red Cards',
                'xG': 'Expected Goals',
                'npxG': 'Non-Penalty Expected Goals',
                'xAG': 'Expected Assisted Goals',
                'npxG+xAG': 'Non-Penalty Expected Goals + Assisted Goals',
                'PrgC': 'Progressive Carries',
                'PrgP': 'Progressive Passes',
                'PrgR': 'Progressive Passes Received',
                'Gls/90': 'Goals per 90 minutes',
                'Ast/90': 'Assists per 90 minutes',
                'G+A/90': 'Goals + Assists per 90 minutes',
                'G-PK/90': 'Non-Penalty Goals per 90 minutes',
                'G+A-PK/90': 'Goals + Assists minus Penalty Kicks per 90 minutes',
                'xG/90': 'Expected Goals per 90 minutes',
                'xAG/90': 'Expected Assisted Goals per 90 minutes',
                'xG+xAG/90': 'Expected Goals + Assisted Goals per 90 minutes',
                'npxG/90': 'Non-Penalty Expected Goals per 90 minutes',
                'npxG+xAG/90': 'Non-Penalty Expected Goals + Assisted Goals per 90 minutes'
            },
        )
    ], style={'width': '100%'}),
], className='data-table-container')
