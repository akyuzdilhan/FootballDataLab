from dash import dcc, Output, Input, State, ALL, callback, callback_context
from layouts.home import sections
from app import app
import os

@callback(
    Output('offcanvas-menu', 'is_open'),
    Input('menu-button', 'n_clicks'),
    State('offcanvas-menu', 'is_open'),
    prevent_initial_call=True
)
def toggle_offcanvas(n_clicks, is_open):
    if n_clicks is None:
        return is_open
    return not is_open

@callback(
    Output('modal', 'is_open'),
    Output('modal-title', 'children'),
    Output('modal-body', 'children'),
    Input({'type': 'open-modal', 'index': ALL}, 'n_clicks'),
    Input('modal', 'n_clicks_close'),
    State('modal', 'is_open'),
    prevent_initial_call=True
)
def toggle_modal(n_clicks_list, n_clicks_close, is_open):
    print("Modal is open:")
    ctx = callback_context

    if not ctx.triggered:
        return is_open, "", ""
    else:
        triggered_id = ctx.triggered_id

        if isinstance(triggered_id, dict) and triggered_id.get('type') == 'open-modal':
            index = triggered_id['index']
            section = next((s for s in sections if s['title'] == index), None)
            if section:
                content_path = section.get('content_markdown_file')
                if content_path and os.path.exists(content_path):
                    with open(content_path, 'r', encoding='utf-8') as f:
                        markdown_content = f.read()
                    content = dcc.Markdown(
                        markdown_content,
                        style={'textAlign': 'justify', 'fontSize': '16px', 'lineHeight': '1.6'},
                        link_target='_blank',
                        className='markdown-content'
                    )
                    return True, section['title'], content
        elif triggered_id == 'modal':
            return False, "", ""
    return is_open, "", ""
