import pandas as pd
import plotly.graph_objects as go

from common.utils import metrics
from dash import html, dcc

PLOT_BG_COLOR = '#f8f5f0'
PAPER_BG_COLOR = '#f8f5f0'
FONT_FAMILY = 'sans-serif'
FONT_COLOR = 'black'
PLOT_WIDTH = 900
PLOT_HEIGHT = 750

df_team_stats = pd.read_csv('assets/stats_team_mls.csv')

def plot_Xgoal_performance(df, selected_teams):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df['Diff_Gls vs'],
            y=df['Diff_Gls'],
            mode='markers',
            marker=dict(size=1, opacity=0),
            hoverinfo='skip'
        )
    )

    for _, row in df.iterrows():
        img_size = 1.7 if row['Team'] not in selected_teams else 2.2
        img_opacity = 0.65 if row['Team'] not in selected_teams else 1
        fig.add_layout_image(
            dict(
                source=row['EncodedLogo'],
                x=row['Diff_Gls vs'],
                y=row['Diff_Gls'],
                opacity=img_opacity,
                xref="x",
                yref="y",
                sizex=img_size,
                sizey=img_size,
                xanchor="center",
                yanchor="middle"
            )
        )

    fig.add_shape(
        type="line",
        x0=0, y0=df['Diff_Gls'].min(),
        x1=0, y1=df['Diff_Gls'].max(),
        line=dict(color='black', width=1, dash='dash')
    )
    fig.add_shape(
        type="line",
        x0=df['Diff_Gls vs'].min(), y0=0,
        x1=df['Diff_Gls vs'].max(), y1=0,
        line=dict(color='black', width=1, dash='dash')
    )

    fig.add_annotation(x=df['Diff_Gls vs'].min(), y=df['Diff_Gls'].max() - 2,
                       text='Offensive efficiency but not defensive', showarrow=False, font=dict(size=13))
    fig.add_annotation(x=df['Diff_Gls vs'].max(), y=df['Diff_Gls'].min() + 2,
                       text='Defensive efficiency but not offensive', showarrow=False, font=dict(size=13))
    fig.add_annotation(x=df['Diff_Gls vs'].max(), y=df['Diff_Gls'].max() - 2,
                       text='Defensive and offensive efficiency', showarrow=False, font=dict(size=13))
    fig.add_annotation(x=df['Diff_Gls vs'].min(), y=df['Diff_Gls'].min() + 2,
                       text='Defensive and offensive inefficiency', showarrow=False, font=dict(size=13))

    fig.update_layout(
        title='XG Performance',
        xaxis_title='Expected Goals Difference Against',
        yaxis_title='Expected Goals Difference For',
        plot_bgcolor=PLOT_BG_COLOR,
        paper_bgcolor=PAPER_BG_COLOR,
        font=dict(family=FONT_FAMILY, color=FONT_COLOR),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#ccc8c8', zeroline=False),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#ccc8c8', zeroline=False),
        margin=dict(l=0, r=0, t=40, b=0),
        autosize=True,
    )
    return fig

def plot_team_radar(df, selected_teams):
    categories = ['Age', 'Poss', 'Gls', 'xG', 'PK', 'CrdY', 'CrdR', 'PrgC', 'PrgP']
    ranges = {
        category: (df[category].min() * 0.8, df[category].max() * 1.1)
        for category in categories
    }

    fig = go.Figure()

    if not selected_teams:
        fig.add_annotation(
            text="No team selected", 
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20, family=FONT_FAMILY, color=FONT_COLOR),
            xref="paper", yref="paper", align="center"
        )
    else:
        for team in selected_teams:
            row = df[df['Team'] == team].iloc[0]
            normalized_values = [
                (row[cat] - ranges[cat][0]) / (ranges[cat][1] - ranges[cat][0])
                for cat in categories
            ]
            actual_values = [row[cat] for cat in categories]

            fig.add_trace(
                go.Scatterpolar(
                    r=normalized_values + [normalized_values[0]],
                    theta=categories + [categories[0]],
                    fill='toself',
                    name=row['Team'],
                    customdata=actual_values + [actual_values[0]],
                    hovertemplate='<b>%{customdata:.2f}</b><extra></extra>'
                )
            )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, range=[0, 1],
                showgrid=True, showline=False, showticklabels=False,
            )
        ),
        plot_bgcolor=PLOT_BG_COLOR,
        paper_bgcolor=PAPER_BG_COLOR,
        showlegend=True,
        title="Team Performance Radar",
        font=dict(family=FONT_FAMILY, color=FONT_COLOR),
        margin=dict(l=0, r=0, t=40, b=0),
        autosize=True,
    )
    return fig

