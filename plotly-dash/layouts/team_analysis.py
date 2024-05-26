import pandas as pd
import base64
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from mplsoccer import Radar, FontManager, grid
from dash import html, dcc, Dash
from dash.dependencies import Input, Output

def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())

df_team_stats = pd.read_csv('../datasets/squad_stats_FBref.csv')

df_team_stats['logo'] = df_team_stats['Logo path'].str.replace('datasets/', 'assets/')
df_team_stats['EncodedLogo'] = df_team_stats['logo'].apply(encode_image)

def plot_Xgoal_performance(df_team_stats):
    fig = go.Figure()

    # Scatter plot
    fig.add_trace(go.Scatter(
        x=df_team_stats['Diff_Gls vs'],
        y=df_team_stats['Diff_Gls'],
        mode='markers',
        marker=dict(size=1, opacity=0),
        hoverinfo='skip'
    ))

    # Adding images
    for i, row in df_team_stats.iterrows():
        fig.add_layout_image(
            dict(
                source=row['EncodedLogo'],
                x=row['Diff_Gls vs'],
                y=row['Diff_Gls'],
                xref="x",
                yref="y",
                sizex=1.7,
                sizey=1.7,
                xanchor="center",
                yanchor="middle"
            )
        )

    # Average lines
    fig.add_shape(
        type="line",
        x0=0, y0=df_team_stats['Diff_Gls'].min(),
        x1=0, y1=df_team_stats['Diff_Gls'].max(),
        line=dict(color='black', width=1, dash='dash')
    )
    fig.add_shape(
        type="line",
        x0=df_team_stats['Diff_Gls vs'].min(), y0=0,
        x1=df_team_stats['Diff_Gls vs'].max(), y1=0,
        line=dict(color='black', width=1, dash='dash')
    )

    # Annotations
    fig.add_annotation(x=df_team_stats['Diff_Gls vs'].min(), y=df_team_stats['Diff_Gls'].max() - 2,
                       text='Offensive efficiency but not defensive', showarrow=False, font=dict(size=13))
    fig.add_annotation(x=df_team_stats['Diff_Gls vs'].max(), y=df_team_stats['Diff_Gls'].min() + 2,
                       text='Defensive efficiency but not offensive', showarrow=False, font=dict(size=13))
    fig.add_annotation(x=df_team_stats['Diff_Gls vs'].max(), y=df_team_stats['Diff_Gls'].max() - 2,
                       text='Defensive and offensive efficiency', showarrow=False, font=dict(size=13))
    fig.add_annotation(x=df_team_stats['Diff_Gls vs'].min(), y=df_team_stats['Diff_Gls'].min() + 2,
                       text='Defensive and offensive inefficiency', showarrow=False, font=dict(size=13))

    # Updating layout
    fig.update_layout(
        title='XG Performance, MLS 2023',
        xaxis_title='Expected Goals Difference Against',
        yaxis_title='Expected Goals Difference For',
        plot_bgcolor='#f8f5f0',
        paper_bgcolor='#f8f5f0',
        font=dict(family='sans-serif', color='black'),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#ccc8c8', zeroline=False),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#ccc8c8', zeroline=False),
        width=900,
        height=750
    )

    return fig

def plot_team_radar(df_team_stats):
    categories = ['Age', 'Poss', 'Gls', 'xG', 'PK', 'CrdY', 'CrdR', 'PrgC', 'PrgP']
    ranges = {category: (df_team_stats[category].min(), df_team_stats[category].max()) for category in categories}

    fig = go.Figure()

    for index, row in df_team_stats.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[(row[category] - ranges[category][0]) / (ranges[category][1] - ranges[category][0]) for category in categories],
            theta=categories,
            fill='toself',
            name=df_team_stats.iloc[index]['Team']
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            ),
            angularaxis=dict(
                tickvals=[i for i in range(len(categories))],
                ticktext=[f'{cat} ({ranges[cat][0]:.2f}-{ranges[cat][1]:.2f})' for cat in categories]
            )
        ),
        showlegend=True,
        title="Team Performance Radar",
        width=900,
        height=700
    )

    return fig

layout = html.Div([
    html.Div([
        dcc.Graph(id='team-analysis-graph', figure=plot_Xgoal_performance(df_team_stats))
    ], style={'display': 'inline-block', 'width': '50%'}),
    html.Div([
        dcc.Graph(id='team-radar-graph', figure=plot_team_radar(df_team_stats))
    ], style={'display': 'inline-block', 'width': '50%'})
])
