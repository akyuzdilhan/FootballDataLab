from dash import html, dash_table, dcc
import pandas as pd
import plotly.graph_objects as go
import base64

# Load dataset
df_MLS23_table = pd.read_csv('../datasets/MLS_23_table.csv')
df_team_expenses = pd.read_csv('../datasets/MLS_team_colors.csv')

# Encode images in base64
def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())

# Table params
df_MLS23_table['logo'] = df_MLS23_table['Logo path'].str.replace('datasets/', 'assets/')
df_MLS23_table['Team'] = df_MLS23_table.apply(lambda x: f"<img src='{x['logo']}' style='height:22px; width:22px; margin-right: 5px; margin-left: 5px;'/> {x['Team']}", axis=1)
df_MLS23_table['GD'] = df_MLS23_table['GD'].replace({'−': '-'}, regex=True)
df_MLS23_table['GD'] = pd.to_numeric(df_MLS23_table['GD'])
df_MLS23_table['Salary'] = df_MLS23_table['SalaryGuaranteed ($)'].apply(lambda x: f"${x:,.0f}")

column_order = ["Pos", "Team", "Pld", "W", "L", "T", "GF", "GA", "GD", "Pts", "Salary"]
df_MLS23_table_display = df_MLS23_table[column_order]

# 'Salary vs Position' params
df_MLS23_table['EncodedLogo'] = df_MLS23_table['logo'].apply(encode_image)

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
        title='Total Salary by Team',
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

def salary_vs_position(df):
    fig = go.Figure()

    # Scatter plot with invisible markers
    fig.add_trace(go.Scatter(
        x=df['Pos'],
        y=df['SalaryGuaranteed ($)'],
        mode='markers',
        marker=dict(size=1, opacity=0),
        hoverinfo='skip'
    ))

    # Images as layout images
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
        title='Final Standings vs. MLS Teams\' Salary Budgets',
        xaxis=dict(title='Final Position', autorange='reversed'),
        plot_bgcolor='white',
        showlegend=False,
        height=650,
        margin=dict(l=40, r=40, t=40, b=40),
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#cccccc')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#cccccc')

    return fig

fig_team_salaries = team_salaries(df_team_expenses)
fig_salary_vs_position = salary_vs_position(df_MLS23_table)

layout = html.Div([
    html.Div([
        dash_table.DataTable(
            id='mls-table',
            columns=get_columns(df_MLS23_table_display),
            data=df_MLS23_table_display.to_dict('records'),
            style_table={'overflowX': 'auto'},
            page_size=30,
            sort_action='native',
            sort_mode="single",
            sort_by=[{'column_id': 'Pos', 'direction': 'asc'}],
            markdown_options={'html': True},
            style_data_conditional=(
                [
                    {
                        'if': {
                            'filter_query': '{GD} < 0',
                            'column_id': 'GD'
                        },
                        'color': 'red',
                    },
                    {
                        'if': {
                            'filter_query': '{GD} >= 0',
                            'column_id': 'GD'
                        },
                        'color': 'green',
                    },
                ]
            ),
            tooltip_header={
                'Pld': 'Played',
                'W': 'Wins',
                'L': 'Losses',
                'T': 'Ties',
                'GF': 'Goals For',
                'GA': 'Goals Against',
                'GD': 'Goal Difference',
                'Pts': 'Points',
                'Salary': 'Guaranteed Salary'
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
                'border': '0px',
                'padding': '5px',
                'fontSize': '18px'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Pos'}, 'width': '3%'},
                {'if': {'column_id': 'Team'}, 'width': '40%'},
                {'if': {'column_id': 'Pld'}, 'width': '3%'},
                {'if': {'column_id': 'W'}, 'width': '3%'},
                {'if': {'column_id': 'L'}, 'width': '3%'},
                {'if': {'column_id': 'T'}, 'width': '3%'},
                {'if': {'column_id': 'GF'}, 'width': '3%'},
                {'if': {'column_id': 'GA'}, 'width': '3%'},
                {'if': {'column_id': 'GD'}, 'width': '3%'},
                {'if': {'column_id': 'Pts'}, 'width': '3%'},
                {'if': {'column_id': 'Salary'}, 'width': '28%'},
            ]
        )
    ], style={'width': '43%', 'float': 'left'}),
    html.Div([
        html.Div([
            dcc.Graph(figure=fig_team_salaries),
        ], style={'padding': '10px', 'backgroundColor': '#F8F5F0', 'marginBottom': '10px'}),
        html.Div([
            dcc.Graph(figure=fig_salary_vs_position),
        ], style={'padding': '10px', 'backgroundColor': '#F8F5F0'}),
    ], style={'width': '57%', 'float': 'right'}),
], className='data-table-container')
