from dash import html, dash_table, dcc
from common.utils import encode_image

import pandas as pd
import plotly.graph_objects as go

df_MLS23_table = pd.read_csv('assets/MLS_23_table.csv')

def get_columns(dataframe):
    columns = []
    for col in dataframe.columns:
        columns.append({"name": col, "id": col, 'presentation': 'markdown' if col == 'Team' else 'input'})
    return columns

def team_salaries(df):
    fig = go.Figure()

    for i, row in df.iterrows():
        fig.add_trace(go.Bar(
            x=[row['SalaryGuaranteed ($)']],
            y=[row['Team']],
            orientation='h',
            marker=dict(
                color=row['SecondaryColor'],
                line=dict(color=row['MainColor'], width=2)
            ),
            name=row['Team'],
            hoverinfo='x'
        ))

    fig.update_layout(
        title='Total Annual Salary by Team',
        yaxis=dict(
            tickmode='array',
            tickvals=list(range(len(df))),
            ticktext=df['Team']
        ),
        plot_bgcolor='white',
        showlegend=False,
        height=650,
        margin=dict(l=0, r=0, t=40, b=10),
    )

    fig.update_xaxes(showgrid=True, gridwidth=2, gridcolor='#cccccc')
    fig.update_yaxes(showgrid=True, gridwidth=2, tickfont=dict(size=13))

    return fig

fig_team_salaries = team_salaries(df_MLS23_table)

df_MLS23_table['logo'] = df_MLS23_table['Logo path'].str.replace('datasets/', 'assets/')
df_MLS23_table['Team'] = df_MLS23_table.apply(lambda x: f"<img src='{x['logo']}' style='height:22px; width:22px; margin-right: 5px; margin-left: 5px;'/> {x['Team']}", axis=1)

df_MLS23_table['Annual Salary'] = df_MLS23_table['SalaryGuaranteed ($)'].apply(lambda x: f"${x:,.0f}")

column_order = ["Pos", "Team", "Pld", "W", "L", "T", "GF", "GA", "GD", "Pts", "Annual Salary"]
df_MLS23_table_display = df_MLS23_table[column_order]

df_MLS23_table['EncodedLogo'] = df_MLS23_table['logo'].apply(encode_image)

def salary_vs_position(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Pos'],
        y=df['SalaryGuaranteed ($)'],
        mode='markers',
        marker=dict(size=1, opacity=0),
        hoverinfo='skip'
    ))

    for i, row in df.iterrows():
        fig.add_layout_image(
            dict(
                source=row['EncodedLogo'],
                x=row['Pos'],
                y=row['SalaryGuaranteed ($)'],
                xref="x",
                yref="y",
                sizex=1.7,
                sizey=1700000,
                xanchor="center",
                yanchor="middle"
            )
        )

    fig.update_layout(
        title='Final Standings vs. MLS Teams\' Annual Salary Budgets',
        xaxis=dict(title='Final Position', autorange='reversed'),
        plot_bgcolor='white',
        showlegend=False,
        height=650,
        margin=dict(l=40, r=40, t=40, b=40),
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#cccccc')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#cccccc')

    return fig

fig_salary_vs_position = salary_vs_position(df_MLS23_table)

layout = html.Div(className='data-table-container', children=[

    html.Div(className='table-section', children=[
        dash_table.DataTable(
            id='mls-table',
            columns=get_columns(df_MLS23_table_display),
            data=df_MLS23_table_display.to_dict('records'),
            style_table={'overflowX': 'auto'},
            page_size=30,
            sort_action='native',
            sort_mode='single',
            sort_by=[{'column_id': 'Pos', 'direction': 'asc'}],
            markdown_options={'html': True},
            style_data_conditional=[
                {
                    'if': {'filter_query': '{GD} < 0', 'column_id': 'GD'},
                    'color': 'red',
                },
                {
                    'if': {'filter_query': '{GD} >= 0', 'column_id': 'GD'},
                    'color': 'green',
                },
            ],
            tooltip_header={
                'Pld': 'Played',
                'W': 'Wins',
                'L': 'Losses',
                'T': 'Ties',
                'GF': 'Goals For',
                'GA': 'Goals Against',
                'GD': 'Goal Difference',
                'Pts': 'Points',
                'Annual Salary': 'Guaranteed Annual Salary'
            },
            style_cell={
                'textAlign': 'center',
                'borderLeft': '0px',
                'padding': '5px',
                'whiteSpace': 'normal',
                'fontSize': '16px'
            },
            style_header={
                'backgroundColor': '#F8F5F0',
                'fontWeight': 'bold',
                'padding': '5px',
                'fontSize': '18px'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Pos'}, 'width': '3%'},
                {'if': {'column_id': 'Team'}, 'width': '43%'},
                {'if': {'column_id': 'Pld'}, 'width': '3%'},
                {'if': {'column_id': 'W'}, 'width': '3%'},
                {'if': {'column_id': 'L'}, 'width': '3%'},
                {'if': {'column_id': 'T'}, 'width': '3%'},
                {'if': {'column_id': 'GF'}, 'width': '3%'},
                {'if': {'column_id': 'GA'}, 'width': '3%'},
                {'if': {'column_id': 'GD'}, 'width': '3%'},
                {'if': {'column_id': 'Pts'}, 'width': '3%'},
                {'if': {'column_id': 'Annual Salary'}, 'width': '25%'},
            ]
        )
    ]),

    html.Div(className='graphs-section', children=[
        html.Div([
            dcc.Graph(
                figure=fig_team_salaries, responsive=True,
                style={
                    'width': '100%',
                    'minWidth': '300px',
                    'height': 'auto'
                }),
        ], className='single-graph-container'),

        html.Div([
            dcc.Graph(
                figure=fig_salary_vs_position, responsive=True,
                style={
                    'width': '100%',
                    'minWidth': '300px',
                    'height': 'auto'
                }),
        ], className='single-graph-container'),
    ])
])
