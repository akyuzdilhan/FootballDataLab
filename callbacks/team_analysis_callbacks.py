from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

from dash import html
from common.utils import metrics
from layouts.team_analysis import plot_team_radar, plot_Xgoal_performance, plot_distribution, get_metric_label_and_color

def register_callbacks(app, df_team_stats):

    @app.callback(
        [Output('distribution-graph', 'figure'),
         Output('metric-2-dropdown', 'options')],
        [Input('metric-1-dropdown', 'value'),
         Input('metric-2-dropdown', 'value'),
         Input('team-dropdown', 'value')]
    )
    def update_graph_and_dropdown(metric1, metric2, selected_teams):
        fig = plot_distribution(df_team_stats, metric1, metric2, selected_teams)
        updated_options = [{'label': item['label'], 'value': item['value']} for item in metrics if item['value'] != metric1]
        return fig, updated_options

    @app.callback(
        Output('metric-2-dropdown', 'value'),
        [Input('metric-1-dropdown', 'value')],
        [State('metric-2-dropdown', 'value')]
    )
    def clear_metric2_if_conflict(metric1, metric2):
        if metric1 == metric2:
            return ''
        return metric2

    @app.callback(
        Output('team-radar-graph', 'figure'),
        [Input('team-dropdown', 'value')]
    )
    def update_team_radar(selected_teams):
        return plot_team_radar(df_team_stats, selected_teams)
    
    @app.callback(
        Output('team-analysis-graph', 'figure'),
        [Input('team-dropdown', 'value')]
    )
    def update_team_analysis_graph(selected_teams):
        return plot_Xgoal_performance(df_team_stats, selected_teams)

    @app.callback(
        [Output('color-info-metric1', 'children'),
         Output('color-info-metric2', 'children')],
        [Input('metric-1-dropdown', 'value'),
         Input('metric-2-dropdown', 'value')]
    )
    def update_color_info(metric1, metric2):
        metric1_label, metric1_color = get_metric_label_and_color(metric1)
        metric2_label, metric2_color = get_metric_label_and_color(metric2)
        
        color_info1 = html.Div([
            html.Div(style={'width': '20px', 'height': '20px', 'backgroundColor': metric1_color, 'display': 'inline-block'}) if metric1_label else None,
            html.Span(f' {metric1_label}', style={'paddingLeft': '5px'}) if metric1_label else None
        ])
        color_info2 = html.Div([
            html.Div(style={'width': '20px', 'height': '20px', 'backgroundColor': metric2_color, 'display': 'inline-block'}) if metric2_label else None,
            html.Span(f' {metric2_label}', style={'paddingLeft': '5px'}) if metric2_label else None
        ])
        return color_info1, color_info2