def get_metric_label_and_color(value):
    for metric in metrics:
        if metric['value'] == value:
            return metric['label'], metric['color']
    return value, '#000000'

def plot_distribution(df, metric1=None, metric2=None, selected_teams=None):
    data = []
    tickvals = df['Team'].tolist()
    ticktext = []

    if metric1:
        metric1_label, metric1_color = get_metric_label_and_color(metric1)
        data.append(go.Bar(
            name=metric1_label,
            x=df['Team'],
            y=df[metric1],
            marker_color=metric1_color,
            hovertemplate='%{x}: %{y}<extra></extra>'
        ))
    if metric2:
        metric2_label, metric2_color = get_metric_label_and_color(metric2)
        data.append(go.Bar(
            name=metric2_label,
            x=df['Team'],
            y=df[metric2],
            marker_color=metric2_color,
            hovertemplate='%{x}: %{y}<extra></extra>'
        ))

    for team in tickvals:
        if team in selected_teams:
            ticktext.append(f'<b><span style="color:red;">{team}</span></b>')
        else:
            ticktext.append(team)

    title = f'{metric1_label}' + (f' and {metric2_label}' if metric2 else '') + ' Distribution'
    fig = go.Figure(data=data)
    fig.update_layout(
        title=title,
        xaxis=dict(
            title='Team',
            tickvals=tickvals,
            ticktext=ticktext
        ),
        barmode='group',
        plot_bgcolor=PLOT_BG_COLOR,
        paper_bgcolor=PAPER_BG_COLOR,
        font=dict(family=FONT_FAMILY, color=FONT_COLOR),
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
        autosize=True,
    )
    return fig

def plot_possession_progressive_actions(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Poss'],
        y=df['PrgC'],
        mode='markers',
        marker=dict(size=15, color=df['PrgP'], colorscale='Viridis', showscale=True),
        text=df['Team']
    ))
    fig.update_layout(
        title='Possession vs Progressive Actions',
        xaxis_title='Possession (%)',
        yaxis_title='Progressive Carries',
        plot_bgcolor=PLOT_BG_COLOR,
        paper_bgcolor=PAPER_BG_COLOR,
        font=dict(family=FONT_FAMILY, color=FONT_COLOR),
        coloraxis_colorbar=dict(title='Progressive Passes'),
        margin=dict(l=0, r=0, t=40, b=0),
    )
    return fig

layout = html.Div(className='team-analysis-container', children=[

    html.Div(className='team-select-row', children=[
        html.Label('Select Teams:', className='team-select-label'),
        dcc.Dropdown(
            id='team-dropdown',
            options=[{'label': t, 'value': t} for t in df_team_stats['Team'].unique()],
            multi=True,
            value=['Toronto FC'],
            className='team-select-dropdown'
        ),
    ]),

    html.Div(className='graphs-row', children=[
        dcc.Graph(
            id='team-analysis-graph',
            className='graph-col',
            config={"responsive": True}, 
            style={"width": "100%", "minWidth": "300px", "height": "100%", "minHeight": "450px"}
        ),
        dcc.Graph(
            id='team-radar-graph',
            className='graph-col',
            config={"responsive": True}, 
            style={"width": "100%", "minWidth": "300px", "height": "100%", "minHeight": "450px"}
        ),
    ]),

    html.Div(className='distribution-row', children=[
        html.Div(className='distribution-metrics-sidebar', children=[
            html.H3('Metrics Selection', className='distribution-metrics-title'),

            html.Div(className='distribution-metric-row', children=[
                html.Label('Metric 1:', className='distribution-metric-label'),
                dcc.Dropdown(
                    id='metric-1-dropdown',
                    options=[{'label': m['label'], 'value': m['value']} for m in metrics],
                    value='GF',
                    className='distribution-metric-dropdown'
                ),
            ]),

            html.Div(className='distribution-metric-row', children=[
                html.Label('Metric 2:', className='distribution-metric-label'),
                dcc.Dropdown(
                    id='metric-2-dropdown',
                    options=[{'label': m['label'], 'value': m['value']} for m in metrics],
                    className='distribution-metric-dropdown'
                ),
            ]),

            html.Div(id='color-info-metric1', className='distribution-color-info'),
            html.Div(id='color-info-metric2', className='distribution-color-info'),
        ]),


        html.Div(className='distribution-graph-container', children=[
            dcc.Graph(
                id='distribution-graph',
                config={"responsive": True},
                style={"width": "100%", "height": "450px", "margin": "0px"}
            ),
        ]),
    ]),

    html.Div(className='final-chart-row', children=[
        dcc.Graph(
            id='cards-distribution',
            figure=plot_possession_progressive_actions(df_team_stats),
            config={"responsive": True},
            style={"width": "100%", "minWidth": "300px", "height": "auto"},
        )
    ]),
])
