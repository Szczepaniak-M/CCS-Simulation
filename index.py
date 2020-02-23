import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import input_app, graph_app

app.layout = html.Div([
    dcc.Store(id='data-input', storage_type='session'),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return input_app.input_layout
    elif pathname == '/graph':
        return graph_app.graph_layout


if __name__ == '__main__':
    app.run_server(debug=True)
