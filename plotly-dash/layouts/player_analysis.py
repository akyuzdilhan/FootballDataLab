import pandas as pd
from dash import html, dash_table, dcc, Dash
from dash.dash_table.Format import Format

df_player_stats = pd.read_csv('../datasets/player_stats_FBref.csv')
flags_iso = pd.read_csv('../datasets/flags_iso.csv')

# Map Alpha-3 codes to flag URLs
flags_dict = pd.Series(flags_iso.URL.values, index=flags_iso['Alpha-3 code']).to_dict()

def add_flag_to_nation(row):
    flag_url = flags_dict.get(row['nation'], '')
    if flag_url:
        return f"![flag]({flag_url}) {row['nation']}"

# Add flag images to the nation column
df_player_stats['nation'] = df_player_stats.apply(lambda row: add_flag_to_nation(row) if pd.notna(row['nation']) else '', axis=1)

# Column groups and headers
column_groups = {
    "": ['team', 'player', 'nation', 'pos', 'age', 'born'],
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
            col_type = "numeric" if col not in ['team', 'player', 'nation', 'pos', 'age', 'born'] else "text"
            presentation = 'markdown' if col == 'nation' else 'input'
            columns.append({
                "name": [group, display_name], 
                "id": col, 
                "type": col_type,
                "format": Format(nully=''), 
                "presentation": presentation
            })
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
            filter_options={'height': '30px', 'fontSize': '20px', "placeholder_text": "filter", "case": "insensitive"},
            style_cell={'textAlign': 'center', 'whiteSpace': 'nowrap', 'fontSize': '6px', 'border': '1px solid #d3d3d3'},
            style_header={'backgroundColor': '#F8F5F0', 'fontWeight': 'bold', 'fontSize': '14px', 'border': '1px solid #d3d3d3', 'whiteSpace': 'nowrap'},

            page_size=30,
            filter_action="native",
            sort_action='native',
            sort_mode="multi",

            merge_duplicate_headers=True,
            style_header_conditional=header_style,
            style_data_conditional=cell_style,
            style_filter_conditional=filter_style,
            tooltip_header={ # TODO apply the metrics from utils
                'nation': 'Nationality',
                'pos': 'Position',
                'born': 'Year Born',
                'MP': 'Matches Played',
                'Starts': 'Game or games started by player',
                'Min': 'Minutes Played',
                'Gls': 'Goals',
                'Ast': 'Assists',
                'G+A': 'Goals + Assists',
                'G-PK': 'Non-Penalty Goals',
                'PK': 'Penalty Kicks Made',
                'PKatt': 'Penalty Kicks Attempted',
                'CrdY': 'Yellow Cards',
                'CrdR': 'Red Cards',
                'xG': 'xG: Expected Goals',
                'npxG': 'npxG: Non-Penalty xG',
                'xAG': 'xAG: Exp. Assisted Goals',
                'npxG+xAG': 'Non-Penalty Expected Goals + Assists',
                'PrgC': 'Progressive Carries',
                'PrgP': 'Progressive Passes',
                'PrgR': 'Progressive Passes Rec',
                'Gls/90': 'Goals per 90 minutes',
                'Ast/90': 'Assists per 90 minutes',
                'G+A/90': 'Goals + Assists per 90 minutes',
                'G-PK/90': 'Non-Penalty Goals per 90 minutes',
                'G+A-PK/90': 'Goals plus Assists minus Penalty Kicks made per 90 minutes',
                'xG/90': 'Expected Goals per 90 minutes',
                'xAG/90': 'Expected Assisted Goals per 90 minutes',
                'xG+xAG/90': 'Expected Goals plus Assisted Goals per 90 minutes',
                'npxG/90': 'Non-Penalty Expected Goals per 90 minutes',
                'npxG+xAG/90': 'Non-Penalty Expected Goals plus Assisted Goals per 90 minutes'
            },
        )
    ], style={'width': '100%'}),
], className='data-table-container')
