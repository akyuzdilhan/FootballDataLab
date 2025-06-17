import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math

# Pitch dimensions
PITCH_LENGTH = 120
PITCH_WIDTH  = 80
LINE_COLOR   = '#444'
FIELD_COLOR  = 'rgba(0,0,0,0)'
LINE_WIDTH   = 2

def draw_pitch(fig=None):
    if fig is None:
        fig = go.Figure()

    fig.update_layout(
        width=900, height=600,
        margin=dict(l=20, r=20, t=0, b=0),
        plot_bgcolor=FIELD_COLOR,
        paper_bgcolor='white',
        xaxis=dict(visible=False, range=[0, PITCH_LENGTH], fixedrange=True),
        yaxis=dict(visible=False, range=[0, PITCH_WIDTH], scaleanchor='x', fixedrange=True),
        showlegend=True
    )

    shapes = []
    shapes.append(dict(
        type='rect', x0=0, y0=0, x1=PITCH_LENGTH, y1=PITCH_WIDTH,
        line=dict(color=LINE_COLOR, width=LINE_WIDTH), layer='below'
    ))
    shapes.append(dict(
        type='line',
        x0=PITCH_LENGTH/2, y0=0, x1=PITCH_LENGTH/2, y1=PITCH_WIDTH,
        line=dict(color=LINE_COLOR, width=LINE_WIDTH), layer='below'
    ))
    shapes.append(dict(
        type='circle',
        x0=PITCH_LENGTH/2-10, y0=PITCH_WIDTH/2-10,
        x1=PITCH_LENGTH/2+10, y1=PITCH_WIDTH/2+10,
        line=dict(color=LINE_COLOR, width=LINE_WIDTH), layer='below'
    ))
    shapes.append(dict(
        type='circle',
        x0=PITCH_LENGTH/2-0.3, y0=PITCH_WIDTH/2-0.3,
        x1=PITCH_LENGTH/2+0.3, y1=PITCH_WIDTH/2+0.3,
        fillcolor=LINE_COLOR, line=dict(width=0), layer='below'
    ))
    for x0, sign in [(0, +1), (PITCH_LENGTH, -1)]:
        shapes.append(dict(
            type='rect',
            x0=x0, y0=(PITCH_WIDTH-44)/2,
            x1=x0+sign*18, y1=(PITCH_WIDTH+44)/2,
            line=dict(color=LINE_COLOR, width=LINE_WIDTH), layer='below'
        ))
        shapes.append(dict(
            type='rect',
            x0=x0, y0=(PITCH_WIDTH-20)/2,
            x1=x0+sign*6, y1=(PITCH_WIDTH+20)/2,
            line=dict(color=LINE_COLOR, width=LINE_WIDTH), layer='below'
        ))
        px = x0 + sign*12
        shapes.append(dict(
            type='circle',
            x0=px-0.3, y0=PITCH_WIDTH/2-0.3,
            x1=px+0.3, y1=PITCH_WIDTH/2+0.3,
            fillcolor=LINE_COLOR, line=dict(width=0), layer='below'
        ))
        shapes.append(dict(
            type='path',
            path=f'M {px},{PITCH_WIDTH/2+10} A10,10 0 0,{"1" if sign>0 else "0"} {px},{PITCH_WIDTH/2-10}',
            line=dict(color=LINE_COLOR, width=LINE_WIDTH), layer='below'
        ))

    fig.update_layout(shapes=shapes)
    return fig


def make_pass_network_figure(events_df, player_name, successful_color='royalblue', unsuccessful_color='crimson'):
    df = events_df.query("type_name=='Pass' and player_name==@player_name")

    def segments(df_sub):
        xs, ys = [], []
        for _, r in df_sub.iterrows():
            xs += [r.x, r.end_x, np.nan]
            ys += [r.y, r.end_y, np.nan]
        return xs, ys

    xs_ok, ys_ok = segments(df[df.outcome_name.isna()])
    xs_ko, ys_ko = segments(df[df.outcome_name.notna()])

    fig = draw_pitch()

    # Successful passes - lines
    fig.add_trace(go.Scatter(
        x=xs_ok, y=ys_ok, mode='lines',
        line=dict(color=successful_color, width=2),
        name='Successful',
        legendgroup='Successful',
        showlegend=True,
        hoverinfo='none'
    ))

    # Unsuccessful passes - dashed lines
    fig.add_trace(go.Scatter(
        x=xs_ko, y=ys_ko, mode='lines',
        line=dict(color=unsuccessful_color, width=2, dash='dash'),
        name='Unsuccessful',
        legendgroup='Unsuccessful',
        showlegend=True,
        hoverinfo='none'
    ))

    # Adding arrowheads
    add_arrow_heads(fig, df[df.outcome_name.isna()], successful_color, 'Successful')
    add_arrow_heads(fig, df[df.outcome_name.notna()], unsuccessful_color, 'Unsuccessful')

    fig.update_layout(
        title=dict(text=f"<b>{len(df)} passes by {player_name}</b>", 
            x=0.5, y=0.97, xanchor='center', font=dict(size=20)
        ),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center',
            x=0.5, font=dict(size=13), bgcolor='rgba(0,0,0,0)', borderwidth=0
        ),
        margin=dict(t=100, b=40, l=20, r=20),
        hovermode=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig


def add_arrow_heads(fig, df, color, legend_group):
    arrow_length = 1
    for _, r in df.iterrows():
        dx = r.end_x - r.x
        dy = r.end_y - r.y
        angle = math.atan2(dy, dx)

        left_angle = angle + math.pi - math.pi / 6
        right_angle = angle + math.pi + math.pi / 6

        x0 = r.end_x
        y0 = r.end_y
        x1 = x0 + arrow_length * math.cos(left_angle)
        y1 = y0 + arrow_length * math.sin(left_angle)
        x2 = x0 + arrow_length * math.cos(right_angle)
        y2 = y0 + arrow_length * math.sin(right_angle)

        for x_end, y_end in [(x1, y1), (x2, y2)]:
            fig.add_trace(go.Scatter(x=[x0, x_end], y=[y0, y_end], mode='lines', line=dict(color=color, width=2), 
                           legendgroup=legend_group, showlegend=False, hoverinfo='none'))

def make_carry_network_figure(events_df, player_name, color='darkgreen'):
    df = events_df.query("type_name=='Carry' and player_name==@player_name")
    
    def segments(df_sub):
        xs, ys = [], []
        for _, r in df_sub.iterrows():
            xs += [r.x, r.end_x, np.nan]
            ys += [r.y, r.end_y, np.nan]
        return xs, ys

    xs, ys = segments(df)

    fig = draw_pitch()

    # Carries - lignes
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode='lines',
        line=dict(color=color, width=2),
        name='Carries',
        legendgroup='Carries',
        showlegend=True,
        hoverinfo='none'
    ))

    add_arrow_heads(fig, df, color, 'Carries')

    fig.update_layout(
        title=dict(text=f"<b>{len(df)} carries by {player_name}</b>", x=0.5, y=0.97, xanchor='center', 
                   font=dict(size=20)),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5,
            font=dict(size=13), bgcolor='rgba(0,0,0,0)', borderwidth=0),
        margin=dict(t=100, b=40, l=20, r=20),
        hovermode=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig
